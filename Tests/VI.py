import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import threading as th
import datetime
from tabulate import tabulate
import Instruments


"""
Since i made Classes for each instrument i am going to use 
i need just to call the library and make and instance of the class 
"""
connected_instruments = Instruments.ctg()
connected_instruments.categorize_instruments()
"""
Declaration of a bunch of list that the code will fill later on 
"""

signal = []
thread_result_volt_1 = []
thread_result_curr_range_Idd = []
thread_result_volt_2 = []
thread_result_curr_step_Icc = []
thread_result_curr_step_Idd = []
thread_result_volt_3 = []
thread_result_volt_4 = []

print("-------------------------------------------")

"""
all the following are test parametres that you need to fill when running the script 
"""

DUT_name = input("Enter the name of your DUT : ")
Ref = input("Enter the Reference of your DUT : ")

"""
Two empty tables will only the header column with appropriate name 
"""

data_case_1 = [
    [
        "Date",
        "DUT_name",
        "Refrence ",
        "DC voltage (V)",
        " Frequency (Hz)",
        "T°",
        "Idd (A)",
        "Icc (A)",
        "Vdd (V)",
        "Vcc (V)",
        "Timestamp",
    ]
]
data_case_2 = [
    [
        "Date",
        "DUT_name",
        "Refrence",
        "DC voltage (V)",
        " Frequency (Hz)",
        "T°",
        "Idd (A)",
        "Icc (A)",
        "Vdd (V)",
        "Vcc (V)",
        "Timestamp",
    ]
]

current_datetime = datetime.datetime.now()

"""
Same as before I made instances of the instruments i will use 
in this case chroma oscillo and electronic load 
Enter the addresses of the instruments listed in your terminal 
"""

print("-------------------------------------------")
print(
    "Please copy the addresses from the table above and paste them into the appropriate location . "
)
Dc_source_address = input("Enter the Address of your DC or AC Source :  ")
Dc_source = Instruments.chroma(Dc_source_address.strip())
osc_address = input("Enter the Address key of your oscilloscope  :  ")
load_address = input("Enter the Address key of your Electronic Load :  ")
electronic_load = Instruments.load(load_address.strip())

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

delay = 3

print("-------------------------------------------")
print(" Enter Parameters for the Current Range (A) :  ")
curr_start = float(input("The start point (A) : "))
curr_end = float(input("The end point (A) : "))
curr_step = float(input("The step  (A) :  "))


desired_length = len(np.arange(curr_start, curr_end, curr_step))


print("-------------------------------------------")
print("Enter the AC or DC source Parameters  ")
freq = float(input("Enter the desired Frequency (Hz): "))
evolution_time = float(input("Enter The Rising time of the signal (seconds): "))
amplitude = float(input("Enter The amplitude of the signal (V) :  "))
print(
    f"NOTE : the next parameter is the duration of the DC source signal it must be minimum {desired_length*nb_values*30} seconds "
)
duration = float(input("Enter The duration of the signal in seconds : "))
# high_time               = duration - (4 * evolution_time)
print("-------------------------------------------")
print("Dont Touch Anything the Test is Running")
print("-------------------------------------------")
print(f"The Chroma signal will go down automatically in {duration} seconds ")

"""
setting up some Parameters before starting the actual test 
all the function I made have some very significant name so they really do what they are named for  
"""

electronic_load.disable_input("1")
electronic_load.disable_input("2")
Dc_source.set_output_off()
Dc_source.set_frequency(freq)


time.sleep(2)


"""
setting up the load on CC current MODE 
"""

electronic_load.set_mode("CC", "1")
electronic_load.set_mode("CC", "2")

time.sleep(2)
"""
Set up of the current limitation calibre 
"""
electronic_load.set_curr_limitation(612e-3, "1")
electronic_load.set_curr_limitation(612e-3, "2")
electronic_load.set_range_low("1")
electronic_load.set_range_low("2")


"""
In the following section I make some multiprocessing using threading python library
since i need to do multiple task simultanseouly i need to used threading in this case 
i need to use 2 chanels of the electronic load because i will change the value of 2 variables Icc and Idd
i need also to have an order of sequences so the measurments will get took at time 
so it starts with threads function so i can always have access to the return values via globla variables  
"""


def thread_Curr_range_function_Idd():
    """
    Perform current range setting for Idd measurement.

    This function sets the current range for Idd measurement using the electronic load.

    Global variables:
    - thread_result_volt_1: Stores the result of the voltage measurement.
    - thread_result_curr_range_Idd: Stores the result of the current range setting for Idd measurement.
    - time_list_1: Stores the list of timestamps during the measurement.
    - time_diff_1: Stores the time differences between consecutive timestamps.

    Args
        :param: None

    Returns:
        None
    """
    global thread_result_volt_1, thread_result_curr_range_Idd, time_list_1
    (
        thread_result_volt_1,
        thread_result_curr_range_Idd,
        time_list_1,
    ) = electronic_load.set_current_range_VI(
        curr_start, curr_end, curr_step, "1", nb_values
    )


def thread_Curr_step_function_Icc():
    """
    Perform current step setting for Icc measurement.

    This function sets the current step for Icc measurement using the electronic load.

    Global variables:
    - thread_result_volt_2: Stores the result of the voltage measurement.
    - thread_result_curr_step_Icc: Stores the result of the current step setting for Icc measurement.

    Args
        :param: None

    Returns:
        None
    """
    global thread_result_volt_2, thread_result_curr_step_Icc
    (
        thread_result_volt_2,
        thread_result_curr_step_Icc,
    ) = electronic_load.set_current_steps_VI(
        current_steps, "2", osc_address.strip(), desired_length
    )


def thread_Curr_range_function_Icc():
    """
    Perform current range setting for Icc measurement.

    This function sets the current range for Icc measurement using the electronic load.

    Global variables:
    - thread_result_volt_3: Stores the result of the voltage measurement.
    - thread_result_curr_range_Icc: Stores the result of the current range setting for Icc measurement.
    - time_list_2: Stores the list of timestamps during the measurement.
    - time_diff_2: Stores the time differences between consecutive timestamps.

    Args
        :param: None

    Returns:
        None
    """
    global thread_result_volt_3, thread_result_curr_range_Icc, time_list_2
    (
        thread_result_volt_3,
        thread_result_curr_range_Icc,
        time_list_2,
    ) = electronic_load.set_current_range_VI(
        curr_start, curr_end, curr_step, "2", nb_values
    )


def thread_chroma():
    """
    Perform Chroma operation.

    This function performs the desired operation using the Chroma device.

    Global variables:
    - signal: Stores the result of the Chroma operation.

    Args
        :param: None

    Returns:
        None
    """
    global signal
    signal = Dc_source.generate_trapezoidal_signal(duration, evolution_time, amplitude)


def thread_Curr_step_function_Idd():
    """
    Perform current step setting for Idd measurement.

    This function sets the current step for Idd measurement using the electronic load.

    Global variables:
    - thread_result_volt_4: Stores the result of the voltage measurement.
    - thread_result_curr_step_Idd: Stores the result of the current step setting for Idd measurement.

    Args
        :param: None

    Returns:
        None
    """
    global thread_result_volt_4, thread_result_curr_step_Idd
    (
        thread_result_volt_4,
        thread_result_curr_step_Idd,
    ) = electronic_load.set_current_steps_VI(
        current_steps, "1", osc_address.strip(), desired_length
    )


"""
Threads creation and Tasks monitoing  
"""

Task_0 = th.Thread(target=thread_chroma)
Task_1 = th.Thread(target=thread_Curr_step_function_Icc)
Task_2 = th.Thread(target=thread_Curr_range_function_Idd)
Task_3 = th.Thread(target=thread_Curr_range_function_Icc)
Task_4 = th.Thread(target=thread_Curr_step_function_Idd)

"""
Starting the threads in the right ordr is key and join methode is to stop them so wheneveer you see a join() methode
it means that since the thread is not finished the code will not execute the rest of the lines and this is 
the importance of threading is that y control sequences and synchronization
"""

Task_0.start()
time.sleep(15)
Task_1.start()
Task_2.start()
Task_1.join()
Task_2.join()
time.sleep(2)
Task_3.start()
Task_4.start()
Task_3.join()
Task_4.join()
time.sleep(2)
Task_0.join()
time.sleep(3)

"""
after finishing the test we are disabling all the outputs on our instruments 
"""

electronic_load.disable_input("1")
electronic_load.disable_input("2")
Dc_source.set_output_off()

"""
the following section is related to data processing and visualization
"""

"""
we made this function to fill the tables we made in the begging 
it will be filled by the values taken out of the instruments  
"""


def generate_data(data_frame, Vcc, Vdd, Icc, Idd, Time_):
    """
    this function  fills  the empy tables decalred earlier with assingned measurments

    Args :
        :param data_frame : List
        :param VCC :float
        :param Vdd : float
        :param Icc :float
        :param Idd :float
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
            amplitude,  # DC voltage
            freq,  # Chroma frequency
            "",  # T°
            Idd[i],  # Idd_variable (scalar value assigned directly)
            Icc[i],  # Icc_fixed
            Vdd[i],  # Vdd
            Vcc[i],  # Vcc
            Time_[i],  # Timestamp (filled automatically)
        ]
        data_frame.append(new_line)

    return data_frame


data_case_1 = generate_data(
    data_case_1,
    thread_result_volt_1,
    thread_result_volt_2,
    thread_result_curr_range_Idd,
    thread_result_curr_step_Icc,
    time_list_1,
)
data_case_2 = generate_data(
    data_case_2,
    thread_result_volt_4,
    thread_result_volt_3,
    thread_result_curr_step_Idd,
    thread_result_curr_range_Icc,
    time_list_2,
)

"""
Print the updated table on the console 
"""
print(
    "--------------------------------------  Case 1 : Fixed Idd , Variable Icc -------------------------------------- "
)
print(tabulate(data_case_1, headers="firstrow", tablefmt="fancy_grid"))
print("\n")
print(
    "--------------------------------------  Case 2 : Fixed Icc , Variable Idd -------------------------------------- "
)
print(tabulate(data_case_2, headers="firstrow", tablefmt="fancy_grid"))
print("\n")

"""
saving the data in excel format , the name will start by case 1 or 2 
and the date and time when the files in generated in order to make it easy to track and store 
"""

df1 = pd.DataFrame(data_case_1[1:], columns=data_case_1[0])
df2 = pd.DataFrame(data_case_2[1:], columns=data_case_2[0])
dateString = time.strftime("%Y-%m-%d_%H%M")
file_name = f"{dateString}_V_characteristic.xlsx"
df1.to_excel("case_1_" + file_name)
df2.to_excel("case_2_" + file_name)

"""
Declaring some thresholds that gonna be used in the ploting part to detect the volatge values bellow them 
"""
Vcc_threshold = 0.96 * 12
Vdd_threshold = 0.96 * 3.3

"""
this fuction will highlith tha part of the graph that are bellow the threshold
by drowing red lines one those points 
"""


def plot_below_threshold(points, threshold, label):
    """
    theis function highlights the portion of the graph that are bellow threshold

    Args :
        :param points : List
        :param threshold : float
        :param label : str
    """
    if below_threshold_points := [
        point for point in points if 0 < point[1] < threshold
    ]:
        plt.scatter(*zip(*below_threshold_points), color="red", label="Below Threshold")
        plt.legend()
        print(
            f"The trigger point for {label} is: {below_threshold_points[0][0]:.6f} A, {below_threshold_points[0][1]:.6f} V"
        )

    else:
        print("No points below the threshold.")


print("-------------------------------------------")
print(
    "Save the Graphs that will be displayed in a second if they seem relevant to you "
)


"""
Plotting part 
"""

# Create separate plots for each subplot
sns.set_theme(style="darkgrid")

# Plot 1: Vdd with fixed Idd & variable Icc
plt.figure(figsize=(8, 6))
sns.lineplot(data=df1, x="Icc (A)", y="Vdd (V)", hue="Idd (A)")
plt.xlabel("Icc")
plt.ylabel("Vdd")
plt.title("Vdd with fixed Idd & variable Icc")
below_threshold_points_1 = list(zip(df1["Icc (A)"], df1["Vdd (V)"]))
plot_below_threshold(below_threshold_points_1, Vdd_threshold, "Vdd(Icc)")
plt.show()

# Plot 2: Vdd fixed Icc & variable Idd
plt.figure(figsize=(8, 6))
sns.lineplot(data=df2, x="Idd (A)", y="Vdd (V)", hue="Icc (A)")
plt.xlabel("Idd")
plt.ylabel("Vdd")
plt.title("Vdd with fixed Icc & variable Idd")
below_threshold_points_2 = list(zip(df2["Idd (A)"], df2["Vdd (V)"]))
plot_below_threshold(below_threshold_points_2, Vdd_threshold, "Vdd(Idd)")
plt.show()

# Plot 3: Vcc with fixed Idd & variable Icc
plt.figure(figsize=(8, 6))
sns.lineplot(data=df1, x="Icc (A)", y="Vcc (V)", hue="Idd (A)")
plt.xlabel("Icc")
plt.ylabel("Vcc")
plt.title("Vcc with fixed Idd & variable Icc")
below_threshold_points_3 = list(zip(df1["Icc (A)"], df1["Vcc (V)"]))
plot_below_threshold(below_threshold_points_3, Vcc_threshold, "Vcc(Icc)")
plt.show()

# Plot 4: Vcc with fixed Icc & variable Idd
plt.figure(figsize=(8, 6))
sns.lineplot(data=df2, x="Idd (A)", y="Vcc (V)", hue="Icc (A)")
plt.xlabel("Idd")
plt.ylabel("Vcc")
plt.title("Vcc with fixed Icc & variable Idd")
below_threshold_points_4 = list(zip(df2["Idd (A)"], df2["Vcc (V)"]))
plot_below_threshold(below_threshold_points_4, Vdd_threshold, "Vcc(Idd)")
plt.show()

# Plot 5: Chroma's DC Source
plt.figure(figsize=(8, 6))
time_axis = np.linspace(0, duration, len(signal))
sns.lineplot(x=time_axis, y=signal)
plt.xlabel("Time")
plt.ylabel("DC Voltage")
plt.title("Chroma's DC Source")
plt.show()

print("-------------------------------------------")
print(
    "Test completed without errors !!!! \nCheck the results saved in your directory . "
)
