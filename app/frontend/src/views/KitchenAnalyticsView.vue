<template>
  <AppLayout>
    <!-- Loading Spinner -->
    <LoadingSpinner v-if="loading" size="lg" />

    <!-- Content Area -->
    <div v-else class="flex-1 flex flex-col overflow-y-auto custom-scrollbar gap-6 pr-2">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Chef Active Index -->
        <div class="rounded-xl border border-primary/20 p-6 bg-white dark:bg-primary/5 shadow-sm">
          <div class="flex justify-between items-center mb-6">
            <h3 class="text-lg font-bold">Chef Work Index (HAR)</h3>
            <span class="text-xs px-2 py-1 bg-primary/10 text-primary rounded font-bold uppercase">Real-time</span>
          </div>

          <!-- Staff Data from WebSocket -->
          <div class="space-y-4">
            <template v-if="staffData.length > 0">
              <div v-for="staff in staffData" :key="staff.staff_id" class="space-y-2">
                <div class="flex justify-between text-xs font-medium">
                  <span>{{ staff.staff_name }}</span>
                  <span class="text-primary">{{ getWorkPercentage(staff.work_time_min) }}% ({{ staff.work_time_min }}min/480min)</span>
                </div>
                <div class="h-6 w-full flex rounded-lg overflow-hidden bg-slate-200 dark:bg-slate-800">
                  <div class="bg-primary h-full" :style="{ width: getWorkPercentage(staff.work_time_min) + '%' }"></div>
                </div>
              </div>
            </template>

            <!-- Demo Data when no WebSocket data -->
            <template v-else>
              <div class="space-y-2">
                <div class="flex justify-between text-xs font-medium">
                  <span>Chef de Cuisine - Marco V.</span>
                  <span class="text-primary">82% (394min/480min)</span>
                </div>
                <div class="h-6 w-full flex rounded-lg overflow-hidden bg-slate-200 dark:bg-slate-800">
                  <div class="bg-primary h-full w-[82%]"></div>
                </div>
              </div>
              <div class="space-y-2">
                <div class="flex justify-between text-xs font-medium">
                  <span>Sous Chef - Sarah L.</span>
                  <span class="text-primary">91% (437min/480min)</span>
                </div>
                <div class="h-6 w-full flex rounded-lg overflow-hidden bg-slate-200 dark:bg-slate-800">
                  <div class="bg-primary h-full w-[91%]"></div>
                </div>
              </div>
            </template>
          </div>
        </div>

        <!-- Kitchen Load Chart Placeholder -->
        <div class="rounded-xl border border-primary/20 p-6 bg-white dark:bg-primary/5 shadow-sm">
          <h3 class="text-lg font-bold mb-6">Kitchen Load Correlation</h3>
          <div class="h-48 flex items-end gap-2">
            <div class="flex-1 bg-primary/40 h-[40%] rounded-t"></div>
            <div class="flex-1 bg-primary/60 h-[70%] rounded-t"></div>
            <div class="flex-1 bg-primary h-[90%] rounded-t"></div>
            <div class="flex-1 bg-primary/30 h-[20%] rounded-t"></div>
          </div>
        </div>
      </div>

      <!-- correlation Table -->
      <div class="rounded-xl border border-primary/20 bg-white dark:bg-primary/5 shadow-sm overflow-hidden">
        <div class="p-6 border-b border-primary/20 flex justify-between items-center">
          <h3 class="text-lg font-bold">Kitchen Efficiency vs Guest Volume</h3>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-left">
            <thead class="bg-primary/5 text-primary text-xs uppercase font-bold">
              <tr>
                <th class="px-6 py-3">Time Period</th>
                <th class="px-6 py-3">Guest Count</th>
                <th class="px-6 py-3">Efficiency Score</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-primary/10">
              <tr>
                <td class="px-6 py-4 font-bold">12:00 - 13:00</td>
                <td class="px-6 py-4">156</td>
                <td class="px-6 py-4 text-green-500 font-bold">OPTIMAL</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { api } from '../services/ApiService'

// WebSocket connection
let ws = null
let wsReconnectTimer = null  // Timer for reconnection
let isComponentMounted = true  // Flag to track component state

// Loading state
const loading = ref(true)

// Staff data from WebSocket
const staffData = ref([])

// Fetch initial data from API
const fetchInitialData = async () => {
  try {
    loading.value = true
    // Get current kitchen HAR data
    const response = await api.get('/dashboard/kitchen/har/current', {
      branch_id: 'branch-main-001'
    })
    if (response && response.staff) {
      staffData.value = response.staff
      console.log('Initial staff data loaded:', staffData.value)
    }
  } catch (error) {
    console.error('Error fetching initial data:', error)
  } finally {
    loading.value = false
  }
}

// Calculate work percentage based on 8 hours (480 minutes)
const getWorkPercentage = (workTimeMin) => {
  const standardWorkTime = 480 // 8 hours = 480 minutes
  const percentage = Math.round((workTimeMin / standardWorkTime) * 100)
  return Math.min(100, percentage) // Max 100%
}

// Connect to WebSocket
const connectWebSocket = () => {
  const apiUrl = import.meta.env.VITE_API_URL?.replace('/api', '') || 'http://localhost:8080'
  const wsUrl = `${apiUrl.replace('http', 'ws')}/ws/dashboard`

  console.log('Kitchen Analytics - Connecting to WebSocket:', wsUrl)

  ws = new WebSocket(wsUrl)

  ws.onopen = () => {
    console.log('Kitchen WebSocket connected')
  }

  ws.onmessage = (event) => {
    try {
      const message = JSON.parse(event.data)

      // Handle dashboard_update wrapper
      if (message.type === 'dashboard_update' && message.data?.type === 'ai_stream') {
        handleAIStreamData(message.data.data)
      } else if (message.type === 'ai_stream') {
        handleAIStreamData(message.data)
      }
    } catch (e) {
      console.error('Error parsing WebSocket message:', e)
    }
  }

  ws.onclose = () => {
    console.log('Kitchen WebSocket disconnected')
    // Only reconnect if component is still mounted
    if (isComponentMounted) {
      wsReconnectTimer = setTimeout(connectWebSocket, 5000)
    }
  }

  ws.onerror = (error) => {
    console.error('Kitchen WebSocket error:', error)
  }
}

// Handle AI Stream Data
const handleAIStreamData = (data) => {
  // Update staff HAR data
  if (data.staff?.har_data) {
    staffData.value = data.staff.har_data
    console.log('Staff HAR data received:', staffData.value)
  }
}

// Lifecycle
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
</script>
