<template>
  <div id="App">
    <NavigationBar/>
    <router-view />
    <NotificationList />
  </div>
</template>

<script>

import NavigationBar from "@/components/NavBar.vue";
import NotificationList from "@/components/NotificationList.vue";

export default {
  name: 'App',
  components: {NotificationList, NavigationBar},
}
</script>

<style>

</style>
