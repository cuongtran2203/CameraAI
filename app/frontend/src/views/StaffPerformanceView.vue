<template>
  <AppLayout>
    <!-- Content Area -->
    <div class="flex-1 flex overflow-hidden rounded-2xl border border-slate-200 dark:border-primary/10 bg-white dark:bg-[#1a120e]">
      <!-- Sidebar: Staff List -->
      <aside class="w-80 border-r border-slate-200 dark:border-primary/20 bg-background-light dark:bg-background-dark p-6 flex flex-col gap-6 shrink-0">
        <h2 class="text-sm font-bold uppercase tracking-wider text-slate-500">Active Analysts</h2>
        <div class="flex-1 overflow-y-auto custom-scrollbar space-y-2">
          <div class="p-3 rounded-xl bg-primary/10 border border-primary/20 flex flex-col gap-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="size-10 rounded-full bg-slate-200 dark:bg-primary/30 bg-cover bg-center" style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuBs5Tq0tnWYfvO3pvNZ0d0dA_NKKDrbumSmBDmqN3ea-ZF9ZCrYbudPjj-PZBXzFPielKxo9IxTcNtswThFFfN2NoGB5wUY3Z6H4Ft7JapSjEETpNXG-qz_OrBjojpKosTf6oDnYaK_vV-mdhm4XUXPOmr9YBUrgIjtPjqUU95WntQxQrLX2zyXdL4wY-8vvpbhq7f_INSd0Q3twJtZDpT9hPNwovAluX8VEpHZffUwWqW4yDKb3o-Y982Z4CRfew6_x0F1KSSNEYs')"></div>
                <p class="text-sm font-bold">John Doe</p>
              </div>
              <p class="text-xs font-bold text-primary">85%</p>
            </div>
          </div>
        </div>
      </aside>

      <!-- Main Content Area -->
      <section class="flex-1 flex flex-col overflow-y-auto custom-scrollbar p-8 gap-8">
        <div class="flex items-end justify-between">
          <div class="space-y-1">
            <h2 class="text-3xl font-black tracking-tight">John Doe's Performance</h2>
            <p class="text-slate-500">Activity and HAR Analysis for Oct 24, 2023</p>
          </div>
        </div>

        <div class="flex-1 min-h-[500px] flex flex-col bg-white dark:bg-background-dark/50 border border-slate-200 dark:border-primary/20 rounded-2xl shadow-sm overflow-hidden">
          <div class="p-6 border-b border-slate-100 dark:border-primary/10 flex items-center justify-between">
            <h3 class="font-bold text-lg">HAR Activity Timeline</h3>
          </div>
          <div class="flex-1 p-8">
            <p class="text-slate-400 italic">Timeline visualization active...</p>
          </div>
        </div>
      </section>
    </div>
  </AppLayout>
</template>

<script setup>
import AppLayout from '../components/AppLayout.vue'
</script>
