<template>
  <AppLayout>
    <!-- Content Area -->
    <div class="flex-1 flex overflow-hidden rounded-2xl border border-slate-200 dark:border-primary/10 bg-white dark:bg-[#1a120e]">
      <!-- Video Grid Column -->
      <div class="flex-1 flex flex-col p-4 overflow-y-auto custom-scrollbar">
        <!-- Layout Controls and Title -->
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-4">
            <h2 class="text-lg font-bold flex items-center gap-2">
              <span class="w-2 h-2 bg-primary rounded-full animate-pulse"></span>
              Live Monitoring
            </h2>
            <span class="px-2 py-0.5 rounded bg-primary/20 text-primary text-[10px] font-bold uppercase tracking-wider">Active Stream</span>
          </div>
          <div class="flex bg-slate-200 dark:bg-surface-dark rounded-xl p-1">
            <button
              @click="gridLayout = 1"
              :class="gridLayout === 1 ? 'bg-white dark:bg-background-dark text-primary shadow-sm' : ''"
              class="px-4 py-1.5 text-xs font-bold rounded-lg hover:text-primary transition-colors"
            >1x1</button>
            <button
              @click="gridLayout = 4"
              :class="gridLayout === 4 ? 'bg-white dark:bg-background-dark text-primary shadow-sm' : ''"
              class="px-4 py-1.5 text-xs font-bold rounded-lg hover:text-primary transition-colors"
            >2x2</button>
            <button
              @click="gridLayout = 9"
              :class="gridLayout === 9 ? 'bg-white dark:bg-background-dark text-primary shadow-sm' : ''"
              class="px-4 py-1.5 text-xs font-bold rounded-lg hover:text-primary transition-colors"
            >3x3</button>
          </div>
        </div>

        <!-- Video Grid -->
        <div
          class="grid gap-4 flex-1"
          :class="{
            'grid-cols-1': gridLayout === 1,
            'grid-cols-2': gridLayout === 4,
            'grid-cols-3': gridLayout === 9
          }"
        >
          <!-- Render cameras based on grid layout -->
          <template v-for="(camera, index) in displayCameras" :key="camera?.id || index">
            <div
              v-if="camera"
              class="relative group rounded-xl overflow-hidden border border-slate-200 dark:border-border-dark bg-black aspect-video"
            >
              <!-- Video Player -->
              <VideoPlayer
                :src="getStreamUrl(camera)"
                :camera-name="camera.name"
                :camera-zone="camera.location"
                @error="handleStreamError($event, camera.id)"
              />
            </div>
            <!-- Placeholder when no camera -->
            <div
              v-else
              class="relative group rounded-xl overflow-hidden border border-slate-200 dark:border-border-dark bg-black aspect-video flex items-center justify-center"
            >
              <div class="flex flex-col items-center gap-2 text-slate-500">
                <span class="material-symbols-outlined text-4xl">videocam_off</span>
                <span class="text-sm">No camera assigned</span>
              </div>
            </div>
          </template>
        </div>

        <!-- Bottom Selector -->
        <div class="mt-4 shrink-0">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-xs font-bold uppercase text-slate-400 tracking-widest">Available Streams</h3>
            <button class="text-primary text-xs font-bold hover:underline">View All</button>
          </div>
          <div class="flex gap-4 overflow-x-auto pb-2 custom-scrollbar">
            <div
              v-for="camera in cameras"
              :key="camera.id"
              @click="selectCamera(camera)"
              class="min-w-[160px] h-24 rounded-xl relative overflow-hidden cursor-pointer border-2 transition-all"
              :class="selectedCameraId === camera.id ? 'border-primary shadow-lg' : 'border-transparent hover:border-slate-400 dark:hover:border-border-dark'"
            >
              <div class="absolute inset-0 bg-black/40 flex flex-col justify-end p-2">
                <p class="text-[10px] font-bold text-white leading-tight">{{ camera.name }}</p>
                <p class="text-[8px]" :class="camera.is_active ? 'text-primary font-bold' : 'text-slate-300'">
                  {{ camera.is_active ? 'ACTIVE' : 'OFFLINE' }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import VideoPlayer from '../components/VideoPlayer.vue'
import { useAuth } from '../composables/useAuth'

const { api } = useAuth()

const cameras = ref([])
const gridLayout = ref(4) // 1, 4, or 9
const selectedCameraId = ref(null)
const isLoading = ref(false)
const error = ref(null)

// API URL for stream proxy
const STREAM_BASE_URL = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:8080'

// Fetch cameras from API
const fetchCameras = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await api.get('/cameras')
    cameras.value = response.data || []

    // Auto-select first active camera
    const activeCamera = cameras.value.find(c => c.is_active)
    if (activeCamera) {
      selectedCameraId.value = activeCamera.id
    }
  } catch (err) {
    console.error('Error fetching cameras:', err)
    error.value = 'Failed to load cameras'
    // Use demo data if API fails
    cameras.value = getDemoCameras()
  } finally {
    isLoading.value = false
  }
}

// Get stream URL - prioritize AI processed stream
const getStreamUrl = (camera) => {
  if (!camera) return ''

  // Priority 1: AI processed HLS stream (from DeepStream/AI pipeline)
  if (camera.ai_hls_url) {
    return camera.ai_hls_url
  }

  // Priority 2: Direct HLS stream
  if (camera.stream_type === 'hls' || camera.rtsp_url?.includes('.m3u8')) {
    return camera.rtsp_url
  }

  // Priority 3: RTSP via proxy (MediaMTX conversion)
  if (camera.rtsp_url?.includes('rtsp://')) {
    // Format: http://localhost:8888/{camera_id}/live.m3u8
    return `${STREAM_BASE_URL}/stream/${camera.id}/hls`
  }

  return ''
}

// Get display cameras based on grid layout
const displayCameras = computed(() => {
  const count = gridLayout.value
  const result = []

  for (let i = 0; i < count; i++) {
    if (selectedCameraId.value && i === 0) {
      // First slot = selected camera
      result.push(cameras.value.find(c => c.id === selectedCameraId.value))
    } else if (i < cameras.value.length) {
      result.push(cameras.value[i])
    } else {
      result.push(null)
    }
  }

  return result
})

// Select camera
const selectCamera = (camera) => {
  selectedCameraId.value = camera.id
}

// Handle stream errors
const handleStreamError = (errorMsg, cameraId) => {
  console.error(`Stream error for camera ${cameraId}:`, errorMsg)
}

// Demo cameras (fallback)
const getDemoCameras = () => [
  {
    id: 'demo-1',
    name: 'Main Entrance',
    location: 'Zone A - Entry',
    rtsp_url: '',
    stream_type: 'rtsp',
    is_active: true
  },
  {
    id: 'demo-2',
    name: 'Front Lobby',
    location: 'Zone B - Interior',
    rtsp_url: '',
    stream_type: 'rtsp',
    is_active: true
  },
  {
    id: 'demo-3',
    name: 'Staff Kitchen',
    location: 'Zone C - Service',
    rtsp_url: '',
    stream_type: 'rtsp',
    is_active: true
  },
  {
    id: 'demo-4',
    name: 'North Parking',
    location: 'Zone D - Perimeter',
    rtsp_url: '',
    stream_type: 'rtsp',
    is_active: false
  }
]

onMounted(() => {
  fetchCameras()
})
</script>
