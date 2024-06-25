import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QStackedWidget
from PyQt5.QtCore import QTimer

# Simulated hardware data retrieval function (replace with actual data)
def fetch_data():
    # Replace with actual data retrieval logic
    return [
        (['0', '1', '2', '3', '4', '5'], ['10', '15', '20', '18', '25', '22'], ['5', '8', '10', '9', '12', '11']),
        (['7', '8', '9', '10', '11', '12'], ['18', '20', '22', '25', '27', '30'], ['12', '15', '18', '20', '22', '25']),
    ]

class MatrixDisplay(QWidget):
    def __init__(self, title, channel_numbers, i_numbers, v_numbers):
        super().__init__()
        self.title = title
        self.channel_numbers = channel_numbers
        self.i_numbers = i_numbers
        self.v_numbers = v_numbers
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # Create group box for the matrix
        self.group_box = QGroupBox(self.title)
        self.group_box.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid gray; border-radius: 5px; margin-top: 1ex; }")

        # Create vertical layout for the group box
        self.group_layout = QVBoxLayout()

        # First row labels: "channel", "I", "V"
        self.header_layout = QHBoxLayout()
        self.channel_label = QLabel('Channel')
        self.i_label = QLabel('I')
        self.v_label = QLabel('V')
        self.header_layout.addWidget(self.channel_label)
        self.header_layout.addWidget(self.i_label)
        self.header_layout.addWidget(self.v_label)
        self.group_layout.addLayout(self.header_layout)

        # Add data
        for channel_num, i_num, v_num in zip(self.channel_numbers, self.i_numbers, self.v_numbers):
            data_layout = QHBoxLayout()
            channel_num_label = QLabel(channel_num)
            i_num_label = QLabel(i_num)
            v_num_label = QLabel(v_num)
            data_layout.addWidget(channel_num_label)
            data_layout.addWidget(i_num_label)
            data_layout.addWidget(v_num_label)
            self.group_layout.addLayout(data_layout)

        self.group_box.setLayout(self.group_layout)
        layout.addWidget(self.group_box)
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matrix')
        self.setGeometry(100, 100, 800, 300)

        self.stacked_widget = QStackedWidget()

        self.initUI()

        # Setup initial pages with dummy data (can be replaced by real data later)
        initial_data = fetch_data()
        self.pages = []
        for idx, data_set in enumerate(initial_data):
            title = f'Matrix {idx + 1}'
            channel_numbers, i_numbers, v_numbers = data_set
            page = MatrixDisplay(title, channel_numbers, i_numbers, v_numbers)
            self.pages.append(page)
            self.stacked_widget.addWidget(page)

        self.current_page_index = 0
        self.max_pages = 6 # Maximum number of pages (matrices) to display

    def initUI(self):
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_button_clicked)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(self.next_button)
        self.setLayout(main_layout)

    def next_button_clicked(self):
        self.current_page_index += 1
        if self.current_page_index >= len(self.pages):
            # If reached end of current data, fetch new data
            data = fetch_data()
            for data_set in data:
                title = f'Matrix {len(self.pages) + 1}'
                channel_numbers, i_numbers, v_numbers = data_set
                page = MatrixDisplay(title, channel_numbers, i_numbers, v_numbers)
                self.pages.append(page)
                self.stacked_widget.addWidget(page)

        self.stacked_widget.setCurrentIndex(self.current_page_index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())









 