import { reactive } from 'vue'

export const store = reactive({
  currentSession: "",
  setSession(sessionId: string) {
    this.currentSession = sessionId
  }
})