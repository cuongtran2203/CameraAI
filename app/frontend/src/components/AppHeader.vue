<template>
  <header class="flex items-center justify-between px-8 py-4 bg-background-light dark:bg-background-dark border-b border-slate-200 dark:border-primary/20 shrink-0">
    <div class="flex items-center gap-8">
      <div class="flex items-center gap-3 text-primary">
        <span class="material-symbols-outlined !text-3xl !font-bold">videocam</span>
        <h2 class="text-slate-900 dark:text-slate-100 text-xl font-bold leading-tight tracking-tight uppercase">Camera Analyst</h2>
      </div>
      <nav class="flex items-center gap-6">
        <a class="text-primary text-sm font-semibold border-b-2 border-primary pb-1" href="#">Overview</a>
        <a class="text-slate-500 dark:text-slate-400 text-sm font-medium hover:text-primary transition-colors" href="#">Analytics</a>
        <a class="text-slate-500 dark:text-slate-400 text-sm font-medium hover:text-primary transition-colors" href="#">Reports</a>
        <a class="text-slate-500 dark:text-slate-400 text-sm font-medium hover:text-primary transition-colors" href="#">System Status</a>
      </nav>
    </div>
    <div class="flex items-center gap-6">
      <div class="relative flex items-center">
        <span class="material-symbols-outlined absolute left-3 text-slate-400">search</span>
        <input class="bg-slate-100 dark:bg-primary/5 border-none rounded-xl pl-10 pr-4 py-2 text-sm focus:ring-1 focus:ring-primary w-64" placeholder="Search operations..."/>
      </div>
      <div class="flex gap-3">
        <button class="p-2 rounded-xl bg-slate-100 dark:bg-primary/10 text-slate-600 dark:text-primary hover:bg-primary hover:text-white transition-all">
          <span class="material-symbols-outlined">notifications</span>
        </button>
        <button class="p-2 rounded-xl bg-slate-100 dark:bg-primary/10 text-slate-600 dark:text-primary hover:bg-primary hover:text-white transition-all">
          <span class="material-symbols-outlined">settings</span>
        </button>
      </div>
      <!-- User Dropdown -->
      <div class="relative pl-4 border-l border-slate-200 dark:border-primary/20">
        <button @click="toggleDropdown" class="flex items-center gap-3 focus:outline-none">
          <div class="text-right">
            <p class="text-xs font-bold uppercase tracking-wider text-primary">{{ userRole }}</p>
            <p class="text-sm font-medium">{{ userName }}</p>
          </div>
          <div class="w-10 h-10 rounded-full bg-primary/20 border-2 border-primary flex items-center justify-center overflow-hidden">
            <img v-if="userAvatar" :src="userAvatar" alt="User profile photo" />
            <span v-else class="material-symbols-outlined text-primary">person</span>
          </div>
          <span class="material-symbols-outlined text-slate-400 text-sm">expand_more</span>
        </button>
        <!-- Dropdown Menu -->
        <div v-if="showDropdown" class="absolute right-0 top-full mt-2 w-48 bg-white dark:bg-primary/10 rounded-xl shadow-lg border border-slate-200 dark:border-primary/20 overflow-hidden z-50">
          <button @click="handleLogout" class="w-full flex items-center gap-3 px-4 py-3 text-slate-600 dark:text-slate-300 hover:bg-red-500/10 hover:text-red-500 transition-colors">
            <span class="material-symbols-outlined">logout</span>
            <span class="text-sm font-medium">Logout</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuth } from '../composables/useAuth'

const { user, logout } = useAuth()

const showDropdown = ref(false)

const userName = computed(() => {
  return user.value?.name || user.value?.email || 'User'
})

const userRole = computed(() => {
  return user.value?.role || user.value?.email?.split('@')[0] || 'User'
})

const userAvatar = computed(() => {
  return user.value?.avatar || ''
})

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
}

const handleLogout = () => {
  showDropdown.value = false
  logout()
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  const dropdown = event.target.closest('.relative.pl-4')
  if (!dropdown) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
