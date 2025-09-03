<template>
  <div class="bg-[#1E1E1E] rounded-xl p-6 border border-[#2D2D2D] hover:border-[#06B6D4] transition-all duration-300">
    <!-- Card Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="p-2 bg-[#06B6D4] bg-opacity-10 rounded-lg">
          <component :is="icon" class="w-6 h-6 text-[#06B6D4]" />
        </div>
        <div>
          <h3 class="text-lg font-semibold text-[#F9FAFB]">{{ title }}</h3>
          <p class="text-sm text-[#9CA3AF]">{{ subtitle }}</p>
        </div>
      </div>
      <div class="text-right">
        <div class="text-2xl font-bold text-[#06B6D4]">{{ value }}</div>
        <div class="text-xs text-[#9CA3AF]">{{ label }}</div>
      </div>
    </div>

    <!-- Progress Bar (if showProgress is true) -->
    <div v-if="showProgress" class="mb-4">
      <div class="flex justify-between text-sm text-[#D1D5DB] mb-2">
        <span>Progress</span>
        <span>{{ progressPercentage }}%</span>
      </div>
      <div class="w-full bg-[#2D2D2D] rounded-full h-2">
        <div 
          class="bg-gradient-to-r from-[#06B6D4] to-[#14B8A6] h-2 rounded-full transition-all duration-500 ease-out"
          :style="{ width: `${progressPercentage}%` }"
        ></div>
      </div>
    </div>

    <!-- Status Breakdown -->
    <div v-if="statusBreakdown" class="space-y-3">
      <div 
        v-for="status in statusBreakdown" 
        :key="status.label"
        class="flex items-center justify-between"
      >
        <div class="flex items-center space-x-3">
          <div 
            class="w-3 h-3 rounded-full"
            :style="{ backgroundColor: status.color }"
          ></div>
          <span class="text-sm text-[#D1D5DB]">{{ status.label }}</span>
        </div>
        <span class="text-sm font-medium text-[#F9FAFB]">{{ status.count }}</span>
      </div>
    </div>

    <!-- Action Button -->
    <div v-if="actionText" class="mt-6 pt-4 border-t border-[#2D2D2D]">
      <button 
        @click="$emit('action')"
        class="w-full px-4 py-2 bg-[#06B6D4] bg-opacity-10 text-[#06B6D4] border border-[#06B6D4] rounded-lg hover:bg-[#06B6D4] hover:text-black transition-all duration-200 font-medium"
      >
        {{ actionText }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface StatusItem {
  label: string
  count: number
  color: string
}

interface Props {
  title: string
  subtitle?: string
  value: string | number
  label?: string
  icon?: any
  showProgress?: boolean
  progress?: number
  total?: number
  statusBreakdown?: StatusItem[]
  actionText?: string
}

const props = withDefaults(defineProps<Props>(), {
  subtitle: '',
  label: '',
  showProgress: false,
  progress: 0,
  total: 100,
  actionText: ''
})


const progressPercentage = computed(() => {
  if (props.total === 0) return 0
  return Math.round((props.progress / props.total) * 100)
})

// Default icon if none provided
const DefaultIcon = {
  template: `<svg fill="currentColor" viewBox="0 0 20 20"><path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
}

const icon = props.icon || DefaultIcon
</script>