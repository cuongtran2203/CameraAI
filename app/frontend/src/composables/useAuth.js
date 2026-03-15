import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

// Constants
const STORAGE_KEY = 'auth_token'
const USER_KEY = 'auth_user'

// State
const token = ref(localStorage.getItem(STORAGE_KEY) || '')
const user = ref(JSON.parse(localStorage.getItem(USER_KEY) || 'null'))

// Computed
const isAuthenticated = computed(() => !!token.value)

// Auth composable
export function useAuth() {
  const router = useRouter()

  // Login function - calls real API
  const login = async (email, password) => {
    try {
      // Call backend login API (form-data format)
      const formData = new URLSearchParams()
      formData.append('username', email)  // Backend expects 'username' field
      formData.append('password', password)

      const response = await fetch(`${import.meta.env.VITE_API_URL}/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData.toString()
      })

      if (!response.ok) {
        const error = await response.json()
        return { success: false, error: error.detail || 'Invalid email or password' }
      }

      const data = await response.json()

      // Store token
      token.value = data.access_token
      localStorage.setItem(STORAGE_KEY, data.access_token)

      // Store user info
      user.value = data.user
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))

      return { success: true, user: data.user }
    } catch (error) {
      console.error('Login error:', error)
      return { success: false, error: 'Connection error. Please try again.' }
    }
  }

  // Logout function
  const logout = () => {
    token.value = ''
    user.value = null
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem(USER_KEY)
    router.push('/login')
  }

  // Get current user
  const getCurrentUser = () => {
    return user.value
  }

  // Check if user is authenticated
  const checkAuth = () => {
    return isAuthenticated.value
  }

  // Get token
  const getToken = () => {
    return token.value
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    logout,
    getCurrentUser,
    checkAuth,
    getToken
  }
}
