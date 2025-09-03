<template>
  <aside class="fixed left-0 top-0 h-full w-64 bg-[#1E1E1E] border-r border-[#2D2D2D] flex flex-col">
    <!-- Logo/Brand Section -->
    <div class="p-6 border-b border-[#2D2D2D]">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 bg-gradient-to-br from-[#06B6D4] to-[#14B8A6] rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-black" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </div>
        <span class="text-[#F9FAFB] font-semibold text-lg">DataShield</span>
      </div>
    </div>

    <!-- Navigation Menu -->
    <nav class="flex-1 px-4 py-6 space-y-2">
      <router-link
        v-for="item in navigationItems"
        :key="item.name"
        :to="item.path"
        class="group flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-all duration-200 hover:bg-[#2D2D2D]"
        :class="{
          'bg-[#06B6D4] bg-opacity-10 text-[#06B6D4] border-r-2 border-[#06B6D4]': isActive(item.path),
          'text-[#D1D5DB] hover:text-[#F9FAFB]': !isActive(item.path)
        }"
      >
        <component 
          :is="item.icon" 
          class="mr-3 h-5 w-5 flex-shrink-0"
          :class="{
            'text-[#06B6D4]': isActive(item.path),
            'text-[#9CA3AF] group-hover:text-[#D1D5DB]': !isActive(item.path)
          }"
        />
        {{ item.name }}
      </router-link>
    </nav>

    <!-- User Profile Section -->
    <div class="p-4 border-t border-[#2D2D2D]">
      <div class="flex items-center space-x-3 px-4 py-3">
        <div class="w-8 h-8 bg-[#06B6D4] rounded-full flex items-center justify-center">
          <span class="text-black font-medium text-sm">{{ userInitials }}</span>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-[#F9FAFB] truncate">{{ userName }}</p>
          <p class="text-xs text-[#9CA3AF] truncate">{{ userEmail }}</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

// Icons as simple SVG components
const HomeIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/></svg>`
}

const DatabaseIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20"><path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/></svg>`
}

const ClipboardIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20"><path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z"/><path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z"/></svg>`
}

const CogIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/></svg>`
}

const route = useRoute()

const navigationItems = [
  { name: 'Dashboard', path: '/dashboard', icon: HomeIcon },
  { name: 'Data Brokers', path: '/data-brokers', icon: DatabaseIcon },
  { name: 'Requests', path: '/requests', icon: ClipboardIcon },
  { name: 'Settings', path: '/settings', icon: CogIcon },
]

// Mock user data - replace with actual user store
const userName = 'John Doe'
const userEmail = 'john@example.com'
const userInitials = computed(() => {
  return userName
    .split(' ')
    .map(name => name.charAt(0))
    .join('')
    .toUpperCase()
})

const isActive = (path: string) => {
  return route.path === path
}
</script>