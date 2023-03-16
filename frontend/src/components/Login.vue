<script setup lang="ts">

const API_URL = "http://localhost:8000/login";

async function login() {
  const redirect = await (await fetch(API_URL)).json();
  const url = redirect.url
  window.location.href = url
}

</script>

<template>
  <div>
    <button @click="login">
      Login
    </button>
  </div>
</template>
