import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../pages/Dashboard.vue'

// Placeholder components for other routes
const Login = { template: '<div class="min-h-screen bg-black-100 flex items-center justify-center"><div class="text-[#F9FAFB] text-xl">Login Page - Coming Soon</div></div>' }
const DataBrokers = { template: '<div class="min-h-screen bg-black-100 flex items-center justify-center"><div class="text-[#F9FAFB] text-xl">Data Brokers Page - Coming Soon</div></div>' }
const Requests = { template: '<div class="min-h-screen bg-black-100 flex items-center justify-center"><div class="text-[#F9FAFB] text-xl">Requests Page - Coming Soon</div></div>' }
const Settings = { template: '<div class="min-h-screen bg-black-100 flex items-center justify-center"><div class="text-[#F9FAFB] text-xl">Settings Page - Coming Soon</div></div>' }

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/data-brokers',
    name: 'DataBrokers',
    component: DataBrokers
  },
  {
    path: '/requests',
    name: 'Requests',
    component: Requests
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router