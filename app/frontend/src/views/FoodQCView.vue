<template>
  <div class="bg-background-light dark:bg-background-dark min-h-screen h-full text-slate-900 dark:text-slate-100">
    <div class="layout-container flex h-full flex-col">
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
            <router-link
              to="/"
              class="text-sm font-medium text-slate-600 transition-colors hover:text-primary dark:text-slate-300"
            >
              Dashboard
            </router-link>
            <router-link
              to="/live-view"
              class="text-sm font-medium text-slate-600 transition-colors hover:text-primary dark:text-slate-300"
            >
              Logs
            </router-link>
            <router-link
              to="/camera-config"
              class="text-sm font-medium text-slate-600 transition-colors hover:text-primary dark:text-slate-300"
            >
              Cameras
            </router-link>
            <span class="border-b-2 border-primary text-sm font-bold text-slate-900 dark:text-white">
              Analysis
            </span>
          </nav>
        </div>

        <div class="flex flex-1 items-center justify-end gap-4">
          <label class="flex h-10 min-w-40 max-w-64 flex-col">
            <div
              class="flex h-full w-full flex-1 items-stretch overflow-hidden rounded-xl border border-slate-200 dark:border-slate-700"
            >
              <div class="flex items-center justify-center bg-slate-50 pl-4 text-slate-400 dark:bg-slate-800">
                <span class="material-symbols-outlined">search</span>
              </div>
              <input
                class="form-input min-w-0 flex-1 border-none bg-slate-50 text-sm placeholder:text-slate-400 focus:ring-0 dark:bg-slate-800"
                placeholder="Search batch or ID..."
                value=""
              />
            </div>
          </label>

          <div class="flex gap-2">
            <button
              class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-600 transition-all hover:bg-primary/10 hover:text-primary dark:bg-slate-800 dark:text-slate-300"
            >
              <span class="material-symbols-outlined">notifications</span>
            </button>
            <button
              class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-600 transition-all hover:bg-primary/10 hover:text-primary dark:bg-slate-800 dark:text-slate-300"
            >
              <span class="material-symbols-outlined">account_circle</span>
            </button>
          </div>

          <div
            class="size-10 rounded-full border-2 border-primary/20 bg-cover bg-center bg-no-repeat"
            data-alt="User profile avatar of a technician"
            style='background-image: url("https://lh3.googleusercontent.com/aida-public/AB6AXuChevDoC59IzQ13P3sgsC-lztsIEhnhnH2eJUW-2hk4X6lfloMAc-95mG5IkL7qTK5re15rHjMU-dc3VgVXgT_vgDlt4J3pVN7hGC8H-zpR8wcDYYKob-dl1QJCuNAZ59aPxjAFdeGJU8pJ159xlrAStn8tWTks6ZNCJwVFt28sfZzQUg7rCJSQbG_lZmSEIWTg0WGp0irHI6Ouy9Nd-9FcggqGbXPB38mehAiv2yLswCPLEwPCjQJVO1ugAtDMLIEy-uzpyNxKY-A");'
          />
        </div>
      </header>

      <main class="mx-auto flex w-full max-w-[1920px] flex-1 flex-col gap-6 overflow-y-auto p-6 lg:px-10">
        <div class="flex flex-col items-start justify-between gap-4 md:flex-row md:items-end">
          <div class="flex flex-col gap-1">
            <div class="mb-1 flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
              <span>Quality Control</span>
              <span class="material-symbols-outlined text-xs">chevron_right</span>
              <span class="font-medium text-primary">QC Screen 7 - Production Line A</span>
            </div>
            <h1 class="text-3xl font-black tracking-tight text-slate-900 dark:text-white">
              Live Food Quality Inspection
            </h1>
            <p class="text-slate-500 dark:text-slate-400">
              Comparing real-time camera feed against Master Reference Batch A-102
            </p>
          </div>

          <div class="flex gap-3">
            <button
              class="flex h-11 items-center gap-2 rounded-xl bg-slate-200 px-6 text-sm font-bold text-slate-700 transition-all hover:bg-slate-300 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
            >
              <span class="material-symbols-outlined">settings</span>
              Configure
            </button>
            <button
              class="flex h-11 items-center gap-2 rounded-xl bg-primary px-6 text-sm font-bold text-white shadow-lg shadow-primary/20 transition-all hover:bg-primary/90"
            >
              <span class="material-symbols-outlined">description</span>
              Export Report
            </button>
          </div>
        </div>

        <div class="grid grid-cols-12 gap-6">
          <div class="col-span-12 flex flex-col gap-6 lg:col-span-8">
            <div class="grid grid-cols-2 gap-4">
              <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
                <div class="mb-4 flex items-center justify-between">
                  <h3 class="flex items-center gap-2 font-bold">
                    <span class="material-symbols-outlined text-primary">verified_user</span>
                    Master Reference
                  </h3>
                  <span class="rounded bg-slate-100 px-2 py-1 text-xs text-slate-500 dark:bg-slate-800">
                    Ref: A-102
                  </span>
                </div>

                <div class="relative aspect-video w-full overflow-hidden rounded-lg border border-slate-200 bg-slate-100 dark:border-slate-700 dark:bg-slate-800">
                  <div
                    class="absolute inset-0 bg-cover bg-center"
                    style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuBksv3P0wCFxjYVxRvCLuEAho47vWkxyUeUU6G0_kb6bNujBDTGJbGjHtgnwH6FZCtvkGgdor9fIxLa-0tpgRq1xBzOBz1jYY5xc57Tf4r9h9QloqstUn31H2fNaVo8CK_cGJUVbmc5uD-CdJmZbOc5ik1gbL9u30fE38ijMxqv_LTvSXg8QliwLOKSmV8j33qzZTCamDCdW09CvHXyrXl0ixWzbYKs_7kBGCzDjI_iu0AmYe73WAYMOlEAcisDOVdlzRONq_w-3DI');"
                  />
                  <div class="absolute left-3 top-3 rounded bg-black/60 px-2 py-0.5 text-[10px] text-white backdrop-blur-md">
                    STATIC REFERENCE
                  </div>
                </div>

                <p class="mt-3 text-sm italic text-slate-500 dark:text-slate-400">
                  "Ideal texture, color saturation, and ingredient distribution."
                </p>
              </div>

              <div
                class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm ring-2 ring-primary/20 dark:border-slate-800 dark:bg-slate-900"
              >
                <div class="mb-4 flex items-center justify-between">
                  <h3 class="flex items-center gap-2 font-bold">
                    <span class="material-symbols-outlined animate-pulse text-red-500">videocam</span>
                    Live Stream
                  </h3>
                  <span class="rounded bg-red-100 px-2 py-1 text-xs font-bold text-red-600 dark:bg-red-900/30 dark:text-red-400">
                    LIVE: NODE 04
                  </span>
                </div>

                <div class="relative aspect-video w-full overflow-hidden rounded-lg border border-slate-200 bg-slate-100 dark:border-slate-700 dark:bg-slate-800">
                  <div
                    class="absolute inset-0 bg-cover bg-center"
                    style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuBjhmAyj2BGrMD_GOhDV9gFtj3VvHHKDcxT3J4rGwZaKONUIVFNNyx-xxAtYYBib32SuQddaVCxjdGBgrM28exOBfxbb5ynqLFlD1x72cAslxKLrUxQkS1n5E1z5BD65pk4ys5TMD187mu6pFc__lBexyUR8CYvgAbo7TzRxtvTkBoeHlhwgbVsk0Jo5o-3hMTYcNMNAvj527KuYTnePen2NgDmsAi8Qj9zTuZpyZBxb01EN-6Ef1VbtNhH4aaEMXTZUY_HagYsDoU');"
                  />
                  <div class="pointer-events-none absolute inset-0 border-[3px] border-primary/40" />
                  <div class="absolute bottom-3 right-3 rounded bg-primary px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider text-white">
                    Analyzing...
                  </div>
                </div>

                <div class="mt-3 flex items-center justify-between">
                  <p class="text-sm text-slate-500 dark:text-slate-400">Timestamp: 14:22:05:12</p>
                  <div class="flex gap-1">
                    <div class="size-2 rounded-full bg-primary" />
                    <div class="size-2 rounded-full bg-primary/30" />
                    <div class="size-2 rounded-full bg-primary/30" />
                  </div>
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
              <div class="flex flex-col">
                <span class="text-sm font-medium uppercase tracking-widest text-slate-500 dark:text-slate-400">
                  Similarity Score
                </span>
                <div class="flex items-baseline gap-3">
                  <h2 class="text-5xl font-black text-slate-900 dark:text-white">98.4%</h2>
                  <span class="flex items-center gap-1 font-bold text-green-500">
                    <span class="material-symbols-outlined">trending_up</span>
                    +0.2%
                  </span>
                </div>
              </div>

              <div class="max-w-md flex-1 px-10">
                <div class="flex h-4 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800">
                  <div class="h-full bg-primary" style="width: 98.4%" />
                </div>
                <div class="mt-2 flex justify-between text-[10px] font-bold uppercase text-slate-400">
                  <span>Critical (85%)</span>
                  <span>Warning (92%)</span>
                  <span>Optimal (95%+)</span>
                </div>
              </div>

              <div class="flex flex-col items-end">
                <span class="rounded-full bg-green-100 px-3 py-1 text-sm font-bold text-green-500 dark:bg-green-900/30">
                  MATCH PASSED
                </span>
                <span class="mt-1 text-xs text-slate-400">Confidence: 0.998</span>
              </div>
            </div>
          </div>

          <div class="col-span-12 flex flex-col gap-6 lg:col-span-4">
            <div class="flex h-full flex-col overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
              <div class="border-b border-slate-200 bg-slate-50/70 p-4 dark:border-slate-800 dark:bg-slate-800/60">
                <h3 class="mb-4 font-bold text-slate-900 dark:text-white">Recent Inspections</h3>

                <div class="flex gap-2 rounded-lg bg-slate-100 p-1 dark:bg-slate-950">
                  <button
                    class="flex-1 rounded-md px-3 py-2 text-xs font-bold transition-all"
                    :class="activeFilter === 'all'
                      ? 'bg-white text-primary shadow-sm dark:bg-slate-800'
                      : 'text-slate-500 hover:bg-white/50 dark:hover:bg-slate-800/50'"
                    @click="handleFilterClick('all')"
                  >
                    All
                  </button>
                  <button
                    class="flex-1 rounded-md px-3 py-2 text-xs font-bold transition-all"
                    :class="activeFilter === 'passed'
                      ? 'bg-white text-primary shadow-sm dark:bg-slate-800'
                      : 'text-slate-500 hover:bg-white/50 dark:hover:bg-slate-800/50'"
                    @click="handleFilterClick('passed')"
                  >
                    Passed
                  </button>
                  <button
                    class="flex-1 rounded-md px-3 py-2 text-xs font-bold transition-all"
                    :class="activeFilter === 'failed'
                      ? 'bg-white text-primary shadow-sm dark:bg-slate-800'
                      : 'text-slate-500 hover:bg-white/50 dark:hover:bg-slate-800/50'"
                    @click="handleFilterClick('failed')"
                  >
                    Failed
                  </button>
                </div>
              </div>

              <div ref="logContainerRef" class="qc-scroll-area overflow-y-auto" @scroll="handleLogScroll">
                <div class="relative min-h-full">
                  <table class="w-full border-collapse text-left">
                    <thead
                      class="sticky top-0 z-20 border-b border-slate-200 bg-white/95 shadow-[0_1px_0_0_rgba(226,232,240,0.8)] backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/95"
                    >
                      <tr class="text-[10px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                        <th class="px-4 py-3">Timestamp</th>
                        <th class="px-4 py-3">Score</th>
                        <th class="px-4 py-3 text-right">Status</th>
                      </tr>
                    </thead>

                    <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                      <tr
                        v-for="item in qcResults"
                        :key="item.id"
                        class="h-[56px]"
                        :class="item.result_status === 'failed'
                          ? 'bg-red-50/30 dark:bg-red-900/10'
                          : 'transition-colors hover:bg-slate-50 dark:hover:bg-slate-800'"
                      >
                        <td class="px-4 py-3">
                          <div class="flex flex-col justify-center leading-tight">
                            <span class="text-sm font-medium">
                              {{ formatTime(item.checked_at) }}
                            </span>
                            <span class="mt-1 text-[10px] text-slate-400">
                              Batch {{ getBatchId(item.id) }}
                            </span>
                          </div>
                        </td>

                        <td class="px-4 py-3 text-sm font-bold" :class="item.result_status === 'failed' ? 'text-red-500' : ''">
                          {{ Math.round(item.similarity_score * 100) }}%
                        </td>

                        <td class="px-4 py-3 text-right">
                          <span
                            v-if="item.result_status === 'passed'"
                            class="inline-flex items-center rounded bg-green-100 px-2 py-0.5 text-xs font-bold text-green-700 dark:bg-green-900/30 dark:text-green-400"
                          >
                            PASS
                          </span>
                          <span
                            v-else
                            class="inline-flex items-center rounded bg-red-100 px-2 py-0.5 text-xs font-bold text-red-700 dark:bg-red-900/30 dark:text-red-400"
                          >
                            FAIL
                          </span>
                        </td>
                      </tr>

                      <tr v-if="qcResults.length === 0">
                        <td colspan="3" class="px-4 py-8 text-center text-slate-400">
                          No data available
                        </td>
                      </tr>
                    </tbody>
                  </table>

                  <div
                    v-if="isLoading"
                    class="absolute inset-0 z-30 flex items-center justify-center bg-white/60 backdrop-blur-[1px] dark:bg-slate-900/60"
                  >
                    <div class="h-8 w-8 animate-spin rounded-full border-b-2 border-primary" />
                  </div>

                  <div
                    v-if="isLoadingMore"
                    class="sticky bottom-0 z-10 flex items-center justify-center gap-2 border-t border-slate-200 bg-white/95 px-4 py-3 text-sm text-slate-400 dark:border-slate-700 dark:bg-slate-900/95"
                  >
                    <div class="h-4 w-4 animate-spin rounded-full border-b-2 border-primary" />
                    Loading more...
                  </div>
                </div>
              </div>

              <div class="border-t border-slate-200 bg-slate-50 p-4 text-center dark:border-slate-800 dark:bg-slate-800/50">
                <button
                  v-if="!showFullLog"
                  class="text-sm font-bold text-primary hover:underline"
                  @click="viewFullLog(activeFilter)"
                >
                  View Full Analysis Log
                </button>

                <button
                  v-else
                  class="text-sm font-bold text-slate-600 hover:underline dark:text-slate-300"
                  @click="collapseFullLog(activeFilter)"
                >
                  Back to Preview
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 gap-4 md:grid-cols-4">
          <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3">
              <div class="flex size-10 items-center justify-center rounded-lg bg-orange-100 text-primary dark:bg-orange-900/30">
                <span class="material-symbols-outlined">palette</span>
              </div>
              <div>
                <p class="text-xs font-bold uppercase tracking-wider text-slate-500">Color Match</p>
                <p class="text-xl font-bold">99.1%</p>
              </div>
            </div>
          </div>

          <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3">
              <div class="flex size-10 items-center justify-center rounded-lg bg-blue-100 text-blue-600 dark:bg-blue-900/30">
                <span class="material-symbols-outlined">texture</span>
              </div>
              <div>
                <p class="text-xs font-bold uppercase tracking-wider text-slate-500">Texture Diff</p>
                <p class="text-xl font-bold">1.2%</p>
              </div>
            </div>
          </div>

          <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3">
              <div class="flex size-10 items-center justify-center rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-900/30">
                <span class="material-symbols-outlined">view_in_ar</span>
              </div>
              <div>
                <p class="text-xs font-bold uppercase tracking-wider text-slate-500">Volume Est.</p>
                <p class="text-xl font-bold">482g</p>
              </div>
            </div>
          </div>

          <div class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3">
              <div class="flex size-10 items-center justify-center rounded-lg bg-green-100 text-green-600 dark:bg-green-900/30">
                <span class="material-symbols-outlined">thermostat</span>
              </div>
              <div>
                <p class="text-xs font-bold uppercase tracking-wider text-slate-500">Surface Temp</p>
                <p class="text-xl font-bold">68.4°C</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer class="border-t border-slate-200 p-4 text-center dark:border-slate-800">
        <p class="text-xs text-slate-400">
          System Version 4.2.1-QC | Node 04 Connected | All systems nominal
        </p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import ApiService from '@/services/ApiService'

const apiService = new ApiService()

const DEFAULT_PAGE_SIZE = 10
const activeFilter = ref('all')
const isLoading = ref(false)
const isLoadingMore = ref(false)
const logContainerRef = ref(null)

const createTabState = () => ({
  items: [],
  currentPage: 1,
  hasMore: true,
  showFullLog: false,
  isLoadedAll: false,
  scrollTop: 0,
})

const tabStates = ref({
  all: createTabState(),
  passed: createTabState(),
  failed: createTabState(),
})

const currentTabState = computed(() => tabStates.value[activeFilter.value] || createTabState())
const qcResults = computed(() => currentTabState.value.items || [])
const showFullLog = computed(() => currentTabState.value.showFullLog || false)

const buildParamsByTab = (tabKey, page = 1, loadAll = false) => {
  const params = {}

  if (loadAll) {
    params.is_all = 1
  } else {
    params.page = page
    params.page_size = DEFAULT_PAGE_SIZE
  }

  if (tabKey === 'passed') {
    params.status_filter = 'passed'
  } else if (tabKey === 'failed') {
    params.status_filter = 'failed'
  }

  return params
}

const waitForPaint = async () => {
  await nextTick()
  await new Promise((resolve) => requestAnimationFrame(() => resolve()))
}

const saveScrollPosition = (tabKey = activeFilter.value) => {
  const tab = tabStates.value[tabKey]
  if (!tab || !logContainerRef.value) return 0

  const top = logContainerRef.value.scrollTop || 0
  tab.scrollTop = top
  return top
}

const restoreScrollPosition = async (tabKey = activeFilter.value) => {
  const tab = tabStates.value[tabKey]
  if (!tab || !logContainerRef.value) return

  await waitForPaint()
  logContainerRef.value.scrollTop = tab.scrollTop || 0
}

const handleLogScroll = () => {
  const tab = tabStates.value[activeFilter.value]
  if (!tab || !logContainerRef.value) return

  tab.scrollTop = logContainerRef.value.scrollTop || 0
}

const fetchQCResults = async (tabKey = 'all', page = 1, reset = false) => {
  const tab = tabStates.value[tabKey]
  if (!tab) return

  isLoading.value = true

  try {
    const params = buildParamsByTab(tabKey, page, false)
    const response = await apiService.get('/v1/food/qc-results', params)
    const data = Array.isArray(response) ? response : []

    if (reset || page === 1) {
      tab.items = data
    } else {
      tab.items = [...tab.items, ...data]
    }

    tab.currentPage = page
    tab.hasMore = data.length === DEFAULT_PAGE_SIZE
  } catch (error) {
    console.error(`Error fetching QC results for tab "${tabKey}":`, error)
  } finally {
    isLoading.value = false
  }
}

const fetchAllQCResults = async (tabKey = 'all') => {
  const tab = tabStates.value[tabKey]
  if (!tab) return

  isLoading.value = true

  try {
    const params = buildParamsByTab(tabKey, 1, true)
    const response = await apiService.get('/v1/food/qc-results', params)
    const data = Array.isArray(response) ? response : []

    tab.items = data
    tab.showFullLog = true
    tab.isLoadedAll = true
    tab.currentPage = 1
    tab.hasMore = false
  } catch (error) {
    console.error(`Error fetching ALL QC results for tab "${tabKey}":`, error)
  } finally {
    isLoading.value = false
  }
}

const viewFullLog = async (tabKey = activeFilter.value) => {
  const tab = tabStates.value[tabKey]
  if (!tab) return

  if (tabKey === activeFilter.value) {
    saveScrollPosition(tabKey)
  }

  if (!tab.isLoadedAll) {
    await fetchAllQCResults(tabKey)
  } else {
    tab.showFullLog = true
  }

  if (tabKey === activeFilter.value) {
    await restoreScrollPosition(tabKey)
  }
}

const collapseFullLog = async (tabKey = activeFilter.value) => {
  const tab = tabStates.value[tabKey]
  if (!tab) return

  tab.showFullLog = false
  tab.isLoadedAll = false
  tab.currentPage = 1
  tab.hasMore = true
  tab.scrollTop = 0

  await fetchQCResults(tabKey, 1, true)

  if (tabKey === activeFilter.value) {
    await restoreScrollPosition(tabKey)
  }
}

const handleFilterClick = async (filter) => {
  const previousTab = activeFilter.value
  saveScrollPosition(previousTab)

  activeFilter.value = filter

  const tab = tabStates.value[filter]
  if (!tab) return

  if (!tab.items.length) {
    await fetchQCResults(filter, 1, true)
  }

  await restoreScrollPosition(filter)
}

const refreshCurrentTab = async () => {
  const tabKey = activeFilter.value
  const tab = tabStates.value[tabKey]
  if (!tab) return

  saveScrollPosition(tabKey)

  if (tab.showFullLog) {
    await fetchAllQCResults(tabKey)
  } else {
    await fetchQCResults(tabKey, 1, true)
  }

  await restoreScrollPosition(tabKey)
}

const formatTime = (timestamp) => {
  if (!timestamp) return '--:--:--'

  const date = new Date(timestamp)
  return date.toLocaleTimeString('vi-VN', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

const getBatchId = (id) => {
  if (!id) return 'N/A'
  return String(id).substring(0, 8).toUpperCase()
}

onMounted(async () => {
  await fetchQCResults('all', 1, true)
})
</script>

<style scoped>
.qc-scroll-area {
  height: 332px;
  max-height: 332px;
  min-height: 332px;
}
</style>