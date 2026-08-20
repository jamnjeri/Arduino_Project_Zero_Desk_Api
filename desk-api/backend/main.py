import json
import serial
import threading
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

app = FastAPI()

latest_data = {
    "pot": None,
    "button": None,
}


def read_sensor_data():
    global latest_data

    while True:
        line = arduino.readline().decode(
            "utf-8",
            errors="replace"
        ).strip()

        if not line:
            continue

        try:
            latest_data = json.loads(line)
        except json.JSONDecodeError:
            continue


serial_thread = threading.Thread(target=read_sensor_data,daemon=True)

serial_thread.start()


@app.get("/data")
def get_data():
    return latest_data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await websocket.send_json(latest_data)
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        print("Client disconnected.")
