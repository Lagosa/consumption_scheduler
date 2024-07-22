<template>
  <div :class="this.stylingClass">
    <canvas ref="lineChart" class="w-3/4"></canvas>
  </div>
</template>
<script>

import Chart from "chart.js/auto"

 export default {
   name: "LineChart",
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
           "#EFB064",
           "#415688",
           "#eba694",
           "#69cec7",
       ]
     };
   },
   mounted() {
     this.renderChart();
   },
   methods: {
     renderChart() {
       const ctx = this.$refs.lineChart.getContext('2d');
       const datasets = this.buildDatasets(this.datasets)


       new Chart(ctx, {
         type: 'line',
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
           borderWidth: 2,
           fill: false,
         })
       }

       return result
     }
   }
 }
</script>