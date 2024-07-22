<template>
  <div v-if="this.include_title" class="text-lg font-semibold text-center">
    {{ title + ":" }}
  </div>
  <table class="m-auto table-fixed border-collapse text-xs h-full">
    <thead>
    <tr>
      <th v-for="(headerE, index) in header" :key="index" class="border-2 border-slate-300 p-1">{{ headerE }}</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="(row, rowIndex) in data" :key="rowIndex">
      <td v-for="(cell, cellIndex) in row" :key="cellIndex" class="border-2 border-slate-300  p-1">{{ cell }}</td>
    </tr>
    </tbody>
  </table>
  <hr class="border-t-2 w-full  border-gray-300 my-10">
</template>
<script>
export default {
  name: "TableComponent",
  props: {
    data: Array,
    header: Array,
    title: String,
    include_title: Boolean
  }
}
</script>