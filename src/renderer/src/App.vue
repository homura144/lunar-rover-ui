<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Chart, registerables } from 'chart.js'
import {
  MOTOR_SOCKET_PORT,
  IMU_SOCKET_PORT_SIX,
  IMU_SOCKET_PORT_FOUR,
  HEIGHT_SOCKET_PORT_SIX,
  HEIGHT_SOCKET_PORT_FOUR
} from '@share/constants'

Chart.register(...registerables)

Chart.defaults.font.size = 18

const shakeChartRef = ref<HTMLCanvasElement | null>(null)
const heightChartRef = ref<HTMLCanvasElement | null>(null)

const distance = ref(0)
const roverPosition = ref(0)
const distance_max = 1.5
// const shake_max = 15
// const height_max = 0.5
const left_offset = 0.92

let shakeChart: Chart | null = null
let heightChart: Chart | null = null

const ID_SIX_WHEELER = 0
const ID_FOUR_WHEELER = 1

let currentDirection: 'forward' | 'backward' | null = null

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
const latestSensorData = ref({
  [ID_SIX_WHEELER]: { shake: 0, height: 0 },
  [ID_FOUR_WHEELER]: { shake: 0, height: 0 }
})

const motorSocket = new WebSocket(`ws://localhost:${MOTOR_SOCKET_PORT}`)
const imuSixSocket = new WebSocket(`ws://localhost:${IMU_SOCKET_PORT_SIX}`)
const imuFourSocket = new WebSocket(`ws://localhost:${IMU_SOCKET_PORT_FOUR}`)
const heightSixSocket = new WebSocket(`ws://localhost:${HEIGHT_SOCKET_PORT_SIX}`)
const heightFourSocket = new WebSocket(`ws://localhost:${HEIGHT_SOCKET_PORT_FOUR}`)

motorSocket.onmessage = (event) => {
  const data = JSON.parse(event.data)
  if (data.type === 'distance') {
    distance.value = data.value
    updateCharts()
    console.log(`Motor distance: ${data.value} m`)
  }
}

const handleIMUMessage = (event: MessageEvent, vehicleType: number) => {
  const data = JSON.parse(event.data)
  if (data.type === 'imu') {
    latestSensorData.value[vehicleType].shake = data.shake
    console.log(`IMU data: ${vehicleType}, shake: ${data.shake}`)
  }
}

const handleHeightMessage = (event: MessageEvent, vehicleType: number) => {
  const data = JSON.parse(event.data)
  if (data.type === 'height') {
    latestSensorData.value[vehicleType].height = data.height
    console.log(`Height data: ${vehicleType}, height: ${data.height}`)
  }
}

imuSixSocket.onmessage = (event) => handleIMUMessage(event, ID_SIX_WHEELER)
imuFourSocket.onmessage = (event) => handleIMUMessage(event, ID_FOUR_WHEELER)
heightSixSocket.onmessage = (event) => handleHeightMessage(event, ID_SIX_WHEELER)
heightFourSocket.onmessage = (event) => handleHeightMessage(event, ID_FOUR_WHEELER)

const updateCharts = () => {
  const newLabel: number = Number(distance.value.toFixed(2))
  shakeData.labels.push(newLabel)
  heightData.labels.push(newLabel)

  shakeData.datasets[ID_SIX_WHEELER].data.push(latestSensorData.value[ID_SIX_WHEELER].shake)
  heightData.datasets[ID_SIX_WHEELER].data.push(latestSensorData.value[ID_SIX_WHEELER].height)

  shakeData.datasets[ID_FOUR_WHEELER].data.push(latestSensorData.value[ID_FOUR_WHEELER].shake)
  heightData.datasets[ID_FOUR_WHEELER].data.push(latestSensorData.value[ID_FOUR_WHEELER].height)

  if (shakeChart) shakeChart.update()
  if (heightChart) heightChart.update()

  roverPosition.value = distance.value / distance_max * 100
}

const clearCharts = () => {
  shakeData.labels = []
  shakeData.datasets.forEach(dataset => dataset.data = [])
  heightData.labels = []
  heightData.datasets.forEach(dataset => dataset.data = [])

  if (shakeChart) shakeChart.update()
  if (heightChart) heightChart.update()
}

const forward = () => {
  if (currentDirection !== 'forward') {
    clearCharts()
    currentDirection = 'forward'
  }
  if (!isRunning.value) {
    isRunning.value = true
    motorSocket.send(JSON.stringify({ command: 'resume', direction: 'forward' }))
  }
}

const backward = () => {
  if (currentDirection !== 'backward') {
    clearCharts()
    currentDirection = 'backward'
  }
  if (!isRunning.value) {
    isRunning.value = true
    motorSocket.send(JSON.stringify({ command: 'resume', direction: 'backward' }))
  }
}

const pause = () => {
  if (isRunning.value) {
    isRunning.value = false
    motorSocket.send(JSON.stringify({ command: 'pause' }))
  }
}

const resetDistance = () => {
  motorSocket.send(JSON.stringify({ command: 'reset' }))
  heightFourSocket.send(JSON.stringify({ command: 'reset' }))
  heightSixSocket.send(JSON.stringify({ command: 'reset' }))

  distance.value = 0
  roverPosition.value = 0
  clearCharts()
}

const setMaxDistance = () => {
  motorSocket.send(JSON.stringify({ command: 'set_max' }))
  heightFourSocket.send(JSON.stringify({ command: 'reset' }))
  heightSixSocket.send(JSON.stringify({ command: 'reset' }))

  distance.value = distance_max
  roverPosition.value = 100
  clearCharts()
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
            // min: 0,
            // max: shake_max,
            // ticks: {
            //   stepSize: 3,
            // }
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
              text: '高度/mm'
            },
            // min: 0,
            // max: height_max,
            // ticks: {
            //   stepSize: 0.1,
            // }
          }
        }
      }
    })
  }
})

const adjustedLeft = computed(() => {
  return `${roverPosition.value * left_offset}%`
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
      <img class="rover" src="@renderer/assets/rover.png" alt="Rover" :style="{ left: adjustedLeft }" />

      <!-- Adjustable width ratio using "flex" -->
      <div class="terrain-label">
        <div class="terrain-area flat" style="flex: 1">平坦区域</div>
        <div class="terrain-area bump" style="flex: 5">起伏区域</div>
        <div class="terrain-area flat" style="flex: 1">平坦区域</div>
      </div>
    </div>

    <!-- control buttons -->
    <div class="control-button">
      <button class="forward" @click="forward">前进</button>
      <button class="backward" @click="backward">后退</button>
      <button class="pause" @click="pause">暂停</button>
      <button class="reset" @click="resetDistance">起点</button>
      <button class="set-max" @click="setMaxDistance">终点</button>
    </div>
  </div>
</template>
