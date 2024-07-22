<template>
  <div class="h-full w-full text-center float" >
    <p class="text-main-color text-2xl font-semibold "> {{ title }}</p>
  </div>
</template>
<script>
export default {
  name:"HeaderTitle",
  props: {
    title: String
  }
}
</script>