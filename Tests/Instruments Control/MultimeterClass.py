import pyvisa
import time


class Multimeter:
    """
    A class representing a multimeter instrument.

    Args:
        address (str): The address of the multimeter instrument.

    Attributes:
        address (str): The address of the multimeter instrument.
        rm (pyvisa.ResourceManager): The PyVISA resource manager.
        instrument (pyvisa.resources.Resource): The multimeter instrument resource.

    """

    def __init__(self, address):
        self.address = address
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(self.address)
        self.instrument.write_termination = "\n"
        self.instrument.read_termination = "\n"

    def set_mode_V(self):
        """
        Set the multimeter measurement mode to voltage (V).
        """
        self.instrument.write("CONFigure:VOLT:DC")

    def set_mode_A(self):
        """
        Set the multimeter measurement mode to current (A).
        """
        self.instrument.write("CONFigure:CURRent:DC")

    def set_mode_R(self):
        """
        Set the multimeter measurement mode to resistance (Ω).
        """
        self.instrument.write("CONF:RES")

    def set_mode_T(self):
        """
        Set the multimeter measurement mode to temperature (°C).
        """
        self.instrument.write("CONFigure:TEMP")

    def set_mode_Period(self):
        """
        Set the multimeter measurement mode to period (s).
        """
        self.instrument.write("CONFigure:PER")

    def set_range(self, range_value):
        """
        Set the range of the multimeter measurement.

        Args:
            range_value (float): The range value to set.
        """
        self.instrument.write(f":RANGe {range_value}")

    def measure_voltage(self):
        """
        Measure the voltage.

        Returns:
            float: The measured voltage value.
        """
        self.instrument.write(":MEASure:VOLTage?")
        return float(self.instrument.read())

    def measure_current(self):
        """
        Measure the current.

        Returns:
            float: The measured current value.
        """
        self.instrument.write(":MEASure:CURRent?")
        return float(self.instrument.read())

    def measure_resistance(self):
        """
        Measure the resistance.

        Returns:
            float: The measured resistance value.
        """
        self.instrument.write(":MEASure:RESistance?")
        return float(self.instrument.read())

    def measure_frequency(self):
        """
        Measure the frequency.

        Returns:
            float: The measured frequency value.
        """
        self.instrument.write(":MEASure:FREQuency?")
        return float(self.instrument.read())

    def measure_period(self):
        """
        Measure the period.

        Returns:
            float: The measured period value.
        """
        self.instrument.write(":MEASure:PERiod?")
        return float(self.instrument.read())

    def measure_temperature(self):
        """
        Measure the temperature.

        Returns:
            float: The measured temperature value.
        """
        self.instrument.write(":MEASure:TEMPerature?")
        return float(self.instrument.read())

    def reset(self):
        """
        Reset the multimeter instrument.
        """
        self.instrument.write("*RST")

    def close_connection(self):
        """
        Close the connection to the multimeter instrument.
        """
        self.instrument.close()
