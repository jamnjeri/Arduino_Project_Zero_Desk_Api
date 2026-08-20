import json
import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

def read_sensor_data(arduino):
    line = arduino.readline().decode("utf-8", errors="replace").strip()

    if not line:
        return None

    try: 
        return json.loads(line)
    except json.JSONDecodeError:
        return None

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

while True:
    data = read_sensor_data(arduino)

    if data is not None:
        print(data)
