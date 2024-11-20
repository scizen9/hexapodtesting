from time import sleep
from pipython import GCSDevice

from f import home, zero, position, read, move

IP='192.168.6.62'
PORT = 50000

with GCSDevice() as pidevice:
    pidevice.ConnectTCPIP(IP, ipport=PORT)  # Hexapod connection.
    print(f"Hexapod Position: {position(pidevice)}")

    _ = input("Home? (y/n): ")
    if _ == "y":
        print("Slewing to Home...")
        home(pidevice)
        print("Homed!")

        sleep(1)

    print(f"Hexapod Position: {position(pidevice)}")