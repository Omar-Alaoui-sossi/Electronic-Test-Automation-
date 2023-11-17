import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import threading as th
import datetime
from tabulate import tabulate
import Instruments


def connected_inst():
    """
    This function detects the connected instruments to your PC
    """
    connected_instruments = Instruments.ctg()
    connected_instruments.categorize_instruments()


def set_multimeter_mode(multimeter, mode):
    """
    Set the measurement mode of a multimeter.

    Args:
        multimeter: The multimeter instance to set the mode for.
        mode (str): The measurement mode to set. 'A' for Amperemeter mode, 'V' for Voltmeter mode.

    Returns:
        None

    Raises:
        ValueError: If an invalid mode is selected.

    """

    if mode == "A":
        multimeter.set_mode_A()  # Select the current measurement mode
    elif mode == "V":
        multimeter.set_mode_V()  # Select the voltage measurement mode
    else:
        print(
            "Invalid mode selected. Please choose 'A' for Amperemeter or 'V' for Voltmeter."
        )


def divide_dataframe(df, num_rows):
    """
    Function to divide a DataFrame by selecting a specific number of rows for each smaller DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame.
        num_rows (int): The number of rows for each smaller DataFrame.

    Returns:
        A list of smaller DataFrames.
    """
    divided_dfs = []
    total_rows = len(df)
    num_divisions = int(total_rows / num_rows)

    for i in range(num_divisions):
        start_idx = i * num_rows
        end_idx = (i + 1) * num_rows
        sub_df = df[start_idx:end_idx]
        divided_dfs.append(sub_df)

    remaining_rows = total_rows % num_rows
    if remaining_rows != 0:
        last_df = df[-remaining_rows:]
        divided_dfs.append(last_df)

    return divided_dfs


def plot_line_plots(df, x_col, y_cols, plot_name):
    """
    Function to generate line plots for multiple columns in a DataFrame.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        x_col (str): The name of the column to be used for the x-axis.
        y_cols (list): A list of column names to be plotted on the y-axis.

    Returns:
        None (displays the plot)

    """
    sns.set_theme(style="darkgrid")
    plt.figure(figsize=(8, 6))

    for y_col in y_cols:
        sns.lineplot(data=df, x=x_col, y=y_col, label=y_col)

    plt.xlabel(x_col)
    plt.ylabel("Values")
    plt.title("Line Plots")

    plt.legend()
    plt.savefig(plot_name)


current_datetime = datetime.datetime.now()
data = [
    [
        "Date",
        "DUT_name",
        "Refrence",
        "V Bus (V)",
        "I Bus (A)",
        "Frequency (Hz)",
        "Idd (A)",
        "Vdd (V)",
        "Icc (A)",
        "Vcc (V)",
        "ILv (A)",
        "Power Secteur (W)",
        "Power Vbus (W)",
        "Power HV (W)",
        "Power LV (W)",
        "Efficency HV",
        "Efficency LV",
        "Efficency Before Rectifier",
        "Efficency After Rectifier",
        "Power Loss",
        "Timestamp",
    ]
]


########## DISPLAY ##############

connected_inst()
DUT_name = input("Enter the name of your DUT : ")
Ref = input("Enter the Reference of your DUT : ")
print("-------------------------------------------")
print(
    "Please copy the addresses from the table above and paste them into the appropriate location . "
)
Ac_source_address = input("Enter the Address of your AC Source :  ")
Ac_source = Instruments.chroma(Ac_source_address.strip())
osc_address = input("Enter the Address key of your oscilloscope  :  ")
load_address = input("Enter the Address key of your Electronic Load :  ")
electronic_load = Instruments.load(load_address.strip())
Multimeter_adrr = input("Enter the Address of your Multimeter :  ")
Multimeter = Instruments.multi(Multimeter_adrr.strip())

mode_1 = input(
    "Choose the mode for Multimeter 1 (A for Amperemeter, V for Voltmeter): "
)
set_multimeter_mode(Multimeter, mode_1)


print("-------------------------------------------")
current_steps = []  # Empty list to store row values

"""
Enter the parameters of each instrument 
evrything is detailed while the code is executed make sure to read every line printed in the console 
"""

nb_values = int(input("Enter the number of current sample values you desire : "))

# Loop through each column
for j in range(nb_values):
    value = float(input(f"Enter value number {j+1} (A): "))
    current_steps.append(value)  # Append value to the row list

print("-------------------------------------------")
print(" Enter Parameters for the Current Range (A) :  ")
curr_start = float(input("The start point (A) : "))
curr_end = float(input("The end point (A) : "))
curr_step = float(input("The step  (A) :  "))
desired_length = len(np.arange(curr_start, curr_end, curr_step))
Idd_1 = np.arange(curr_start, curr_end, curr_step)
print("-------------------------------------------")
print("Precise the Channels of your Signals")
print(
    "NOTE : Write CH in capital letters then the number of the channel ----> Example : CH1"
)
ch1 = input("Enter the Corresponding Channel for your IAC  : ")
ch2 = input("Enter the Corresponding Channel for your VAC  : ")
ch3 = input("Enter the Corresponding Channel for your IBus : ")
ch4 = input("Enter the Corresponding Channel for your VBus : ")


print("-------------------------------------------")
print("Enter the AC or DC source Parameters  ")
freq = float(input("Enter the desired Frequency (Hz): "))
amplitude = float(input("Enter The amplitude of the signal (V) : "))
print("-------------------------------------------")
print("Dont Touch Anything the Test is Running")
print("-------------------------------------------")


def thread_Curr_step_function_Icc():
    """
    Perform current step setting for Icc measurement.

    This function sets the current step for Icc measurement using the electronic load.

    Global variables:
    - Vcc: Stores the result of the voltage measurement.
    - Icc: Stores the result of the current step setting for Icc measurement.
    - Ilv : Stores the result of the output current of the low voltage block

    Args
        :param: None

    Returns:
        None
    """
    global Vdd, Icc, ILv
    Vdd, Icc, ILv = electronic_load.set_current_steps_PE(
        current_steps, "2", Multimeter_adrr, desired_length
    )


def thread_Curr_range_function_Idd():
    """
    Perform current range setting for Icc measurement.

    This function sets the current range for Icc measurement using the electronic load.

    Global variables:
    - Vdd: Stores the result of the voltage measurement.
    - Idd: Stores the result of the current range setting for Icc measurement.
    - time_list: Stores the list of timestamps during the measurement.


    Args
        :param: None

    Returns:
        None
    """
    global Vcc, Idd, time_list, Iac, Ibus, Vbus, Psector
    (
        Vcc,
        Idd,
        time_list,
        Iac,
        Ibus,
        Vbus,
        Psector,
    ) = electronic_load.set_current_range_PE(
        curr_start,
        curr_end,
        curr_step,
        "1",
        osc_address.strip(),
        nb_values,
        ch1,
        ch2,
        ch3,
        ch4,
    )


electronic_load.disable_input("1")
electronic_load.disable_input("2")
electronic_load.set_range_low("1")
electronic_load.set_range_low("2")

Ac_source.set_output_off()
Ac_source.set_frequency(freq)


time.sleep(5)

"""
setting up the load on CC current MODE 
"""

electronic_load.set_mode("CC", "1")
electronic_load.set_mode("CC", "2")

time.sleep(2)
"""
Set up of the current limitation calibre 
"""
Ac_source.set_voltage_AC(amplitude)
Ac_source.set_output_on()
time.sleep(30)

Task_1 = th.Thread(target=thread_Curr_step_function_Icc)
Task_2 = th.Thread(target=thread_Curr_range_function_Idd)

Task_1.start()
Task_2.start()
Task_1.join()
Task_2.join()

Ac_source.set_output_off()
electronic_load.disable_input("1")
electronic_load.disable_input("2")


def generate_data(data_frame, Vbus, Ibus, Idd, Vdd, Icc, Vcc, I_Lv, P_sec, Time_):
    """
    this function  fills  the empy table decalred earlier with the assingned measurments

    Args :
        :param data_frame : List
        :param Idd :float
        :param Vdd : float
        :param Icc :float
        :param Vcc :float
        :param I_Lv :float
        :param P_sec :float
        :param Time_ :str


    Return :
        data_frame : List
    """
    current_datetime = datetime.datetime.now()
    for i in range(len(Vcc)):
        new_line = [
            current_datetime.date(),  # Date (filled automatically)
            DUT_name,  # DUT_name (fixed value)
            Ref,  # Reference
            Vbus[i],  # DC voltage
            Ibus[i],
            freq,  # Chroma frequency
            Idd[i],  # Idd_variable (scalar value assigned directly)
            Vdd[i],  # Icc_fixed
            Icc[i],  # Vdd
            Vcc[i],  # Vcc
            I_Lv[i],
            P_sec[i],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            Time_[i],  # Timestamp (filled automatically)
        ]
        data_frame.append(new_line)

    return data_frame


data = generate_data(data, Vbus, Ibus, Idd, Vdd, Icc, Vcc, ILv, Psector, time_list)
df = pd.DataFrame(data[1:], columns=data[0])

# the following formulas are calculating powers and efficency

df["Power Vbus (W)"] = df["V Bus (V)"] * df["I Bus (A)"]
df["Power HV (W)"] = df["Vcc (V)"] * (df["Icc (A)"] + df["ILv (A)"])
df["Power LV (W)"] = df["Vdd (V)"] * df["Idd (A)"]
df["Efficency HV"] = df["Power HV (W)"] / df["Power LV (W)"]
df["Efficency LV"] = df["Power HV (W)"] / (df["Vcc (V)"] * df["ILv (A)"])
df["Efficency Before Rectifier"] = (
    (df["Vcc (V)"] * df["Icc (A)"]) + df["Power LV (W)"]
) / df["Power Secteur (W)"]
df["Efficency After Rectifier"] = (
    (df["Vcc (V)"] * df["Icc (A)"]) + df["Power LV (W)"]
) / df["Power Vbus (W)"]
df["Power Loss"] = df["Power Secteur (W)"] - df["Power Vbus (W)"]

# since the data frame has multiple instances of Idd we will divide the df by the lenght of one istance Idd
# all this in order to have multiple plots one for each step of Icc
divisions = divide_dataframe(df, desired_length)
division_variables = [f"division_{i+1}" for i in range(len(divisions))]
for i, division in enumerate(divisions):
    date_str = time.strftime("%Y-%m-%d_%H%M")
    plot_name = f"PE_plot_{i}_{date_str}.png"
    globals()[division_variables[i]] = division
    plot_line_plots(
        globals()[division_variables[i]],
        "Idd (A)",
        [
            "Efficency HV",
            "Efficency LV",
            "Efficency Before Rectifier",
            "Efficency After Rectifier",
        ],
        plot_name,
    )

decimal_precision = 3
columns_to_convert = [
    "Efficency HV",
    "Efficency LV",
    "Efficency Before Rectifier",
    "Efficency After Rectifier",
]
# Convert the efficencies colulns to percentages
df[columns_to_convert] = df[columns_to_convert].apply(
    lambda x: x.apply(lambda y: "{:.{}f}%".format(y * 100, decimal_precision))
)

# saving the data as an excel sheet
dateString = time.strftime("%Y-%m-%d_%H%M")
file_name = f"{dateString}_Power_Efficency.xlsx"
df.to_excel(file_name)

# Switch the dataframe to a list in order to plot it in the console
data = [df.columns.tolist()] + df.values.tolist()
print("\n")
print(tabulate(data, headers="firstrow", tablefmt="fancy_grid"))
print("\n")
