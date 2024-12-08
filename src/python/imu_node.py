import asyncio
import websockets
import json
import random
import threading
import time

# Server address and port
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8767

current_shake = 0.0

# TODO: Function to generate simulated IMU data
def generate_imu_data():
    global current_shake
    while True:
        gyro_x = round(random.uniform(-250, 250), 2)
        gyro_y = round(random.uniform(-250, 250), 2)
        gyro_z = round(random.uniform(-250, 250), 2)
        current_shake = round((gyro_x**2 + gyro_y**2 + gyro_z**2) ** 0.5, 2)
        print(f"Generated IMU data: {current_shake}")
        time.sleep(0.5)


# Function to send IMU data
async def send_imu_data(websocket):
    while True:
        message = {"type": "imu", "value": current_shake}
        await websocket.send(json.dumps(message))
        print(f"Sent IMU data: {current_shake}")
        await asyncio.sleep(1)


# WebSocket handler function
async def handler(websocket, path):
    print(f"New connection from {websocket.remote_address}")
    try:
        send_task = asyncio.create_task(send_imu_data(websocket))
        async for message in websocket:
            pass  # No commands to handle for IMU
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
