<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';

const API_URL = "http://localhost:8000/data/hrv-bulk";

async function getData() {
  const params = {
    session_id: localStorage.getItem("sessionId"),
    start_date: "2022-01-01",
    end_date: "2022-01-10",
  };
  const res = await axios.get(API_URL, { params: params });
  console.log(res)
}

</script>

<script lang="ts">

const startDate = ref("yyyy-mm-dd");
const endDate = ref("yyyy-mm-dd");

</script>

<template>
  <div>
    <form @click="getData">
      <input v-model="startDate" />
      <input v-model="endDate" />
      <button type="submit" value="Get data">Get data</button>
    </form>
  </div>
</template>
