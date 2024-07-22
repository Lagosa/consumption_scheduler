<template>
  <nav class="fixed inset-x-0 top-0 bg-main-color p-4 z-40 drop-shadow-lg">
    <div class="container mx-auto">
      <div class="flex justify-between items-center">
        <router-link to="/">
          <div class="text-white text-2xl font-semibold text-text">Energy Management System</div>
        </router-link>
      </div>
    </div>
  </nav>
</template>
<script>

export default {
  name: 'NavigationBar',
}
</script>
<style>

</style>