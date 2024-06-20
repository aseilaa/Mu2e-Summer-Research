import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton

class MatrixDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Matrix Display')
        self.setGeometry(100, 100, 800, 300)

        self.initUI()

    def initUI(self): #User interface
        # Create first group box for the first matrix
        self.group_box1 = QGroupBox('Matrix 1')
        self.group_box1.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid gray; border-radius: 5px; margin-top: 1ex; }") #style
        
        # Create vertical layout for the first group box
        self.group_layout1 = QVBoxLayout()

        # First row labels: "channel", "I", "V"
        self.header_layout1 = QHBoxLayout()
        self.channel_label1 = QLabel('channel')
        self.i_label1 = QLabel('I')
        self.v_label1 = QLabel('V')
        self.header_layout1.addWidget(self.channel_label1)
        self.header_layout1.addWidget(self.i_label1)
        self.header_layout1.addWidget(self.v_label1)
        self.group_layout1.addLayout(self.header_layout1)

        # Example data for matrix 1 (replace with your actual data)
        self.channel_numbers1 = ['0', '1', '2', '3', '4', '5']
        self.i_numbers1 = ['10', '15', '20', '18', '25', '22']
        self.v_numbers1 = ['5', '8', '10', '9', '12', '11']

        for channel_num, i_num, v_num in zip(self.channel_numbers1, self.i_numbers1, self.v_numbers1):
            data_layout1 = QHBoxLayout()
            channel_num_label1 = QLabel(channel_num)
            i_num_label1 = QLabel(i_num)
            v_num_label1 = QLabel(v_num)
            data_layout1.addWidget(channel_num_label1)
            data_layout1.addWidget(i_num_label1)
            data_layout1.addWidget(v_num_label1)
            self.group_layout1.addLayout(data_layout1)
        self.group_box1.setLayout(self.group_layout1)


        # Create second group box for the second matrix
        self.group_box2 = QGroupBox('Matrix 2')
        self.group_box2.setStyleSheet("QGroupBox { font-weight: bold; border: 2px solid gray; border-radius: 5px; margin-top: 1ex; }")

        # Create vertical layout for the second group box
        self.group_layout2 = QVBoxLayout()

        # First row labels: "channel", "I", "V"
        self.header_layout2 = QHBoxLayout()
        self.channel_label2 = QLabel('channel')
        self.i_label2 = QLabel('I')
        self.v_label2 = QLabel('V')
        self.header_layout2.addWidget(self.channel_label2)
        self.header_layout2.addWidget(self.i_label2)
        self.header_layout2.addWidget(self.v_label2)
        self.group_layout2.addLayout(self.header_layout2)

        # Example data for matrix 2 (replace with your actual data)
        self.channel_numbers2 = ['7', '8', '9', '10', '11', '12']
        self.i_numbers2 = ['18', '20', '22', '25', '27', '30']
        self.v_numbers2 = ['12', '15', '18', '20', '22', '25']

        for channel_num, i_num, v_num in zip(self.channel_numbers2, self.i_numbers2, self.v_numbers2):
            data_layout2 = QHBoxLayout()
            channel_num_label2 = QLabel(channel_num)
            i_num_label2 = QLabel(i_num)
            v_num_label2 = QLabel(v_num)
            data_layout2.addWidget(channel_num_label2)
            data_layout2.addWidget(i_num_label2)
            data_layout2.addWidget(v_num_label2)
            self.group_layout2.addLayout(data_layout2)

        self.group_box2.setLayout(self.group_layout2)

        # Create horizontal layout for placing group boxes side by side
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.group_box1)
        self.main_layout.addWidget(self.group_box2)

        # Create a Next button
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next_button_clicked)
        self.main_layout.addWidget(self.next_button)

        self.setLayout(self.main_layout)


# Need more work
    def next_button_clicked(self):
        # Action to perform when the Next button is clicked
        print("Next button clicked!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MatrixDisplay()
    ex.show()
    sys.exit(app.exec_()) 
    