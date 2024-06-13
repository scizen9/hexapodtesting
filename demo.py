from pipython import GCSDevice
from serial import Serial
from f import home, move, position, zero, read

with GCSDevice() as pidevice:
    with Serial("/dev/ttyACM0", 115200) as ser:
        pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
        print(f"Hexapod Position: {position(pidevice)}\n"
              f"Indicator Position: {read(ser)}")

        _ = input("Home? (y/n): ")
        if _ == "y":
            print("Slewing to Home...")
            home(pidevice)
            print("Homed!")

            print("Zeroing Indicators...")
            zero(ser)
            print("Zeroed!\n"
                  f"Hexapod Position: {position(pidevice)}\n"
                  f"Indicator Position: {read(ser)}")

        while True:
            _ = input("Move? (y/n): ")
            if _ == "n":
                break

            x = input("X-Position (mm): ")
            y = input("Y-Position (mm): ")
            z = input("Z-Position (mm): ")
            pos = [x, y, z]

            print(f"Slewing to {pos}.")
            move(pidevice, pos)
            print("Slewed!\n"
                  f"Hexapod Position: {position(pidevice)}\n"
                  f"Indicator Position: {read(ser)}")
