<script lang="ts">

interface LoginProps {
  sessionId: string;
  login: () => void;
  logout: () => void;
}

export default defineComponent<LoginProps>({
  data() {
    return {
      sessionId: localStorage.getItem("sessionId")
    }
  }
})

</script>

<script setup lang="ts">

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
