import { ref, onMounted, onUnmounted } from 'vue'
import { useAuth } from './useAuth'

// Constants
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

// Global state for singleton pattern
const wsConnection = ref(null)
const isConnected = ref(false)
const lastMessage = ref(null)
const connectionError = ref(null)

// Event handlers
const eventHandlers = {
  food_qc_result: [],
  food_qc_stats: [],
  food_qc_history: [],
  connected: [],
  disconnected: [],
  error: []
}

// =====================================================
// WebSocket Composable for Food QC
// =====================================================

export function useFoodQCWebSocket() {
  const { getToken } = useAuth()

  let reconnectAttempts = 0
  const maxReconnectAttempts = 5
  let reconnectTimeout = null
  let pingInterval = null

  // ---------------------------------------------
  // Connection Management
  // ---------------------------------------------

  const connect = () => {
    if (wsConnection.value && wsConnection.value.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected')
      return
    }

    const token = getToken()
    const wsUrl = token
      ? `${WS_URL}/ws/food-qc?token=${token}`
      : `${WS_URL}/ws/food-qc`

    try {
      console.log('Connecting to Food QC WebSocket...')
      wsConnection.value = new WebSocket(wsUrl)

      wsConnection.value.onopen = () => {
        console.log('Food QC WebSocket connected')
        isConnected.value = true
        connectionError.value = null
        reconnectAttempts = 0

        // Start ping interval
        startPingInterval()

        // Notify handlers
        emitEvent('connected', { timestamp: new Date().toISOString() })
      }

      wsConnection.value.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data)
          handleMessage(message)
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      wsConnection.value.onerror = (error) => {
        console.error('Food QC WebSocket error:', error)
        connectionError.value = error
        emitEvent('error', error)
      }

      wsConnection.value.onclose = (event) => {
        console.log('Food QC WebSocket closed', event.code, event.reason)
        isConnected.value = false

        // Clear ping interval
        stopPingInterval()

        // Notify handlers
        emitEvent('disconnected', { code: event.code, reason: event.reason })

        // Attempt to reconnect
        if (reconnectAttempts < maxReconnectAttempts) {
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000)
          console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts + 1}/${maxReconnectAttempts})`)
          reconnectTimeout = setTimeout(() => {
            reconnectAttempts++
            connect()
          }, delay)
        }
      }
    } catch (error) {
      console.error('Error creating WebSocket:', error)
      connectionError.value = error
    }
  }

  const disconnect = () => {
    // Clear reconnection timeout
    if (reconnectTimeout) {
      clearTimeout(reconnectTimeout)
      reconnectTimeout = null
    }

    stopPingInterval()

    // Close connection
    if (wsConnection.value) {
      wsConnection.value.close()
      wsConnection.value = null
    }

    isConnected.value = false
  }

  // ---------------------------------------------
  // Message Handling
  // ---------------------------------------------

  const handleMessage = (message) => {
    lastMessage.value = message

    switch (message.type) {
      case 'food_qc_result':
        emitEvent('food_qc_result', message.data || message)
        break

      case 'food_qc_stats':
        emitEvent('food_qc_stats', message.data || message)
        break

      case 'food_qc_history':
        emitEvent('food_qc_history', message.data || message)
        break

      case 'connected':
        console.log('WebSocket connected:', message.message)
        break

      case 'ping':
        // Respond to server ping
        sendMessage({ type: 'pong' })
        break

      case 'pong':
        // Server acknowledged our ping
        break

      default:
        console.log('Unknown message type:', message.type)
    }
  }

  const sendMessage = (data) => {
    if (wsConnection.value && wsConnection.value.readyState === WebSocket.OPEN) {
      wsConnection.value.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket not connected, cannot send message')
    }
  }

  // ---------------------------------------------
  // Ping/Pong for Keep-Alive
  // ---------------------------------------------

  const startPingInterval = () => {
    stopPingInterval()
    pingInterval = setInterval(() => {
      sendMessage({ type: 'ping' })
    }, 30000) // Ping every 30 seconds
  }

  const stopPingInterval = () => {
    if (pingInterval) {
      clearInterval(pingInterval)
      pingInterval = null
    }
  }

  // ---------------------------------------------
  // Event System
  // ---------------------------------------------

  const on = (event, handler) => {
    if (eventHandlers[event]) {
      eventHandlers[event].push(handler)
    }
  }

  const off = (event, handler) => {
    if (eventHandlers[event]) {
      const index = eventHandlers[event].indexOf(handler)
      if (index > -1) {
        eventHandlers[event].splice(index, 1)
      }
    }
  }

  const emitEvent = (event, data) => {
    if (eventHandlers[event]) {
      eventHandlers[event].forEach(handler => {
        try {
          handler(data)
        } catch (error) {
          console.error(`Error in ${event} handler:`, error)
        }
      })
    }
  }

  // ---------------------------------------------
  // Request Data
  // ---------------------------------------------

  const requestHistory = (limit = 10) => {
    sendMessage({
      type: 'get_history',
      limit: limit
    })
  }

  const subscribeToCamera = (cameraId) => {
    sendMessage({
      type: 'subscribe_camera',
      camera_id: cameraId
    })
  }

  // ---------------------------------------------
  // Cleanup
  // ---------------------------------------------

  onUnmounted(() => {
    disconnect()
  })

  return {
    // State
    isConnected,
    lastMessage,
    connectionError,

    // Connection
    connect,
    disconnect,

    // Messaging
    sendMessage,

    // Events
    on,
    off,

    // Data requests
    requestHistory,
    subscribeToCamera
  }
}

// =====================================================
// Simple event emitter for non-Vue usage
// =====================================================

export const foodQCEvents = {
  on: (event, handler) => {
    if (eventHandlers[event]) {
      eventHandlers[event].push(handler)
    }
  },
  off: (event, handler) => {
    if (eventHandlers[event]) {
      const index = eventHandlers[event].indexOf(handler)
      if (index > -1) {
        eventHandlers[event].splice(index, 1)
      }
    }
  },
  emit: (event, data) => {
    if (eventHandlers[event]) {
      eventHandlers[event].forEach(handler => handler(data))
    }
  }
}
