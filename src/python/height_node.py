import asyncio
import websockets
import json
import threading
from gpiozero import DigitalInputDevice
import time
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description="Height Node")
parser.add_argument(
    "--server_address", type=str, default="localhost", help="Server address"
)
parser.add_argument("--server_port", type=int, default=8769, help="Server port")
parser.add_argument("--A", type=int, default=17, help="GPIO pin number for A phase")
parser.add_argument("--B", type=int, default=27, help="GPIO pin number for B phase")
parser.add_argument(
    "--sleep_duration", type=float, default=1.0, help="Sleep duration in seconds"
)
parser.add_argument(
    "--height_factor",
    type=float,
    default=0.02,
    help="Conversion factor for position to height",
)
args = parser.parse_args()

# Initialize GPIO pins
A = DigitalInputDevice(args.A)
B = DigitalInputDevice(args.B)

# Initialize position counter
position = 0

# Last state of A and B phases
last_A = A.value
last_B = B.value

# Server address
SERVER_ADDRESS = args.server_address
SERVER_PORT = args.server_port


# Function to update position
def update_position():
    global position, last_A, last_B

    # Check changes in A and B phases to determine direction
    A_value = A.value
    B_value = B.value

    # Check relative changes
    if A_value == 1 and last_A == 0:
        if B_value == 0:
            position -= 1  # Clockwise direction
        else:
            position += 1  # Counter-clockwise direction

    # Update last state
    last_A = A_value
    last_B = B_value


# Function to generate height data
def generate_height_data():
    last_print_time = time.time()  # 记录当前时间
    while True:
        update_position()

        current_time = time.time()
        if current_time - last_print_time >= args.sleep_duration:
            print(f"position data: {position}")
            last_print_time = current_time


# Function to send height data
async def send_height_data(websocket):
    while True:
        height_value = position * args.height_factor  # Convert position to height
        message = {
            "type": "height",
            "height": height_value,
        }
        await websocket.send(json.dumps(message))
        print(f"Sent height data: {message}")
        await asyncio.sleep(args.sleep_duration)


# WebSocket handler function
async def handler(websocket, path):
    global position
    print(f"New connection from {websocket.remote_address}")
    try:
        send_task = asyncio.create_task(send_height_data(websocket))
        async for message in websocket:
            data = json.loads(message)
            if data.get("command") == "reset":
                position = 0
                print("Height reset.")
        await send_task
    except Exception as e:
        print(f"Error occurred with {websocket.remote_address}: {e}")
    finally:
        send_task.cancel()
        print(f"Connection closed with {websocket.remote_address}")


# Start the WebSocket server and data generation thread
if __name__ == "__main__":
    threading.Thread(target=generate_height_data, daemon=True).start()
    start_server = websockets.serve(handler, SERVER_ADDRESS, SERVER_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"Height WebSocket server started on ws://{SERVER_ADDRESS}:{SERVER_PORT}")
    asyncio.get_event_loop().run_forever()
