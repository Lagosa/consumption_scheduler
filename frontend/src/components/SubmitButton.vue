<template>
  <ActionButton :use-image="false" :bg-color="'bg-highlight'" @onClicked="clicked"  :text="'Submit'" :hoverColor="'hover:bg-highlight-light'"/>
</template>
<script>
import ActionButton from "@/components/ActionButton.vue";

export default {
  name: "SubmitButton",
  components: {ActionButton},
  methods: {
    clicked() {
      this.$emit("clicked");
    }
  }
}
</script>