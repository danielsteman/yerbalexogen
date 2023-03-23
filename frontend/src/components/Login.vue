<script setup lang="ts">

import axios from 'axios';

const API_URL = "http://localhost:8000/login";
const SESSION_URL = "http://localhost:8000/session";

async function login() {
  const redirect = await axios.get(API_URL, { withCredentials: true });
  const url = redirect.data.url
  window.location.href = url
}

async function session() {
  const res = await axios.get(SESSION_URL, { withCredentials: true });
  console.log(document.cookie)
}

</script>

<template>
  <div>
    <button @click="login">
      Login
    </button>
    <button @click="session">
      Check session
    </button>
  </div>
</template>
