<template>
  <AppLayout>
    <!-- Loading Spinner -->
    <LoadingSpinner v-if="loading" size="lg" />

    <!-- Main Content -->
    <div v-show="!loading" class="layout-container flex flex-col h-screen">
      <!-- Main Content Area -->
      <main class="flex flex-1 overflow-hidden gap-6">
        <!-- Middle Content: Stats and Charts -->
        <div class="flex-1 flex flex-col gap-6 overflow-y-auto custom-scrollbar pr-2">
          <!-- Dashboard Widgets -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div
              class="bg-primary/10 dark:bg-primary/5 p-4 rounded-xl border border-primary/20 flex flex-col justify-center">
              <p class="text-xs font-bold text-primary uppercase mb-1">Current Sector</p>
              <p class="text-lg font-bold">{{ currentSector }}</p>
            </div>

            <div
              class="md:col-span-2 bg-white dark:bg-primary/5 p-4 rounded-xl border border-dashed border-slate-300 dark:border-primary/30 flex items-center justify-between gap-4">
              <div>
                <p class="text-xs font-medium text-slate-500 mb-1 uppercase tracking-widest">Quick Insights</p>
                <div class="flex gap-6">
                  <div class="flex flex-col">
                    <span class="text-[10px] text-slate-500">Peak Traffic</span>
                    <span class="text-sm font-bold">{{ peakTraffic }}</span>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-[10px] text-slate-500">QC Pass Rate</span>
                    <span class="text-sm font-bold" :class="qcPassRate.includes('99') ? 'text-green-500' : 'text-primary'">{{ qcPassRate }}</span>
                  </div>
                </div>
              </div>
              <!-- Connection Status -->
              <div class="flex items-center gap-2">
                <div class="flex items-center gap-1.5">
                  <div class="w-2 h-2 rounded-full" :class="wsConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'"></div>
                  <span class="text-xs" :class="wsConnected ? 'text-green-500' : 'text-red-500'">{{ wsConnected ? 'Live' : 'Disconnected' }}</span>
                </div>
              </div>
              <!-- Module Links Compact -->
              <div class="flex gap-2">
                <button
                  class="p-2 bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white rounded-lg transition-colors"
                  title="AI Lab">
                  <span class="material-symbols-outlined text-sm">biotech</span>
                </button>
                <button
                  class="p-2 bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white rounded-lg transition-colors"
                  title="Audits">
                  <span class="material-symbols-outlined text-sm">receipt_long</span>
                </button>
                <button
                  class="p-2 bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white rounded-lg transition-colors"
                  title="HR Link">
                  <span class="material-symbols-outlined text-sm">group</span>
                </button>
                <button
                  class="p-2 bg-slate-100 dark:bg-slate-800 hover:bg-primary hover:text-white rounded-lg transition-colors"
                  title="Data Export">
                  <span class="material-symbols-outlined text-sm">dataset</span>
                </button>
              </div>
            </div>
          </div>
          <!-- Top Row: Stats -->
          <div class="grid grid-cols-2 gap-6">
            <!-- OEI Summary Card -->
            <div
              class="bg-white dark:bg-primary/5 p-6 rounded-xl border border-slate-200 dark:border-primary/10 flex flex-col justify-between">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <h3 class="text-slate-500 dark:text-slate-400 font-medium uppercase text-xs tracking-wider">Operation
                    Efficiency Index (OEI)</h3>
                  <p class="text-4xl font-bold mt-1 text-slate-900 dark:text-white">{{ oeiValue }}<span
                      class="text-xl text-primary">%</span></p>
                </div>
                <div class="flex items-center gap-1 bg-green-500/10 text-green-500 px-2 py-1 rounded text-xs font-bold">
                  <span class="material-symbols-outlined text-sm">trending_up</span>
                  <span>+2.5%</span>
                </div>
              </div>
              <div class="h-28 w-full overflow-visible">
                <Line :data="oeiChartData" :options="oeiChartOptions" />
              </div>
            </div>
            <!-- Labor Cost Card -->
            <div class="bg-white dark:bg-primary/5 p-6 rounded-xl border border-slate-200 dark:border-primary/10">
              <div class="flex justify-between items-start mb-6">
                <div>
                  <h3 class="text-slate-500 dark:text-slate-400 font-medium uppercase text-xs tracking-wider">Labor Cost
                    vs Budget</h3>
                  <p class="text-4xl font-bold mt-1 text-slate-900 dark:text-white">$42,500</p>
                </div>
                <div class="flex items-center gap-1 bg-red-500/10 text-red-500 px-2 py-1 rounded text-xs font-bold">
                  <span class="material-symbols-outlined text-sm">trending_up</span>
                  <span>+1.2% Over</span>
                </div>
              </div>
              <div class="h-24 w-full overflow-hidden">
                <Bar :data="laborChartData" :options="laborChartOptions" />
              </div>
            </div>
          </div>
          <!-- Secondary Row: Analysis & Map -->
          <div class="grid grid-cols-1 gap-6">
            <div
              class="bg-white dark:bg-primary/5 rounded-xl border border-slate-200 dark:border-primary/10 overflow-hidden">
              <div class="p-4 border-b border-slate-200 dark:border-primary/10 flex justify-between items-center">
                <h3 class="font-bold flex items-center gap-2">
                  <span class="material-symbols-outlined text-primary">analytics</span>
                  Operational Heatmap
                </h3>
                <div class="flex gap-2">
                  <button class="px-3 py-1 bg-primary text-white text-xs font-bold rounded-lg uppercase">Global</button>
                  <button
                    class="px-3 py-1 bg-slate-100 dark:bg-primary/10 text-slate-500 text-xs font-bold rounded-lg uppercase">Regional</button>
                </div>
              </div>
              <div class="h-[300px] relative bg-slate-100 dark:bg-slate-800">
                <img alt="World Map Distribution" class="w-full h-full object-cover opacity-60"
                  data-alt="Satellite map view of industrial warehouses with orange heatmap overlays"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuBkY49Sl8EwGbwjHTEmuicrADqf3KksnGC3Vca6TVjdqrd9Idqt8iHyG3RfRCsDUeOjvSukmRxVpqhTkMDTbJT80W-ABe463O6W0ANdtdXnAuDo8UYk_StbVg5yd8RR1tnSbAGGlTHvw20Exgchf8D8haF1FH3E3o-2K9f2PDsUyWJfQoY0th8v6nRMvz-fZ5Aoq5z3BJzSPJIMclPwyFvOjZjxiMlS1ZIWbBvQ_HFKtgwYAtUnr8D2ivmtJoitVoA7v92zXoA8S4A" />
                <div
                  class="absolute top-4 left-4 bg-background-dark/80 p-3 rounded-lg backdrop-blur-sm border border-primary/20">
                  <p class="text-[10px] text-primary font-bold uppercase mb-1 tracking-tighter">Live Status</p>
                  <div class="flex items-center gap-2 mb-2">
                    <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                    <span class="text-xs">Node 04: Operating Nominal</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
                    <span class="text-xs">Node 09: High Traffic</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Right Sidebar: Critical Alerts -->
        <aside class="w-80 flex flex-col gap-6 shrink-0 h-full">
          <div
            class="flex-1 flex flex-col bg-white dark:bg-primary/5 rounded-xl border border-slate-200 dark:border-primary/10 overflow-hidden">
            <div class="p-4 border-b border-slate-200 dark:border-primary/10 flex items-center justify-between">
              <h3 class="font-bold flex items-center gap-2">
                <span class="material-symbols-outlined text-red-500">warning</span>
                Critical Alerts
              </h3>
              <span v-if="alertCount > 0" class="px-2 py-0.5 bg-red-500 text-white text-[10px] font-bold rounded-full">{{ alertCount }} NEW</span>
              <span v-else class="px-2 py-0.5 bg-green-500 text-white text-[10px] font-bold rounded-full">CLEAR</span>
            </div>
            <div class="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-4">
              <!-- Dynamic Alerts from WebSocket -->
              <template v-if="criticalAlerts.length > 0">
                <div
                  v-for="(alert, index) in criticalAlerts"
                  :key="index"
                  class="p-4 rounded-xl border-l-4 relative group transition-all"
                  :class="alert.severity === 'critical' ? 'bg-red-500/10 border-red-500 hover:bg-red-500/20' : 'bg-primary/10 border-primary hover:bg-primary/20'"
                >
                  <div class="flex justify-between items-start mb-1">
                    <p class="text-xs font-bold uppercase" :class="alert.severity === 'critical' ? 'text-red-500' : 'text-primary'">{{ alert.type.replace('_', ' ') }}</p>
                    <span class="text-[10px] text-slate-400">Just now</span>
                  </div>
                  <p class="text-sm font-semibold mb-2 leading-snug">{{ alert.description }}</p>
                  <div class="flex gap-2">
                    <button
                      class="px-3 py-1.5 text-white text-[10px] font-bold rounded-lg uppercase"
                      :class="alert.severity === 'critical' ? 'bg-red-500' : 'bg-primary'"
                    >{{ alert.severity === 'critical' ? 'Critical' : 'Warning' }}</button>
                  </div>
                </div>
              </template>
              <!-- Default State when no alerts -->
              <template v-else>
                <div class="p-4 bg-green-500/10 rounded-xl border-l-4 border-green-500 relative">
                  <div class="flex justify-between items-start mb-1">
                    <p class="text-xs font-bold text-green-500 uppercase">All Clear</p>
                    <span class="text-[10px] text-slate-400">Live</span>
                  </div>
                  <p class="text-sm font-semibold leading-snug opacity-70">No safety alerts at this time. System operating normally.</p>
                </div>
              </template>

              <!-- Equipment Warnings -->
              <div v-if="aiStreamData?.equipment?.warnings > 0" class="p-4 bg-yellow-500/10 rounded-xl border-l-4 border-yellow-500">
                <div class="flex justify-between items-start mb-1">
                  <p class="text-xs font-bold text-yellow-500 uppercase">Equipment Warning</p>
                  <span class="text-[10px] text-slate-400">Just now</span>
                </div>
                <p class="text-sm font-semibold leading-snug">{{ aiStreamData.equipment.warnings }} equipment(s) require attention.</p>
              </div>
            </div>
            <div class="p-4 border-t border-slate-200 dark:border-primary/10">
              <button
                class="w-full py-2 text-sm font-bold text-slate-500 hover:text-primary transition-colors text-center uppercase tracking-widest">View
                All Notifications</button>
            </div>
          </div>
          <!-- Navigation Module Links -->
          <div class="bg-primary p-6 rounded-xl text-white">
            <h4 class="font-bold text-lg mb-4">Launch Modules</h4>
            <div class="grid grid-cols-2 gap-3">
              <button
                class="p-3 bg-white/20 hover:bg-white/30 rounded-lg flex flex-col items-center gap-1 transition-all">
                <span class="material-symbols-outlined">biotech</span>
                <span class="text-[10px] font-bold uppercase">AI Lab</span>
              </button>
              <button
                class="p-3 bg-white/20 hover:bg-white/30 rounded-lg flex flex-col items-center gap-1 transition-all">
                <span class="material-symbols-outlined">receipt_long</span>
                <span class="text-[10px] font-bold uppercase">Audits</span>
              </button>
              <button
                class="p-3 bg-white/20 hover:bg-white/30 rounded-lg flex flex-col items-center gap-1 transition-all">
                <span class="material-symbols-outlined">group</span>
                <span class="text-[10px] font-bold uppercase">HR Link</span>
              </button>
              <button
                class="p-3 bg-white/20 hover:bg-white/30 rounded-lg flex flex-col items-center gap-1 transition-all">
                <span class="material-symbols-outlined">dataset</span>
                <span class="text-[10px] font-bold uppercase">Data Export</span>
              </button>
            </div>
          </div>
        </aside>
      </main>
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '../components/AppLayout.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { ref, computed, shallowRef, onMounted, onUnmounted } from 'vue'
import { useAuth } from '../composables/useAuth'
import { Line, Bar } from 'vue-chartjs'
import { api } from '../services/ApiService'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Register only used ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const { user } = useAuth()

// WebSocket connection
let ws = null
let wsReconnectTimer = null  // Timer for reconnection
const wsConnected = ref(false)
let isComponentMounted = true  // Flag to track component state

// Loading state
const loading = ref(true)

// Fetch initial data from API
const fetchInitialData = async () => {
  try {
    loading.value = true
    const response = await api.get('/dashboard/stats')
    if (response) {
      console.log('Initial dashboard data loaded')
    }
  } catch (error) {
    console.error('Error fetching initial data:', error)
  } finally {
    loading.value = false
  }
}

// AI Stream Data from WebSocket
const aiStreamData = ref(null)
const aiStreamHistory = ref([])

// Initial static data for charts
const laborLabels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const laborData = shallowRef([70, 85, 75, 90, 80, 45])

// OEI Data - khởi tạo với số nguyên sạch
const oeiLabels = ['00:00', '08:00', '16:00', 'Now']
const oeiData = shallowRef([25, 75, 70, 33])

// Connect to WebSocket - using cookie for authentication (more secure)
const connectWebSocket = () => {
  // VITE_API_URL = http://localhost:8080/api (backend chạy port 8080)
  // WebSocket endpoint = ws://localhost:8080/ws/dashboard
  const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8080/api'
  const baseUrl = apiUrl.replace(/\/api$/, '').replace(/^http/, 'ws')
  const wsUrl = `${baseUrl}/ws/dashboard`

  console.log('WebSocket URL:', wsUrl)

  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('WebSocket connected')
    wsConnected.value = true
  }

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data)
      console.log('WebSocket message:', message)

      // Backend gửi: { type: "dashboard_update", data: { type: "ai_stream", data: {...} } }
      if (message.type === 'dashboard_update' && message.data?.type === 'ai_stream') {
        handleAIStreamData(message.data.data)
      } else if (message.type === 'ai_stream') {
        // Fallback: nếu có message trực tiếp
        handleAIStreamData(message.data)
      } else if (message.type === 'connected') {
        console.log('WS Connected:', message.message)
      } else if (message.type === 'ping') {
        if (ws?.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'pong' }))
        }
      }
    } catch (e) {
      console.error('Error parsing WS message:', e)
    }
  }

  ws.onclose = () => {
    console.log('WebSocket disconnected')
    wsConnected.value = false
    // Only reconnect if component is still mounted
    if (isComponentMounted) {
      wsReconnectTimer = setTimeout(connectWebSocket, 5000)
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
}

// Handle AI Stream Data from WebSocket
const handleAIStreamData = (data) => {
  console.log('AI Stream Data received:', data)
  aiStreamData.value = data

  // Add to history
  aiStreamHistory.value.push({
    timestamp: data.timestamp,
    ...data
  })

  // Keep only last 10 records
  if (aiStreamHistory.value.length > 10) {
    aiStreamHistory.value.shift()
  }

  // Update charts with real data - validate before updating
  // ParseInt to ensure we get clean numbers
  if (data.summary && data.summary.overall_score) {
    const rawScore = parseFloat(data.summary.overall_score)
    if (!isNaN(rawScore) && isFinite(rawScore)) {
      const newScore = Math.round(Math.min(100, Math.max(0, rawScore)))
      // Create completely new array with validated numbers
      const newData = [...oeiData.value.slice(1), newScore].map(v => Number(v) || 0)
      oeiData.value = newData
      console.log('OEI updated:', newData)
    }
  }

  if (data.food_qc) {
    // Update QC pass rate display
    console.log('QC Pass Rate:', data.food_qc.pass_rate)
  }

  if (data.staff) {
    // Update staff productivity
    console.log('Staff Productivity:', data.staff.productivity_score)
  }
}

// Get current sector from user/branch
const currentSector = computed(() => {
  return user.value?.branch_name || 'North Logistics Hub'
})

// Quick stats from AI data
const peakTraffic = computed(() => {
  if (!aiStreamData.value?.customers) return '14:00 - 16:00'
  if (aiStreamData.value.customers.peak_detection) return 'Now (Peak)'
  return '14:00 - 16:00'
})

const qcPassRate = computed(() => {
  if (!aiStreamData.value?.food_qc) return '99.2%'
  return `${aiStreamData.value.food_qc.pass_rate}%`
})

const oeiValue = computed(() => {
  if (!aiStreamData.value?.summary) return 33.1
  return aiStreamData.value.summary.overall_score
})

const criticalAlerts = computed(() => {
  if (!aiStreamData.value?.safety) return []
  return aiStreamData.value.safety.alerts || []
})

const alertCount = computed(() => {
  return criticalAlerts.value.length
})

// Cleanup on unmount
onMounted(async () => {
  // Step 1: Fetch initial data from API
  await fetchInitialData()

  // Step 2: Then connect WebSocket for real-time updates
  connectWebSocket()
})

onUnmounted(() => {
  isComponentMounted = false  // Mark as unmounted
  if (wsReconnectTimer) {
    clearTimeout(wsReconnectTimer)
    wsReconnectTimer = null
  }
  if (ws) {
    ws.close()
  }
})

// OEI Chart Data for Chart.js
const oeiChartData = computed(() => ({
  labels: oeiLabels,
  datasets: [{
    label: 'OEI',
    data: oeiData.value.map(v => Number(v) || 0),
    borderColor: '#ec5b13',
    backgroundColor: 'rgba(236, 91, 19, 0.2)',
    fill: true,
    tension: 0.4,
    pointRadius: 4,
    pointBackgroundColor: '#ec5b13',
    pointBorderColor: '#fff',
    pointBorderWidth: 2
  }]
}))

// OEI Chart Options for Chart.js
const oeiChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: true }
  },
  scales: {
    x: {
      display: true,
      grid: { display: false },
      ticks: {
        color: '#94a3b8',
        font: { size: 10 }
      }
    },
    y: {
      display: false,
      min: 0,
      max: 100
    }
  },
  animation: {
    duration: 0
  }
}

// Labor Chart Data for Chart.js
const laborChartData = computed(() => ({
  labels: laborLabels,
  datasets: [{
    label: 'Labor Cost',
    data: laborData.value.map(v => Number(v) || 0),
    backgroundColor: '#3d2c24',
    borderRadius: 4,
    barThickness: 20
  }]
}))

// Labor Chart Options for Chart.js
const laborChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: true }
  },
  scales: {
    x: {
      display: true,
      grid: { display: false },
      ticks: {
        color: '#94a3b8',
        font: { size: 10 }
      }
    },
    y: {
      display: false,
      min: 0,
      max: 100
    }
  },
  animation: {
    duration: 0
  }
}
</script>
<!-- 
<style scoped>
:deep(.apexcharts-xaxis-label) {
  transform: translateX(-5px);
}
:deep(.apexcharts-xaxis) {
  padding: 0 5px;
}
</style> -->
