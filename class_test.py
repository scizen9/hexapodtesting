from pipython import GCSDevice, pitools
from time import sleep
import random


class PiDevice:
    def __init__(self, home):
        self.h = home

    def start_up(self, hexapod):
        if self.h is True:
            print("Slewing to Home...")
            pitools.moveandwait(hexapod, {"x": 0, "y": 0, "z": 0})

        position = hexapod.qPOS()
        print(f"Position: {position}")
        return position

    def auto_correct(self, hexapod, position_current, position_togo):
        deltas, axes = [], ["x", "y", "z"]
        for i in axes:
            delta = abs(position_current[i]-position_togo[i])
            deltas.append(delta)

        n = 0
        for i in deltas:
            if i < 10**-3:  # 1 μm in mm
                deltas[n] = 0  # Eliminates unnecessary movement
            n += 1

        if deltas != [0, 0, 0]:
            print(f"Slewing to ideal position: {position_togo}")
            pitools.moveandwait(hexapod, position_togo)

            position_current = hexapod.qPOS()
            print(f"Position: {position_current}")

        else:
            print("Slew unnecessary.")

        return position_current


with GCSDevice() as test_device:
    test_device.InterfaceSetupDlg()

    test_object = PiDevice(True)
    position = test_object.start_up(test_device)

    while True:
        position_new = {"x": random.random(), "y": random.random(), "z": random.random()}  # Random positions for testing
        if False in position_new:
            pitools.moveandwait(test_device, {"x": 0, "y": 0, "z": 0})  # Return to home when observation period ends?
            break

        position = test_object.auto_correct(test_device, position, position_new)
        sleep(5)  # Correction interval
