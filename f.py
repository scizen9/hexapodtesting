from pipython import pitools


def home(pidevice):
    """
    Move hexapod to its home position.
    """
    pitools.moveandwait(pidevice, {"x": 0, "y": 0, "z": 0})  # Positions in millimeters (mm).


def move(pidevice, position):
    """
    Move hexapod to specific position.
    """
    try:
        position = [float(i) for i in position]
    except ValueError:
        print("Input is not float.")

    for i in position:
        if i > 2:
            print("CRITICAL WARNING: POSITION BEYOND LIMITS. STOPPING MOTION")
            quit()
        elif i < -2:
            print("CRITICAL WARNING: POSITION BEYOND LIMITS. STOPPING MOTION")
            quit()
    pitools.moveandwait(pidevice, {"x": position[0], "y": position[1], "z": position[2]})


def position(pidevice):
    """
    Get hexapod position list from hexapod position dictionary.
    """
    pos = pidevice.qPOS()  # Gets hexapod self-identified position.
    return [pos["X"], pos["Y"], pos["Z"]]


def zero(ser):
    """
    Zero indicators.
    """
    channels = [b"0011", b"0021", b"0031"]  # Indicator 1, 2, and 3 (x, y, and z).
    for i in channels:
        ser.write(b"PZS,"+i+b"\r\n")  # Command to zero indicators. \r\n is CRLF.


def read(ser):
    """
    Get indicator readings.
    """
    channels, readings = [b"0011", b"0021", b"0031"], []
    ser.flushInput()  # Prevents duplicate readings.
    for i in channels:
        ser.write(b"GCJ,"+i+b"\r\n")  # Command to read indicators.
        line = ser.readline()  # Gets reading.

        if b"L0" not in line:  # L0 reading designates indicator error.
            line = float(line[11:][:11])/100000  # Converts reading to mm.
            readings.append(line)

        else:
            readings.append(None)

    return readings
