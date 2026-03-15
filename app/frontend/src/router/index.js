import { createRouter, createWebHistory } from 'vue-router'

// Lazy loading all views for better performance
const LoginView = () => import('../views/LoginView.vue')
const DashboardView = () => import('../views/DashboardView.vue')
const LiveView = () => import('../views/LiveView.vue')
const CameraConfigView = () => import('../views/CameraConfigView.vue')
const FoodQCView = () => import('../views/FoodQCView.vue')
const KitchenAnalyticsView = () => import('../views/KitchenAnalyticsView.vue')
const ReceptionistDashboardView = () => import('../views/ReceptionistDashboardView.vue')
const RTSPSetupView = () => import('../views/RTSPSetupView.vue')
const StaffAttendanceView = () => import('../views/StaffAttendanceView.vue')
const StaffPerformanceView = () => import('../views/StaffPerformanceView.vue')
const CustomerAnalyticsView = () => import('../views/CustomerAnalyticsView.vue')

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView
  },
  {
    path: '/live-view',
    name: 'live-view',
    component: LiveView
  },
  {
    path: '/camera-config',
    name: 'camera-config',
    component: CameraConfigView
  },
  {
    path: '/food-qc',
    name: 'food-qc',
    component: FoodQCView
  },
  {
    path: '/kitchen-analytics',
    name: 'kitchen-analytics',
    component: KitchenAnalyticsView
  },
  {
    path: '/receptionist-dashboard',
    name: 'receptionist-dashboard',
    component: ReceptionistDashboardView
  },
  {
    path: '/rtsp-setup',
    name: 'rtsp-setup',
    component: RTSPSetupView
  },
  {
    path: '/staff-attendance',
    name: 'staff-attendance',
    component: StaffAttendanceView
  },
  {
    path: '/staff-performance',
    name: 'staff-performance',
    component: StaffPerformanceView
  },
  {
    path: '/customer-analytics',
    name: 'customer-analytics',
    component: CustomerAnalyticsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Auth guard - redirect to login if not authenticated
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('auth_token')

  // List of routes that require authentication
  const protectedRoutes = ['dashboard', 'live-view', 'camera-config', 'food-qc',
    'kitchen-analytics', 'receptionist-dashboard', 'rtsp-setup',
    'staff-attendance', 'staff-performance', 'customer-analytics']

  const isProtectedRoute = protectedRoutes.includes(to.name)

  if (isProtectedRoute && !token) {
    next({ name: 'login' })
  } else if (to.name === 'login' && token) {
    // If already logged in, redirect to dashboard
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
