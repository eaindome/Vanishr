import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface User {
  id: string
  name: string
  email: string
  createdAt: Date
}

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)

  // Mock user data for development
  const mockUser: User = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    createdAt: new Date('2024-01-01')
  }

  // Actions
  const login = async (_email: string, _password: string) => {
    isLoading.value = true
    try {
      // Mock login - replace with actual API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      user.value = mockUser
      isAuthenticated.value = true
      return { success: true }
    } catch (error) {
      return { success: false, error: 'Login failed' }
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    isAuthenticated.value = false
  }

  const updateProfile = (updates: Partial<User>) => {
    if (user.value) {
      user.value = { ...user.value, ...updates }
    }
  }

  // Initialize with mock data for development
  const initializeMockUser = () => {
    user.value = mockUser
    isAuthenticated.value = true
  }

  // Getters
  const getUserInitials = () => {
    if (!user.value) return ''
    return user.value.name
      .split(' ')
      .map(name => name.charAt(0))
      .join('')
      .toUpperCase()
  }

  const getFullName = () => {
    return user.value?.name || ''
  }

  const getEmail = () => {
    return user.value?.email || ''
  }

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    
    // Actions
    login,
    logout,
    updateProfile,
    initializeMockUser,
    
    // Getters
    getUserInitials,
    getFullName,
    getEmail
  }
})