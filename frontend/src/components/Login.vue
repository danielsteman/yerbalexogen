<script setup lang="ts">
import { ref, watchEffect } from 'vue'
import { RouterLink } from 'vue-router'

const API_URL = "http://localhost:8000/login"
const redirect_url = ref("")

watchEffect(async () => {
  // this effect will run immediately and then
  // re-run whenever currentBranch.value changes
  redirect_url.value = await (await fetch(API_URL)).json()
})

function login() {
  console.log("hoi")
}

</script>

<template>
  <router-link to="/">Go to Home</router-link>
  <button @click="login">
    Login
  </button>
</template>

