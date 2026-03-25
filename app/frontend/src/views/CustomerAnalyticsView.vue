<template>
  <AppLayout>
    <!-- Content Area -->
    <div class="flex-1 flex flex-col overflow-y-auto custom-scrollbar gap-6 pr-2">
      <!-- KPI Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white dark:bg-primary/5 p-6 rounded-xl border border-slate-200 dark:border-primary/10 flex flex-col justify-between">
          <div class="flex justify-between items-start">
            <span class="text-slate-500 dark:text-slate-400 text-sm font-medium">Verified Guest Count</span>
            <span class="p-2 bg-primary/10 rounded-lg text-primary"><span class="material-symbols-outlined">group</span></span>
          </div>
          <div class="mt-4">
            <div class="text-4xl font-bold text-slate-900 dark:text-white">1,284</div>
            <div class="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 text-sm font-semibold mt-1">
              <span class="material-symbols-outlined text-sm">trending_up</span>
              <span>+12% vs last week</span>
            </div>
          </div>
        </div>
        <div class="bg-white dark:bg-primary/5 p-6 rounded-xl border border-slate-200 dark:border-primary/10 flex flex-col justify-between">
          <div class="flex justify-between items-start">
            <span class="text-slate-500 dark:text-slate-400 text-sm font-medium">Avg Dwell Time</span>
            <span class="p-2 bg-primary/10 rounded-lg text-primary"><span class="material-symbols-outlined">schedule</span></span>
          </div>
          <div class="mt-4">
            <div class="text-4xl font-bold text-slate-900 dark:text-white">14m 32s</div>
            <div class="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 text-sm font-semibold mt-1">
              <span class="material-symbols-outlined text-sm">trending_up</span>
              <span>+5% vs last week</span>
            </div>
          </div>
        </div>
        <div class="bg-white dark:bg-primary/5 p-6 rounded-xl border border-slate-200 dark:border-primary/10 flex flex-col justify-between">
          <div class="flex justify-between items-start">
            <span class="text-slate-500 dark:text-slate-400 text-sm font-medium">Peak Hour</span>
            <span class="p-2 bg-primary/10 rounded-lg text-primary"><span class="material-symbols-outlined">bolt</span></span>
          </div>
          <div class="mt-4">
            <div class="text-4xl font-bold text-slate-900 dark:text-white">14:00 - 15:00</div>
            <div class="text-xs text-slate-400 mt-1">Max capacity utilized</div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Trend Chart Placeholder -->
        <div class="bg-white dark:bg-primary/5 p-6 rounded-xl border border-slate-200 dark:border-primary/10">
          <h2 class="text-lg font-bold mb-6">Guest Count Trend</h2>
          <div class="h-64 flex items-end justify-between gap-3 px-2">
            <div class="flex-1 bg-primary/20 rounded-t-lg h-[40%]"></div>
            <div class="flex-1 bg-primary/20 rounded-t-lg h-[60%]"></div>
            <div class="flex-1 bg-primary/20 rounded-t-lg h-[55%]"></div>
            <div class="flex-1 bg-primary/20 rounded-t-lg h-[85%]"></div>
            <div class="flex-1 bg-primary rounded-t-lg h-[95%]"></div>
            <div class="flex-1 bg-primary/20 rounded-t-lg h-[75%]"></div>
            <div class="flex-1 bg-primary/20 rounded-t-lg h-[50%]"></div>
          </div>
        </div>
        <!-- Visitor classification -->
        <div class="bg-white dark:bg-primary/5 p-6 rounded-xl border border-slate-200 dark:border-primary/10">
          <h2 class="text-lg font-bold mb-6">Visitor Classification</h2>
          <div class="space-y-6">
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="font-medium text-slate-600 dark:text-slate-400">New Visitors</span>
                <span class="font-bold">65%</span>
              </div>
              <div class="w-full h-2 bg-slate-100 dark:bg-primary/10 rounded-full overflow-hidden">
                <div class="bg-primary h-full w-[65%] rounded-full"></div>
              </div>
            </div>
            <div class="space-y-2">
              <div class="flex justify-between text-sm">
                <span class="font-medium text-slate-600 dark:text-slate-400">Returning Customers</span>
                <span class="font-bold">28%</span>
              </div>
              <div class="w-full h-2 bg-slate-100 dark:bg-primary/10 rounded-full overflow-hidden">
                <div class="bg-primary/60 h-full w-[28%] rounded-full"></div>
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
