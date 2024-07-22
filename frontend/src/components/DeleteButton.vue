<template>
  <ActionButton :source="this.deleteButtonSrc" :use-image="true" :bgColor="'bg-gray-100'" :width="'w-6'" :height="'w-6'" :hoverColor="'hover:bg-gray-300'"
  @onClicked="clicked"/>
</template>
<script>
  import ActionButton from "@/components/ActionButton.vue";

  export default {
    name: "DeleteButton",
    data() {
      return {
        deleteButtonSrc: require('@/assets/delete.png')
      }
    },
    components: {
      ActionButton
    },
    props: {
      rowId: Number
    },
    methods: {
      clicked() {
        this.$emit('deleteActioned', this.rowId);
      }
    }
  }
</script>