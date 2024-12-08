# import serial

# # Initialize serial connection
# ser = serial.Serial()
# ser.baudrate = 115200
# ser.port = 'COM11'
# ser.open()

# # Data to send
# values = bytearray([4, 9, 62, 144, 56, 30, 147, 3, 210, 89, 111, 78, 184, 151, 17, 129])
# ser.write(values)

# # Track total bytes received
# total = 0

# while total < len(values):
#     byte = ser.read(1)  # Read one byte
#     if byte:
#         print(int.from_bytes(byte, "big"))  # Convert byte to integer
#         total += 1

# ser.close()
import serial
 
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM11'
ser.open()
 
values = bytearray([4, 9, 62, 144, 56, 30, 147, 3, 210, 89, 111, 78, 184, 151, 17, 129])
ser.write(values)
 
total = 0
 
while total < len(values):
    print (ser.read(1))
    total=total+1
 
ser.close()