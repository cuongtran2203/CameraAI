import router from '../router'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  /**
   * Get auth token from localStorage
   */
  getToken() {
    return localStorage.getItem('auth_token')
  }

  /**
   * Set auth token to localStorage
   */
  setToken(token) {
    localStorage.setItem('auth_token', token)
  }

  /**
   * Remove auth token from localStorage
   */
  removeToken() {
    localStorage.removeItem('auth_token')
  }

  /**
   * Get headers with Authorization token
   */
  getHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    }

    const token = this.getToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    return headers
  }

  /**
   * Handle API response
   */
  async handleResponse(response) {
    if (response.status === 401) {
      // Token expired or invalid - redirect to login
      this.removeToken()
      router.push('/login')
      throw new Error('Unauthorized')
    }

    if (response.status === 403) {
      throw new Error('Forbidden')
    }

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Something went wrong')
    }

    return data
  }

  /**
   * GET request
   */
  async get(endpoint, params = {}) {
    const url = new URL(`${this.baseURL}${endpoint}`)

    // Add query params if exists
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined) {
        url.searchParams.append(key, params[key])
      }
    })

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: this.getHeaders(),
    })

    return this.handleResponse(response)
  }

  /**
   * POST request
   */
  async post(endpoint, data = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    })

    return this.handleResponse(response)
  }

  /**
   * PUT request
   */
  async put(endpoint, data = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PUT',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    })

    return this.handleResponse(response)
  }

  /**
   * PATCH request
   */
  async patch(endpoint, data = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PATCH',
      headers: this.getHeaders(),
      body: JSON.stringify(data),
    })

    return this.handleResponse(response)
  }

  /**
   * DELETE request
   */
  async delete(endpoint) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    })

    return this.handleResponse(response)
  }

  /**
   * Upload file with FormData
   */
  async upload(endpoint, formData) {
    const headers = {}
    const token = this.getToken()
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers,
      body: formData,
    })

    return this.handleResponse(response)
  }
}

// Export singleton instance
export const api = new ApiService()

// Export class for extension
export default ApiService
