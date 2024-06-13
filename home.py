from pipython import GCSDevice
from f import home

with GCSDevice() as pidevice:
    pidevice.ConnectRS232("/dev/ttyUSB0", 115200)
    home(pidevice)
