__author__ = "Omar ALAOUI SOSSI "
import pyvisa
from tabulate import tabulate
import os


class ConnectedInstruments:
    """
    Class for categorizing connected instruments.
    this code is creating a usable class that executes intrument detection and identification
    so all the instruments connected will be displace in a table format with their appropriate name and address
    """

    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.inst_addresses = self.rm.list_resources()
        usb_resources = [
            resource for resource in self.inst_addresses if resource.startswith("USB")
        ]
        gpib_resources = [
            resource for resource in self.inst_addresses if resource.startswith("GPIB")
        ]
        self.all_resources = usb_resources + gpib_resources
        self.table = [["Instrument Serie", "Instrument Address"]]

    def categorize_instruments(self):
        """
        Categorize and display the connected instruments.
        """
        if len(self.all_resources) == 0:
            print("\n")
            print(
                "----------------------------------- No USB or GPIB devices are connected -----------------------------------"
            )
            print("\n")
            os._exit(0)
        else:
            print("\n")
            print(
                "-------------------------------------- List of connected instruments --------------------------------------"
            )

        for address in self.all_resources:
            instr = self.rm.open_resource(address)
            id = instr.query("*IDN?")
            data = [id, address]
            self.table.append(data)
        print(tabulate(self.table, headers="firstrow", tablefmt="fancy_grid"))
