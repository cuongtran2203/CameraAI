<template>
  <div class="bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 min-h-screen overflow-hidden">
    <div class="layout-container flex flex-col h-screen">
      <AppHeader />
      <main class="flex flex-1 overflow-hidden p-6 gap-6">
        <AppSidebar />
        <div class="flex-1 flex flex-col gap-6 overflow-y-auto custom-scrollbar pr-2">
          <slot></slot>
        </div>
      </main>
      <AppFooter />
    </div>
  </div>
</template>

<script setup>
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import AppFooter from './AppFooter.vue'
</script>

<style scoped>
</style>
