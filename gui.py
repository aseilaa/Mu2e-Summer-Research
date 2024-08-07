#Aseila Awad
import sys
import signal
import socket
import time
import os
import struct
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QTableWidget, QMainWindow, QWidget, QTableWidgetItem,
    QVBoxLayout, QTabWidget, QHeaderView
)
from PyQt5.QtCore import QThread, pyqtSignal

os.environ["DISPLAY"] = ':0'
background_color = 'background-color: white;'
button_color = 'background-color: lightgray;'

def bitstring_to_bytes(s):
    """Convert a bitstring 's' to bytes."""
    return int(s, 2).to_bytes(4, byteorder='big')

def process_float(byte_seq):
    """Convert a byte sequence to a float value."""
    if len(byte_seq) != 4:
        return None
    try:
        return struct.unpack('>f', byte_seq)[0]
    except struct.error as e:
        print(f"Error unpacking bytes to float: {e}")
        return None

class DataFetcher(QThread):
    """Thread for fetching data from a socket and emitting signals with the fetched data."""

    data_fetched = pyqtSignal(list, list, list, list, list, list, list)

    def __init__(self):
        """Initialize the DataFetcher thread."""
        super().__init__()
        self.command_dict = {}  # Initialize the command dictionary attribute
        self.load_commands()    # Load commands into the dictionary
        self.sock = self.create_socket() # Create and connect the socket

    def create_socket(self):
        """Create a socket and connect to a server."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 631)) # Connect to the server at localhost on port 631
            return sock
        except Exception as e:
            print(f"Socket connection failed: {e}")
            return None

    def load_commands(self):
        """Load commands from a file (e.g., commands.h) into a dictionary."""
        try:
            with open("commands.h", "r") as file:
                pre_command_list = [line.split() for line in file if line.strip()]
                self.command_dict = {i[1]: format(int(i[2]), '032b') for i in pre_command_list}
        except FileNotFoundError:
            print("commands.h not found. Please check the file path.")
        except Exception as e:
            print(f"Error loading commands: {e}")

    def run(self):
        """Run the thread to continuously fetch data."""
        while True:
            if self.sock:
                try:
                    # Initialize lists for different types of data
                    hv_v = [0] * 12
                    hv_i = [0] * 12
                    v48 = [0] * 6
                    i48 = [0] * 6
                    v6 = [0] * 6
                    i6 = [0] * 6
                    T48 = [0] * 6

                    # Send commands to the server and receive data
                    self.send_command("COMMAND_get_vhv", hv_v)
                    self.send_command("COMMAND_get_ihv", hv_i)
                    self.send_command("COMMAND_readMonV48", v48)
                    self.send_command("COMMAND_readMonI48", i48)
                    self.send_command("COMMAND_readMonV6", v6)
                    self.send_command("COMMAND_readMonI6", i6)

                    # Emit signal with the fetched data
                    self.data_fetched.emit(hv_v, hv_i, v48, i48, v6, i6, T48)
                    time.sleep(1)  # Adjust the sleep time as needed
                except Exception as e:
                    print(f"Data fetching error: {e}")
                    self.data_fetched.emit([0] * 12, [0] * 12, [0] * 6, [0] * 6, [0] * 6, [0] * 6, [0] * 6)
            else:
                time.sleep(1)  # Wait before trying to reconnect
                self.sock = self.create_socket()  # Try to reconnect

    def send_command(self, command_key, data_list):
        """Send a command to the server and populate 'data_list' with the response."""
        if not self.sock:
            return
        command = self.command_dict.get(command_key)
        if not command:
            print(f"Command {command_key} not found in the command dictionary.")
            return
        try:
            self.sock.sendall(bitstring_to_bytes(command))
            response = self.sock.recv(1024)  # Adjust buffer size as needed
            if response:
                # Process the response into data_list
                data_list[:] = [process_float(response[i:i+4]) for i in range(0, len(response), 4)]
        except Exception as e:
            print(f"Failed to send command {command_key}: {e}")

class Window(QMainWindow):
    """Main window class for the LVHV GUI."""

    def __init__(self):
        """Initialize the main window."""
        super(Window, self).__init__()

        # Initialize data lists
        self.v48 = [0] * 6
        self.i48 = [0] * 6
        self.v6 = [0] * 6
        self.i6 = [0] * 6
        self.T48 = [0] * 6
        self.hv_v = [0] * 12
        self.hv_i = [0] * 12

        self.setWindowTitle("LVHV GUI")
        self.setStyleSheet(background_color)

        self.display_setup() # Setup the GUI layout and widgets
        self.load_commands() # Load commands from file

        # Start the data fetching thread
        self.data_fetcher = DataFetcher()
        self.data_fetcher.data_fetched.connect(self.update_data)
        self.data_fetcher.start()  # Start data fetching thread

        self.show()

    def update_data(self, hv_v, hv_i, v48, i48, v6, i6, T48):
        """Update the GUI with fetched data."""
        self.hv_v = hv_v
        self.hv_i = hv_i
        self.v48 = v48
        self.i48 = i48
        self.v6 = v6
        self.i6 = i6
        self.T48 = T48

        # Update the tables with the new data
        for i in range(6):
            self.lv_table.setItem(i, 0, QTableWidgetItem(str(self.v48[i])))
            self.lv_table.setItem(i, 1, QTableWidgetItem(str(self.i48[i])))
            self.lv_table.setItem(i, 2, QTableWidgetItem(str(self.T48[i])))

            self.six_lv_table.setItem(i, 0, QTableWidgetItem(str(self.v6[i])))
            self.six_lv_table.setItem(i, 1, QTableWidgetItem(str(self.i6[i])))

        for i in range(12):
            self.hv_table.setItem(i, 0, QTableWidgetItem(str(self.hv_v[i])))
            self.hv_table.setItem(i, 1, QTableWidgetItem(str(self.hv_i[i])))

    def load_commands(self):
        """Load commands from a file (e.g., commands.h) into a dictionary."""
        try:
            with open("commands.h", "r") as file:
                pre_command_list = [line.split() for line in file if line.strip()]
                self.command_dict = {i[1]: format(int(i[2]), '032b') for i in pre_command_list}
        except FileNotFoundError:
            print("commands.h not found. Please check the file path.")
        except Exception as e:
            print(f"Error loading commands: {e}")

    def display_setup(self):
        """Setup the main GUI layout and widgets."""
        self.all_display = QWidget()
        self.setCentralWidget(self.all_display)

        main_layout = QVBoxLayout(self.all_display)

        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # Setup 48V LV tab
        lv_widget = QWidget()
        lv_layout = QVBoxLayout(lv_widget)
        self.lv_table = QTableWidget(6, 3)
        self.lv_table.setVerticalHeaderLabels([f"Ch {i}" for i in range(6)])
        self.lv_table.setHorizontalHeaderLabels(["Voltage (V)", "Current (A)", "Temp (C)"])
        self.lv_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Stretch columns to fill the table width
        lv_layout.addWidget(self.lv_table)
        tab_widget.addTab(lv_widget, "48V LV")

        # Setup 6V LV tab
        six_lv_widget = QWidget()
        six_lv_layout = QVBoxLayout(six_lv_widget)
        self.six_lv_table = QTableWidget(6, 2)
        self.six_lv_table.setVerticalHeaderLabels([f"Ch {i}" for i in range(6)])
        self.six_lv_table.setHorizontalHeaderLabels(["Voltage (V)", "Current (A)"])
        self.six_lv_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        six_lv_layout.addWidget(self.six_lv_table)
        tab_widget.addTab(six_lv_widget, "6V LV")

        # Setup HV tab
        hv_widget = QWidget()
        hv_layout = QVBoxLayout(hv_widget)
        self.hv_table = QTableWidget(12, 2)
        self.hv_table.setVerticalHeaderLabels([f"Ch {i}" for i in range(12)])
        self.hv_table.setHorizontalHeaderLabels(["Voltage (V)", "Current (A)"])
        self.hv_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        hv_layout.addWidget(self.hv_table)
        tab_widget.addTab(hv_widget, "HV")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


