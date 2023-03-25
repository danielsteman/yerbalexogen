<script lang="ts">
import { defineComponent } from "vue";
import Login from "./Login.vue";
import Data from "./Data.vue"

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
  <Data v-if="sessionId" />
</template>

<style scoped></style>
