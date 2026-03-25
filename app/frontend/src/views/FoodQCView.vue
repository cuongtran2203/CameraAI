<template>
  <div class="bg-background-light dark:bg-background-dark min-h-screen h-full text-slate-900 dark:text-slate-100">
    <div class="layout-container flex h-full flex-col">
      <!-- Header -->
      <header
        class="flex items-center justify-between whitespace-nowrap border-b border-slate-200 bg-white px-10 py-3 dark:border-slate-800 dark:bg-slate-900"
      >
        <div class="flex items-center gap-8">
          <div class="flex items-center gap-4 text-primary">
            <div class="flex size-6 items-center justify-center">
              <span class="material-symbols-outlined text-3xl">camera_outdoor</span>
            </div>
            <h2 class="text-lg font-bold leading-tight tracking-tight text-slate-900 dark:text-white">
              Camera Analyst QC
            </h2>
          </div>
          <nav class="flex items-center gap-6">
            <router-link to="/" class="text-sm font-medium text-slate-600 hover:text-primary dark:text-slate-300">Dashboard</router-link>
            <router-link to="/live-view" class="text-sm font-medium text-slate-600 hover:text-primary dark:text-slate-300">Logs</router-link>
            <router-link to="/camera-config" class="text-sm font-medium text-slate-600 hover:text-primary dark:text-slate-300">Cameras</router-link>
            <span class="border-b-2 border-primary text-sm font-bold text-slate-900 dark:text-white">Analysis</span>
          </nav>
        </div>
        <div class="flex flex-1 items-center justify-end gap-4">
          <div class="flex gap-2">
            <button class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-600 hover:bg-primary/10 hover:text-primary dark:bg-slate-800 dark:text-slate-300">
              <span class="material-symbols-outlined">notifications</span>
            </button>
            <button class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-600 hover:bg-primary/10 hover:text-primary dark:bg-slate-800 dark:text-slate-300">
              <span class="material-symbols-outlined">account_circle</span>
            </button>
          </div>
          <div class="size-10 rounded-full border-2 border-primary/20 bg-cover bg-center bg-no-repeat"
            style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuChevDoC59IzQ13P3sgsC-lztsIEhnhnH2eJUW-2hk4X6lfloMAc-95mG5IkL7qTK5re15rHjMU-dc3VgVXgT_vgDlt4J3pVN7hGC8H-zpR8wcDYYKob-dl1QJCuNAZ59aPxjAFdeGJU8pJ159xlrAStn8tWTks6ZNCJwVFt28sfZzQUg7rCJSQbG_lZmSEIWTg0WGp0irHI6Ouy9Nd-9FcggqGbXPB38mehAiv2yLswCPLEwPCjQJVO1ugAtDMLIEy-uzpyNxKY-A");' />
        </div>
      </header>

      <main class="mx-auto flex w-full max-w-[1920px] flex-1 flex-col gap-6 overflow-y-auto p-6 lg:px-10">

        <!-- Title Row -->
        <div class="flex flex-col items-start justify-between gap-4 md:flex-row md:items-end">
          <div class="flex flex-col gap-1">
            <div class="mb-1 flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
              <span>Quality Control</span>
              <span class="material-symbols-outlined text-xs">chevron_right</span>
              <span class="font-medium text-primary">AI Food Retrieval</span>
            </div>
            <h1 class="text-3xl font-black tracking-tight text-slate-900 dark:text-white">Food Quality Inspection</h1>
            <p class="text-slate-500 dark:text-slate-400">Upload food image to search and compare against reference database</p>
          </div>
          <div class="flex gap-3">
            <button class="flex h-11 items-center gap-2 rounded-xl bg-slate-200 px-6 text-sm font-bold text-slate-700 hover:bg-slate-300 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700">
              <span class="material-symbols-outlined">settings</span>Configure
            </button>
            <button class="flex h-11 items-center gap-2 rounded-xl bg-primary px-6 text-sm font-bold text-white shadow-lg shadow-primary/20 hover:bg-primary/90">
              <span class="material-symbols-outlined">description</span>Export Report
            </button>
          </div>
        </div>

        <!-- Main Grid -->
        <div class="grid grid-cols-12 gap-6">

          <!-- Left Column -->
          <div class="col-span-12 flex flex-col gap-6 lg:col-span-8">

            <!-- Upload + Reference Row -->
            <div class="grid grid-cols-2 gap-4">

              <!-- Best Match Reference -->
              <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
                <div class="mb-4 flex items-center justify-between">
                  <h3 class="flex items-center gap-2 font-bold">
                    <span class="material-symbols-outlined text-primary">verified_user</span>
                    Best Match
                  </h3>
                  <span v-if="bestMatch" class="rounded bg-green-100 px-2 py-1 text-xs font-bold text-green-600 dark:bg-green-900/30 dark:text-green-400">
                    {{ displayMatchScore }}%
                  </span>
                  <span v-else class="rounded bg-slate-100 px-2 py-1 text-xs text-slate-500 dark:bg-slate-800">No match</span>
                </div>

                <div class="relative aspect-video w-full overflow-hidden rounded-lg border border-slate-200 bg-slate-100 dark:border-slate-700 dark:bg-slate-800">
                  <img
                    v-if="bestMatch"
                    :key="bestMatchImageUrl"
                    :src="bestMatchImageUrl"
                    :alt="bestMatch.id"
                    class="absolute inset-0 h-full w-full object-contain"
                    @error="(e) => e.target.style.display = 'none'"
                  />
                  <div class="absolute inset-0 flex flex-col items-center justify-center gap-2">
                    <span class="material-symbols-outlined text-5xl text-slate-300">restaurant</span>
                  </div>
                </div>

                <div v-if="bestMatch" class="mt-3 flex items-center gap-2">
                  <span
                    class="rounded-full px-3 py-1 text-xs font-bold"
                    :class="matchStatusBadgeClass"
                  >
                    {{ matchStatusLabel }}
                  </span>
                  <span class="text-xs text-slate-400">{{ bestMatch.description?.slice(0, 60) }}...</span>
                </div>
              </div>

              <!-- Upload to Search -->
              <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm ring-2 ring-primary/20 dark:border-slate-800 dark:bg-slate-900">
                <div class="mb-4 flex items-center justify-between">
                  <h3 class="flex items-center gap-2 font-bold">
                    <span class="material-symbols-outlined text-primary">upload_image</span>
                    Upload to Search
                  </h3>
                  <span v-if="uploadedImageUrl" class="rounded bg-green-100 px-2 py-1 text-xs font-bold text-green-600 dark:bg-green-900/30 dark:text-green-400">READY</span>
                  <span v-else class="rounded bg-slate-100 px-2 py-1 text-xs text-slate-500 dark:bg-slate-800">AWAITING</span>
                </div>

                <div
                  class="relative aspect-video w-full cursor-pointer overflow-hidden rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 transition-all hover:border-primary/50 dark:border-slate-600 dark:bg-slate-800"
                  :class="{ 'border-primary bg-primary/5': uploadedImageUrl }"
                  @click="openImagePicker"
                >
                  <img v-if="uploadedImageUrl" :src="uploadedImageUrl" alt="Uploaded" class="absolute inset-0 h-full w-full object-contain" />
                  <div v-if="!uploadedImageUrl" class="absolute inset-0 flex flex-col items-center justify-center gap-2">
                    <span class="material-symbols-outlined text-4xl text-slate-400">add_photo_alternate</span>
                    <p class="text-sm font-medium text-slate-500">Click to upload</p>
                    <p class="text-xs text-slate-400">JPG, PNG, WEBP (max 10MB)</p>
                  </div>
                  <div v-if="uploadedImageUrl" class="absolute inset-0 flex items-center justify-center gap-2 bg-black/40 opacity-0 transition-opacity hover:opacity-100">
                    <button class="flex items-center gap-1 rounded-lg bg-white px-3 py-1.5 text-xs font-bold text-slate-700 shadow hover:bg-slate-100" @click.stop="openImagePicker">
                      <span class="material-symbols-outlined text-sm">refresh</span>Change
                    </button>
                    <button class="flex items-center gap-1 rounded-lg bg-red-500 px-3 py-1.5 text-xs font-bold text-white shadow hover:bg-red-600" @click.stop="resetSearch">
                      <span class="material-symbols-outlined text-sm">close</span>Remove
                    </button>
                  </div>
                </div>

                <input ref="fileInputRef" type="file" accept="image/*" class="hidden" @change="handleImageSelected" />

                <div class="mt-3 flex items-center justify-between">
                  <p class="max-w-[180px] truncate text-xs text-slate-400">{{ uploadedImageFile?.name || 'No file selected' }}</p>
                  <button
                    class="flex items-center gap-2 rounded-xl bg-primary px-5 py-2 text-sm font-bold text-white shadow hover:bg-primary/90 disabled:opacity-50"
                    :disabled="!uploadedImageFile || isSearching"
                    @click="submitSearch"
                  >
                    <span v-if="isSearching" class="h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
                    <span v-else class="material-symbols-outlined text-lg">search</span>
                    {{ isSearching ? 'Searching...' : 'Search' }}
                  </button>
                </div>

                <div v-if="searchError" class="mt-2 flex items-center gap-2 rounded-lg bg-red-50 px-3 py-2 text-xs text-red-600 dark:bg-red-900/20">
                  <span class="material-symbols-outlined text-sm">error</span>{{ searchError }}
                </div>
                <div v-else-if="noMatchFound" class="mt-2 flex items-center gap-2 rounded-lg bg-amber-50 px-3 py-2 text-xs text-amber-700 dark:bg-amber-900/20 dark:text-amber-300">
                  <span class="material-symbols-outlined text-sm">info</span>Không có món ăn nào phù hợp.
                </div>
              </div>
            </div>

            <!-- Score Card -->
            <div class="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
              <template v-if="bestMatch">
                <div class="flex flex-col">
                  <span class="text-xs font-medium uppercase tracking-widest text-slate-500">Best Match Score</span>
                  <div class="flex items-baseline gap-3">
                    <h2 class="text-5xl font-black text-slate-900 dark:text-white">{{ displayMatchScore }}%</h2>
                    <span class="flex items-center gap-1 text-sm font-bold text-slate-400">
                      <span class="material-symbols-outlined text-base">psychology</span>AI
                    </span>
                  </div>
                </div>
                <div class="max-w-md flex-1 px-10">
                  <div class="flex h-4 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                    <div class="h-full transition-all duration-500" :class="matchScoreBarColor" :style="{ width: displayMatchScore + '%' }" />
                  </div>
                  <div class="mt-2 flex justify-between text-[10px] font-bold uppercase text-slate-400">
                    <span>Pass (&gt;= 85%)</span><span>Optimal (95%+)</span>
                  </div>
                </div>
                <div class="flex flex-col items-end gap-1">
                  <span class="rounded-full px-3 py-1 text-sm font-bold" :class="matchStatusBadgeClass">{{ matchStatusLabel }}</span>
                  <div class="flex gap-3 text-xs text-slate-400">
                    <span>Visual: {{ Math.round((bestMatch.base_score || 0) * 100) }}%</span>
                    <span>Ingr: {{ Math.round((bestMatch.ingredient_score || 0) * 100) }}%</span>
                  </div>
                </div>
              </template>
              <template v-else>
                <div class="flex flex-col">
                  <span class="text-xs font-medium uppercase tracking-widest text-slate-500">Best Match Score</span>
                  <div class="flex items-baseline gap-3">
                    <h2 class="text-5xl font-black text-slate-300 dark:text-slate-600">--%</h2>
                    <span class="text-sm text-slate-400">{{ noMatchFound ? 'Không có món ăn phù hợp' : 'Upload image to search' }}</span>
                  </div>
                </div>
                <div class="max-w-md flex-1 px-10">
                  <div class="flex h-4 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                    <div class="h-full w-0 bg-slate-300" />
                  </div>
                  <div class="mt-2 flex justify-between text-[10px] font-bold uppercase text-slate-400">
                    <span>Pass (&gt;= 85%)</span><span>Optimal (95%+)</span>
                  </div>
                </div>
                <div class="flex flex-col items-end">
                  <span class="rounded-full bg-slate-100 px-3 py-1 text-sm font-bold text-slate-400 dark:bg-slate-800">AWAITING</span>
                </div>
              </template>
            </div>

            <!-- Match Detail -->
            <div v-if="bestMatch" class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
              <h3 class="mb-4 font-bold text-slate-900 dark:text-white">Match Details</h3>
              <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
                <!-- Description -->
                <div>
                  <p class="mb-2 text-xs font-bold uppercase tracking-wider text-slate-500">AI Description</p>
                  <p class="text-sm leading-relaxed text-slate-600 dark:text-slate-300">
                    {{ bestMatch.description || searchResult?.query_description || 'N/A' }}
                  </p>
                </div>
                <!-- Ingredients -->
                <div>
                  <p class="mb-2 text-xs font-bold uppercase tracking-wider text-slate-500">Ingredients</p>
                  <div class="flex flex-wrap gap-1.5">
                    <span v-for="ing in bestMatch.ingredients" :key="ing"
                      class="rounded-full bg-primary/10 px-2 py-0.5 text-xs font-medium text-primary">
                      {{ ing }}
                    </span>
                    <span v-for="ing in (searchResult?.query_ingredients || [])" :key="'q-' + ing"
                      class="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-500 dark:bg-slate-800 dark:text-slate-400">
                      {{ ing }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Recent Inspections -->
          <div class="col-span-12 flex flex-col gap-6 lg:col-span-4">
            <div class="flex h-full flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
              <div class="border-b border-slate-200 bg-slate-50/70 p-4 dark:border-slate-800 dark:bg-slate-800/60">
                <div class="mb-3 flex items-center justify-between">
                  <h3 class="font-bold text-slate-900 dark:text-white">Recent Inspections</h3>
                  <span class="rounded bg-primary/10 px-2 py-0.5 text-xs font-bold text-primary">
                    {{ allCount }} results
                  </span>
                </div>
                <div class="flex gap-1 rounded-lg bg-slate-100 p-1 dark:bg-slate-950">
                  <button v-for="tab in ['all', 'passed', 'failed']" :key="tab"
                    class="flex flex-1 items-center justify-center gap-1 rounded-md px-2 py-1.5 text-xs font-bold transition-all"
                    :class="activeFilter === tab
                      ? 'bg-white shadow-sm dark:bg-slate-800'
                      : 'text-slate-500 hover:bg-white/50'"
                    :style="activeFilter === tab ? { color: tab === 'passed' ? '#16a34a' : tab === 'failed' ? '#dc2626' : 'var(--color-primary, #3b82f6)' } : {}"
                    @click="activeFilter = tab">
                    {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
                    <span class="rounded bg-slate-200 px-1 py-0.5 text-[10px] dark:bg-slate-700">
                      {{ tab === 'all' ? allCount : tab === 'passed' ? passedCount : failedCount }}
                    </span>
                  </button>
                </div>
              </div>

              <!-- Inspection List -->
              <div ref="logContainerRef" class="qc-scroll-area overflow-y-auto">
                <div class="flex flex-col">
                  <div v-if="qcResults.length === 0" class="flex flex-col items-center justify-center py-12 text-slate-400">
                    <span class="material-symbols-outlined text-4xl">search_off</span>
                    <p class="mt-2 text-sm">{{ noMatchFound ? 'Không có món ăn nào phù hợp' : 'No results yet' }}</p>
                    <p class="text-xs">{{ noMatchFound ? 'Hãy thử ảnh khác hoặc kiểm tra lại dữ liệu tham chiếu' : 'Upload an image to search' }}</p>
                  </div>

                  <div v-for="item in qcResults" :key="item.inspection_id"
                    class="flex items-center gap-3 border-b border-slate-100 px-4 py-3 transition-colors hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/50"
                    :class="item.result_status === 'failed' ? 'border-l-2 border-l-red-400' : 'border-l-2 border-l-green-400'">
                    <!-- Food thumbnail -->
                    <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-400 dark:bg-slate-800">
                      <span class="material-symbols-outlined text-lg">restaurant</span>
                    </div>
                    <!-- Info -->
                    <div class="min-w-0 flex-1">
                      <p class="truncate text-sm font-medium text-slate-900 dark:text-white">{{ item.food_name }}</p>
                      <p class="text-[10px] text-slate-400">{{ formatTime(item.checked_at) }}</p>
                    </div>
                    <!-- Score + Status -->
                    <div class="flex flex-shrink-0 flex-col items-end gap-1">
                      <span class="text-sm font-bold" :class="item.result_status === 'failed' ? 'text-red-500' : 'text-green-600'">
                        {{ item.score_pct }}%
                      </span>
                      <span class="rounded px-1.5 py-0.5 text-[10px] font-bold"
                        :class="item.result_status === 'passed'
                          ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                          : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'">
                        {{ item.result_status === 'passed' ? 'PASS' : 'FAIL' }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Footer -->
              <div class="border-t border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-800/50">
                <button v-if="hasMoreItems" class="flex w-full items-center justify-center gap-1 text-xs font-bold text-primary hover:text-primary/80" @click="loadMore" :disabled="isLoadingMore">
                  <span v-if="isLoadingMore" class="h-4 w-4 animate-spin rounded-full border-b-2 border-primary" />
                  <span v-else class="material-symbols-outlined">expand_more</span>
                  {{ isLoadingMore ? 'Loading...' : 'Load More' }}
                </button>
                <p v-else-if="allCount > 0" class="text-center text-xs text-slate-400">{{ allCount }} results</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer class="border-t border-slate-200 p-4 text-center dark:border-slate-800">
        <p class="text-xs text-slate-400">System Version 4.2.1-QC | AI Retrieval Mode</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import ApiService from '@/services/ApiService'

const apiService = new ApiService()

// ---------------------------------------------
// Search State
// ---------------------------------------------
const uploadedImageUrl = ref(null)
const uploadedImageFile = ref(null)
const isSearching = ref(false)
const searchError = ref(null)
const searchResult = ref(null)
const noMatchFound = ref(false)
const fileInputRef = ref(null)

const openImagePicker = () => fileInputRef.value?.click()

const handleImageSelected = (event) => {
  const file = event.target.files[0]
  if (!file) return
  if (!file.type.startsWith('image/')) { searchError.value = 'Invalid image file.'; return }
  if (file.size > 10 * 1024 * 1024) { searchError.value = 'File too large (max 10MB).'; return }
  searchError.value = null
  uploadedImageFile.value = file
  const reader = new FileReader()
  reader.onload = (e) => { uploadedImageUrl.value = e.target.result; searchResult.value = null }
  reader.readAsDataURL(file)
}

const submitSearch = async () => {
  if (!uploadedImageFile.value) { searchError.value = 'Select an image first.'; return }
  isSearching.value = true
  searchError.value = null
  searchResult.value = null
  noMatchFound.value = false
  try {
    const formData = new FormData()
    formData.append('image', uploadedImageFile.value)
    formData.append('top_k', '10')
    const response = await apiService.upload('/v1/food/search', formData)
    searchResult.value = response
    noMatchFound.value = !response?.top_k?.length
  } catch (error) {
    console.error('Search failed:', error)
    searchResult.value = null
    searchError.value = error.message || 'Search failed.'
    noMatchFound.value = false
  } finally {
    isSearching.value = false
  }
}

const resetSearch = () => {
  uploadedImageUrl.value = null
  uploadedImageFile.value = null
  searchResult.value = null
  searchError.value = null
  noMatchFound.value = false
  if (fileInputRef.value) fileInputRef.value.value = ''
}

// ---------------------------------------------
// Image URL Helper
// ---------------------------------------------
const getImageUrl = (imagePath) => {
  if (!imagePath) return ''
  // imagePath example: "images/My_quang.jpg"
  // Serve from AI service static files
  const baseUrl = import.meta.env.VITE_AI_SERVICE_URL || 'http://localhost:8000'
  return `${baseUrl}/${imagePath}`
}

// ---------------------------------------------
// Recent Inspections
// ---------------------------------------------
const activeFilter = ref('all')
const isLoadingMore = ref(false)
const logContainerRef = ref(null) // reserved for future scroll control

const createTabState = () => ({ items: [], visibleCount: 10, INITIAL_COUNT: 10, LOAD_MORE_COUNT: 20 })
const tabStates = ref({ all: createTabState(), passed: createTabState(), failed: createTabState() })

const allCount = computed(() => passedCount.value + failedCount.value)
const passedCount = computed(() => tabStates.value.passed.items.length)
const failedCount = computed(() => tabStates.value.failed.items.length)
const currentTabState = computed(() => tabStates.value[activeFilter.value] || createTabState())
const qcResults = computed(() => currentTabState.value.items.slice(0, currentTabState.value.visibleCount))
const hasMoreItems = computed(() => currentTabState.value.items.length > currentTabState.value.visibleCount)

const populateInspections = (topK) => {
  if (!topK?.length) return
  const passed = [], failed = []
  const now = new Date().toISOString()
  topK.forEach((item, i) => {
    const isPassed = item.score >= 0.85
    const qcItem = {
      inspection_id: `search-${now}-${i}-${Math.random().toString(36).slice(2, 8)}`,
      id: item.id || `search-item-${i}`,
      checked_at: now,
      score_pct: Math.round((item.score || 0) * 100),
      result_status: isPassed ? 'passed' : 'failed',
      food_name: item.id || 'Unknown',
      description: item.description || '',
      ingredients: item.ingredients || [],
      image_path: item.image_path || '',
    }
    isPassed ? passed.push(qcItem) : failed.push(qcItem)
  })
  tabStates.value.all.items = [...passed, ...failed, ...tabStates.value.all.items].slice(0, 100)
  tabStates.value.passed.items = [...passed, ...tabStates.value.passed.items].slice(0, 100)
  tabStates.value.failed.items = [...failed, ...tabStates.value.failed.items].slice(0, 100)
}

watch(searchResult, (val) => {
  if (!val) return
  noMatchFound.value = !val?.top_k?.length
  if (val.top_k?.length) populateInspections(val.top_k)
})

const loadMore = () => {
  const tab = currentTabState.value
  if (!tab) return
  isLoadingMore.value = true
  setTimeout(() => { tab.visibleCount += tab.LOAD_MORE_COUNT; isLoadingMore.value = false }, 200)
}

const formatTime = (ts) => {
  if (!ts) return '--:--:--'
  return new Date(ts).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

// ---------------------------------------------
// Best Match Computed
// ---------------------------------------------
const bestMatch = computed(() => searchResult.value?.top_k?.[0] ?? null)
const bestMatchImageUrl = computed(() => bestMatch.value ? getImageUrl(bestMatch.value.image_path) : '')
const displayMatchScore = computed(() => bestMatch.value ? Math.round((bestMatch.value.score || 0) * 100) : null)

const matchStatusLabel = computed(() => bestMatch.value && bestMatch.value.score >= 0.85 ? 'PASSED' : 'FAILED')
const matchStatusBadgeClass = computed(() =>
  bestMatch.value && bestMatch.value.score >= 0.85
    ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
)
const matchScoreBarColor = computed(() => bestMatch.value && bestMatch.value.score >= 0.85 ? 'bg-primary' : 'bg-red-500')
</script>

<style scoped>
.qc-scroll-area { height: 520px; max-height: 520px; min-height: 520px; }
</style>