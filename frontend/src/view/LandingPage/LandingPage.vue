
<script src="./LandingPage.js"> </script>

<template>
  <div class="relative w-full h-screen">
      <div class="absolute inset-0">
        <img class="object-cover w-full h-full"
             src="../../assets/main_bg.jpg"
        />
      </div>
    <div class="absolute inset-0 bg-black opacity-40"></div>
    <div class="absolute inset-0 flex items-center justify-center text-highlight-light text-4xl font-bold">
      <div class="">
        <p class="text-highlight"> Achieve <span class="text-white"> true </span> power efficiency. </p>
        <div class="flex flex-grow justify-center items-center text-2xl my-4">
          <router-link to="/upload" class="text-highlight-light">
            <button class="bg-white hover:bg-highlight-light text-main-color py-2 px-4 rounded font-semibold drop-shadow-md">
              Get started
            </button>
          </router-link>
        </div>
       </div>
    </div>
  </div>
</template>


