<script setup lang="ts">

import { onMounted } from "vue";
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute()

onMounted(() => {
  const code = route.query.code
  const url = "http://localhost:8000/callback";
  axios.get(url, {
    params: {
      code: code
    }
  });
})

</script>

<template>
  <div>
    hoi
  </div>
</template>
