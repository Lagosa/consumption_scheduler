<template>
    <div class="flex items-center max-w-xs p-4 mb-4 text-gray-500 bg-white rounded-lg shadow">
      <div
          class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 rounded-lg"
          :class="[iconBackgroundColor]">
        <img :src="source" :alt="altText" class="w-3/4 h-3/4">
      </div>
      <div class="ms-3 w-2/3 text-m font-normal" style="word-break: break-word;">{{ text }}</div>
      <button type="button"
              class="ml-5 ms-auto -mx-1.5 -my-1.5 bg-white text-gray-400 hover:text-gray-900 rounded-lg p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8"
              @click="removeNotification(this.id)">
        X
      </button>
    </div>
</template>
<script>

import {mapActions} from "vuex";

export default {
  name: 'Notification-window',
  data() {
    return {
      timeout: null,
    }
  },
  props: {
    id: String,
    text: String,
    source: String,
    altText: String,
    iconBackgroundColor: String
  },
  created() {
    this.timeout = setTimeout(() => {
      this.removeNotification(this.id)
    }, 6000)
  },
  beforeUnmount() {
    clearTimeout(this.timeout)
  },
  methods: mapActions(["removeNotification"])
}
</script>