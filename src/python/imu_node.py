import asyncio
import websockets
import json
import random
import threading
import time
import sys

# Server address
SERVER_ADDRESS = "localhost"

shake_max = 15
height_max = 0.5

# Vehicle types
ID_SIX_WHEELER = 0
ID_FOUR_WHEELER = 1

# Get serial port, vehicle type, and server port from command line arguments
if len(sys.argv) != 4:
    print("Usage: python imu_node.py <serial_port> <vehicle_type> <server_port>")
    sys.exit(1)

serial_port = sys.argv[1]
vehicle_type = int(sys.argv[2])
server_port = int(sys.argv[3])

# Function to generate IMU data
def generate_imu_data():
    while True:
        shake_value = round(random.uniform(0, shake_max), 2)
        height_value = round(random.uniform(0, height_max), 2)
        imu_data = {
            "vehicle_type": vehicle_type,
            "shake": shake_value,
            "height": height_value,
        }
        print(f"Generated IMU data: {imu_data}")
        time.sleep(1)

# Function to send IMU data
async def send_imu_data(websocket):
    while True:
        shake_value = round(random.uniform(0, shake_max), 2)
        height_value = round(random.uniform(0, height_max), 2)
        message = {
            "type": "imu",
            "vehicle_type": vehicle_type,
            "shake": shake_value,
            "height": height_value,
        }
        await websocket.send(json.dumps(message))
        print(f"Sent IMU data: {message}")
        await asyncio.sleep(1)


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
    start_server = websockets.serve(handler, SERVER_ADDRESS, server_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"IMU WebSocket server started on ws://{SERVER_ADDRESS}:{server_port}")
    asyncio.get_event_loop().run_forever()
