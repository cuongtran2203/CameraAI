<template>
  <div class="video-player relative w-full h-full bg-black rounded-xl overflow-hidden">
    <!-- Video Element -->
    <video
      ref="videoRef"
      class="w-full h-full object-cover"
      controls
      playsinline
      muted
    ></video>

    <!-- Loading State -->
    <div
      v-if="isLoading"
      class="absolute inset-0 flex items-center justify-center bg-black/50"
    >
      <div class="flex flex-col items-center gap-2">
        <span class="material-symbols-outlined text-primary text-4xl animate-spin">
          sync
        </span>
        <span class="text-white text-sm">Connecting to stream...</span>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-if="error"
      class="absolute inset-0 flex items-center justify-center bg-black/70"
    >
      <div class="flex flex-col items-center gap-2 text-center px-4">
        <span class="material-symbols-outlined text-red-500 text-4xl">
          error_outline
        </span>
        <span class="text-white font-medium">{{ error }}</span>
        <button
          @click="retry"
          class="mt-2 px-4 py-2 bg-primary text-white text-sm font-bold rounded-lg hover:bg-primary/80"
        >
          Retry
        </button>
      </div>
    </div>

    <!-- No Stream State -->
    <div
      v-if="!src && !isLoading && !error"
      class="absolute inset-0 flex items-center justify-center bg-black/50"
    >
      <div class="flex flex-col items-center gap-2">
        <span class="material-symbols-outlined text-slate-500 text-4xl">
          videocam_off
        </span>
        <span class="text-slate-400 text-sm">No stream available</span>
      </div>
    </div>

    <!-- Overlay Info -->
    <div class="absolute top-3 left-3 flex gap-2" v-if="src">
      <span
        class="flex items-center gap-1.5 px-2 py-1 rounded-lg backdrop-blur-md text-[10px] font-bold"
        :class="isPlaying ? 'bg-green-500/80 text-white' : 'bg-yellow-500/80 text-white'"
      >
        <span
          class="w-1.5 h-1.5 rounded-full"
          :class="isPlaying ? 'bg-white animate-pulse' : 'bg-white/50'"
        ></span>
        {{ isPlaying ? 'LIVE' : 'CONNECTING' }}
      </span>
    </div>

    <!-- Camera Info -->
    <div
      v-if="cameraName"
      class="absolute bottom-3 left-3 flex flex-col"
    >
      <h3 class="text-white font-bold text-sm drop-shadow-md">{{ cameraName }}</h3>
      <p v-if="cameraZone" class="text-white/60 text-[10px] drop-shadow-md">{{ cameraZone }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import Hls from 'hls.js'

const props = defineProps({
  src: {
    type: String,
    default: ''
  },
  cameraName: {
    type: String,
    default: ''
  },
  cameraZone: {
    type: String,
    default: ''
  },
  // RTSP direct URL (sẽ convert sang HLS)
  rtspUrl: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['error', 'loaded', 'play', 'pause'])

const videoRef = ref(null)
const isLoading = ref(false)
const isPlaying = ref(false)
const error = ref(null)
let hls = null

/**
 * Fetch HLS manifest and rewrite all URLs to be same-origin.
 * This ensures segment requests go through nginx (no CORS, no 404).
 *
 * How it works:
 * 1. Fetch the manifest from MediaMTX (returns URLs like "video1_stream.m3u8"
 *    or "f867edc9c0c2_video1_seg22.mp4")
 * 2. Detect the stream's base path from the manifest URL
 * 3. Rewrite relative filenames to absolute URLs pointing through nginx
 * 4. Return a Blob URL so hls.js can load the rewritten manifest
 */
const fetchAndRewriteManifest = async (manifestUrl) => {
  const res = await fetch(manifestUrl)
  if (!res.ok) throw new Error(`Failed to fetch manifest: ${res.status}`)
  const text = await res.text()

  // Determine the base path of the manifest for rewriting relative URLs
  // e.g. "http://localhost:5173/hls/ds-test/video1_stream.m3u8"
  //      → "http://localhost:5173/hls/ds-test/"
  const url = new URL(manifestUrl)
  const basePath = url.origin + url.pathname.replace(/\/[^/]+\.m3u8(\?.*)?$/, '/')

  // Rewrite the manifest content:
  // - Absolute URLs (http://localhost:8888/...) → keep as-is or strip port
  // - Relative filenames → prepend basePath
  const lines = text.split('\n')
  const rewritten = lines.map(line => {
    const trimmed = line.trim()

    // Top-level master manifest: rewrite variant track names
    if (trimmed.startsWith('#EXT-X-STREAM-INF:')) {
      // Keep bandwidth/resolution attributes as-is
      return line
    }
    if (trimmed.endsWith('.m3u8') && !trimmed.startsWith('#')) {
      // Variant playlist URL — prepend basePath
      const clean = trimmed.split('?')[0].split('#')[0]
      return basePath + encodeURIComponent(clean)
    }

    // Second-level manifest: rewrite segment filenames
    // Patterns: *_init.mp4, *_seg[N].mp4, *_part[N].mp4, gap.mp4
    if (trimmed.endsWith('.mp4') && !trimmed.startsWith('#')) {
      // Strip query params, rewrite filename
      const clean = trimmed.split('?')[0].split('#')[0]
      return basePath + encodeURIComponent(clean)
    }

    // URI= attributes inside #EXT-X-MAP and #EXT-X-PART tags
    if (trimmed.startsWith('URI="') && trimmed.endsWith('.mp4"')) {
      const match = trimmed.match(/^URI="(.+?)"(.+)?$/)
      if (match) {
        const clean = match[1].split('?')[0]
        return `URI="${basePath}${encodeURIComponent(clean)}"${match[2] || ''}`
      }
    }

    return line
  }).join('\n')

  return URL.createObjectURL(new Blob([rewritten], { type: 'application/vnd.apple.mpegurl' }))
}

// Initialize video player
const initPlayer = () => {
  if (!videoRef.value) return

  // Cleanup existing player
  if (hls) {
    hls.destroy()
    hls = null
  }

  const video = videoRef.value
  const streamUrl = props.src || props.rtspUrl

  if (!streamUrl) {
    error.value = 'No stream URL provided'
    return
  }

  isLoading.value = true
  error.value = null

  // Check if HLS stream
  if (streamUrl.includes('.m3u8') || streamUrl.includes('hls')) {
    if (Hls.isSupported()) {
      // Fetch manifest, rewrite URLs to same-origin, load as Blob
      // This avoids CORS issues and URL path rewriting problems
      fetchAndRewriteManifest(streamUrl).then(rewrittenUrl => {
        hls = new Hls({
          enableWorker: true,
          lowLatencyMode: true,
          backBufferLength: 90
        })
        hls.loadSource(rewrittenUrl)
        hls.attachMedia(video)
        hls.on(Hls.Events.MANIFEST_PARSED, () => {
          isLoading.value = false
          video.play().catch(() => {
            // Autoplay blocked - user interaction required
          })
        })
        hls.on(Hls.Events.ERROR, (event, data) => {
          if (data.fatal) {
            handleError(data)
          }
        })
      }).catch(err => {
        error.value = 'Failed to load stream manifest'
        isLoading.value = false
        console.error('Manifest fetch error:', err)
      })
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      // Native HLS support (Safari) — can use URL directly
      video.src = streamUrl
      video.addEventListener('loadedmetadata', () => {
        isLoading.value = false
        video.play().catch(() => {})
      })
    }
  }
  // Check if RTMP/RTSP - need proxy
  else if (streamUrl.includes('rtsp://') || streamUrl.includes('rtmp://')) {
    error.value = 'RTSP/RTMP requires media server proxy. Use HLS endpoint.'
    isLoading.value = false
  }
  // Direct video file or other
  else {
    video.src = streamUrl
    video.addEventListener('loadedmetadata', () => {
      isLoading.value = false
    })
    video.addEventListener('error', () => {
      error.value = 'Failed to load video stream'
    })
  }
}

const handleError = (data) => {
  isLoading.value = false
  let errorMessage = 'Stream error'

  switch (data.type) {
    case Hls.ErrorTypes.NETWORK_ERROR:
      errorMessage = 'Network error - check connection'
      break
    case Hls.ErrorTypes.MEDIA_ERROR:
      errorMessage = 'Media format not supported'
      break
    case Hls.ErrorTypes.OTHER_ERROR:
      errorMessage = 'Stream error occurred'
      break
  }

  error.value = errorMessage
  emit('error', errorMessage)

  // Auto retry for network errors
  if (data.type === Hls.ErrorTypes.NETWORK_ERROR) {
    setTimeout(() => {
      initPlayer()
    }, 3000)
  }
}

const retry = () => {
  initPlayer()
}

const play = () => {
  if (videoRef.value) {
    videoRef.value.play()
  }
}

const pause = () => {
  if (videoRef.value) {
    videoRef.value.pause()
  }
}

// Watch for src changes
watch(() => props.src, (newSrc) => {
  if (newSrc) {
    initPlayer()
  }
})

watch(() => props.rtspUrl, (newUrl) => {
  if (newUrl) {
    initPlayer()
  }
})

// Event listeners
onMounted(() => {
  if (videoRef.value) {
    videoRef.value.addEventListener('play', () => {
      isPlaying.value = true
      emit('play')
    })
    videoRef.value.addEventListener('pause', () => {
      isPlaying.value = false
      emit('pause')
    })
    videoRef.value.addEventListener('ended', () => {
      isPlaying.value = false
    })
  }

  if (props.src || props.rtspUrl) {
    initPlayer()
  }
})

onUnmounted(() => {
  if (hls) {
    hls.destroy()
    hls = null
  }
})

defineExpose({
  play,
  pause,
  retry
})
</script>

<style scoped>
.video-player video::-webkit-media-controls {
  display: none !important;
}

.video-player:hover video::-webkit-media-controls {
  display: flex !important;
}
</style>
