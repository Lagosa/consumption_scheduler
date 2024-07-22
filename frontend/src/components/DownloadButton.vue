<template>
  <div class="m-auto w-fit">
    <ActionButton :use-image="false" :bg-color="'bg-highlight'" @onClicked="clicked"  :text="'Download'" :hoverColor="'hover:bg-primary-highlight'"/>
  </div>
</template>
<script>
import ActionButton from "@/components/ActionButton.vue";

export default {
  name: "DownloadButton",
  components: {ActionButton},
  methods: {
    clicked() {
      this.$emit("clicked");
    }
  }
}
</script>