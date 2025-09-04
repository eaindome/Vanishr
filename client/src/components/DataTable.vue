<template>
  <div class="bg-[#1E1E1E] rounded-xl border border-[#2D2D2D] overflow-hidden">
    <!-- Table Header -->
    <div class="px-6 py-4 border-b border-[#2D2D2D] bg-[#121212]">
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-[#F9FAFB]">{{ title }}</h3>
        <div class="flex items-center space-x-3">
          <!-- Search -->
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search..."
              class="w-64 px-4 py-2 bg-[#2D2D2D] border border-[#2D2D2D] rounded-lg text-[#F9FAFB] placeholder-[#9CA3AF] focus:outline-none focus:border-[#06B6D4] focus:ring-1 focus:ring-[#06B6D4] transition-colors"
            >
            <svg class="absolute right-3 top-2.5 w-4 h-4 text-[#9CA3AF]" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
            </svg>
          </div>
          <!-- Filter -->
          <select
            v-model="statusFilter"
            class="px-3 py-2 bg-[#2D2D2D] border border-[#2D2D2D] rounded-lg text-[#F9FAFB] focus:outline-none focus:border-[#06B6D4] focus:ring-1 focus:ring-[#06B6D4] transition-colors"
          >
            <option value="">All Status</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
            <option value="failed">Failed</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Table Content -->
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead class="bg-[#121212]">
          <tr>
            <th
              v-for="column in columns"
              :key="column.key"
              class="px-6 py-4 text-left text-xs font-medium text-[#9CA3AF] uppercase tracking-wider border-b border-[#2D2D2D]"
              :class="column.class"
            >
              <div class="flex items-center space-x-2">
                <span>{{ column.label }}</span>
                <button 
                  v-if="column.sortable"
                  @click="toggleSort(column.key)"
                  class="text-[#6B7280] hover:text-[#06B6D4] transition-colors"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M5 12a1 1 0 102 0V6.414l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L5 6.414V12zM15 8a1 1 0 10-2 0v5.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L15 13.586V8z" />
                  </svg>
                </button>
              </div>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-[#2D2D2D]">
          <tr 
            v-for="(row, index) in paginatedData" 
            :key="row.id || index"
            class="hover:bg-[#2D2D2D] transition-colors"
          >
            <td
              v-for="column in columns"
              :key="column.key"
              class="px-6 py-4 whitespace-nowrap text-sm"
              :class="column.class"
            >
              <!-- Status Badge -->
              <span 
                v-if="column.key === 'status'"
                class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                :class="getStatusClass(row[column.key])"
              >
                <span 
                  class="w-1.5 h-1.5 rounded-full mr-1.5"
                  :class="getStatusDotClass(row[column.key])"
                ></span>
                {{ formatStatus(row[column.key]) }}
              </span>
              <!-- Date formatting -->
              <span 
                v-else-if="column.type === 'date'"
                class="text-[#D1D5DB]"
              >
                {{ formatDate(row[column.key]) }}
              </span>
              <!-- Action buttons -->
              <div 
                v-else-if="column.key === 'actions'"
                class="flex items-center space-x-2"
              >
                <button
                  @click="$emit('view', row)"
                  class="p-1 text-[#9CA3AF] hover:text-[#06B6D4] transition-colors"
                  title="View"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                  </svg>
                </button>
                <button
                  v-if="row.status === 'failed'"
                  @click="$emit('retry', row)"
                  class="p-1 text-[#9CA3AF] hover:text-[#F59E0B] transition-colors"
                  title="Retry"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
              <!-- Default text -->
              <span 
                v-else
                class="text-[#D1D5DB]"
              >
                {{ row[column.key] }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Empty State -->
      <div v-if="filteredData.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-[#6B7280]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-4 text-sm font-medium text-[#9CA3AF]">No data found</h3>
        <p class="mt-2 text-sm text-[#6B7280]">{{ emptyMessage || 'Try adjusting your search or filter criteria.' }}</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="filteredData.length > itemsPerPage" class="px-6 py-4 bg-[#121212] border-t border-[#2D2D2D]">
      <div class="flex items-center justify-between">
        <div class="text-sm text-[#9CA3AF]">
          Showing {{ ((currentPage - 1) * itemsPerPage) + 1 }} to {{ Math.min(currentPage * itemsPerPage, filteredData.length) }} of {{ filteredData.length }} results
        </div>
        <div class="flex items-center space-x-2">
          <button
            @click="currentPage--"
            :disabled="currentPage === 1"
            class="px-3 py-1 text-sm border border-[#2D2D2D] rounded text-[#D1D5DB] hover:bg-[#2D2D2D] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Previous
          </button>
          <span class="px-3 py-1 text-sm text-[#F9FAFB]">{{ currentPage }} of {{ totalPages }}</span>
          <button
            @click="currentPage++"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 text-sm border border-[#2D2D2D] rounded text-[#D1D5DB] hover:bg-[#2D2D2D] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Column {
  key: string
  label: string
  sortable?: boolean
  type?: 'text' | 'date' | 'status' | 'actions'
  class?: string
}

interface Props {
  title: string
  columns: Column[]
  data: any[]
  itemsPerPage?: number
  emptyMessage?: string
}

const props = withDefaults(defineProps<Props>(), {
  itemsPerPage: 10,
  emptyMessage: ''
})

const emit = defineEmits<{
  view: [row: any]
  retry: [row: any]
}>()

const searchQuery = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const sortColumn = ref('')
const sortDirection = ref<'asc' | 'desc'>('asc')

const filteredData = computed(() => {
  let filtered = props.data

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(row =>
      Object.values(row).some(value =>
        String(value).toLowerCase().includes(query)
      )
    )
  }

  // Apply status filter
  if (statusFilter.value) {
    filtered = filtered.filter(row => row.status === statusFilter.value)
  }

  // Apply sorting
  if (sortColumn.value) {
    filtered = [...filtered].sort((a, b) => {
      const aVal = a[sortColumn.value]
      const bVal = b[sortColumn.value]
      
      if (aVal < bVal) return sortDirection.value === 'asc' ? -1 : 1
      if (aVal > bVal) return sortDirection.value === 'asc' ? 1 : -1
      return 0
    })
  }

  return filtered
})

const totalPages = computed(() => Math.ceil(filteredData.value.length / props.itemsPerPage))

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return filteredData.value.slice(start, end)
})

const toggleSort = (column: string) => {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortColumn.value = column
    sortDirection.value = 'asc'
  }
}

const getStatusClass = (status: string) => {
  const classes = {
    pending: 'bg-[#F59E0B] bg-opacity-10 text-[#F59E0B] border border-[#F59E0B] border-opacity-20',
    completed: 'bg-[#22C55E] bg-opacity-10 text-[#22C55E] border border-[#22C55E] border-opacity-20',
    failed: 'bg-[#EF4444] bg-opacity-10 text-[#EF4444] border border-[#EF4444] border-opacity-20',
  }
  return classes[status as keyof typeof classes] || 'bg-[#6B7280] bg-opacity-10 text-[#6B7280] border border-[#6B7280] border-opacity-20'
}

const getStatusDotClass = (status: string) => {
  const classes = {
    pending: 'bg-[#F59E0B]',
    completed: 'bg-[#22C55E]',
    failed: 'bg-[#EF4444]',
  }
  return classes[status as keyof typeof classes] || 'bg-[#6B7280]'
}

const formatStatus = (status: string) => {
  return status.charAt(0).toUpperCase() + status.slice(1)
}

const formatDate = (date: string | Date) => {
  if (!date) return '-'
  const d = new Date(date)
  return d.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>