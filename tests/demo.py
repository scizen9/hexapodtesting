from time import sleep
from serial import Serial
from pipython import GCSDevice

from f import home, zero, position, read, move

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:  # Indicator connection.
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)  # Hexapod connection.
        print(f"Hexapod Position: {position(pidevice)}\n"
              f"Indicator Position: {read(ser)}")

        _ = input("Home? (y/n): ")
        if _ == "y":
            print("Slewing to Home...")
            home(pidevice)
            print("Homed!")

            sleep(1)

            print("Zeroing Indicators...")
            zero(ser)
            print("Zeroed!\n"
                  f"Hexapod Position: {position(pidevice)}\n"
                  f"Indicator Position: {read(ser)}")

        while True:
            _ = input("Move? (y/n): ")
            if _ == "n":
                break

            x = float(input("x'-Position (µm): "))
            y = float(input("y'-Position (µm): "))
            z = float(input("z'-Position (µm): "))
            pos = [x/1000, y/1000, z/1000]

            print(f"Slewing to {pos}.")
            move(pidevice, pos)
            sleep(1)
            print("Slewed!\n"
                  f"Hexapod Position: {position(pidevice)}\n"
                  f"Indicator Position: {read(ser)}")
