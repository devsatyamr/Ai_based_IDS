from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QTextEdit, QLabel, QGroupBox, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from model_func import load_and_prepare_data, train_model_and_predict, flag_malicious_ips, calculate_accuracy

class MaliciousIPDetector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.network_data_path = None
        self.bad_ips_path = None

    def initUI(self):
        self.setWindowTitle('Malicious IP Detector')
        self.setGeometry(100, 100, 600, 400)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Title label
        title_label = QLabel('Malicious IP Detector')
        title_label.setFont(QFont('Arial', 18))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Group box for loading data
        load_group_box = QGroupBox('Load Data')
        load_layout = QGridLayout()

        self.btn_load_network = QPushButton('Load Network Data')
        self.btn_load_network.clicked.connect(self.load_network_data)
        load_layout.addWidget(self.btn_load_network, 0, 0)

        self.btn_load_bad_ips = QPushButton('Load Bad IPs')
        self.btn_load_bad_ips.clicked.connect(self.load_bad_ips)
        load_layout.addWidget(self.btn_load_bad_ips, 0, 1)

        load_group_box.setLayout(load_layout)
        layout.addWidget(load_group_box)

        # Label column input
        label_layout = QHBoxLayout()
        label_label = QLabel('Label Column:')
        self.label_input = QLineEdit()
        label_layout.addWidget(label_label)
        label_layout.addWidget(self.label_input)
        layout.addLayout(label_layout)

        # Button for running the model
        self.btn_run_model = QPushButton('Run Model')
        self.btn_run_model.clicked.connect(self.run_model)
        layout.addWidget(self.btn_run_model)

        # Text area for displaying results
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        main_widget.setLayout(layout)

        # Apply stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #333;
                border: 1px solid #aaa;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
            }
            QPushButton {
                font-size: 12px;
                padding: 5px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                font-size: 12px;
                padding: 5px;
                border: 1px solid #aaa;
                border-radius: 3px;
                background-color: white;
            }
        """)

    def load_network_data(self):
        self.network_data_path, _ = QFileDialog.getOpenFileName(self, "Load Network Data", "", "CSV Files (*.csv)")
        if self.network_data_path:
            self.results_area.append(f"Loaded network data from {self.network_data_path}")

    def load_bad_ips(self):
        self.bad_ips_path, _ = QFileDialog.getOpenFileName(self, "Load Bad IPs", "", "CSV Files (*.csv)")
        if self.bad_ips_path:
            self.results_area.append(f"Loaded bad IPs from {self.bad_ips_path}")

    def run_model(self):
        if self.network_data_path is None or self.bad_ips_path is None:
            self.results_area.append("Please load both network data and bad IPs before running the model.")
            return

        label_column = self.label_input.text()
        if not label_column:
            self.results_area.append("Please specify the label column.")
            return

        try:
            # Load and prepare data
            X, y, malicious_ips = load_and_prepare_data(self.network_data_path, self.bad_ips_path, label_column)

            # Train model and get predictions
            y_pred = train_model_and_predict(X, y)

            # Flag malicious IPs
            flagged_ips = flag_malicious_ips(X, malicious_ips)

            # Calculate accuracy
            accuracy = calculate_accuracy(X, y, malicious_ips)

            # Display results
            self.results_area.append("\nModel Results:")
            self.results_area.append(f"Total predictions: {len(y_pred)}")
            self.results_area.append(f"Malicious predictions: {sum(y_pred)}")
            self.results_area.append(f"\nFlagged IPs for further investigation: {flagged_ips}")
            self.results_area.append(f"Number of flagged IPs: {len(flagged_ips)}")
            self.results_area.append(f"\nAccuracy of malicious IP identification: {accuracy:.2f}")

        except Exception as e:
            self.results_area.append(f"Error: {str(e)}")