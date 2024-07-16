import sys
import signal
import socket
import time
import os
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QTableWidget,
    QLabel,
    QMainWindow,
    QWidget,
    QTableWidgetItem
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt

os.environ["DISPLAY"] = ':0'
background_color = 'background-color: white;'
button_color = 'background-color: white;'

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(4, byteorder='big')

def process_float(input):
    if len(input) < 4:
        return None

    v = format(input[3], '08b') + format(input[2], '08b') + format(input[1], '08b') + format(input[0], '08b')
    sign = (-1) ** int(v[0], 2)
    exponent = int(v[1:9], 2) - 127
    mantissa = int(v[9:], 2)
    return sign * (1 + mantissa * (2 ** -23)) * (2 ** exponent)

class DataFetcher(QThread):
    data_fetched = pyqtSignal(list, list, list, list, list, list, list, list)

    def __init__(self):
        super().__init__()
        self.sock = self.create_socket()

    def create_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 631))
            return sock
        except Exception as e:
            print(f"Socket connection failed: {e}")
            return None

    def run(self):
        while True:
            if self.sock:
                try:
                    # Replace with actual fetching logic
                    hv_v = [0] * 12
                    hv_i = [0] * 12
                    v48 = [0] * 6
                    i48 = [0] * 6
                    v6 = [0] * 6
                    i6 = [0] * 6
                    T48 = [0] * 6

                    self.send_command("COMMAND_get_vhv", hv_v)
                    self.send_command("COMMAND_get_ihv", hv_i)
                    self.send_command("COMMAND_readMonV48", v48)
                    self.send_command("COMMAND_readMonI48", i48)
                    self.send_command("COMMAND_readMonV6", v6)
                    self.send_command("COMMAND_readMonI6", i6)

                    self.data_fetched.emit(hv_v, hv_i, v48, i48, v6, i6, T48)
                    time.sleep(1)  # Adjust the sleep time as needed
                except Exception as e:
                    print(f"Data fetching error: {e}")

    def send_command(self, command_key, data_list):
        # Implement command sending logic, including socket communication
        pass

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.v48 = [0] * 6
        self.i48 = [0] * 6
        self.v6 = [0] * 6
        self.i6 = [0] * 6
        self.T48 = [0] * 6
        self.hv_v = [0] * 12
        self.hv_i = [0] * 12

        self.setWindowTitle("LVHV GUI")
        self.setStyleSheet(background_color)

        self.display_setup()
        self.load_commands()

        self.data_fetcher = DataFetcher()
        self.data_fetcher.data_fetched.connect(self.update_data)
        self.data_fetcher.start()  # Start data fetching thread

        self.show()

    def update_data(self, hv_v, hv_i, v48, i48, v6, i6, T48):
        self.hv_v = hv_v
        self.hv_i = hv_i
        self.v48 = v48
        self.i48 = i48
        self.v6 = v6
        self.i6 = i6
        self.T48 = T48

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
        try:
            with open("commands.h", "r") as file:
                pre_command_list = [line.split() for line in file]
                self.command_dict = {i[1]: format(int(i[2]), '032b') for i in pre_command_list}
        except FileNotFoundError:
            print("commands.h not found. Please check the file path.")

    def display_setup(self):
        self.all_display = QWidget()
        self.setCentralWidget(self.all_display)

        layout = QGridLayout(self.all_display)

        layout.addWidget(QLabel("48V LV"), 0, 0)
        layout.addWidget(QLabel("HV"), 0, 1)
        layout.addWidget(QLabel("6V LV"), 2, 0)

        self.lv_table = QTableWidget(6, 3)
        self.lv_table.setVerticalHeaderLabels([f"Ch {i}" for i in range(6)])
        self.lv_table.setHorizontalHeaderLabels(["Voltage (V)", "Current (A)", "Temp (C)"])
        layout.addWidget(self.lv_table, 1, 0)

        self.six_lv_table = QTableWidget(6, 2)
        self.six_lv_table.setVerticalHeaderLabels([f"Ch {i}" for i in range(6)])
        self.six_lv_table.setHorizontalHeaderLabels(["Voltage (V)", "Current (uA)"])
        layout.addWidget(self.six_lv_table, 3, 0)

        self.hv_table = QTableWidget(12, 2)
        self.hv_table.setVerticalHeaderLabels([f"Ch {i}" for i in range(12)])
        self.hv_table.setHorizontalHeaderLabels(["Voltage (V)", "Current (uA)"])
        layout.addWidget(self.hv_table, 1, 1)

        self.all_display.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    window = Window()
    sys.exit(app.exec_())



