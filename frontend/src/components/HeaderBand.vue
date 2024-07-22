<template>
  <div class="flex flex-grow rounded-t-lg bg-gray-300 p-2 items-center justify-center drop-shadow-md  m-auto">
    <HeaderTitle v-for="(title, index) in titles" v-bind:key="index" :title="title" />
  </div>
</template>
<script>
import HeaderTitle from "@/components/HeaderTitle.vue";

export default {
  name: "HeaderBand",
  components: {HeaderTitle},
  props: {
    titles: Array
  }
}
</script>