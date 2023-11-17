__author__ = "Omar ALAOUI SOSSI "

import pyvisa
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ChromaACSourceControl:
    """
    This class provides an interface to control and interact with a Chroma AC Source .

    Args :
        : address: The address of the chroma.
        :type address: str

    Attributes:
        address (str): The address of the Chroma .
        instrument (visa.resources.Resource): The Chroma instrument resource.
    """

    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(address)

    def set_frequency(self, frequency):
        """
        Set the frequency of the AC source.
        """
        self.instrument.write(f"FREQ {frequency}")

    def set_voltage_DC(self, voltage):
        """
        Set the DC voltage of the AC source.
        """
        return self.instrument.write(f"VOLT:DC {voltage}")

    def set_voltage_AC(self, voltage):
        """
        Set the DC voltage of the AC source.
        """
        return self.instrument.write(f"VOLT:AC {voltage}")

    def set_voltage(self, mode, voltage):
        return self.instrument.write(f"VOLT:{mode} {voltage}")

    def set_voltage_range(self, start_voltage, end_voltage, step_voltage):
        """
        Set the voltage range of the AC source.

        Args :
            :start_voltage: The starting voltage.
            :type start_voltage: float
            :end_voltage: The ending voltage.
            :type end_voltage: float
            :step_voltage: The voltage step size.
            :type step_voltage: float
        """

        def frange(start, end, step):
            while start <= end:
                yield start
                start += step

        for voltage in frange(start_voltage, end_voltage, step_voltage):
            self.instrument.write(f"VOLT:DC {voltage}")
            print("Setting Voltage:", voltage)
            time.sleep(1)  # Adjust the delay as needed

    def set_current_limit(self, current_limit):
        """
        Set the current limit of the AC source.
        """
        self.instrument.write(f"CURR {current_limit}")

    def set_output_on(self):
        """
        Turn on the output of the AC source.
        """
        self.instrument.write("OUTP ON")

    def set_output_off(self):
        """
        Turn off the output of the AC source.
        """
        self.instrument.write("OUTP OFF")

    def set_waveform_type(self, waveform_type):
        """
        Set the waveform type of the AC source.
        """
        self.instrument.write(f"FUNC {waveform_type}")

    def set_phase_angle(self, phase_angle):
        """
        Set the phase angle of the AC source.
        """
        self.instrument.write(f"PHAS {phase_angle}")

    def set_voltage_offset(self, voltage_offset):
        """
        Set the voltage offset of the AC source.
        """
        self.instrument.write(f"VOLT:OFFS {voltage_offset}")

    def set_frequency_sweep(self, start_frequency, end_frequency, sweep_time):
        """
        Set the frequency sweep eters of the AC source.
        """
        self.instrument.write(f"SWE:FREQ:STAR {start_frequency}")
        self.instrument.write(f"SWE:FREQ:STOP {end_frequency}")
        self.instrument.write(f"SWE:TIME {sweep_time}")

    def set_current_sweep(self, start_current, end_current, sweep_time):
        """
        Set the current sweep eters of the AC source.
        """
        self.instrument.write(f"SWE:CURR:STAR {start_current}")
        self.instrument.write(f"SWE:CURR:STOP {end_current}")
        self.instrument.write(f"SWE:TIME {sweep_time}")

    def generate_trapezoidal_signal(self, duration, rise_time, amplitude):
        """
        Generate a trapezoid signal with specified eters.

        Args :
            :duration: The duration of the signal.
            :type duration: float
            :rise_time: The rise time of the signal.
            :type rise_time: float
            :amplitude: The amplitude of the signal.
            :type amplitude: float

        Return :
            :return: The generated trapezoid signal.
            :rtype: numpy.ndarray
        """

        start_time = time.time()
        signal_values = []
        time_values = []
        total_points = 200  # Number of data points within the duration
        self.set_output_on()
        while True:
            current_time = time.time() - start_time
            if current_time >= duration:
                break

            # Calculate the signal value based on the current time and amplitude
            if current_time <= rise_time:
                signal_value = (current_time / rise_time) * amplitude
            elif current_time <= duration - rise_time:
                signal_value = amplitude
            else:
                signal_value = (
                    1 - (current_time - (duration - rise_time)) / rise_time
                ) * amplitude

            signal_values.append(signal_value)
            time_values.append(current_time)

            self.instrument.write(f"VOLT:DC {signal_value}")

            # Delay to maintain the desired time resolution
            time.sleep(0.075)

        return signal_values
