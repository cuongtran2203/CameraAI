<template>
  <div class="video-player relative w-full h-full bg-black rounded-xl overflow-hidden">
    <!-- Video Element -->
    <video
      ref="videoRef"
      class="w-full h-full object-contain"
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
      hls = new Hls({
        enableWorker: true,
        lowLatencyMode: true,
        backBufferLength: 90
      })
      hls.loadSource(streamUrl)
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
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      // Native HLS support (Safari)
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
