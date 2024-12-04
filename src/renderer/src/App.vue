<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

Chart.defaults.font.size = 18

const shakeChartRef = ref<HTMLCanvasElement | null>(null)
const heightChartRef = ref<HTMLCanvasElement | null>(null)

const distance = ref(0)
const roverPosition = ref(0)
const distance_max = 1.5
const shake_max = 15
const height_max = 0.5

let shakeChart: Chart | null = null
let heightChart: Chart | null = null

// Initial shake chart
let shakeData = {
  datasets: [
    {
      label: '六轮车',
      borderColor: '#5c458d',
      backgroundColor: '#5c458d',
      tension: 0.4,
      pointRadius: 0
    },
    {
      label: '四轮车',
      borderColor: '#e6b422',
      backgroundColor: '#e6b422',
      tension: 0.4,
      pointRadius: 0
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
      tension: 0.4,
      pointRadius: 0
    },
    {
      label: '四轮车',
      borderColor: '#e6b422',
      backgroundColor: '#e6b422',
      tension: 0.4,
      pointRadius: 0
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
            max: distance_max,
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
            max: shake_max,
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
            max: distance_max,
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
            max: height_max,
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
    distance.value += 0.01;
  }, 100);

  // update the shakeChart 
  setInterval(() => {
    // add label
    const newLabel: Number = distance.value.toFixed(2);

    // add shake data periodically
    // TODO: get shake data from the IMU
    shakeData.labels.push(Number(newLabel));
    shakeData.datasets[0].data.push(Math.random() * shake_max / 3);
    shakeData.datasets[1].data.push(Math.random() * shake_max);

    // Update the charts
    if (shakeChart) shakeChart.update();
  }, 100);

  // update the heightChart 
  setInterval(() => {
    // add label
    const newLabel: Number = distance.value.toFixed(2);

    // add height data periodically
    // TODO: get height data from the grating scale
    heightData.labels.push(Number(newLabel));
    heightData.datasets[0].data.push(Math.random() * height_max / 3);
    heightData.datasets[1].data.push(Math.random() * height_max);

    // Update the charts
    if (heightChart) heightChart.update();
  }, 100);

  // update the rover position periodically
  setInterval(() => {
    roverPosition.value = distance.value / distance_max * 100;
  }, 100);
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
      <!-- Rover image -->
      <img class="rover" src="@renderer/assets/rover.png" alt="Rover" :style="{ left: roverPosition + '%' }" />

      <!-- Adjustable width ratio using "flex" -->
      <div class="terrain-label">
        <div class="terrain-area flat" style="flex: 2">平坦区域</div>
        <div class="terrain-area bump" style="flex: 4">起伏区域</div>
        <div class="terrain-area flat" style="flex: 1">平坦区域</div>
      </div>
    </div>
  </div>
</template>
