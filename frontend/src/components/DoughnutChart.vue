<template>
  <div :class="this.stylingClass"  class="h-1/3 ">
    <canvas ref="doughnutChart"></canvas>
  </div>
</template>
<script>

import Chart from "chart.js/auto";
import ChartDataLabels from "chartjs-plugin-datalabels";


 export default {
   name: "DoughnutChart",
   components: {
   },
   props : {
     stylingClass:String,
     datasets: Array,
     labels: Array
   },
   data() {
     return {
       colors: [
         "#EFB064",
         "#F3E9CC",
         "#A0A1B9",
         "#415688",
       ]
     };
   },
   mounted() {
     this.renderChart();
   },
   methods: {
     renderChart() {
       const ctx = this.$refs.doughnutChart.getContext('2d');
       const datasets = this.buildDatasets(this.datasets)


       new Chart(ctx, {
         type: 'doughnut',
         data: {
           labels: this.labels,
           datasets: datasets,
         },
         plugins: [ChartDataLabels],
         options: {
           maintainAspectRatio: false,
           plugins: {
             datalabels: {
               formatter: (value) =>{
                  return `${value}%`
               },
               color: "#000000",
               font: {
                 size: 15
               }
             }
           }
         }
       });
     },
     buildDatasets(datasets) {
       var result = []

       for (let i = 0; i < datasets.length; i++) {
         result.push({
           label: datasets[i].seriesName,
           data: datasets[i].seriesValues,
           backgroundColor: this.colors,
           hoverOffset: 4,
           clip: 5
         })
       }

       return result
     }
   }
 }
</script>