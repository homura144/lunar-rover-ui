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

const ID_SIX_WHEELER = 0
const ID_FOUR_WHEELER = 1

const MOTOR_SOCKET_PORT = 8766
const IMU_SOCKET_PORT_SIX = 8767
const IMU_SOCKET_PORT_FOUR = 8768

// Initial shake chart
let shakeData = {
  labels: [] as number[],
  datasets: [
    {
      label: '六轮车',
      borderColor: '#5c458d',
      backgroundColor: '#5c458d',
      tension: 0.4,
      pointRadius: 0,
      data: [] as number[]
    },
    {
      label: '四轮车',
      borderColor: '#e6b422',
      backgroundColor: '#e6b422',
      tension: 0.4,
      pointRadius: 0,
      data: [] as number[]
    }
  ]
}

let heightData = {
  labels: [] as number[],
  datasets: [
    {
      label: '六轮车',
      borderColor: '#5c458d',
      backgroundColor: '#5c458d',
      tension: 0.4,
      pointRadius: 0,
      data: [] as number[]
    },
    {
      label: '四轮车',
      borderColor: '#e6b422',
      backgroundColor: '#e6b422',
      tension: 0.4,
      pointRadius: 0,
      data: [] as number[]
    }
  ]
}

const isRunning = ref(false)
const latestIMUData = ref({
  [ID_SIX_WHEELER]: { shake: 0, height: 0 },
  [ID_FOUR_WHEELER]: { shake: 0, height: 0 }
})

const motorSocket = new WebSocket(`ws://localhost:${MOTOR_SOCKET_PORT}`)
const imuSixSocket = new WebSocket(`ws://localhost:${IMU_SOCKET_PORT_SIX}`)
const imuFourSocket = new WebSocket(`ws://localhost:${IMU_SOCKET_PORT_FOUR}`)

motorSocket.onmessage = (event) => {
  const data = JSON.parse(event.data)
  if (data.type === 'distance') {
    distance.value = data.value
    updateCharts()
    console.log(`Motor distance: ${data.value} m`)
  }
}

const handleIMUMessage = (event: MessageEvent) => {
  const data = JSON.parse(event.data)
  if (data.type === 'imu') {
    latestIMUData.value[data.vehicle_type] = {
      shake: data.shake,
      height: data.height
    }
    console.log(`IMU data: ${data.vehicle_type}, shake: ${data.shake}, height: ${data.height}`)
  }
}

imuSixSocket.onmessage = handleIMUMessage
imuFourSocket.onmessage = handleIMUMessage

const updateCharts = () => {
  const newLabel: number = Number(distance.value.toFixed(2))
  shakeData.labels.push(newLabel)
  heightData.labels.push(newLabel)

  shakeData.datasets[ID_SIX_WHEELER].data.push(latestIMUData.value[ID_SIX_WHEELER].shake)
  heightData.datasets[ID_SIX_WHEELER].data.push(latestIMUData.value[ID_SIX_WHEELER].height)

  shakeData.datasets[ID_FOUR_WHEELER].data.push(latestIMUData.value[ID_FOUR_WHEELER].shake)
  heightData.datasets[ID_FOUR_WHEELER].data.push(latestIMUData.value[ID_FOUR_WHEELER].height)

  if (shakeChart) shakeChart.update()
  if (heightChart) heightChart.update()

  roverPosition.value = distance.value / distance_max * 100
}

const start = () => {
  if (!isRunning.value) {
    isRunning.value = true
    motorSocket.send(JSON.stringify({ command: 'resume' }))
  }
}

const pause = () => {
  if (isRunning.value) {
    isRunning.value = false
    motorSocket.send(JSON.stringify({ command: 'pause' }))
  }
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

    <!-- control buttons -->
    <div class="control-button">
      <button class="start" @click="start">开始</button>
      <button class="pause" @click="pause">暂停</button>
    </div>
  </div>
</template>
