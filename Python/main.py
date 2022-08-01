import sys, copy
#from PySide6 import QtGui, QtQuick
from PySide6.QtWidgets import *
from PySide6.QtGui import QGuiApplication, QAction, QPixmap, QPalette, QPainter, QColor, QIcon
from PySide6.QtCore import QTimer, Slot, Qt, QCoreApplication, QSize
from InputMappingGUIClasses import *
from SerialClasses import *
from pathlib import Path

QSS_FILE = "app_style.qss"
QML_FILE = "app.qml"
ICON_IMAGE_FILE = image_folder = Path.cwd().joinpath("images").joinpath("icon.png").as_posix()
ICON_ERROR_IMAGE_FILE = image_folder = Path.cwd().joinpath("images").joinpath("icon_error.png").as_posix()
BACKGROUND_IMAGE_FILE = image_folder = Path.cwd().joinpath("images").joinpath("background.png").as_posix()
CONTROLLER_VIEW_TOP_FILE = image_folder = Path.cwd().joinpath("images").joinpath("controller_back.png").as_posix()
BUTTON_IMAGE_FILES = [Path.cwd().joinpath("images").joinpath("button_{}.png".format(i)).as_posix() for i in range(10)]
CONTROLLER_VIEW_BOTTOM_FILE = image_folder = Path.cwd().joinpath("images").joinpath("controller_joystick.png").as_posix()
CONFIG_FOLDER = cfg_dir = Path.cwd().joinpath("configs").as_posix()
DEFAULT_CFG_FILE = Path.cwd().joinpath("configs").joinpath("{}.cfg".format(DEFAULT_CFG_FILE)).as_posix()
DEVICE_PING_INTERVAL = 5000 #ms
STATUS_INTERVAL = 2000 #ms

class MainWindow(QMainWindow):
    def __init__(self, app, serialController):
        super().__init__()
        self.app = app
        self.serialController = serialController
        
        self.config = ControllerConfiguration.fromFile(DEFAULT_CFG_FILE)
        self.initUI()
        self.setWindowTitle("GMK Controller Configuration Tool")
        self.setWindowIcon(QIcon(ICON_IMAGE_FILE))

    def initUI(self):
        self.menubar = self.menuBar()
        self.fileMenu = FileMenu(self)
        self.menubar.addMenu(self.fileMenu)

        self.setStatusBar(StatusBar(self.config))
        
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
        self.painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0, 32))
        self.painter.setOpacity(0.35)
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
            self.config = self.config.printConfigToFile(file_name)
        except Exception as e:
            ErrorMessageBox("Error Opening File", e, QMessageBox.Ok)
            return

    def new(self):
        print("New Configuration")

class StatusBar(QStatusBar):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.initUI()
        self.timer = QTimer(self)
        self.timer.setInterval(STATUS_INTERVAL)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start()

    def initUI(self):
        self.updateStatus()

    def updateStatus(self):
        if len(self.config.configurations) > 0:
            configSize = self.config.getConfigSize()
            text = "Configuration Utilization: {} / {} ({:0.2f}%)".format(configSize, CONFIGURATION_SIZE, configSize * 100 / CONFIGURATION_SIZE)
            if configSize > 2048:
                text += "\t Error: Configuration will not fit."
            self.showMessage(text)
        else:
            self.showMessage("No Configurations found.")

class FileMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setTitle("&File")
        self.initUI()

    def initUI(self):
        self.newAction = QAction("New", self)
        self.newAction.setShortcut("Ctrl+N")
        self.newAction.triggered.connect(self.parent.new)
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
        self.setWindowIcon(QIcon(ICON_ERROR_IMAGE_FILE))
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
        
        self.layout.addWidget(self.viewTop)
        self.layout.addWidget(self.viewBottom)

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

        for img in BUTTON_IMAGE_FILES:
            buttonImg = QPixmap(img).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.painter.drawPixmap((self.width() - self.image.width())/2, (self.height() - self.image.height())/2, buttonImg)

        self.painter.end()

    def moveEvent(self, event):
        print(event)

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
        #self.inputMapping.setMinimumHeight(400)
        #self.inputMapping.setMaximumHeight(500)
        self.inputMapping.setTitle("Configuration Mapping")
        self.layout.addWidget(self.inputMapping, alignment=Qt.AlignBottom)

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
        self.inputMappingList[self.currentMapping+1].closeMapping()
        if item:
            self.currentMapping = item.config.type
        else:
            self.currentMapping = -1
        self.inputMappingList[self.currentMapping+1].showMapping(item)

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
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragDropMode(self.InternalMove)
        self.setColumnCount(2)
        self.setHeaderLabels(["Configurations", "Output Mapping"])
        self.setColumnWidth(0, 160)
        self.setColumnWidth(1, 100)
        self.root = self.invisibleRootItem()
        self.buttonConfigs = HeaderItem(self, "Button Configurations")
        self.joystickConfigs = HeaderItem(self, "Joystick Configurations")
        self.encoderConfigs = HeaderItem(self, "Encoder Configurations")
        self.gyroConfigs = HeaderItem(self, "Gyro Configurations")

        self.root.addChild(self.buttonConfigs)
        self.root.addChild(self.joystickConfigs)
        self.root.addChild(self.encoderConfigs)
        self.root.addChild(self.gyroConfigs)
        self.populateTree(self.parent.config)

    def populateTree(self, config):
        if config:
            configs = config.configurations
            self.clearList(self.buttonConfigs)
            self.clearList(self.joystickConfigs)
            self.clearList(self.encoderConfigs)
            self.clearList(self.gyroConfigs)
            buttonConfigs = [config for config in configs if config.inputType == "button"]
            joystickConfigs = [config for config in configs if config.inputType == "joystick"]
            encoderConfigs = [config for config in configs if config.inputType == "encoder"]
            gyroConfigs = [config for config in configs if config.inputType == "gyro"]
            self.populateTreeItems(self.buttonConfigs, buttonConfigs)
            self.populateTreeItems(self.joystickConfigs, joystickConfigs)
            self.populateTreeItems(self.encoderConfigs, encoderConfigs)
            self.populateTreeItems(self.gyroConfigs, gyroConfigs)
        else:
            print("No configs found.")

    def populateTreeItems(self, treeHeader, configs):
        if configs:
            for i in range(len(configs)):
                
                TreeItem(treeHeader, configs[i])
        else:
            print("No configs found for: {}".format(treeHeader.text(0)))

    def removeItem(self, headerItem, item):
        headerItem.removeChild(item)

    def addItem(self, headerItem, item):
        headerItem.addChild(item)

    def clearList(self, list_header):
        for i in reversed(range(list_header.childCount())):
            list_header.removeChild(list_header.child(i))

    def mousePressEvent(self, event):
        QTreeWidget.mousePressEvent(self, event)
        pos = event.position()
        item_clicked = self.itemAt(pos.toPoint())
        is_header = item_clicked in [self.buttonConfigs, self.joystickConfigs, self.encoderConfigs, self.gyroConfigs]
        if item_clicked:
            if event.button() == Qt.RightButton:
                if is_header:
                    self.headerRightClicked(item_clicked, event.globalPosition().toPoint())
                else:
                    self.itemRightClicked(item_clicked, event.globalPosition().toPoint())

    def mouseDoubleClickEvent(self, event):
        pos = event.position()
        item_clicked = self.itemAt(pos.toPoint())
        is_header = item_clicked in [self.buttonConfigs, self.joystickConfigs, self.encoderConfigs, self.gyroConfigs]
        if event.button() == Qt.LeftButton:
                if not is_header:
                    self.itemLeftClicked(item_clicked, event.globalPosition().toPoint())

    def dropEvent(self, event):
        itemSource = event.source().currentItem()
        itemDest = self.itemAt(event.pos())
        if(itemSource.parent == itemDest.parent and itemSource is not itemDest):
            event.setDropAction(Qt.MoveAction)
            itemSourceIndex = itemSource.parent.indexOfChild(itemSource)
            itemDestIndex = itemDest.parent.indexOfChild(itemDest)
            print(itemSourceIndex, itemDestIndex)
            itemSource.parent.takeChild(itemSourceIndex)
            itemDest.parent.insertChild(itemDestIndex, itemSource)

    def itemRightClicked(self, item, pos):
        ItemRightClickMenu(item, self.parent.config, pos, self.changeInputMappingUI, self.addItem, self.removeItem)

    def headerRightClicked(self, header, pos):
        HeaderRightClickMenu(header, self.parent.config, pos, self.addItem)

    def itemLeftClicked(self, item, pos):
        self.changeInputMappingUI(item)

class TreeItem(QTreeWidgetItem):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.parent = parent
        self.config = config
        self.updateText()

    def updateText(self):
        itemText = "{} as {}".format(self.config.inputType, self.config.outputType).title()
        self.setText(0, itemText)
        if self.config:
            self.setText(1, self.config.outputMapping().title())

class HeaderItem(QTreeWidgetItem):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.parent = parent
        self.setText(0, text)

class ItemRightClickMenu(QMenu):
    def __init__(self, item, config, pos, editFunc, dupeFunc, deleteFunc):
        super().__init__()
        self.item = item
        self.config = config
        self.editFunc = editFunc
        self.dupeFunc = dupeFunc
        self.deleteFunc = deleteFunc
        self.editAction = QAction("Edit", self)
        self.editAction.triggered.connect(self.editConfig)
        self.addAction(self.editAction)
        self.dupeAction = QAction("Duplicate {} : {}".format(self.item.text(0), self.item.text(1)), self)
        self.dupeAction.triggered.connect(self.duplicateConfig)
        self.addAction(self.dupeAction)
        self.deleteAction = QAction("Delete", self)
        self.deleteAction.triggered.connect(self.deleteConfig)
        self.addAction(self.deleteAction)
        self.exec(pos)

    def editConfig(self):
        self.editFunc(self.item)

    def duplicateConfig(self):
        newConfig = copy.copy(self.item.config)
        newItem = TreeItem(self.item.parent, newConfig)
        self.config.configurations.append(newConfig)
        self.dupeFunc(self.item.parent, self.item)

    def deleteConfig(self):
        self.config.configurations.pop(self.config.configurations.index(self.item.config))
        self.deleteFunc(self.item.parent, self.item)

class HeaderRightClickMenu(QMenu):
    def __init__(self, header, config, pos, newConfigFunc):
        super().__init__()
        self.header = header
        self.config = config
        self.newConfigFunc = newConfigFunc

        self.newMenu = QMenu("New", self)
        self.newButtonConfigAction = QAction("Button Configuration", self.newMenu)
        self.newJoystickConfigAction = QAction("Joystick Configuration", self.newMenu)
        self.newEncoderConfigAction = QAction("Encoder Configuration", self.newMenu)
        self.newGyroConfigAction = QAction("Gyro Configuration", self.newMenu)
        
        self.newButtonConfigAction.triggered.connect(self.newButtonConfig)
        self.newJoystickConfigAction.triggered.connect(self.newJoystickConfig)
        self.newEncoderConfigAction.triggered.connect(self.newEncoderConfg)
        self.newGyroConfigAction.triggered.connect(self.newGyroConfig)
        
        self.newMenu.addAction(self.newButtonConfigAction)
        self.newMenu.addAction(self.newJoystickConfigAction)
        self.newMenu.addAction(self.newEncoderConfigAction)
        self.newMenu.addAction(self.newGyroConfigAction)

        self.addMenu(self.newMenu)
        self.exec(pos)

    def newButtonConfig(self):
        NewConfigWizard(self.header.parent, self.config, self.newConfigFunc, -1)

    def newJoystickConfig(self):
        NewConfigWizard(self.header.parent, self.config, self.newConfigFunc, 1)

    def newEncoderConfg(self):
        NewConfigWizard(self.header.parent, self.config, self.newConfigFunc, 2)

    def newGyroConfig(self):
        NewConfigWizard(self.header.parent, self.config, self.newConfigFunc, 3)

class NewConfigWizard(QWizard):
    def __init__(self, config, mappingList, newConfigFunc, preSelectedOption):
        super().__init__()
        self.config = config
        self.newConfigFunc = newConfigFunc
        self.inputSelection = -1
        self.addPage(NewConfigStartWizardPage(self, preSelectedOption))
        self.exec()

class NewConfigStartWizardPage(QWizardPage):
    def __init__(self, parent, preSelectedOption):
        super().__init__(parent)
        self.parent = parent
        self.setTitle("New Input Mapping")
        self.setSubTitle("Select the input configuration to map.")
        self.initUI(preSelectedOption)

    def initUI(self, preSelectedOption):
        self.layout = QVBoxLayout(self)

        self.group = QGroupBox(self)
        self.group.setTitle("Input Mapping")
        self.groupLayout = QVBoxLayout(self.group)

        self.buttonGroup = QButtonGroup(self)

        self.button = QRadioButton("Button Mapping")
        self.joystick = QRadioButton("Joystick Mapping")
        self.encoder = QRadioButton("Encoder Mapping")
        self.gyro = QRadioButton("Gyro Mapping")

        self.buttonGroup.addButton(self.button)
        self.buttonGroup.addButton(self.joystick)
        self.buttonGroup.addButton(self.encoder)
        self.buttonGroup.addButton(self.gyro)

        if preSelectedOption > -1:
            self.buttonGroup.buttons()[preSelectedOption].setChecked(True)

        self.groupLayout.addWidget(self.button)
        self.groupLayout.addWidget(self.joystick)
        self.groupLayout.addWidget(self.encoder)
        self.groupLayout.addWidget(self.gyro)

        self.layout.addWidget(self.group)

        self.buttonBox = QComboBox(self)
        self.buttonBox.addItems(["As Button", "As Joystick", "As Keyboard", "As Trigger"])
        self.buttonBox.currentIndexChanged.connect(self.updateText)
        self.layout.addWidget(self.buttonBox)

        self.group = QGroupBox("Description")

    def updateText(self):
        print(self.buttonBox.currentIndex())

    def validatePage(self):
        if self.buttonGroup.checkedButton():
            return True
        else:
            return False

if __name__ == "__main__":
    #Initialize the serial controller
    serialController = SerialController()

    #Initialize the Application window
    app = QApplication()

    #Import the application styling
    with open(QSS_FILE, "r") as f:
        appStyle = f.read()
        app.setStyleSheet(appStyle)

    #Initialize the main window
    main = MainWindow(app, serialController)
    main.resize(1200, 800)
    main.show()

    app.exec()
