<script lang="ts">
import { defineComponent } from "vue";
import Login from "./Login.vue";

interface Session {
  sessionId: String
}


export default defineComponent<Session>({
  data() {
    return {
      sessionId: localStorage.getItem("sessionId")
    }
  }
})

</script>

<template>
  <Login v-if="!sessionId" />
  <div v-if="sessionId">

  </div>
</template>

<style scoped></style>
