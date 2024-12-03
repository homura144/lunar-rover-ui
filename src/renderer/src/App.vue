<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

Chart.defaults.font.size = 18

// Drawing charts
const chartRef = ref<HTMLCanvasElement | null>(null)
const heightChartRef = ref<HTMLCanvasElement | null>(null)

onMounted(() => {
  if (chartRef.value) {
    new Chart(chartRef.value, {
      type: 'line',
      data: {
        labels: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
        datasets: [
          {
            label: '六轮车',
            data: [0, 1, 2, 3, 4, 5, 4, 3, 2, 4, 5, 3, 2, 1, 0, 0],
            borderColor: '#5c458d',
            backgroundColor: '#5c458d',
            pointStyle: 'circle',
            tension: 0.4
          },
          {
            label: '四轮车',
            data: [0, 2, 5, 8, 10, 12, 10, 8, 6, 8, 9, 7, 6, 4, 1, 0],
            borderColor: '#e6b422',
            backgroundColor: '#e6b422',
            pointStyle: 'circle',
            tension: 0.4
          }
        ]
      },
      options: {
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: '行驶距离/m'
            }
          },
          y: {
            title: {
              display: true,
              text: '摇晃程度'
            }
          }
        }
      }
    })
  }

  if (heightChartRef.value) {
    new Chart(heightChartRef.value, {
      type: 'line',
      data: {
        labels: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
        datasets: [
          {
            label: '六轮车',
            data: [0, 1, 1.5, 2, 2.5, 3, 2.8, 2.5, 2, 1.8, 1.5, 1.2, 1, 0.8, 0.5, 0],
            borderColor: '#5c458d',
            backgroundColor: '#5c458d',
            pointStyle: 'circle',
            tension: 0.4
          },
          {
            label: '四轮车',
            data: [0, 2, 2.5, 3, 3.5, 4, 3.8, 3.5, 3, 2.8, 2.5, 2.2, 2, 1.8, 1.5, 1],
            borderColor: '#e6b422',
            backgroundColor: '#e6b422',
            pointStyle: 'circle',
            tension: 0.4
          }
        ]
      },
      options: {
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: '行驶距离/m'
            }
          },
          y: {
            title: {
              display: true,
              text: '高度/m'
            }
          }
        }
      }
    })
  }
})
</script>

<template>
  <div class="container">
    <!-- charts -->
    <div class="charts">
      <div>
        <canvas ref="chartRef"></canvas>
      </div>
      <div>
        <canvas ref="heightChartRef"></canvas>
      </div>
    </div>

    <!-- terrain -->
    <div class="terrain">
      <!-- Adjustable width ratio using "flex" -->
      <div class="terrain-area flat" style="flex: 2">平坦区域</div>
      <div class="terrain-area bump" style="flex: 4">起伏区域</div>
      <div class="terrain-area flat" style="flex: 1">平坦区域</div>
    </div>
  </div>
</template>
