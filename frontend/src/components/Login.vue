<script lang="ts">

import axios from 'axios';
import { defineComponent } from 'vue';

const API_URL = "http://localhost:8000/login";

async function login() {
  const redirect = await axios.get(API_URL, { withCredentials: true });
  const url = redirect.data.url
  window.location.href = url
}

function logout() {
  localStorage.removeItem("sessionId")
}

interface Login {
  sessionId: string
  login: any
  logout: any
}

export default defineComponent<Login>({
  data() {
    return {
      sessionId: localStorage.getItem("sessionId")
    }
  }
})

</script>

<template>
  <div>
    <button @click="login" v-if="!sessionId">
      Login
    </button>
    <button @click="logout" v-if="sessionId">
      Logout
    </button>
  </div>
</template>
