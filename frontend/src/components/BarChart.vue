<template>
  <div :class="this.stylingClass">
    <canvas ref="barChart" class="w-3/4"></canvas>
  </div>
</template>
<script>

import Chart from "chart.js/auto"

 export default {
   name: "BarChart",
   components: {
   },
   props : {
     stylingClass:String,
     datasets: Array,
     labels: Array,
     yAxisTitle: String,
     xAxisTitle: String
   },
   data() {
     return {
       colors: [
         "#415688",
         "#EFB064",
         "#F3E9CC",
         "#A0A1B9",
       ]
     };
   },
   mounted() {
     this.renderChart();
   },
   methods: {
     renderChart() {
       const ctx = this.$refs.barChart.getContext('2d');
       const datasets = this.buildDatasets(this.datasets)


       new Chart(ctx, {
         type: 'bar',
         data: {
           labels: this.labels,
           datasets: datasets,
         },
         options: {
           maintainAspectRatio: false,
           scales: {
             y: {
               beginAtZero: false,
               title: {
                 display: true,
                 text: this.yAxisTitle
               }
             },
             x: {
               title: {
                 display: true,
                 text: this.xAxisTitle
               }
             }
           },
         },
       });
     },
     buildDatasets(datasets) {
       var result = []

       for (let i = 0; i < datasets.length; i++) {
         result.push({
           label: datasets[i].seriesName,
           data: datasets[i].seriesValues,
           borderColor: this.colors[i],
           backgroundColor: this.colors[i],
         })
       }

       return result
     }
   }
 }
</script>