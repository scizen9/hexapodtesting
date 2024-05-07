from pipython import GCSDevice
from operational import home


def move(pidevice):
    coordinate = ""
    coordinates = ["x", "y", "z"]
    while coordinate not in coordinates:
        coordinate = input("Coordinate (x, y, z): ")
        coordinate = coordinate.strip().lower()

    distance = ""
    w = False
    while w is False:
        try:
            distance = float(distance)
            w = True
        except:
            distance = input("Distance (mm): ")
            w = False

    print(f"Moving {distance} mm along {coordinate}-axis.")
    pidevice.MOV({coordinate: distance})
    print(pidevice.qPOS())


with GCSDevice() as pidevice:
    pidevice.InterfaceSetupDlg()
    home(pidevice)

    stop = ""
    while stop != 'q':
        stop = input("Enter anything to continue. Enter 'q' to quit.")
        stop.strip().lower()
        move(pidevice)
