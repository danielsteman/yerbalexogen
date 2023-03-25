<script setup lang="ts">

import { onMounted } from "vue";
import { useRoute } from 'vue-router';
import axios from 'axios';
import { store } from '../store'

export default {
  data() {
    return {
      store
    }
  }
}

const route = useRoute()

onMounted(() => {
  const code = route.query.code
  const url = "http://localhost:8000/callback";
  axios.get(url, {
    params: {
      code: code
    }
  }).then(data => console.log(data));
})


</script>

<template>
  <div>
    hoi
  </div>
</template>
