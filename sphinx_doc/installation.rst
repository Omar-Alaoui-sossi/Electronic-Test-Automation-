
.. admonition:: Important

    To use this project, you have to read the installation and System requirements .It is necessary to download all the python libraries and Drivers before the launching

Operating System Requirements
--------------------------------------------
- Windows: Windows 7 or higher
- macOS: macOS 10.10 or higher
- Linux: Any modern distribution

Python Requirements
--------------------------------------------
- Python 3.x: Install Python from the Microsoft Store. You can find Python in the Microsoft Store by following these steps:

   1. Open the Microsoft Store application on your computer.
   2. Search for "Python" in the search bar.
   3. Select the Python version you prefer (e.g., Python 3.9).
   4. Click on the "Get" or "Install" button to download and install Python from the Microsoft Store.

   Installing Python from the Microsoft Store ensures an easy and hassle-free installation process.


Command-Line Interface
--------------------------------------------
To execute commands, you need to have a command-line interface such as:

- Windows: Command Prompt or Powernone
- macOS: Terminal
- Linux: Terminal

Python Libraries
--------------------------------------------

The project relies on the following Python libraries:

PyVISA
~~~~~~~
- Description: PyVISA provides a Python API for accessing resources (such as instruments) connected to the computer.
- Installation command:

  .. code-block:: none

     pip install pyvisa

Numpy
~~~~~~~
- Description: NumPy is a fundamental library for scientific computing with Python. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions.
- Installation command:

  .. code-block:: none

     pip install numpy

Pandas
~~~~~~~
- Description: Pandas is a powerful library for data manipulation and analysis. It provides data structures and functions to efficiently handle and process structured data.
- Installation command:

  .. code-block:: none

     pip install pandas

Seaborn
~~~~~~~~~
- Description: Seaborn is a data visualization library built on top of Matplotlib. It provides a high-level interface for creating informative and attractive statistical graphics.
- Installation command:

  .. code-block:: none

     pip install seaborn

Matplotlib
~~~~~~~~~~~
- Description: Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python. It provides a wide range of plotting functions and customization options.
- Installation command:

  .. code-block:: none

     pip install matplotlib

Tabulate
~~~~~~~~~~~
- Description: Tabulate is a simple library for creating formatted tables in plain text, Markdown, or HTML. It is useful for displaying tabular data in a readable and structured format.
- Installation command:

  .. code-block:: none

     pip install tabulate

Datetime
~~~~~~~~~
- Description: The datetime module supplies classes for working with dates, times, and time intervals. It allows you to manipulate, format, and perform calculations on dates and times.

Threading
~~~~~~~~~~~
- Description: The threading module provides a high-level interface for creating and managing threads in Python. It allows you to run multiple threads concurrently, enabling efficient parallel execution.

To install each library, open your command-line interface and run the corresponding `pip install` command.


Drivers
--------------------------------------------

.. admonition:: Note
  
      For certain functionalities, you may need to install specific drivers. In this project, we use the following drivers:
      Make sure to install the appropriate driver version for your operating system.
      After installing the required libraries and drivers, you're ready to use the project.


NI VISA
~~~~~~~
- Description: NI VISA (Virtual Instrument Software Architecture) is a software interface used to communicate with and control instruments such as oscilloscopes, signal generators, and multimeters.
  - Download the NI VISA driver from the following link:
    `Download NI VISA driver <https://www.ni.com/fr-fr/support/downloads/drivers/download.ni-visa.html#460225>`_
  - Importance: The NI VISA driver is crucial for establishing communication with the instruments and is essential for running the tests in this project.

NI 488
~~~~~~~~
- Description: NI 488 is a software and hardware package that provides high-level programming functions for controlling GPIB (General Purpose Interface Bus) devices. It allows communication with instruments connected via GPIB.
  - Download the NI 488 driver from the following link:
    `Download NI 488 driver <https://www.ni.com/fr-fr/support/downloads/drivers/download.ni-488-2.html#467646>`_
  - Importance: The NI 488 driver is necessary for GPIB communication and is vital for the proper functioning of the tests in this project.


