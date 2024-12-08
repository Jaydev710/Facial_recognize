import serial
import time

def connect_to_esp32(port='COM11', baud_rate=115200):
    while True:
        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
            print(f"Connected to ESP32 on {port}")
            return ser
        except serial.SerialException as e:
            print(f"Error connecting to ESP32: {e}")
            time.sleep(2)

# ... rest of your code

serial_port = connect_to_esp32()

# Send a command to the ESP32
serial_port.write(b"Hello, ESP32!\n")

# Read the response
response = serial_port.readline().decode('utf-8').strip()
print(f"Received from ESP32: {response}")