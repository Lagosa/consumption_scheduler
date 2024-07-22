<template>
  <ActionButton :use-image="false" :bg-color="'bg-highlight'" @onClicked="clicked"  :text="'Upload'" :hoverColor="'hover:bg-primary-highlight'"/>
</template>
<script>
import ActionButton from "@/components/ActionButton.vue";

export default {
  name: "UploadButton",
  components: {ActionButton},
  methods: {
    clicked() {
      this.$emit("clicked");
    }
  }
}
</script>