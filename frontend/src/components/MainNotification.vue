<template>
  <NotificationSuccess v-if="notification.type === 'SUCCESS'" :text="notification.text" :id="notification.id"/>
  <NotificationWarning v-if="notification.type === 'WARNING'" :text="notification.text" :id="notification.id"/>
  <NotificationError v-if="notification.type === 'ERROR'" :text="notification.text" :id="notification.id"/>
</template>
<script>
import NotificationSuccess from "@/components/NotificationSuccess.vue";
import NotificationWarning from "@/components/NotificationWarning.vue";
import NotificationError from "@/components/NotificationError.vue";

export default {
  name: "MainNotification",
  components: {NotificationError, NotificationWarning, NotificationSuccess},
  props: {
    notification: Object
  }
}
</script>