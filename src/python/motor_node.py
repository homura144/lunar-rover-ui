import asyncio
import websockets
import json
import threading
import time

# Server address and port
SERVER_ADDRESS = "localhost"
SERVER_PORT = 8766

motor_running = False
distance_max = 1.5
current_distance = 0.0


# TODO: Function to generate motor distance data
def generate_motor_distance():
    global current_distance, motor_running
    while True:
        if motor_running:
            if current_distance < distance_max:
                current_distance = round(current_distance + 0.1, 2)
                print(f"Generated distance: {current_distance} m")
            else:
                motor_running = False
                current_distance = 0
                print("Motor stopped at maximum distance.")
        time.sleep(1)


# Function to send motor distance data
async def send_motor_distance(websocket):
    while True:
        if motor_running:
            message = {"type": "distance", "value": current_distance}
            await websocket.send(json.dumps(message))
            print(f"Sent distance: {current_distance} m")
        await asyncio.sleep(1)


# WebSocket handler function
async def handler(websocket, path):
    global motor_running
    print(f"New connection from {websocket.remote_address}")
    try:
        send_task = asyncio.create_task(send_motor_distance(websocket))
        async for message in websocket:
            data = json.loads(message)
            if data.get("command") == "pause":
                motor_running = False
                print("Motor paused.")
            elif data.get("command") == "resume":
                motor_running = True
                print("Motor resumed.")
    except Exception as e:
        print(f"Error occurred with {websocket.remote_address}: {e}")
    finally:
        send_task.cancel()
        print(f"Connection closed with {websocket.remote_address}")


# Start the WebSocket server and data generation thread
if __name__ == "__main__":
    threading.Thread(target=generate_motor_distance, daemon=True).start()
    start_server = websockets.serve(handler, SERVER_ADDRESS, SERVER_PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"Motor WebSocket server started on ws://{SERVER_ADDRESS}:{SERVER_PORT}")
    asyncio.get_event_loop().run_forever()
