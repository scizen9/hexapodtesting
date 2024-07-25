from pipython import pitools


def home(pidevice):
    """
    Home hexapod.
    """
    pitools.moveandwait(pidevice, {"x": 0, "y": 0, "z": 0})  # Script stops until hexapod reaches position. Positions in millimeters (mm).


def move(pidevice, position):
    """
    Move hexapod.
    """
    pitools.moveandwait(pidevice, {"x": position[0], "y": position[1], "z": position[2]})


def position(pidevice):
    """
    Read hexapod.
    """
    pos = pidevice.qPOS()  # Gets hexapod self-identified position.
    return [pos["X"], pos["Y"], pos["Z"]]  # Converts dictionary to list.


def zero(ser):
    """
    Zero indicators.
    """
    channels = [b"0011", b"0021", b"0031"]  # Indicator X, Y, Z channels. Encodes string to bytes.
    for i in channels:
        ser.write(b"PZS,"+i+b"\r\n")  # Command to zero indicators. \r\n is CRLF.


def read(ser):
    """
    Read indicators.
    """
    channels, readings = [b"0011", b"0021", b"0031"], []
    ser.flushInput()  # Prevents duplicate readings.
    for i in channels:
        ser.write(b"GCJ,"+i+b"\r\n")  # Command to read indicators.
        line = ser.readline()  # Gets reading.

        if b"L0" not in line:  # Indicator error.
            line = float(line[11:][:11])/100000  # Converts reading to mm.
            readings.append(line)

        else:
            readings.append(None)

    return readings
