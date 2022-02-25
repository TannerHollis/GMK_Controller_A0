import sys
from PySide6 import QtGui, QtQuick
from PySide6.QtWidgets import *
from PySide6.QtGui import QGuiApplication, QAction, QPixmap, QPalette, QPainter, QColor
from PySide6.QtCore import QTimer, Slot, Qt, QCoreApplication, QSize
from InputMappingGUIClasses import *
from SerialClasses import *
from pathlib import Path

QSS_FILE = "app_style.qss"
QML_FILE = "app.qml"
CONTROLLER_VIEW_TOP_FILE = image_folder = Path.cwd().joinpath("images").joinpath("controller_back.png").as_posix()
CONTROLLER_VIEW_BOTTOM_FILE = image_folder = Path.cwd().joinpath("images").joinpath("controller_joystick.png").as_posix()
BACKGROUND_IMAGE_FILE = image_folder = Path.cwd().joinpath("images").joinpath("background.png").as_posix()
CONFIG_FOLDER = cfg_dir = Path.cwd().joinpath("configs").as_posix()
DEFAULT_CFG_FILE = Path.cwd().joinpath("configs").joinpath("{}.cfg".format(DEFAULT_CFG_FILE)).as_posix()
DEVICE_PING_INTERVAL = 5000 #ms

class MainWindow(QMainWindow):
    def __init__(self, app, serialController):
        super().__init__()
        self.app = app
        self.serialController = serialController
        
        self.config = Controller_Configuration.fromFile(DEFAULT_CFG_FILE)
        self.initUI()
        self.setWindowTitle("GMK Controller Configuration Tool")

    def initUI(self):
        self.menubar = self.menuBar()
        self.fileMenu = FileMenu(self)
        self.menubar.addMenu(self.fileMenu)
        
        self.centralWidget = QWidget(self)
        self.layout = QHBoxLayout(self.centralWidget)

        self.controllerView = ControllerView(self)
        self.layout.addWidget(self.controllerView)
        
        self.inputMappingColumn = InputMappingColumn(self)
        self.layout.addWidget(self.inputMappingColumn)
        
        self.setCentralWidget(self.centralWidget) 

    def paintEvent(self, event):
        self.paintBackground()

    def paintBackground(self):
        self.background = QPixmap(BACKGROUND_IMAGE_FILE).scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.setOpacity(0.15)
        self.painter.drawPixmap((self.width() - self.background.width())/2, (self.height() - self.background.height())/2, self.background)
        self.painter.end()

    def exit(self):
        QCoreApplication.quit()

    def open(self):
        (filePath, file_type) = QFileDialog.getOpenFileName(self, "Open Configuration", CONFIG_FOLDER, "Configurations (*.cfg)")
        if not filePath:
            return
        try:
            self.config = ControllerConfiguration.fromFile(filePath)
        except Exception as e:
            ErrorMessageBox("Error Opening File", e, QMessageBox.Ok)
            return
        self.inputMappingColumn.mappingList.populateTree(self.config)
        
    def save(self):
        (file_name, file_type) = QFileDialog.getSaveFileName(self, "Save Configuration", CONFIG_FOLDER, "Configurations (*.cfg)")
        if not file_name:
            return
        try:
            self.config = self.config.print_config_to_file(file_name)
        except Exception as e:
            ErrorMessageBox("Error Opening File", e, QMessageBox.Ok)
            return

class FileMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setTitle("&File")
        self.initUI()

    def initUI(self):
        self.newAction = QAction("New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.addAction(self.newAction)

        self.openAction = QAction("Open...", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.parent.open)
        self.addAction(self.openAction)

        self.saveAction = QAction("Save...", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.parent.save)
        self.addAction(self.saveAction)

        self.exitAction = QAction("Exit", self)
        self.exitAction.setShortcut("Ctrl+W")
        self.exitAction.triggered.connect(self.parent.exit)
        self.addAction(self.exitAction)
        
class ErrorMessageBox(QMessageBox):
    def __init__(self, text, text_detailed, buttons):
        super().__init__()
        self.setWindowTitle("Error")
        self.setText(text)
        self.setDetailedText(str(text_detailed))
        self.setStandardButtons(buttons)
        self.exec()

class ControllerView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        
        self.layout = QVBoxLayout(self)

        self.viewTop = ControllerTopView(self)
        self.viewBottom = ControllerBottomView(self)
        
        self.layout.addWidget(self.view_top)
        self.layout.addWidget(self.view_bottom)

    def showEvent(self, event):
        self.resizeEvent(None)

class ControllerTopView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setMaximumWidth(800)

    def paintEvent(self, event):
        self.image = QPixmap(CONTROLLER_VIEW_TOP_FILE).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.setOpacity(1.0)
        self.painter.drawPixmap((self.width() - self.image.width())/2, (self.height() - self.image.height())/2, self.image)
        self.painter.end()

class ControllerBottomView(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setMinimumWidth(400)
        self.setMaximumWidth(800)

    def paintEvent(self, event):
        self.image = QPixmap(CONTROLLER_VIEW_BOTTOM_FILE).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.setOpacity(1.0)
        self.painter.drawPixmap((self.width() - self.image.width())/2, (self.height() - self.image.height())/2, self.image)
        self.painter.end()

class InputMappingColumn(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setMinimumWidth(300)
        self.setMaximumWidth(400)
        self.currentMapping = -1
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.inputMapping = QGroupBox(self)
        self.inputMapping.setMinimumHeight(400)
        self.inputMapping.setMaximumHeight(500)
        self.inputMapping.setTitle("Configuration Mapping")
        self.layout.addWidget(self.inputMapping, alignment=Qt.AlignTop)

        self.inputMappingLayout = QVBoxLayout(self.inputMapping)
        self.populateInputMappingList()
        self.changeInputMappingUI(None)
        
        self.mappingList = MappingList(self.parent, self.changeInputMappingUI)
        self.layout.addWidget(self.mappingList)
        
        self.deviceConnectionEditor = DeviceConnectionEditor(self.parent)
        self.layout.addWidget(self.deviceConnectionEditor, alignment=Qt.AlignTop)

    def populateInputMappingList(self):
        self.inputMappingList = []
        self.inputMappingList.append(InputMappingDefault(self, None))
        self.inputMappingList.append(InputMappingButtonAsButton(self, None))
        self.inputMappingList.append(InputMappingButtonAsJoystick(self, None))
        self.inputMappingList.append(InputMappingButtonAsKeyboard(self, None))
        self.inputMappingList.append(InputMappingButtonAsTrigger(self, None))
        self.inputMappingList.append(InputMappingJoystickAsButton(self, None))
        self.inputMappingList.append(InputMappingJoystickAsJoystick(self, None))
        self.inputMappingList.append(InputMappingJoystickAsKeyboard(self, None))
        self.inputMappingList.append(InputMappingJoystickAsTrigger(self, None))
        self.inputMappingList.append(InputMappingEncoderAsButton(self, None))
        self.inputMappingList.append(InputMappingEncoderAsJoystick(self, None))
        
        for mapping in self.inputMappingList:
            self.inputMappingLayout.addWidget(mapping)

    def changeInputMappingUI(self, item):
        self.inputMappingList[self.currentMapping+1].close_mapping()
        if item:
            self.currentMapping = item.config.type
        else:
            self.currentMapping = -1
        self.inputMappingList[self.currentMapping+1].show_mapping(item)

class DeviceConnectionEditor(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.timer = QTimer()
        self.timer.setInterval(DEVICE_PING_INTERVAL)
        self.timer.timeout.connect(self.ping_device)
        self.timer.start()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.group = QGroupBox(self)
        self.group.setTitle("Device Connection")
        self.layout.addWidget(self.group)
        self.group_layout = QGridLayout(self.group)

        self.comm_ports_list = DeviceList(self.parent)
        self.group_layout.addWidget(self.comm_ports_list, 0, 0, 1, 2)
        
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_device)
        self.group_layout.addWidget(self.connect_button, 1, 0)

        self.scan_for_devices = QPushButton("Scan")
        self.scan_for_devices.clicked.connect(self.comm_ports_list.populateList)
        self.group_layout.addWidget(self.scan_for_devices, 1, 1)

        self.connected = QLabel(self)
        self.connected.setAlignment(Qt.AlignCenter)
        self.check_device_connected()
        self.group_layout.addWidget(self.connected, 2, 0, 1, 2)

    def ping_device(self):
        serialController.ping()
        self.check_device_connected()
        self.comm_ports_list.populateList()

    def check_device_connected(self):
        if serialController.isOpen():
            self.connected.setText("Connected")
            self.connected.setStyleSheet("color: green")
        else:
            self.connected.setText("Not Connected")
            self.connected.setStyleSheet("color: red")

    def connect_device(self):
        if self.comm_ports_list.currentText():
            serialController.connect_with_port(self.comm_ports_list.currentText())
            self.check_device_connected()

class DeviceList(QComboBox):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.populateList()

    def populateList(self):
        for item in range(self.count()):
            self.removeItem(item)
        for device in SerialController.getDevices():
            self.addItem(device)

class MappingList(QTreeWidget):
    def __init__(self, parent, changeInputMappingUI):
        super().__init__()
        self.parent = parent
        self.initUI()
        self.setMinimumHeight(200)
        self.changeInputMappingUI = changeInputMappingUI

    def initUI(self):
        self.setColumnCount(2)
        self.setHeaderLabels(["Configurations", "Output Mapping"])
        self.setColumnWidth(0, 160)
        self.setColumnWidth(1, 100)
        self.root = self.invisibleRootItem()
        self.button_configs = TreeItem(self, "Button Configurations", None)
        self.joystick_configs = TreeItem(self, "Joystick Configurations", None)
        self.encoder_configs = TreeItem(self, "Encoder Configurations", None)
        self.gyro_configs = TreeItem(self, "Gyro Configurations", None)

        self.root.addChild(self.button_configs)
        self.root.addChild(self.joystick_configs)
        self.root.addChild(self.encoder_configs)
        self.root.addChild(self.gyro_configs)
        self.populateTree(self.parent.config)

    def populateTree(self, config):
        if config:
            configs = config.configurations
            self.clearList(self.button_configs)
            self.clearList(self.joystick_configs)
            self.clearList(self.encoder_configs)
            self.clearList(self.gyro_configs)
            button_configs = [config for config in configs if config.input_type == "button"]
            joystick_configs = [config for config in configs if config.input_type == "joystick"]
            encoder_configs = [config for config in configs if config.input_type == "encoder"]
            gyro_configs = [config for config in configs if config.input_type == "gyro"]
            self.populateTreeItems(self.button_configs, button_configs)
            self.populateTreeItems(self.joystick_configs, joystick_configs)
            self.populateTreeItems(self.encoder_configs, encoder_configs)
            self.populateTreeItems(self.gyro_configs, gyro_configs)
        else:
            print("No configs found.")

    def populateTreeItems(self, tree_header, configs):
        if configs:
            for i in range(len(configs)):
                item_text = "{} as {}".format(configs[i].input_type.capitalize(), configs[i].output_type.capitalize())
                TreeItem(tree_header, item_text, configs[i])
        else:
            print("No configs found for: {}".format(tree_header.text(0)))

    def removeItem(self, header_item, item):
        header_item.removeChild(item)

    def addItem(self, header_item, item):
        header_item.addChild(item)
    
    def clearList(self, list_header):
        for i in reversed(range(list_header.childCount())):
            list_header.removeChild(list_header.child(i))

    def mousePressEvent(self, event):
        QTreeWidget.mousePressEvent(self, event)
        pos = event.position()
        item_clicked = self.itemAt(pos.toPoint())
        is_header = item_clicked in [self.button_configs, self.joystick_configs, self.encoder_configs, self.gyro_configs]
        if item_clicked:
            if event.button() == Qt.RightButton:
                if is_header:
                    self.headerRightClicked(item_clicked, event.globalPosition().toPoint())
                else:
                    self.itemRightClicked(item_clicked, event.globalPosition().toPoint())
            if event.button() == Qt.LeftButton:
                if not is_header:
                    self.itemLeftClicked(item_clicked, event.globalPosition().toPoint())

    def itemRightClicked(self, item, pos):
        ItemRightClickMenu(item, self.parent.config, pos, self.changeInputMappingUI, self.removeItem)

    def headerRightClicked(self, header, pos):
        HeaderRightClickMenu(header, self.parent.config, pos, self.populateTree)

    def itemLeftClicked(self, item, pos):
        self.changeInputMappingUI(item)

class TreeItem(QTreeWidgetItem):
    def __init__(self, parent, text, config):
        super().__init__(parent)
        self.parent = parent
        self.config_text = text
        self.config = config
        self.updateText()

    def updateText(self):
        self.setText(0, self.config_text)
        if self.config:
            self.setText(1, self.config.output_mapping().title())

class ItemRightClickMenu(QMenu):
    def __init__(self, item, config, pos, edit_func, delete_func):
        super().__init__()
        self.item = item
        self.config = config
        self.edit_func = edit_func
        self.delete_func = delete_func
        self.edit_action = QAction("Edit", self)
        self.edit_action.triggered.connect(self.edit_config)
        self.addAction(self.edit_action)
        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.delete_config)
        self.addAction(self.delete_action)
        self.exec(pos)

    def edit_config(self):
        self.edit_func(self.item)

    def delete_config(self):
        self.config.configurations.pop(self.config.configurations.index(self.item.config))
        self.delete_func(self.item.parent, self.item)

class HeaderRightClickMenu(QMenu):
    def __init__(self, header, config, pos, populateFunc):
        super().__init__()
        self.header = header
        self.config = config
        self.new_action = QAction("New", self)
        self.new_action.triggered.connect(self.new_config)
        self.addAction(self.new_action)
        self.exec(pos)

    def new_config(self):
        print(self.current_config)

class NewConfigDialogBox(QDialog):
    def __init__(self, text):
        print(text)

if __name__ == "__main__":
    #Initialize the serial controller
    serialController = SerialController()

    #Initialize the Application window
    app = QApplication()

    #Import the application styling
    with open(QSS_FILE, "r") as f:
        app_style = f.read()
        app.setStyleSheet(app_style)

    #Initialize the main window
    main = MainWindow(app, serialController)
    main.resize(1200, 800)
    main.show()

    app.exec()
