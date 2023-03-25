<script setup lang="ts">

import { onMounted } from "vue";
import { useRoute } from 'vue-router';
import axios from 'axios';
import { store } from '../store'
import router from "../router";

const route = useRoute()

onMounted(() => {
  const code = route.query.code
  const url = "http://localhost:8000/callback";
  axios.get(url, {
    params: {
      code: code
    }
  }).then(data => store.setSession(data.data.session_id)).then(() => router.push("/"));
})


</script>

<template>
  <div>
    hoi
  </div>
</template>
