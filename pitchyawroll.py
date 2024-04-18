from pipython import GCSDevice
from operational import home


def measure_roll():
    """
    Record the pixel position (x, y) of a spot on any of the detectors (science or FCS).
    Command the hexapod to move 225 microns (15 pixels) in any direction.
    Record the new pixel position.
    This measurement is sufficient to determine the roll angle.
    """
    home(pidevice)
    pidevice.MOV({"X": 0.225})
    print(pidevice.qPOS())


with GCSDevice("C-184") as pidevice:
    pidevice.InterfaceSetupDlg()
    measure_roll()
