import { app, shell, BrowserWindow } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { spawn } from 'child_process'
import {
  MOTOR_SOCKET_PORT,
  IMU_SOCKET_PORT_SIX,
  IMU_SOCKET_PORT_FOUR,
  HEIGHT_SOCKET_PORT_SIX,
  HEIGHT_SOCKET_PORT_FOUR,
  SERVER_ADDRESS,
  SLEEP_DURATION,
  DISTANCE_MAX,
  PWM_FREQUENCY,
  PWM_DUTY_CYCLE,
  DIR_PIN,
  PWM_PIN,
  SPEED_FACTOR,
  HEIGHT_FACTOR,
  A_PIN_SIX,
  B_PIN_SIX,
  A_PIN_FOUR,
  B_PIN_FOUR,
  SERIAL_PORT_SIX,
  SERIAL_PORT_FOUR,
  BAUDRATE
} from '../share/constants'

let imuSixProcess: any
let imuFourProcess: any
let motorProcess: any
let heightSixProcess: any
let heightFourProcess: any

function createWindow(): void {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    ...(process.platform === 'linux' ? { icon } : {}),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

function startPythonProcesses() {
  imuSixProcess = spawn('python', [
    'src/python/imu_node.py',
    '--server_address',
    SERVER_ADDRESS,
    '--server_port',
    IMU_SOCKET_PORT_SIX.toString(),
    '--serial_port',
    SERIAL_PORT_SIX,
    '--baudrate',
    BAUDRATE.toString(),
    '--sleep_duration',
    SLEEP_DURATION
  ])
  console.log('IMU Six process started')

  imuFourProcess = spawn('python', [
    'src/python/imu_node.py',
    '--server_address',
    SERVER_ADDRESS,
    '--server_port',
    IMU_SOCKET_PORT_FOUR.toString(),
    '--serial_port',
    SERIAL_PORT_FOUR,
    '--baudrate',
    BAUDRATE.toString(),
    '--sleep_duration',
    SLEEP_DURATION
  ])
  console.log('IMU Four process started')

  motorProcess = spawn('python', [
    'src/python/motor_node.py',
    '--server_address',
    SERVER_ADDRESS,
    '--server_port',
    MOTOR_SOCKET_PORT.toString(),
    '--distance_max',
    DISTANCE_MAX,
    '--pwm_frequency',
    PWM_FREQUENCY,
    '--pwm_duty_cycle',
    PWM_DUTY_CYCLE,
    '--dir_pin',
    DIR_PIN,
    '--pwm_pin',
    PWM_PIN,
    '--speed_factor',
    SPEED_FACTOR,
    '--sleep_duration',
    SLEEP_DURATION
  ])
  console.log('Motor process started')

  heightSixProcess = spawn('python', [
    'src/python/height_node.py',
    '--server_address',
    SERVER_ADDRESS,
    '--server_port',
    HEIGHT_SOCKET_PORT_SIX.toString(),
    '--A',
    A_PIN_SIX,
    '--B',
    B_PIN_SIX,
    '--sleep_duration',
    SLEEP_DURATION,
    '--height_factor',
    HEIGHT_FACTOR
  ])
  console.log('Height Six process started')

  heightFourProcess = spawn('python', [
    'src/python/height_node.py',
    '--server_address',
    SERVER_ADDRESS,
    '--server_port',
    HEIGHT_SOCKET_PORT_FOUR.toString(),
    '--A',
    A_PIN_FOUR,
    '--B',
    B_PIN_FOUR,
    '--sleep_duration',
    SLEEP_DURATION,
    '--height_factor',
    HEIGHT_FACTOR
  ])
  console.log('Height Four process started')
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  // startPythonProcesses()

  startPythonProcesses()
  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (imuSixProcess) imuSixProcess.kill()
    if (imuFourProcess) imuFourProcess.kill()
    if (motorProcess) motorProcess.kill()
    if (heightSixProcess) heightSixProcess.kill()
    if (heightFourProcess) heightFourProcess.kill()
    app.quit()
  }
})

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.
