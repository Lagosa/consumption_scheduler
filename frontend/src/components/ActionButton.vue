<template>
  <button @click="clicked" class="rounded-lg flex justify-center pt-1 mx-1 shadow-md" :class="[bgColor, width, height, hoverColor]">
    <img v-if="useImage" :src="source" alt="edit" class="w-3/4 h-3/4">
    <div v-else class="text-white font-semibold text-centerv text-lg px-5 pb-1">
      {{text}}
    </div>
  </button>
</template>
<script>
export default {
  name: "ActionButton",
  data() {
    return {
    }
  },
  props: {
    source: String,
    bgColor: String,
    useImage: Boolean,
    text:String,
    width: String,
    height: String,
    hoverColor: String
  },
  computed: {
  },
  methods: {
    clicked() {
      this.$emit("onClicked");
    }
  }
}
</script>