<script setup lang="ts">

import axios from 'axios';

const API_URL = "http://localhost:8000/data/hrv-bulk";

async function getData() {
  const res = await axios.get(API_URL, { params: { session_id: localStorage.getItem("sessionId") } });
  console.log(res)
}

</script>

<template>
  <div>
    <button @click="getData">
      Get data
    </button>
  </div>
</template>
