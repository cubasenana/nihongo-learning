<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

type FontMode = 'browser' | 'anthropic-serif'

const STORAGE_KEY = 'nihongo-learning-font-mode'
const MODES: Array<{ id: FontMode; label: string }> = [
  { id: 'browser', label: '浏览器默认' },
  { id: 'anthropic-serif', label: 'Anthropic 衬线' }
]

const currentMode = ref<FontMode>('browser')
const mounted = ref(false)

function saveMode(mode: FontMode): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, mode)
  } catch {
    // Ignore storage failures and keep the current UI state.
  }
}

function applyMode(mode: FontMode): void {
  currentMode.value = mode
  document.documentElement.dataset.fontMode = mode
}

onMounted(() => {
  mounted.value = true

  try {
    const saved = window.localStorage.getItem(STORAGE_KEY)
    if (saved === 'browser' || saved === 'anthropic-serif') {
      currentMode.value = saved
    }
  } catch {
    // Ignore storage failures and fall back to the default mode.
  }

  document.documentElement.dataset.fontMode = currentMode.value
})

watch(currentMode, (mode) => {
  if (!mounted.value) {
    return
  }
  document.documentElement.dataset.fontMode = mode
  saveMode(mode)
})
</script>

<template>
  <div class="font-mode-toggle" role="group" aria-label="字体模式">
    <button
      v-for="mode in MODES"
      :key="mode.id"
      class="font-mode-button"
      :class="{ 'is-active': currentMode === mode.id }"
      :aria-pressed="String(currentMode === mode.id)"
      type="button"
      @click="applyMode(mode.id)"
    >
      {{ mode.label }}
    </button>
  </div>
</template>
