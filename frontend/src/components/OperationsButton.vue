<template>
  <ActionButton :use-image="false" :bg-color="'bg-amber-400'" @onClicked="clicked" :text="'Submit operation'"
                :hoverColor="'hover:bg-highlight-light'"/>
</template>
<script>
import ActionButton from "@/components/ActionButton.vue";

export default {
  name: "OperationsButton",
  components: {ActionButton},
  methods: {
    clicked() {
      this.$emit("clicked");
    }
  }
}
</script>