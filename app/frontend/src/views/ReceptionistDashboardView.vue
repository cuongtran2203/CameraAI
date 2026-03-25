<template>
  <AppLayout>
    <!-- Content Area -->
    <div class="flex flex-col overflow-y-auto custom-scrollbar gap-8 pr-2">
      <div class="flex flex-col gap-2">
        <h2 class="text-3xl font-black text-slate-900 dark:text-slate-100 tracking-tight">Front-of-House Overview</h2>
        <p class="text-slate-500 dark:text-slate-400">Real-time engagement and service metrics for the reception team.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white dark:bg-primary/5 border border-slate-200 dark:border-primary/10 p-5 rounded-xl flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <div class="p-2 rounded-lg bg-emerald-500/10 text-emerald-500">
              <span class="material-symbols-outlined">groups</span>
            </div>
            <span class="text-xs font-bold text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded-full">+12% vs LW</span>
          </div>
          <div>
            <p class="text-slate-500 text-sm font-medium">Total Guests Welcomed</p>
            <h3 class="text-3xl font-bold text-slate-900 dark:text-slate-100 mt-1">1,284</h3>
          </div>
        </div>
        <div class="bg-white dark:bg-primary/5 border border-slate-200 dark:border-primary/10 p-5 rounded-xl flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <div class="p-2 rounded-lg bg-primary/10 text-primary">
              <span class="material-symbols-outlined">timer</span>
            </div>
            <span class="text-xs font-bold text-primary bg-primary/10 px-2 py-1 rounded-full">-0.5s improvement</span>
          </div>
          <div>
            <p class="text-slate-500 text-sm font-medium">Avg. Greeting Time</p>
            <h3 class="text-3xl font-bold text-slate-900 dark:text-slate-100 mt-1">4.2<span class="text-lg font-normal ml-1">sec</span></h3>
          </div>
        </div>
        <div class="bg-white dark:bg-primary/5 border border-slate-200 dark:border-primary/10 p-5 rounded-xl flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <div class="p-2 rounded-lg bg-blue-500/10 text-blue-500">
              <span class="material-symbols-outlined">shopping_cart_checkout</span>
            </div>
            <span class="text-xs font-bold text-blue-500 bg-blue-500/10 px-2 py-1 rounded-full">Top Tier</span>
          </div>
          <div>
            <p class="text-slate-500 text-sm font-medium">Avg. Conversion Rate</p>
            <h3 class="text-3xl font-bold text-slate-900 dark:text-slate-100 mt-1">18.4<span class="text-lg font-normal ml-1">%</span></h3>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <div class="flex items-center justify-between">
          <h4 class="text-xl font-bold text-slate-900 dark:text-slate-100">Individual Performance</h4>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          <!-- Staff Card 1 -->
          <div class="bg-white dark:bg-background-dark/50 border border-slate-200 dark:border-primary/10 p-4 rounded-xl flex flex-col gap-4 hover:border-primary/40 transition-all group">
            <div class="flex items-center gap-3">
              <div class="size-12 rounded-full border-2 border-primary overflow-hidden">
                <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBri_EcetIIiQMCUQBGKpSLr5v_cjZ3git8odckaHnOkCRKrL0N5dmJ9XP0v0qcso7hFWreKnKs0Rd_Johrlyz_gZhITMSDk5C0sMcPsWTfw5LkYXEDYkFlGwDFhX0Ay5Qv7AOlZ6jglmKEXKJFTUhb7PJFUaPbMfThnuLNC7sXnzjNBpnajuAlRNFaaEYh_sFTBSBFEC4s-aEGpm8ZoGxLL8NYMtWjt5zj0fMj1iPcPrbTzOqkmMS8hNIpJb3vDnXIXzEnu4HkLLY"/>
              </div>
              <div>
                <h5 class="font-bold text-slate-900 dark:text-slate-100">Sarah Jenkins</h5>
                <p class="text-xs text-slate-500">Senior Receptionist</p>
              </div>
            </div>
            <div class="grid grid-cols-3 gap-2 py-2 border-t border-slate-100 dark:border-primary/5">
              <div class="text-center">
                <p class="text-[10px] uppercase text-slate-400 font-bold">Welcomed</p>
                <p class="font-bold text-primary">342</p>
              </div>
              <div class="text-center border-x border-slate-100 dark:border-primary/5">
                <p class="text-[10px] uppercase text-slate-400 font-bold">Greeting</p>
                <p class="font-bold text-primary">3.8s</p>
              </div>
              <div class="text-center">
                <p class="text-[10px] uppercase text-slate-400 font-bold">Conv.</p>
                <p class="font-bold text-primary">22.1%</p>
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
