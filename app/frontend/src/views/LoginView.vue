<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-background-light dark:bg-background-dark group/design-root overflow-x-hidden">
    <div class="layout-container flex h-full grow flex-col">
      <header class="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-primary/20 px-6 md:px-10 py-4 bg-background-light dark:bg-background-dark/50 backdrop-blur-md sticky top-0 z-50">
        <div class="flex items-center gap-3 text-slate-900 dark:text-slate-100">
          <div class="size-8 flex items-center justify-center bg-primary rounded-lg text-white">
            <span class="material-symbols-outlined">videocam</span>
          </div>
          <h2 class="text-slate-900 dark:text-slate-100 text-xl font-bold leading-tight tracking-tight">Camera Analyst</h2>
        </div>
        <div class="flex items-center gap-2">
          <button class="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-200 dark:bg-primary/10 text-slate-700 dark:text-primary hover:bg-primary/20 transition-colors">
            <span class="material-symbols-outlined">shield_lock</span>
          </button>
        </div>
      </header>
      <main class="flex flex-1 items-center justify-center p-4 md:p-10 relative overflow-hidden">
        <!-- Background Decorative Elements -->
        <div class="absolute inset-0 z-0 opacity-20 pointer-events-none overflow-hidden">
          <div class="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-primary/20 blur-[120px]"></div>
          <div class="absolute bottom-[-10%] left-[-10%] w-[400px] h-[400px] rounded-full bg-primary/10 blur-[100px]"></div>
          <div class="absolute inset-0" data-alt="Subtle digital data grid pattern background" style="background-image: radial-gradient(circle at 2px 2px, rgba(236, 91, 19, 0.05) 1px, transparent 0); background-size: 40px 40px;"></div>
        </div>
        <div class="layout-content-container flex flex-col max-w-[480px] w-full flex-1 z-10">
          <div class="bg-white dark:bg-slate-900/40 backdrop-blur-xl border border-slate-200 dark:border-primary/10 rounded-xl shadow-2xl p-8 md:p-10">
            <div class="mb-8 flex flex-col items-center">
              <div class="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-6">
                <span class="material-symbols-outlined text-primary text-4xl">admin_panel_settings</span>
              </div>
              <h2 class="text-slate-900 dark:text-slate-100 tracking-tight text-3xl font-bold leading-tight text-center">Admin Login</h2>
              <p class="text-slate-500 dark:text-slate-400 text-base font-normal leading-normal mt-2 text-center">Secure access to the surveillance dashboard</p>
            </div>
            <form class="space-y-5" @submit.prevent="handleLogin">
              <div v-if="errorMessage" class="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-500 text-sm">
                {{ errorMessage }}
              </div>
              <div class="flex flex-col gap-2">
                <label class="text-slate-700 dark:text-slate-300 text-sm font-medium leading-none">Username or Email</label>
                <div class="relative">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-xl">person</span>
                  <input v-model="email" class="form-input flex w-full rounded-xl text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 focus:border-primary focus:ring-1 focus:ring-primary h-12 pl-12 pr-4 text-base transition-all placeholder:text-slate-400" placeholder="Enter admin credentials" type="text"/>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <div class="flex justify-between items-center">
                  <label class="text-slate-700 dark:text-slate-300 text-sm font-medium leading-none">Password</label>
                  <a class="text-primary text-sm font-semibold hover:underline" href="#">Forgot Password?</a>
                </div>
                <div class="relative">
                  <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-xl">lock</span>
                  <input v-model="password" class="form-input flex w-full rounded-xl text-slate-900 dark:text-white border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50 focus:border-primary focus:ring-1 focus:ring-primary h-12 pl-12 pr-4 text-base transition-all placeholder:text-slate-400" placeholder="••••••••" type="password"/>
                </div>
              </div>
              <div class="flex items-center gap-2 py-2">
                <input class="rounded border-slate-300 dark:border-slate-700 text-primary focus:ring-primary bg-transparent" id="remember" type="checkbox"/>
                <label class="text-slate-600 dark:text-slate-400 text-sm" for="remember">Remember this device</label>
              </div>
              <button :disabled="isLoading" class="w-full flex h-12 items-center justify-center rounded-xl bg-primary text-white text-base font-bold transition-all hover:bg-primary/90 hover:shadow-lg active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed" type="submit">
                          <span v-if="isLoading">Signing in...</span>
                          <span v-else>Sign In</span>
                        </button>
            </form>
            <div class="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800 flex justify-center gap-4">
              <p class="text-slate-500 dark:text-slate-400 text-xs text-center">
                            By logging in, you agree to our
                            <a class="text-primary hover:underline" href="#">Terms of Service</a> and
                            <a class="text-primary hover:underline" href="#">Privacy Policy</a>.
                        </p>
            </div>
          </div>
          <div class="mt-10 flex flex-wrap justify-center gap-8 opacity-60 grayscale hover:grayscale-0 transition-all duration-500">
            <div class="flex items-center gap-2 text-slate-400">
              <span class="material-symbols-outlined text-lg">verified_user</span>
              <span class="text-xs font-medium uppercase tracking-widest">End-to-End Encrypted</span>
            </div>
            <div class="flex items-center gap-2 text-slate-400">
              <span class="material-symbols-outlined text-lg">policy</span>
              <span class="text-xs font-medium uppercase tracking-widest">Compliance Ready</span>
            </div>
          </div>
        </div>
      </main>
      <footer class="py-6 px-10 border-t border-slate-200 dark:border-primary/10 text-center">
        <p class="text-slate-400 text-sm">
                © 2024 Camera Analyst Security Systems. All rights reserved.
            </p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const { login } = useAuth()

const email = ref('admin@cameraai.com')
const password = ref('admin123')
const errorMessage = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  errorMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Please enter both email and password'
    return
  }

  isLoading.value = true

  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 500))

  const result = await login(email.value, password.value)

  if (result.success) {
    router.push('/')
  } else {
    errorMessage.value = result.error
  }

  isLoading.value = false
}
</script>

<style scoped>
</style>
