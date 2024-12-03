<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

Chart.defaults.font.size = 18

const shakeChartRef = ref<HTMLCanvasElement | null>(null)
const heightChartRef = ref<HTMLCanvasElement | null>(null)

const distance = ref(0)

let shakeChart: Chart | null = null
let heightChart: Chart | null = null

// Initial shake chart
let shakeData = {
  datasets: [
    {
      label: '六轮车',
      borderColor: '#5c458d',
      backgroundColor: '#5c458d',
      pointStyle: 'circle',
      tension: 0.4
    },
    {
      label: '四轮车',
      borderColor: '#e6b422',
      backgroundColor: '#e6b422',
      pointStyle: 'circle',
      tension: 0.4
    }
  ]
}

// Initial height chart
let heightData = {
  datasets: [
    {
      label: '六轮车',
      borderColor: '#5c458d',
      backgroundColor: '#5c458d',
      pointStyle: 'circle',
      tension: 0.4
    },
    {
      label: '四轮车',
      borderColor: '#e6b422',
      backgroundColor: '#e6b422',
      pointStyle: 'circle',
      tension: 0.4
    }
  ]
}

onMounted(() => {
  if (shakeChartRef.value) {
    shakeChart = new Chart(shakeChartRef.value, {
      type: 'line',
      data: shakeData,
      options: {
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: '行驶距离/m'
            },
            type: 'linear',
            min: 0,
            max: 1.5,
            ticks: {
              stepSize: 0.3,
            }
          },
          y: {
            title: {
              display: true,
              text: '摇晃程度'
            },
            min: 0,
            max: 15,
            ticks: {
              stepSize: 3,
            }
          }
        }
      }
    })
  }

  if (heightChartRef.value) {
    heightChart = new Chart(heightChartRef.value, {
      type: 'line',
      data: heightData,
      options: {
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: '行驶距离/m'
            },
            type: 'linear',
            min: 0,
            max: 1.5,
            ticks: {
              stepSize: 0.3,
            }
          },
          y: {
            position: 'right',
            title: {
              display: true,
              text: '高度/m'
            },
            min: 0,
            max: 0.5,
            ticks: {
              stepSize: 0.1,
            }
          }
        }
      }
    })
  }


  // update the distance periodically
  setInterval(() => {
    // TODO: get distance from the motor
    distance.value += 0.1
  }, 1000)

  // update the shakeChart 
  setInterval(() => {
    // add label
    const newLabel: Number = distance.value.toFixed(2);

    // add shake data periodically
    // TODO: get shake data from the IMU
    shakeData.labels.push(Number(newLabel));
    shakeData.datasets[0].data.push(Math.random() * 15);
    shakeData.datasets[1].data.push(Math.random() * 15);

    // Update the charts
    if (shakeChart) shakeChart.update();
  }, 1000);

  // update the heightChart 
  setInterval(() => {
    // add label
    const newLabel: Number = distance.value.toFixed(2);

    // add height data periodically
    // TODO: get height data from the grating scale
    heightData.labels.push(Number(newLabel));
    heightData.datasets[0].data.push(Math.random() * 0.5);
    heightData.datasets[1].data.push(Math.random() * 0.5);

    // Update the charts
    if (heightChart) heightChart.update();
  }, 1000);
})

</script>

<template>
  <div class="container">
    <!-- charts -->
    <div class="charts">
      <div>
        <canvas ref="shakeChartRef"></canvas>
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
