from pipython import GCSDevice
from operational import home


def measure_flexure():
    """
    Command the hexapod to move to its home position.
    Record the values of X, Y, and Z.
    Rotate the test stand by 30 degrees.
    Record X, Y, and Z.
    Repeat step 2 for two full rotations (720 degrees).
    Report any change in the dial gauges as unanticipated flexure.
    If the flexure is non-negligible, the flexure could be due to the dummy weights rather than the hexapod.
    To confirm hexapod flexure, relocate the dial gauges to the hex-to-cryo plate.
    Repeat the experiment from step 1.
    """
    home(pidevice)
    rotate_confirm30 = input("Rotate test stand 30 degrees.")  # Inputs force code to "pause".
    print(pidevice.qPOS())
    rotate_confirm720 = input("Rotate test stand 720 degrees.")
    print(pidevice.qPOS())


with GCSDevice("C-184") as pidevice:
    pidevice.InterfaceSetupDlg()
    measure_flexure()
    weights_confirm = input("Repeat without dummy weights.")
