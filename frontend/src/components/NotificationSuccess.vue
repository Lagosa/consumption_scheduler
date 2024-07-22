<template>
  <NotificationSkeleton :source="this.srcImg" :icon-background-color="'bg-green-400'" :text="this.text" :id="this.id" :alt-text="this.altText"/>
</template>
<script>
import NotificationSkeleton from "@/components/NotificationSkeleton.vue";

export default {
  name:"NotificationSuccess",
  components: {NotificationSkeleton},
  data() {
    return {
      srcImg: require('@/assets/check-circle.png')
    }
  },
  props: {
    text: String,
    altText: String,
    id: String
  }
}
</script>