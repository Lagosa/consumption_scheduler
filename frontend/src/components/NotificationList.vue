<template>
  <div class="absolute bottom-0 right-0 flex flex-col mr-6 justify-end mt-20 z-30 drop-shadow-lg">
    <div class="float-right  mb-0">
      <MainNotification v-for="notification in notifications" :key="notification.id" :notification="notification"/>
    </div>
  </div>
</template>
<script>
import MainNotification from "@/components/MainNotification.vue";
import {mapState} from 'vuex'

export default {
  name: 'NotificationList',
  components: {MainNotification},
  computed: mapState(['notifications'])
}
</script>