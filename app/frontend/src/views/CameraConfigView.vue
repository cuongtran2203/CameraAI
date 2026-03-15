<template>
  <AppLayout>
    <!-- Content Area -->
    <div class="flex-1 flex overflow-hidden rounded-2xl border border-slate-200 dark:border-primary/10 bg-white dark:bg-[#1a110d]">
      <!-- Sidebar: Camera List -->
      <aside class="w-72 border-r border-primary/20 bg-background-light dark:bg-background-dark p-6 flex flex-col gap-6 shrink-0">
        <div class="flex flex-col gap-1">
          <h1 class="text-slate-900 dark:text-slate-100 text-lg font-bold">Camera List</h1>
          <p class="text-primary text-sm font-medium">5 Online - 2 Offline</p>
        </div>
        <div class="flex flex-col gap-2 overflow-y-auto pr-2 custom-scrollbar">
          <div class="flex items-center gap-3 px-4 py-3 rounded-xl bg-primary text-white shadow-lg shadow-primary/20">
            <span class="material-symbols-outlined">videocam</span>
            <div class="flex flex-col">
              <p class="text-sm font-bold">Main Entrance</p>
              <p class="text-[10px] opacity-80 uppercase tracking-wider font-semibold">Recording</p>
            </div>
          </div>
          <div class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
            <span class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam</span>
            <p class="text-slate-700 dark:text-slate-300 text-sm font-medium">Lobby North</p>
          </div>
          <div class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
            <span class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam</span>
            <p class="text-slate-700 dark:text-slate-300 text-sm font-medium">Parking Gate 1</p>
          </div>
          <div class="flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-primary/10 transition-colors cursor-pointer group">
            <span class="material-symbols-outlined text-slate-500 group-hover:text-primary">videocam_off</span>
            <p class="text-slate-400 dark:text-slate-500 text-sm font-medium italic">Warehouse A (Offline)</p>
          </div>
        </div>
        <button class="mt-auto flex items-center justify-center gap-2 w-full rounded-xl py-3 bg-primary/10 border-2 border-dashed border-primary/30 text-primary hover:bg-primary/20 transition-all font-bold text-sm">
          <span class="material-symbols-outlined">add_circle</span>
          <span>Add New Camera</span>
        </button>
      </aside>

      <!-- Configuration Content Area -->
      <div class="flex-1 flex flex-col overflow-y-auto custom-scrollbar">
        <!-- Header Section -->
        <div class="flex flex-wrap justify-between items-center gap-4 p-8">
          <div class="flex flex-col gap-1">
            <h2 class="text-slate-900 dark:text-slate-100 text-3xl font-black tracking-tight">Camera Configuration</h2>
            <div class="flex items-center gap-2">
              <span class="size-2 rounded-full bg-green-500 animate-pulse"></span>
              <p class="text-slate-500 dark:text-primary/60 text-sm font-medium">Main Entrance - 4K IP Stream (192.168.1.104)</p>
            </div>
          </div>
          <div class="flex gap-3">
            <button class="flex items-center justify-center rounded-xl h-11 px-6 bg-slate-200 dark:bg-primary/10 text-slate-700 dark:text-slate-300 text-sm font-bold hover:bg-primary/20 transition-all">Cancel</button>
            <button class="flex items-center justify-center rounded-xl h-11 px-8 bg-primary text-white text-sm font-bold hover:brightness-110 shadow-lg shadow-primary/30 transition-all">Save Changes</button>
          </div>
        </div>
        <!-- Tabs -->
        <div class="px-8">
          <div class="flex border-b border-primary/10 gap-8">
            <button class="flex items-center gap-2 border-b-2 border-primary text-primary pb-4 px-2">
              <span class="material-symbols-outlined text-xl">polyline</span>
              <span class="text-sm font-bold">Video Feed & ROI</span>
            </button>
            <button class="flex items-center gap-2 border-b-2 border-transparent text-slate-500 dark:text-slate-400 hover:text-primary pb-4 px-2 transition-colors">
              <span class="material-symbols-outlined text-xl">psychology</span>
              <span class="text-sm font-bold">AI Model Parameters</span>
            </button>
          </div>
        </div>
        <!-- Configuration Content -->
        <div class="p-8 grid grid-cols-12 gap-8">
          <!-- Left: ROI and Video Preview -->
          <div class="col-span-12 lg:col-span-8 flex flex-col gap-6">
            <div class="bg-slate-900 dark:bg-black rounded-2xl overflow-hidden relative border border-primary/30 shadow-2xl">
              <div class="aspect-video w-full bg-slate-800 flex items-center justify-center relative group">
                <img class="w-full h-full object-cover opacity-80" src="https://lh3.googleusercontent.com/aida-public/AB6AXuC6_3vpnSg01hp2poCQj1VfaSvBRoB2a4JND_y_IATOJ_PLvQH8-I243LLiXEhv6eu0duhCQRA7fZkq_4Q1gGCcYAnnT-zflO0BL50DzrM18snLR5ynFykD9m3A8x2lI86JJzboCayEYSyk-E-vHzZxpG7MpAC1xX86MrzM1e5vAR9Neb6yna3BwOWBgzYNpiyvjJr57AjH46y4Hga8fHYIi-6vlikChPsfCUZqBszGpFN_reryZQfe4m-EmDdG780FB67XzStnu78"/>
                <svg class="absolute inset-0 w-full h-full pointer-events-none">
                  <polygon fill="rgba(236, 91, 19, 0.2)" points="100,100 400,120 450,300 150,350" stroke="#ec5b13" stroke-dasharray="8 4" stroke-width="3"></polygon>
                  <text fill="#ec5b13" font-size="14" font-weight="bold" x="110" y="90">Entrance ROI</text>
                </svg>
              </div>
            </div>
          </div>
          <!-- Right: AI Parameters Panel -->
          <div class="col-span-12 lg:col-span-4 flex flex-col gap-6">
            <div class="bg-background-light dark:bg-background-dark p-6 rounded-2xl border border-primary/20 shadow-sm flex flex-col gap-8">
              <div>
                <h3 class="text-lg font-bold text-slate-900 dark:text-slate-100 mb-4 flex items-center gap-2">
                  <span class="material-symbols-outlined text-primary">face</span>
                  Face ID Confidence
                </h3>
                <input class="w-full h-1.5 bg-slate-200 dark:bg-primary/10 rounded-lg appearance-none cursor-pointer accent-primary" type="range"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '../components/AppLayout.vue'
</script>
