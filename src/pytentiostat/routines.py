import sys

import matplotlib.pyplot as plt
import serial.tools.list_ports
from pyfirmata2 import Arduino, util

_BAUD_RATE = 115200
RESTING_DUTY_CYCLE = 0.5
SAMPLING_RATE = 10 # 10 Hz

# Data storage
timestamps = []
analog_data = {0: [], 2: []}  # A0 and A2 data

# Callback function to collect data
def data_callback(data, pin_num):
    timestamps.append(time.time())
    analog_data[pin_num].append(data)

def _load_arduino():
    """Creates a list of all the active serial ports and then checks how many
    arduino unos are connected If only one is found, it's COM port is returned.

    If any other number is found, the corresponding error message is printed
    and the program exits.


    Returns
    -------
    com: string
        the COM port the arduino is connected to.
    """
    print("Searching for potentiostat...")
    ports = list(serial.tools.list_ports.comports())
    n_arduinos = 0
    for p in ports:  # Checking for Arduino Unos connected
        if "Arduino Uno" in p.description:
            com = p.device
            n_arduinos += 1
    if n_arduinos > 1:
        sys.exit("More than one Arduino Uno found. Exiting...")
    if n_arduinos == 0:
        sys.exit("No JUAMI potentiostat found. Exiting...")
    return com

def startup_routine():
    """Initializes the communication port with the JUAMI potentistat.

    Returns
    -------
    Map of hardware
    com : string
      the name of the port with the potentiostat on it
    board : serial communication for board
    a0 : location of analog read pin 0
    a2 : location of analog read pin 2
    d9 : location of digital pwm pin 9
    """

    print("Welcome to the JUAMI pytentiostat interface!")
    input("Press enter to connect to a JUAMI potentiostat.")
    com = _load_arduino()
    board = _initialize_arduino(com)

    it = util.Iterator(board)
    it.start()

    board.samplingOn(1000 / SAMPLING_RATE)

    # Setup Arduino pins
    a0 = board.get_pin("a:0:i")
    a2 = board.get_pin("a:2:i")
    d9 = board.get_pin("d:9:p")

    a0.enable_reporting()
    a2.enable_reporting()

    return com, board, a0, a2, d9

def closing_routine(board, d9):
    """Called after experiment is finished. Function brings the potential back
    to 0 V and closes the board object.

    Parameters
    ----------
    board: board object for communication
    d9: pin object for digital pin 9
    """
    # Prompt
    print("Experiment Complete! Closing...")

    # Reset PWM

    d9.write(RESTING_DUTY_CYCLE)

    # Close Connection
    board.exit()

    # Show Final Data
    plt.show()
