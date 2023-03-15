<script setup lang="ts">
import { ref, watchEffect } from 'vue'

const API_URL = "http://localhost:8000/login"
const data = ref(null)

watchEffect(async () => {
  // this effect will run immediately and then
  // re-run whenever currentBranch.value changes
  data.value = await (await fetch(API_URL)).json()
  console.log(data.value)
})

</script>

<template>
  <div>
    {{ data }}
  </div>
</template>

<style scoped>

</style>
