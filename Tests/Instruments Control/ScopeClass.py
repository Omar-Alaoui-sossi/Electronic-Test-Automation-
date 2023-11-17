__author__ = "Omar ALAOUI SOSSI"

import pyvisa
import numpy as np
from PIL import Image
import io
import time
import os
import datetime


class Oscilloscope:
    """
    This class provides an interface to control and interact with a Tektronix oscilloscope.

    Args :
        address (str): The address of the oscilloscope.

    Attributes :
        address (str): The address of the oscilloscope.
        instrument (visa.resources.Resource): The oscilloscope instrument resource.
    """

    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.scope = self.rm.open_resource(address)
        self.scope.timeout = 10000  # set timeout to 10 seconds

    def capture_screenshot(self, num_screenshots, delay=3):
        """
        Capture multiple screenshots from the oscilloscope and save them.

        Args :
            :num_screenshots: The number of screenshots to capture.
            :delay: The delay in seconds between each screenshot (default is 3 seconds).

        """

        dateString = time.strftime("%Y-%m-%d_%H%M")
        path = "C:\omar_local\Validated\img"  # Update the path according to your needs
        for i in range(num_screenshots):
            if not os.path.exists(path):
                os.makedirs(path)
            filepath = f"./{dateString}_{str(i)}.png"
            self.scope.write("HARDCOPY START")
            data = self.scope.read_raw()
            img = Image.open(io.BytesIO(data))
            filename = os.path.join(path, filepath)
            img.save(filename)
            time.sleep(delay)

    def one_screenshot(self):
        """
        Capture a single screenshot from the oscilloscope and save it in the same directory as the code.
        """
        dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"{dateString}.png"
        path = "./"
        self.scope.write("HARDCOPY START")
        data = self.scope.read_raw()
        img = Image.open(io.BytesIO(data))
        filename = os.path.join(path, filename)
        img.save(filename)
        time.sleep(3)
        return filename

    def extracted_from_get_measurements(self, arg0, arg1, arg2, arg3):
        """
        Write measurements to the scope.

        Args :
            :arg0: The first measurement to write.
            :type arg0: str
            :arg1: The second measurement to write.
            :type arg1: str
            :arg2: The third measurement to write.
            :type arg2: str
            :arg3: The fourth measurement to write.
            :type arg3: str

        Return :
            None

        """
        self.scope.write(arg0)
        self.scope.write(arg1)
        self.scope.write(arg2)
        self.scope.write(arg3)

    def get_measurements(self, channel):
        """
        Perform measurements on the oscilloscope and return the results.

        Return :
            :return: A tuple containing the measurements (pk2pk, mean, max_val, min_val).
            :type: tuple
        """
        self.extracted_from_get_measurements(
            "MEASUREMENT:MEAS1:TYPE PK2PK",
            "MEASUREMENT:MEAS2:TYPE MEAN",
            "MEASUREMENT:MEAS3:TYPE MAX",
            "MEASUREMENT:MEAS4:TYPE MIN",
        )
        self.scope.write(f"MEASUREMENT:MEAS1:IMMed:SOURCE {channel}")
        self.scope.write(f"MEASUREMENT:MEAS2:IMMed:SOURCE {channel}")
        self.scope.write(f"MEASUREMENT:MEAS3:IMMed:SOURCE {channel}")
        self.scope.write(f"MEASUREMENT:MEAS4:IMMed:SOURCE {channel}")

        self.extracted_from_get_measurements(
            "MEASUREMENT:MEAS1:STATE ON",
            "MEASUREMENT:MEAS2:STATE ON",
            "MEASUREMENT:MEAS3:STATE ON",
            "MEASUREMENT:MEAS4:STATE ON",
        )
        time.sleep(2)

        # Get the measurements
        pk2pk = float(self.scope.query("MEASUREMENT:MEAS1:VALUE?"))
        mean = float(self.scope.query("MEASUREMENT:MEAS2:VALUE?"))
        max_val = float(self.scope.query("MEASUREMENT:MEAS3:VALUE?"))
        min_val = float(self.scope.query("MEASUREMENT:MEAS4:VALUE?"))

        return pk2pk, mean, max_val, min_val

    def measure_mean(self, channel, nb):
        """
        Measures the signal of the choosen signal .

        Args :
            :channel: the number of the channel
            :type channel: str {e.g '1','2'}

        Returns:
            :Signal Mean: of the choosen channel
            :type Mean: float

        """
        self.scope.write(f"MEASUREMENT:MEAS{nb}:IMMed:SOURCE {channel}")
        self.scope.write(f"MEASUREMENT:MEAS{nb}:TYPE MEAN)")
        self.scope.write(f"MEASUREMENT:MEAS{nb}:STATE ON")
        return float(self.scope.query(f"MEASUREMENT:MEAS{nb}:VALUE?"))

    def capture_waveform(self, channel, points=100000):
        """
        Capture a waveform from the specified channel and return it as an array.

        Args :
            :channel: The channel number (e.g., 1, 2).
            :type channel: int
            :points: The number of data points to capture (default is 100000).
            :type points: int

        Return :
            :return: An array containing the waveform data.
            :type: numpy.ndarray
        """
        self.scope.write(f"DATA:SOUrce CH{channel}")
        self.scope.write("DATA:ENCdg ASCII")
        self.scope.write("DATA:WIDth 1")
        self.scope.write("DATA:STARt 1")
        self.scope.write(f"DATA:STOP {points}")
        data = self.scope.query_ascii_values("CURVE?")
        return np.array(data)

    def set_signal_scale(self, channel, scale):
        """
        Set the signal scale for the specified channel.

        Args :
            :channel: The channel number (e.g., 1, 2).
            :type channel: int
            :scale: The signal scale value.
            :type scale: float
        """
        self.scope.write(f"CHAN{channel}:SCALe {scale}")

    def set_time_scale(self, scale):
        """
        Set the time scale.

        Args :
            :scale: The time scale value.
            :type scale: float
        """
        self.scope.write(f"TIMEBASE:SCALE {scale}")

    def set_trigger_level(self, channel, level):
        """
        Set the trigger level for the specified channel.

        Args :
            :channel: The channel number (e.g., 1, 2).
            :type channel: int
            :level: The trigger level value.
            :type level: float
        """
        self.scope.write(f"TRIGGER:LEVEL:CH{channel} {level}")

    def set_trigger_source(self, source):
        """
        Set the trigger source.

        Args :
            :source: The trigger source.
            :type source: str
        """
        self.scope.write(f"TRIGGER:A:EDGE:SOURCE {source}")

    def run(self):
        """
        Start the oscilloscope.
        """
        self.scope.write("ACQuire:STATE RUN")
        time.sleep(4)

    def stop(self):
        """
        Stop the oscilloscope.
        """
        self.scope.write("ACQuire:STATE STOP")
        time.sleep(10)

    def reset(self):
        """
        Reset the oscilloscope to its default settings.
        """
        self.scope.write("*RST")

    def close(self):
        """
        Close the connection to the oscilloscope.
        """
        self.scope.close()
        self.rm.close()

    def math_signal_operation(self, channel_1, channel_2, operation):
        """
        This function performs the mathematical operation on the signals and visualizes it on the oscilloscope screen.

        Args :
            :channel_1: the channel of the first signal
            :type channel_1: str {CH1 CH2 CH3 CH4}
            :channel_2: the channel of the second signal
            :type channel_2: str {CH1 CH2 CH3 CH4}
            :operation: the mathematical operation to perform (+, -, *, /)
            :type operation: str {+,-,*,/}

        """

        self.scope.write(f":MATH:DEFINE '{channel_1}{operation}{channel_2}'")
        self.scope.write(":SELect:MATH 1")
        time.sleep(7)  # Time to stabilize


    def measure_value(self,channel,nb): 

        """
        Measures the signal of the choosen signal .

        Args :
            :channel: the number of the channel
            :type channel: str {e.g '1','2'}

        Returns:
            :Signal Mean: of the choosen channel
            :type Mean: float

        """
        self.scope.write(f"MEASUREMENT:MEAS{nb}:IMMed:SOURCE {channel}")
        self.scope.write(f"MEASUREMENT:MEAS{nb}:TYPE VALue)")
        self.scope.write(f"MEASUREMENT:MEAS{nb}:STATE ON")
        return float(self.scope.query(f"MEASUREMENT:MEAS{nb}:VALUE?"))
    
    def units(self): 
        unit_query = 'UNIT?'
        unit_result = self.scope.query(unit_query).strip()
        return unit_result



# b = a.measure_value("CH1",1) #Measurent 1  
# c = a.measure_value("CH2",2)
# d =  a.measure_value("MATH",3)

# print(f"############## {b} {a.units} ##############")
# print(f"############## {c} ##############")
# print(f"############## {d} ##############")
