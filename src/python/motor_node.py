import asyncio
import websockets
import json
import threading
import time
from gpiozero import LED, PWMOutputDevice
from time import sleep
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description="Motor Node")
parser.add_argument(
    "--server_address", type=str, default="localhost", help="Server address"
)
parser.add_argument("--server_port", type=int, default=8766, help="Server port")
parser.add_argument("--distance_max", type=float, default=1.5, help="Maximum distance")
parser.add_argument("--pwm_frequency", type=int, default=500, help="PWM frequency")
parser.add_argument("--pwm_duty_cycle", type=float, default=0.5, help="PWM duty cycle")
parser.add_argument("--dir_pin", type=int, default=11, help="GPIO pin for direction")
parser.add_argument("--pwm_pin", type=int, default=12, help="GPIO pin for PWM")
parser.add_argument("--speed_factor", type=float, default=0.1, help="Speed factor")
parser.add_argument(
    "--sleep_duration", type=float, default=1.0, help="Sleep duration in seconds"
)
args = parser.parse_args()

motor_running = False
current_distance = 0.0
start_time = None
direction = 1  # 1 for forward, -1 for backward

# Initialize GPIO pins
dir = LED(args.dir_pin)
pwm_pin = PWMOutputDevice(args.pwm_pin)  # GPIO pin for PWM

# Set PWM signal frequency and duty cycle
pwm_pin.frequency = args.pwm_frequency  # Set frequency
pwm_pin.value = args.pwm_duty_cycle  # Set duty cycle
pwm_pin.off()


# Function to generate motor distance data
def generate_motor_distance():
    global current_distance, motor_running, start_time, direction
    while True:
        if motor_running:
            elapsed_time = time.time() - start_time
            start_time=time.time()

            # Speed is proportional to PWM duty cycle
            speed = args.speed_factor * pwm_pin.value

            current_distance = current_distance + direction * elapsed_time * speed

            print(f"current_distance{current_distance}")
        sleep(args.sleep_duration)


# Function to send motor distance data
async def send_motor_distance(websocket):
    while True:
        if motor_running:
            message = {"type": "distance", "value": current_distance}
            await websocket.send(json.dumps(message))
            print(f"Sent distance: {current_distance} m")
        await asyncio.sleep(args.sleep_duration)


# WebSocket handler function
async def handler(websocket, path):
    global motor_running, start_time, current_distance, direction
    print(f"New connection from {websocket.remote_address}")
    try:
        send_task = asyncio.create_task(send_motor_distance(websocket))
        async for message in websocket:
            data = json.loads(message)
            if data.get("command") == "pause":
                motor_running = False
                pwm_pin.off()
                print("Motor paused.")
            elif data.get("command") == "resume":
                motor_running = True
                start_time = time.time()
                pwm_pin.on()
                pwm_pin.frequency = args.pwm_frequency  # Set frequency
                pwm_pin.value = args.pwm_duty_cycle  # Set duty cycle
                if data.get("direction") == "forward":
                    dir.on()
                    direction = 1
                    print("Motor resumed in forward direction.")
                elif data.get("direction") == "backward":
                    dir.off()
                    direction = -1
                    print("Motor resumed in backward direction.")
            elif data.get("command") == "reset":
                current_distance = 0
                print("Distance reset.")
            elif data.get("command") == "set_max":
                current_distance = args.distance_max
                print("Distance set to maximum.")
    except Exception as e:
        print(f"Error occurred with {websocket.remote_address}: {e}")
    finally:
        send_task.cancel()
        print(f"Connection closed with {websocket.remote_address}")


# Start the WebSocket server and data generation thread
if __name__ == "__main__":
    threading.Thread(target=generate_motor_distance, daemon=True).start()
    start_server = websockets.serve(handler, args.server_address, args.server_port)
    asyncio.get_event_loop().run_until_complete(start_server)
    print(
        f"Motor WebSocket server started on ws://{args.server_address}:{args.server_port}"
    )
    asyncio.get_event_loop().run_forever()
