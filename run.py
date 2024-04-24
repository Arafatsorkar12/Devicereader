
--------->For Single USB 
#!/usr/bin/python3
import asyncio
import serial
import socketio
import threading
import time


ser = serial.Serial('/dev/ttyUSB0')

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    
])
app = socketio.ASGIApp(sio)
serial_thread = None
async def read_serial():
    print("it working")
    while True:
        # Read a line from the serial port
        line = ser.readline().decode().strip()
        print("Received:", line)
        await sio.emit('serial_data', line)
        await asyncio.sleep(0.1)

async def demo_serial():
    time.sleep(5)
    while True:
        if sio:
            time.sleep(1)
            await sio.emit("serial_data","12345")
            print("demo")


@sio.event
async def connect(sid, environ):
    print('Client connected')

@sio.event
async def disconnect(sid):
    print('Client disconnected')

if __name__ == '__main__':
    # serial_thread = threading.Thread(target=lambda: asyncio.run(read_serial()))
    serial_thread = threading.Thread(target=lambda: asyncio.run(demo_serial()))
    serial_thread.start()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)












--------->For multiple USB 


import asyncio
import serial
import socketio
import threading
import time

# List of USB ports to connect to
usb_ports = ['/dev/ttyUSB0','/dev/ttyUSB1']

# Dictionary to hold serial instances
serial_ports = {}

# Initialize socket.io server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[
    'http://localhost:8000',
    'http://127.0.0.1:8000',
])
app = socketio.ASGIApp(sio)
async def read_serial(port):
    print("Reading from", port)
    serial_port = serial.Serial(port)
    while True:
        # Read a line from the serial port
        line = serial_port.readline().decode().strip()
        print("Received from", port, ":", line)
        await sio.emit('serial_data',port +' '+ line )


@sio.event
async def connect(sid, environ):
    print('Client connected')

@sio.event
async def disconnect(sid):
    print('Client disconnected')

if __name__ == '__main__':
    # Start a separate thread for each serial port
    serial_threads = []
    for port in usb_ports:
        t=threading.Thread(target=lambda: asyncio.run(read_serial(port)))
        t.start()
        
    # Start the socket.io server
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
