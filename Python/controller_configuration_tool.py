import sys
from PySide6 import QtCore, QtWidgets, QtGui
from serial_classes import *

QSS_FILE = "app_style.qss"
DEVICE_PING_INTERVAL = 5000 #ms

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()        
        self.initUI()
        self.setWindowTitle("GMK Controller Configuration Tool")

    def initUI(self):
        self.central_widget = QtWidgets.QWidget(self)
        self.layout = QtWidgets.QHBoxLayout(self.central_widget)

        self.controller_view = ControllerView()
        self.layout.addWidget(self.controller_view)
        
        self.input_mapping_column = InputMappingColumn()
        self.layout.addWidget(self.input_mapping_column)
        
        self.setCentralWidget(self.central_widget)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

class ControllerView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.view_top = QtWidgets.QGraphicsView(self.scene)
        self.view_bottom = QtWidgets.QGraphicsView(self.scene)
        self.layout.addWidget(self.view_top)
        self.layout.addWidget(self.view_bottom)

class InputMappingColumn(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.group = QtWidgets.QGroupBox(self)
        self.layout.addWidget(self.group)

        self.mapping_list = MappingList()
        self.layout.addWidget(self.mapping_list)
        
        self.device_connection_editor = DeviceConnectionEditor()
        self.layout.addWidget(self.device_connection_editor, alignment=QtCore.Qt.AlignBottom)

class DeviceConnectionEditor(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(DEVICE_PING_INTERVAL)
        self.timer.timeout.connect(self.ping_device)
        self.timer.start()
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.group = QtWidgets.QGroupBox(self)
        self.group.setTitle("Device Connection")
        self.layout.addWidget(self.group)
        self.group_layout = QtWidgets.QGridLayout(self.group)

        self.comm_ports_list = DeviceList()
        self.group_layout.addWidget(self.comm_ports_list, 0, 0, 1, 2)
        
        self.connect_button = QtWidgets.QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_device)
        self.group_layout.addWidget(self.connect_button, 1, 0)

        self.scan_for_devices = QtWidgets.QPushButton("Scan")
        self.scan_for_devices.clicked.connect(self.comm_ports_list.populateList)
        self.group_layout.addWidget(self.scan_for_devices, 1, 1)

        self.connected = QtWidgets.QLabel(self)
        self.connected.setAlignment(QtCore.Qt.AlignCenter)
        self.check_device_connected()
        self.group_layout.addWidget(self.connected, 2, 0, 1, 2)

    def ping_device(self):
        serial_controller.ping()
        self.check_device_connected()
        self.comm_ports_list.populateList()

    def check_device_connected(self):
        if serial_controller.isOpen():
            self.connected.setText("Connected")
            self.connected.setStyleSheet("color: green")
        else:
            self.connected.setText("Not Connected")
            self.connected.setStyleSheet("color: red")

    def connect_device(self):
        if self.comm_ports_list.currentText():
            serial_controller.connect_with_port(self.comm_ports_list.currentText())
            self.check_device_connected()

class DeviceList(QtWidgets.QComboBox):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.populateList()

    def populateList(self):
        for item in range(self.count()):
            self.removeItem(item)
        for device in Serial_Controller.get_devices():
            self.addItem(device)

class MappingList(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setColumnCount(1)
        self.setHeaderLabels(["Configurations"])
        self.root = self.invisibleRootItem()
        self.button_configs = QtWidgets.QTreeWidgetItem(self)
        self.button_configs.setText(0, "Button Configurations")
        self.joystick_configs = QtWidgets.QTreeWidgetItem(self)
        self.joystick_configs.setText(0, "Joystick Configurations")
        self.encoder_configs = QtWidgets.QTreeWidgetItem(self)
        self.encoder_configs.setText(0, "Encoder Configurations")
        self.gyro_configs = QtWidgets.QTreeWidgetItem(self)
        self.gyro_configs.setText(0, "Gryo Configurations")

        self.root.addChild(self.button_configs)
        self.root.addChild(self.joystick_configs)
        self.root.addChild(self.encoder_configs)
        self.root.addChild(self.gyro_configs)

        self.get_configs()

    def get_configs(self):
        self.configs = serial_controller.get_configuration(0)

    def right_click(self):
        print("Item right-clciked")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    with open(QSS_FILE, "r") as f:
        app_style = f.read()
        app.setStyleSheet(app_style)
    
    main = MainWindow()
    main.resize(800, 600)
    main.show()

    sys.exit(app.exec())
