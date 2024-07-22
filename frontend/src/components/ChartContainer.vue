<template>
  <div>
    <div class="text-lg font-semibold text-center">
      {{ chart.title + ":" }}
    </div>
    <div v-if="chart.type === 'LINE'">
      <LineChart :labels="chart.labels" :y-axis-title="chart.yAxisTitle" :x-axis-title="chart.xAxisTitle" :datasets="chart.datasets" :styling-class="''"/>
    </div>
    <div v-if="chart.type === 'BAR'">
      <BarChart :labels="chart.labels" :y-axis-title="chart.yAxisTitle" :x-axis-title="chart.xAxisTitle" :datasets="chart.datasets" :styling-class="''"/>
    </div>
    <div v-if="chart.type === 'PIE'">
      <DoughnutChart :labels="chart.labels" :datasets="chart.datasets" :styling-class="''"/>
    </div>
  </div>
  <hr class="border-t-2 w-full  border-gray-300 my-10">
</template>

<script>
import LineChart from "@/components/LineChart.vue";
import BarChart from "@/components/BarChart.vue";
import DoughnutChart from "@/components/DoughnutChart.vue";


export default {
  name: "ChartContainer",
  components: {DoughnutChart, BarChart, LineChart},
  props: {
    chart: Object,
  }
}
</script>