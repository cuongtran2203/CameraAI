<template>
  <div class="flex items-center justify-center" :class="containerClass">
    <div
      class="animate-spin rounded-full border-2 border-t-transparent"
      :class="[sizeClass, colorClass]"
    ></div>
    <span v-if="text" class="ml-3 text-sm text-gray-600 dark:text-gray-400">{{ text }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md', // sm, md, lg
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  color: {
    type: String,
    default: 'primary', // primary, white, gray
    validator: (value) => ['primary', 'white', 'gray'].includes(value)
  },
  text: {
    type: String,
    default: ''
  },
  fullScreen: {
    type: Boolean,
    default: false
  }
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  }
  return sizes[props.size]
})

const colorClass = computed(() => {
  const colors = {
    primary: 'border-primary',
    white: 'border-white',
    gray: 'border-gray-400'
  }
  return colors[props.color]
})

const containerClass = computed(() => {
  return props.fullScreen ? 'h-screen w-screen bg-white/80 dark:bg-black/80' : ''
})
</script>
