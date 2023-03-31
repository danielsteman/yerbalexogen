<script setup lang="ts">

import { onMounted } from "vue";
import { useRoute } from 'vue-router';
import axios from 'axios';
import router from "../router";

const route = useRoute()

onMounted(() => {
  const code = route.query.code
  const url = "http://localhost:8000/callback";
  axios.get(url, {
    params: {
      code: code
    }
  }).then(data => localStorage.setItem('sessionId', data.data.session_id)).then(() => router.push("/"));
})


</script>

<template>
  <div>
    Welcome! You'll be redirected to the home page.
  </div>
</template>
