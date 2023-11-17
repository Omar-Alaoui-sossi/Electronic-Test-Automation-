__author__ = "Omar ALAOUI SOSSI "
import pyvisa
import time
import numpy as np
import datetime
import Instruments


class ElectronicLoad:
    """
    This class provides an interface to control and interact with an Electronic Load .
    Args :
        : address: The address of the Load .
        :type address: str

    Attributes:
        address (str): The address of the Electronic Load instrument.
        instrument (visa.resources.Resource): The Electronic Load instrument resource.
    """

    def __init__(self, address):
        self.address = address
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(self.address)
        self.instrument.write_termination = "\n"
        self.instrument.read_termination = "\n"

    def set_mode(self, mode, chanel):
        """
        Set the mode of the electronic load for a specific channel.
         Args :
            :channel: the targeted channel
            :type channel: str
            :mode: CC CR CV CP
            :type mode: str

        """
        self.instrument.write(f":FUNCtion {mode} ,(@{chanel})")

    def set_range_low(self, channel):
        """
        Set the range of the electronic load to Low

        Args :
            :channel: the targeted channel
            :type channel: str

        """
        self.instrument.write(f":CURR:RANG 0.4, (@{channel})")

    def set_range_medium(self, channel):
        """
        Set the range of the electronic load to Medium

        Args :
            :channel: the targeted channel
            :type channel: str

        """
        self.instrument.write(f":CURR:RANG 3, (@{channel})")

    def set_range_high(self, channel):
        """
        Set the range of the electronic load to High

        Args :
            :channel: the targeted channel
            :type channel: str

        """
        self.instrument.write(f":CURR:RANG 10, (@{channel})")

    def set_load(self, load):
        """
        Set the resistance load value.
        """
        self.instrument.write(f":RESistance {load}")

    def set_current(self, current):
        """
        Set the current value.
        """
        self.instrument.write(f":CURRent {current}")

    def set_voltage(self, voltage):
        """
        Set the voltage value.
        """
        self.instrument.write(f":VOLTage {voltage}")

    def set_power(self, power):
        """
        Set the power value.
        """
        self.instrument.write(f":POWer {power}")

    def enable_input(self, chanel):
        """
        Enable the input for a specific channel.
        """
        self.instrument.write(f":INPut ON,(@{chanel})")

    def disable_input(self, chanel):
        """
        Disable the input for a specific channel.
        """
        self.instrument.write(f":INPut OFF ,(@{chanel})")

    def enable_output(self, chanel):
        """
        Enable the output for a specific channel.
        """
        self.instrument.write(f":OUTPut ON,(@{chanel})")

    def disable_output(self, chanel):
        """
        Disable the output for a specific channel.
        """
        self.instrument.write(f":OUTPut OFF ,(@{chanel})")

    def measure_voltage(self, chanel):
        """
        Measure the voltage for a specific channel.
        """
        time.sleep(2)
        return float(self.instrument.query(f"MEAS:VOLT? (@{chanel})"))

    def measure_current(self, chanel):
        """
        Measure the current for a specific channel.
        """
        self.instrument.write(f":MEASure:CURRent? (@{chanel})")
        time.sleep(2)
        return float(self.instrument.read())

    def measure_power(self, chanel):
        """
        Measure the power for a specific channel.
        """
        self.instrument.write(f":MEASure:POWer? (@{chanel})")
        return float(self.instrument.read())

    def set_current_range_VI(self, start, end, step, channel, lenght_):
        """
        Set the current range from a start point to an end point with a specific step.

        Args :
            :start: The start current value.
            :type start: float
            :end: The end current value.
            :type end: float
            :step: The step size.
            :type step: float
            :channel: The channel number (e.g., 1, 2).
            :type channel: str
            :lenght_: lenght of the current table
            :type lenght : int

        Return :
            :return: Lists containing the voltage, current, timestamps, and time differences.
            :type: tuple(list, list, list, list)
        """

        voltage_list = []
        current_list = []
        time_list = []

        self.enable_input(channel)
        list = np.round(np.arange(start, end, step), 6)
        updated_range_list = np.tile(list, lenght_)
        for i in updated_range_list:
            current = i
            self.instrument.write(
                f"SOUR:CURR:LEV:IMM:AMPL {current:.3f},(@{channel})"
            )  # set current level
            time.sleep(1)  # wait for settling time
            v = self.measure_voltage(channel)
            voltage_list.append(v)
            current_list.append(current)
            time_str = self.instrument.query(":SYST:TIME?")
            time_str_ = datetime.datetime.strptime(time_str.strip(), "+%H,+%M,+%S")
            time_list.append(
                time_str
            )  # store current timestamp from the instrument itself

            time.sleep(3)

        return voltage_list, current_list, time_list

    def set_current_steps_VI(self, steps, chanel, osc_address, lenght):
        """
        Set the current steps for a specific channel.

        Args :
            :steps: A list of current steps.
            :type steps: list
            :chanel: The channel number (e.g., 1, 2).
            :type chanel: str
            :osc_address: The address of the oscilloscope.
            :type osc_address: str
            :lenght_: lenght of the current table
            :type lenght : int

        Return :
            :return: Lists containing the voltage and current values.
            :type: tuple(list, list)
        """
        voltage_list = []
        current_list = []
        self.enable_input(chanel)
        osc = Instruments.scope(osc_address)
        updated_step_list = np.repeat(np.array(steps), lenght)
        for step in updated_step_list:
            self.instrument.write(f":SOUR:CURR:LEV:IMM:AMPL {step},(@{chanel})")
            time.sleep(0.5)
            v = self.measure_voltage(chanel)
            time.sleep(0.8)
            voltage_list.append(v)
            current_list.append(step)
            time.sleep(3)

            osc.one_screenshot()
            time.sleep(3)

        return voltage_list, current_list

    def set_curr_limitation(self, limit, chanel):
        """
        Set the current limitation for a specific channel.
        """
        self.instrument.write(f": CURR:LIM {limit} (@{chanel})")

    def Reset(self):
        """
        Reset the electronic load.
        """
        self.instrument.write("*RST")

    def set_current_steps_PE(self, steps, chanel, addr, lenght):
        """
        Set the current steps for a specific channel.

        Args :
            :steps: A list of current steps.
            :type steps: list
            :chanel: The channel number (e.g., 1, 2).
            :type chanel: str
            :lenght: lenght of the current table
            :type lenght : int r

        Return :
            :return: Lists containing the voltage and current values.
            :type: tuple(list, list)
        """
        voltage_list = []
        current_list = []
        ILv = []
        self.enable_input(chanel)
        mutimeter = Instruments.multi(addr)
        updated_step_list = np.repeat(np.array(steps), lenght)
        for step in updated_step_list:
            self.instrument.write(f":SOUR:CURR:LEV:IMM:AMPL {step},(@{chanel})")
            time.sleep(0.5)
            v = self.measure_voltage(chanel)
            curr_lv = mutimeter.measure_current()
            time.sleep(0.8)
            voltage_list.append(v)
            current_list.append(step)
            ILv.append(curr_lv)
            time.sleep(3)

            time.sleep(3)

        return voltage_list, current_list, ILv

    def set_current_range_PE(
        self, start, end, step, channel, osc_address, lenght_, CH1, CH2, CH3, CH4
    ):
        """
        Set the current range from a start point to an end point with a specific step.

        Args :
            :start: The start current value.
            :type start: float
            :end: The end current value.
            :type end: float
            :step: The step size.
            :type step: float
            :channel: The channel number (e.g., 1, 2).
            :type channel: str
            :osc_address: Oscilloscope address
            :type osc_address: str
            :lenght_: lenght of the current table
            :type lenght_ : int

        Return :
            :return: Lists containing the voltage, current, timestamps, Iac,Vac,Ibus, and Vbus
            :type: tuple(list, list, list, list,list, list, list,list)
        """
        osc = Instruments.scope(osc_address)

        voltage_list = []
        current_list = []
        time_list = []
        Iac = []
        Ibus = []
        Vbus = []
        Psecteur = []

        self.enable_input(channel)
        list = np.round(np.arange(start, end, step), 6)
        updated_range_list = np.tile(list, lenght_)
        for i in updated_range_list:
            osc.run()
            current = i
            self.instrument.write(
                f"SOUR:CURR:LEV:IMM:AMPL {current:.3f},(@{channel})"
            )  # set current level
            time.sleep(1)  # wait for settling time
            v = self.measure_voltage(channel)
            voltage_list.append(v)
            current_list.append(current)

            time_str = self.instrument.query(":SYST:TIME?")
            time_list.append(
                time_str
            )  # store current timestamp from the instrument itself

            osc.stop()
            time.sleep(10)
            Mean_Iac = osc.measure_mean(CH1, 1)
            Mean_Ibus = osc.measure_mean(CH3, 2)
            Mean_Vbus = osc.measure_mean(CH4, 3)
            Iac.append(Mean_Iac)
            Ibus.append(Mean_Ibus)
            Vbus.append(Mean_Vbus)
            time.sleep(3)
            osc.one_screenshot()
            osc.math_signal_operation(CH1, "*", CH2)
            time.sleep(3)
            Mean_Psecteur = osc.measure_mean("MATH", 4)
            Psecteur.append(Mean_Psecteur)

        return voltage_list, current_list, time_list, Iac, Ibus, Vbus, Psecteur

    def set_current_steps_jule(self, steps, chanel,lenght):
        """
        Set the current steps for a specific channel.

        Args :
            :steps: A list of current steps.
            :type steps: list
            :chanel: The channel number (e.g., 1, 2).
            :type chanel: str
            :osc_address: The address of the oscilloscope.
            :type osc_address: str
            :lenght_: lenght of the current table
            :type lenght : int

        Return :
            :return: Lists containing the voltage and current values.
            :type: tuple(list, list)
        """
        voltage_list = []
        current_list = []

        self.enable_input(chanel)

        updated_step_list = np.repeat(np.array(steps), lenght)
        for step in updated_step_list:
            self.instrument.write(f":SOUR:CURR:LEV:IMM:AMPL {step},(@{chanel})")
            time.sleep(0.5)
            v = self.measure_voltage(chanel)
            time.sleep(0.8)
            voltage_list.append(v)
            current_list.append(step)
            time.sleep(3)
        return voltage_list, current_list



    def range_i(self, start, end, step, channel, lenght_,osc_address):

        voltage_list = []
        current_list = []
        time_list = []
        Math = []
        IRMS = []
        VRMS = []
        screenshot=[]
        osc = Instruments.scope(osc_address)
        self.enable_input(channel)
        list = np.round(np.arange(start, end, step), 6)
        updated_range_list = np.tile(list, lenght_)
        for i in updated_range_list:
            current = i
            self.instrument.write(
                f"SOUR:CURR:LEV:IMM:AMPL {current:.3f},(@{channel})"
            )  # set current level
            time.sleep(1)  # wait for settling time
            v = self.measure_voltage(channel)
            voltage_list.append(v)
            current_list.append(current)
            time_str = self.instrument.query(":SYST:TIME?")
            time_str_ = datetime.datetime.strptime(time_str.strip(), "+%H,+%M,+%S")
            time_list.append(
                time_str
            )  # store current timestamp from the instrument itself
            time.sleep(1)
            M =osc.measure_value("MATH",3)
            IR = osc.measure_value("CH1",1)
            VR = osc.measure_value("CH2",2)
            Math.append(M)
            IRMS.append(IR)
            VRMS.append(VR)
            time.sleep(1)
            s = osc.one_screenshot()
            screenshot.append(s)
            time.sleep(3)

        return voltage_list, current_list, time_list,Math, IRMS, VRMS,screenshot