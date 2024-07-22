<template>
  <NotificationSkeleton :source="this.srcImg" :icon-background-color="'bg-amber-400'" :text="this.text" :id="this.id" :alt-text="this.altText"/>
</template>
<script>
import NotificationSkeleton from "@/components/NotificationSkeleton.vue";

export default {
  name:"NotificationWarning",
  components: {NotificationSkeleton},
  data() {
    return {
      srcImg: require('@/assets/triangle-warning.png')
    }
  },
  props: {
    text: String,
    altText: String,
    id: String
  }
}
</script>