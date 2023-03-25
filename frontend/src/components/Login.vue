<script setup lang="ts">

import axios from 'axios';

const API_URL = "http://localhost:8000/login";

async function login() {
  const redirect = await axios.get(API_URL, { withCredentials: true });
  const url = redirect.data.url
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
