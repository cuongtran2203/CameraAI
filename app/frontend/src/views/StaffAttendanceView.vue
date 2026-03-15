<template>
  <AppLayout>
    <!-- Content Area -->
    <div class="flex-1 flex flex-col overflow-y-auto custom-scrollbar gap-8 pr-2">
      <div class="flex flex-col gap-2">
        <h2 class="text-3xl font-black text-slate-900 dark:text-slate-100 tracking-tight">Staff Attendance Report</h2>
        <p class="text-slate-500 dark:text-slate-400">Detailed daily logs and punctuality analysis.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white dark:bg-primary/5 border border-slate-200 dark:border-primary/10 p-6 rounded-2xl flex flex-col gap-1 shadow-sm">
          <span class="text-slate-500 dark:text-slate-400 font-medium uppercase tracking-wider text-xs">Total Staff Present</span>
          <span class="text-3xl font-black">142/150</span>
        </div>
        <div class="bg-white dark:bg-primary/5 border border-slate-200 dark:border-primary/10 p-6 rounded-2xl flex flex-col gap-1 shadow-sm">
          <span class="text-slate-500 dark:text-slate-400 font-medium uppercase tracking-wider text-xs">Late Arrivals</span>
          <span class="text-3xl font-black text-orange-500">12</span>
        </div>
        <div class="bg-white dark:bg-primary/5 border border-slate-200 dark:border-primary/10 p-6 rounded-2xl flex flex-col gap-1 shadow-sm">
          <span class="text-slate-500 dark:text-slate-400 font-medium uppercase tracking-wider text-xs">Avg. Working Hours</span>
          <span class="text-3xl font-black text-blue-500">8h 15m</span>
        </div>
      </div>

      <div class="bg-white dark:bg-primary/5 border border-slate-200 dark:border-primary/10 rounded-2xl overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 dark:bg-primary/10 border-b border-slate-200 dark:border-primary/10">
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500 dark:text-primary/70">Staff Member</th>
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500 dark:text-primary/70">Check-In</th>
              <th class="px-6 py-4 text-xs font-bold uppercase tracking-widest text-slate-500 dark:text-primary/70">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 dark:divide-primary/10">
            <tr>
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-slate-200 overflow-hidden border-2 border-primary/20">
                    <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBlt3OJvm1mZiEAxgtzbS1M-FnmGXdASApKDa-1MP8eXuO7DMxYb8VdpedJ9lEa8hj0EqXxybtMG1uVYcPAPVpLYgjDJplDPRvMx9B447kIxlTXci_bDaYLcYqtahHHvHhsxHinVyoCIpM6N1OY0givppTZFPOMGEOJTGwJtW1BLkHCm0HX2lhHqeN1-B5pNq20FgvOz6BqATsEVQk3OGnkQOY29S-jIgBgIsKCGqXNXmiLrIQlIMN-hve9EtvnAdNmS1cbvwKm48w"/>
                  </div>
                  <div>
                    <p class="font-bold text-sm">Marcus Chen</p>
                    <p class="text-xs text-slate-500">Senior Developer</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-sm font-medium text-slate-400">08:52 AM</td>
              <td class="px-6 py-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-500/20 dark:text-emerald-400">On Time</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '../components/AppLayout.vue'
</script>
