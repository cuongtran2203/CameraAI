<template>
  <aside class="w-64 flex flex-col gap-2 shrink-0 border-r border-slate-200 dark:border-primary/20 pr-4 bg-background-light dark:bg-background-dark">
    <div class="flex flex-col gap-2">
      <p class="text-xs font-bold text-slate-400 uppercase px-4 mt-2 mb-1">General</p>
      <router-link to="/" :class="getNavClass('/')">
        <span class="material-symbols-outlined">dashboard</span>
        <span>Dashboard</span>
      </router-link>
      <router-link to="/live-view" :class="getNavClass('/live-view')">
        <span class="material-symbols-outlined">videocam</span>
        <span>Live Monitoring</span>
      </router-link>
    </div>

    <div class="flex flex-col gap-2 mt-2">
      <p class="text-xs font-bold text-slate-400 uppercase px-4 mb-1">Analytics</p>
      <router-link to="/customer-analytics" :class="getNavClass('/customer-analytics')">
        <span class="material-symbols-outlined">groups</span>
        <span>Customer Flow</span>
      </router-link>
      <router-link to="/kitchen-analytics" :class="getNavClass('/kitchen-analytics')">
        <span class="material-symbols-outlined">soup_kitchen</span>
        <span>Kitchen Traffic</span>
      </router-link>
      <router-link to="/receptionist-dashboard" :class="getNavClass('/receptionist-dashboard')">
        <span class="material-symbols-outlined">support_agent</span>
        <span>Receptionist Perf.</span>
      </router-link>
    </div>

    <div class="flex flex-col gap-2 mt-2">
      <p class="text-xs font-bold text-slate-400 uppercase px-4 mb-1">Staff</p>
      <router-link to="/staff-attendance" :class="getNavClass('/staff-attendance')">
        <span class="material-symbols-outlined">badge</span>
        <span>Attendance</span>
      </router-link>
      <router-link to="/staff-performance" :class="getNavClass('/staff-performance')">
        <span class="material-symbols-outlined">trending_up</span>
        <span>Performance</span>
      </router-link>
    </div>

    <div class="flex flex-col gap-2 mt-2">
      <p class="text-xs font-bold text-slate-400 uppercase px-4 mb-1">Operations</p>
      <router-link to="/food-qc" :class="getNavClass('/food-qc')">
        <span class="material-symbols-outlined">fact_check</span>
        <span>Food QC</span>
      </router-link>
    </div>

    <div class="flex flex-col gap-2 mt-2">
      <p class="text-xs font-bold text-slate-400 uppercase px-4 mb-1">Configuration</p>
      <router-link to="/camera-config" :class="getNavClass('/camera-config')">
        <span class="material-symbols-outlined">settings_video_camera</span>
        <span>Camera AI</span>
      </router-link>
      <router-link to="/rtsp-setup" :class="getNavClass('/rtsp-setup')">
        <span class="material-symbols-outlined">router</span>
        <span>RTSP Setup</span>
      </router-link>
    </div>

    <div class="mt-auto p-4">
      <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-red-500/10 hover:text-red-500 transition-all">
        <span class="material-symbols-outlined">logout</span>
        <span>Logout</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuth } from '../composables/useAuth'
import { computed } from 'vue'

const route = useRoute()
const { logout } = useAuth()

// Computed property for current path - better performance
const currentPath = computed(() => route.path)

const getNavClass = (path) => {
  const isActive = currentPath.value === path
  if (isActive) {
    return 'flex items-center gap-3 px-4 py-3 rounded-xl bg-primary text-white font-semibold'
  }
  return 'flex items-center gap-3 px-4 py-3 rounded-xl text-slate-600 dark:text-slate-400 hover:bg-primary/10 hover:text-primary transition-all'
}

const handleLogout = () => {
  logout()
}
</script>
