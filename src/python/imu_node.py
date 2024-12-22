import asyncio
import websockets
import json
import threading
import serial
import argparse
import time
from imu_data_processor import DueData, get_latest_data
import math

# Parse command line arguments
parser = argparse.ArgumentParser(description="IMU Node")
parser.add_argument(
    "--server_address", type=str, default="localhost", help="Server address"
)
parser.add_argument("--server_port", type=int, default=8767, help="Server port")
parser.add_argument("--serial_port", type=str, required=True, help="Serial port")
parser.add_argument("--baudrate", type=int, required=True, help="Baudrate")
parser.add_argument(
    "--sleep_duration", type=float, default=1.0, help="Sleep duration in seconds"
)
args = parser.parse_args()

# Initialize serial port
ser = serial.Serial(args.serial_port, args.baudrate, timeout=0.5)
print(f"Serial port {args.serial_port} opened: {ser.is_open}")

# Server address
SERVER_ADDRESS = args.server_address
SERVER_PORT = args.server_port


# Function to generate IMU data
def generate_imu_data():
    last_print_time = time.time()  # 记录当前时间
    while True:
        datahex = ser.read(33)
        DueData(datahex)

        current_time = time.time()
        if current_time - last_print_time >= args.sleep_duration:
            acc,w,angle=get_latest_data()
            print(f"current_imu_angle:{angle}")
            last_print_time = current_time

# Function to send IMU data
async def send_imu_data(websocket):
    while True:
        acc, w, angle = get_latest_data()
        shake = math.sqrt(angle[0] ** 2 + angle[1] ** 2)
        message = {
            "type": "imu",
            "shake": shake,
        }
        await websocket.send(json.dumps(message))
        print(f"Sent IMU data: {message}")
        await asyncio.sleep(args.sleep_duration)


# WebSocket handler function
async def handler(websocket, path):
    print(f"New connection from {websocket.remote_address}")
    try:
        send_task = asyncio.create_task(send_imu_data(websocket))
        await send_task
    except Exception as e:
        print(f"Error occurred with {websocket.remote_address}: {e}")
    finally:
        send_task.cancel()
        print(f"Connection closed with {websocket.remote_address}")


# Start the WebSocket server and data generation thread
if __name__ == "__main__":
    threading.Thread(target=generate_imu_data, daemon=True).start()
    start_server = websockets.serve(handler, SERVER_ADDRESS, SERVER_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"IMU WebSocket server started on ws://{SERVER_ADDRESS}:{SERVER_PORT}")
    asyncio.get_event_loop().run_forever()
