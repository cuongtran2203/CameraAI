<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed, onMounted, watch } from 'vue'

const route = useRoute()

// Check if current route is FoodQC (should be light mode)
const isLightMode = computed(() => {
  return route.path === '/food-qc'
})

// Apply dark class to html element based on route
onMounted(() => {
  updateDarkClass()
})

watch(() => route.path, () => {
  updateDarkClass()
})

function updateDarkClass() {
  const html = document.documentElement
  if (isLightMode.value) {
    html.classList.remove('dark')
  } else {
    html.classList.add('dark')
  }
}
</script>

<template>
  <RouterView />
</template>

<style scoped>
</style>
