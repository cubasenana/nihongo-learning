<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import FontModeToggle from './components/FontModeToggle.vue'
</script>

<template>
  <DefaultTheme.Layout>
    <template #layout-bottom>
      <FontModeToggle />
    </template>
  </DefaultTheme.Layout>
</template>
