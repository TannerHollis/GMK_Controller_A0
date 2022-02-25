import sys
from PySide6 import QtGui, QtQuick
from PySide6.QtWidgets import *
from PySide6.QtGui import QGuiApplication, QAction, QPixmap, QPalette, QPainter, QColor
from PySide6.QtCore import QTimer, Slot, Qt, QCoreApplication, QSize
from serial_classes import *
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
    def __init__(self, app, serial_controller):
        super().__init__()
        self.app = app
        self.serial_controller = serial_controller
        
        self.config = Controller_Configuration.from_file(DEFAULT_CFG_FILE)
        self.initUI()
        self.setWindowTitle("GMK Controller Configuration Tool")

    def initUI(self):
        self.menubar = self.menuBar()
        self.file_menu = FileMenu(self)
        self.menubar.addMenu(self.file_menu)
        
        self.central_widget = QWidget(self)
        self.layout = QHBoxLayout(self.central_widget)

        self.controller_view = ControllerView(self)
        self.layout.addWidget(self.controller_view)
        
        self.input_mapping_column = InputMappingColumn(self)
        self.layout.addWidget(self.input_mapping_column)
        
        self.setCentralWidget(self.central_widget)       

    def paintEvent(self, event):
        self.paintBackground()

    def paintBackground(self):
        self.background = QPixmap(BACKGROUND_IMAGE_FILE).scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.background_transparent = QPixmap(self.width(), self.height())
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.setOpacity(0.15)
        self.painter.drawPixmap((self.width() - self.background.width())/2, (self.height() - self.background.height())/2, self.background)
        self.painter.end()

    def exit(self):
        QCoreApplication.quit()

    def open(self):
        (file_name, file_type) = QFileDialog.getOpenFileName(self, "Open Configuration", CONFIG_FOLDER, "Configurations (*.cfg)")
        if not file_name:
            return
        try:
            self.config = Controller_Configuration.from_file(file_name)
        except Exception as e:
            ErrorMessageBox("Error Opening File", e, QMessageBox.Ok)
            return
        self.input_mapping_column.mapping_list.populateTree(self.config)
        
    def save(self):
        (file_name, file_type) = QFileDialog.getSaveFileName(self, "Save Configuration", CONFIG_FOLDER, "Configurations (*.cfg)")
        print(file_name)

class FileMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setTitle("&File")
        self.initUI()

    def initUI(self):
        self.new_action = QAction("New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.addAction(self.new_action)

        self.open_action = QAction("Open...", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.parent.open)
        self.addAction(self.open_action)

        self.save_action = QAction("Save...", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.parent.save)
        self.addAction(self.save_action)

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+W")
        self.exit_action.triggered.connect(self.parent.exit)
        self.addAction(self.exit_action)
        
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

        self.view_top = ControllerTopView(self)
        self.view_bottom = ControllerBottomView(self)
        
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
        self.current_mapping = -1
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        self.input_mapping = QGroupBox(self)
        self.input_mapping.setMinimumHeight(400)
        self.input_mapping.setMaximumHeight(500)
        self.input_mapping.setTitle("Configuration Mapping")
        self.layout.addWidget(self.input_mapping, alignment=Qt.AlignTop)

        self.input_mapping_layout = QVBoxLayout(self.input_mapping)
        self.populate_input_mapping_list()
        self.change_input_mapping_ui(None)
        
        self.mapping_list = MappingList(self.parent, self.change_input_mapping_ui)
        self.layout.addWidget(self.mapping_list)
        
        self.device_connection_editor = DeviceConnectionEditor(self.parent)
        self.layout.addWidget(self.device_connection_editor, alignment=Qt.AlignTop)

    def populate_input_mapping_list(self):
        self.input_mapping_list = []
        self.input_mapping_list.append(InputMappingDefault(self, None))
        self.input_mapping_list.append(InputMappingButtonAsButton(self, None))
        self.input_mapping_list.append(InputMappingButtonAsJoystick(self, None))
        self.input_mapping_list.append(InputMappingButtonAsKeyboard(self, None))
        self.input_mapping_list.append(InputMappingButtonAsTrigger(self, None))
        self.input_mapping_list.append(InputMappingJoystickAsButton(self, None))
        self.input_mapping_list.append(InputMappingJoystickAsJoystick(self, None))
        self.input_mapping_list.append(InputMappingJoystickAsKeyboard(self, None))
        self.input_mapping_list.append(InputMappingJoystickAsTrigger(self, None))
        self.input_mapping_list.append(InputMappingEncoderAsButton(self, None))
        self.input_mapping_list.append(InputMappingEncoderAsJoystick(self, None))
        
        for mapping in self.input_mapping_list:
            self.input_mapping_layout.addWidget(mapping)

    def change_input_mapping_ui(self, item):
        self.input_mapping_list[self.current_mapping+1].close_mapping()
        if item:
            self.current_mapping = item.config.type
        else:
            self.current_mapping = -1
        self.input_mapping_list[self.current_mapping+1].show_mapping(item)

class InputMappingDefault(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)
        self.label = QLabel("Select an input mapping or create a new one to get started.")
        self.layout.addWidget(self.label, 0, 0, Qt.AlignCenter)

    def show_mapping(self, tree_item):
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingButtonAsButton(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        button_nums = [i for i in range(14)]
        button_inputs = ["Button {}".format(i) for i in button_nums]
        button_outputs = [map_output_button(i).title() for i in button_nums]

        self.button_in_label = QLabel("Input Button")
        self.layout.addWidget(self.button_in_label, 0, 0, Qt.AlignRight)
        
        self.button_in = QComboBox(self)
        self.button_in.addItems(button_inputs)
        self.button_in.currentIndexChanged.connect(self.change_button_in)
        self.layout.addWidget(self.button_in, 0, 1)

        self.button_out_label = QLabel("Output Button")
        self.layout.addWidget(self.button_out_label, 1, 0, Qt.AlignRight)

        self.button_out = QComboBox(self)
        self.button_out.addItems(button_outputs)
        self.button_out.currentIndexChanged.connect(self.change_button_out)
        self.layout.addWidget(self.button_out, 1, 1)

    def change_button_in(self, index):
        self.tree_item.config.button_in = index
        self.tree_item.updateText()

    def change_button_out(self, index):
        self.tree_item.config.button_out = index
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.button_in.setCurrentIndex(self.tree_item.config.button_in)
        self.button_out.setCurrentIndex(self.tree_item.config.button_out)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingButtonAsJoystick(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        button_nums = [i for i in range(14)]
        button_inputs = ["Button {}".format(i) for i in button_nums]
        joystick_outputs = ["Left Joystick", "Right Joystick"]
        axis_outputs = ["X", "Y"]
        pos_negs = ["Positive", "Negative"]

        self.button_in_label = QLabel("Input Button")
        self.layout.addWidget(self.button_in_label, 0, 0, Qt.AlignRight)
        
        self.button_in = QComboBox(self)
        self.button_in.addItems(button_inputs)
        self.button_in.currentIndexChanged.connect(self.change_button_in)
        self.layout.addWidget(self.button_in, 0, 1)

        self.joystick_lr_label = QLabel("Output Joystick")
        self.layout.addWidget(self.joystick_lr_label, 1, 0, Qt.AlignRight)

        self.joystick_lr = QComboBox(self)
        self.joystick_lr.addItems(joystick_outputs)
        self.joystick_lr.currentIndexChanged.connect(self.change_joystick_lr)
        self.layout.addWidget(self.joystick_lr, 1, 1)

        self.axis_xy_label = QLabel("Output Axis")
        self.layout.addWidget(self.axis_xy_label, 2, 0, Qt.AlignRight)

        self.axis_xy = QComboBox(self)
        self.axis_xy.addItems(axis_outputs)
        self.axis_xy.currentIndexChanged.connect(self.change_axis_xy)
        self.layout.addWidget(self.axis_xy, 2, 1)

        self.pos_neg_label = QLabel("Positive/Negative")
        self.layout.addWidget(self.pos_neg_label, 3, 0, Qt.AlignRight)

        self.pos_neg = QComboBox(self)
        self.pos_neg.addItems(pos_negs)
        self.pos_neg.currentIndexChanged.connect(self.change_pos_neg)
        self.layout.addWidget(self.pos_neg, 3, 1)

    def change_button_in(self, index):
        self.tree_item.config.button_in = index
        self.tree_item.updateText()

    def change_joystick_lr(self, index):
        self.tree_item.config.joystick_lr = index
        self.tree_item.updateText()

    def change_axis_xy(self, index):
        self.tree_item.config.axis_xy = index
        self.tree_item.updateText()

    def change_pos_neg(self, index):
        self.tree_item.config.pos_neg = index
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.button_in.setCurrentIndex(self.tree_item.config.button_in)
        self.joystick_lr.setCurrentIndex(self.tree_item.config.joystick_lr)
        self.axis_xy.setCurrentIndex(self.tree_item.config.axis_xy)
        self.pos_neg.setCurrentIndex(self.tree_item.config.pos_neg)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingButtonAsKeyboard(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        button_nums = [i for i in range(14)]
        button_inputs = ["Button {}".format(i) for i in button_nums]

        self.button_in_label = QLabel("Input Button")
        self.layout.addWidget(self.button_in_label, 0, 0, Qt.AlignRight)
        
        self.button_in = QComboBox(self)
        self.button_in.addItems(button_inputs)
        self.button_in.currentIndexChanged.connect(self.change_button_in)
        self.layout.addWidget(self.button_in, 0, 1)

        self.keypress_label = QLabel("Keypress")
        self.layout.addWidget(self.keypress_label, 1, 0, Qt.AlignRight)

        self.keypress = QLineEdit(self)
        self.keypress.textChanged.connect(self.change_string)
        self.layout.addWidget(self.keypress, 1, 1)
        

    def change_button_in(self, index):
        self.tree_item.config.button_in = index
        self.tree_item.updateText()

    def change_string(self, arg__1):
        self.tree_item.config.string = arg__1
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.button_in.setCurrentIndex(self.tree_item.config.button_in)
        self.keypress.setText(self.tree_item.config.string)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingButtonAsTrigger(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        button_nums = [i for i in range(14)]
        button_inputs = ["Button {}".format(i) for i in button_nums]
        trigger_lrs = ["Left Trigger", "Right Trigger"]

        self.button_in_label = QLabel("Input Button")
        self.layout.addWidget(self.button_in_label, 0, 0, Qt.AlignRight)
        
        self.button_in = QComboBox(self)
        self.button_in.addItems(button_inputs)
        self.button_in.currentIndexChanged.connect(self.change_button_in)
        self.layout.addWidget(self.button_in, 0, 1)

        self.trigger_lr_label = QLabel("Output Trigger")
        self.layout.addWidget(self.trigger_lr_label, 1, 0, Qt.AlignRight)

        self.trigger_lr = QComboBox(self)
        self.trigger_lr.addItems(trigger_lrs)
        self.trigger_lr.currentIndexChanged.connect(self.change_trigger_lr)
        self.layout.addWidget(self.trigger_lr, 1, 1)
        

    def change_button_in(self, index):
        self.tree_item.config.button_in = index
        self.tree_item.updateText()

    def change_trigger_lr(self, index):
        self.tree_item.config.trigger_lr = index
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.button_in.setCurrentIndex(self.tree_item.config.button_in)
        self.trigger_lr.setCurrentIndex(self.tree_item.config.trigger_lr)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingJoystickAsButton(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        joystick_outputs = ["Left Joystick", "Right Joystick"]
        axis_outputs = ["X", "Y"]
        pos_negs = ["Positive", "Negative"]
        button_nums = [i for i in range(14)]
        button_outputs = [map_output_button(i).title() for i in button_nums]

        self.joystick_lr_label = QLabel("Input Joystick")
        self.layout.addWidget(self.joystick_lr_label, 0, 0, Qt.AlignRight)

        self.joystick_lr = QComboBox(self)
        self.joystick_lr.addItems(joystick_outputs)
        self.joystick_lr.currentIndexChanged.connect(self.change_joystick_lr)
        self.layout.addWidget(self.joystick_lr, 0, 1)

        self.axis_xy_label = QLabel("Input Axis")
        self.layout.addWidget(self.axis_xy_label, 1, 0, Qt.AlignRight)

        self.axis_xy = QComboBox(self)
        self.axis_xy.addItems(axis_outputs)
        self.axis_xy.currentIndexChanged.connect(self.change_axis_xy)
        self.layout.addWidget(self.axis_xy, 1, 1)

        self.pos_neg_label = QLabel("Positive/Negative")
        self.layout.addWidget(self.pos_neg_label, 2, 0, Qt.AlignRight)

        self.pos_neg = QComboBox(self)
        self.pos_neg.addItems(pos_negs)
        self.pos_neg.currentIndexChanged.connect(self.change_pos_neg)
        self.layout.addWidget(self.pos_neg, 2, 1)

        self.invert_label = QLabel("Invert Input Axis")
        self.layout.addWidget(self.invert_label, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.change_invert)
        self.layout.addWidget(self.invert, 3, 1)

        self.threshold_label = QLabel("Threshold")
        self.layout.addWidget(self.threshold_label, 4, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.change_threshold)
        self.threshold.setRange(0, 1000)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 4, 1)

        self.threshold_val = QLabel("")
        self.threshold_val.setMinimumWidth(50)
        self.layout.addWidget(self.threshold_val, 4, 2, Qt.AlignLeft)

        self.button_out_label = QLabel("Output Button")
        self.layout.addWidget(self.button_out_label, 5, 0, Qt.AlignRight)

        self.button_out = QComboBox(self)
        self.button_out.addItems(button_outputs)
        self.button_out.currentIndexChanged.connect(self.change_button_out)
        self.layout.addWidget(self.button_out, 5, 1)

    def change_joystick_lr(self, index):
        self.tree_item.config.joystick_lr = index
        self.tree_item.updateText()

    def change_axis_xy(self, index):
        self.tree_item.config.axis_xy = index
        self.tree_item.updateText()

    def change_pos_neg(self, index):
        self.tree_item.config.pos_neg = index
        self.tree_item.updateText()

    def change_invert(self, arg__1):
        self.tree_item.config.invert = arg__1
        self.tree_item.updateText()

    def change_threshold(self, arg__1):
        self.tree_item.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3)))
        self.tree_item.updateText()

    def change_button_out(self, index):
        self.tree_item.config.button_out = index
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.joystick_lr.setCurrentIndex(self.tree_item.config.joystick_lr)
        self.axis_xy.setCurrentIndex(self.tree_item.config.axis_xy)
        self.pos_neg.setCurrentIndex(self.tree_item.config.pos_neg)
        if self.tree_item.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3)))
        self.button_out.setCurrentIndex(self.tree_item.config.button_out)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingJoystickAsJoystick(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        joystick_options = ["Left Joystick", "Right Joystick"]
        axis_outputs = ["X", "Y"]
        pos_negs = ["Positive", "Negative"]

        self.joystick_in_label = QLabel("Input Joystick")
        self.layout.addWidget(self.joystick_in_label, 0, 0, Qt.AlignRight)

        self.joystick_in = QComboBox(self)
        self.joystick_in.addItems(joystick_options)
        self.joystick_in.currentIndexChanged.connect(self.change_joystick_in)
        self.layout.addWidget(self.joystick_in, 0, 1)

        self.invert_x_label = QLabel("Invert X Axis")
        self.layout.addWidget(self.invert_x_label, 1, 0 ,Qt.AlignRight)

        self.invert_x = QCheckBox(self)
        self.invert_x.stateChanged.connect(self.change_invert_x)
        self.layout.addWidget(self.invert_x, 1, 1)

        self.invert_y_label = QLabel("Invert Y Axis")
        self.layout.addWidget(self.invert_y_label, 2, 0 ,Qt.AlignRight)

        self.invert_y = QCheckBox(self)
        self.invert_y.stateChanged.connect(self.change_invert_y)
        self.layout.addWidget(self.invert_y, 2, 1)

        self.deadzone_x_label = QLabel("X Deadzone")
        self.layout.addWidget(self.deadzone_x_label, 3, 0, Qt.AlignRight)

        self.deadzone_x = QSlider(self)
        self.deadzone_x.sliderMoved.connect(self.change_deadzone_x)
        self.deadzone_x.setRange(0, 1000)
        self.deadzone_x.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.deadzone_x, 3, 1)

        self.deadzone_x_val = QLabel("")
        self.deadzone_x_val.setMinimumWidth(50)
        self.layout.addWidget(self.deadzone_x_val, 3, 2, Qt.AlignLeft)

        self.deadzone_y_label = QLabel("Y Deadzone")
        self.layout.addWidget(self.deadzone_y_label, 4, 0, Qt.AlignRight)

        self.deadzone_y = QSlider(self)
        self.deadzone_y.sliderMoved.connect(self.change_deadzone_y)
        self.deadzone_y.setRange(0, 1000)
        self.deadzone_y.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.deadzone_y, 4, 1)

        self.deadzone_y_val = QLabel("")
        self.deadzone_y_val.setMinimumWidth(50)
        self.layout.addWidget(self.deadzone_y_val, 4, 2, Qt.AlignLeft)

        self.joystick_out_label = QLabel("Output Joystick")
        self.layout.addWidget(self.joystick_out_label, 5, 0, Qt.AlignRight)

        self.joystick_out = QComboBox(self)
        self.joystick_out.addItems(joystick_options)
        self.joystick_out.currentIndexChanged.connect(self.change_joystick_out)
        self.layout.addWidget(self.joystick_out, 5, 1)

    def change_joystick_in(self, index):
        self.tree_item.config.joystick_lr = index
        self.tree_item.updateText()

    def change_invert_x(self, index):
        self.tree_item.config.invert_x = index
        self.tree_item.updateText()

    def change_invert_y(self, index):
        self.tree_item.config.invert_y = index
        self.tree_item.updateText()

    def change_joystick_out(self, index):
        self.tree_item.config.joystick_out = index
        self.tree_item.updateText()

    def change_deadzone_x(self, arg__1):
        self.tree_item.config.deadzone_x = float(arg__1) / 1000.0
        self.deadzone_x.setValue(int(self.tree_item.config.deadzone_x * 1000))
        self.deadzone_x_val.setText(str(round(self.tree_item.config.deadzone_x, 3)))
        self.tree_item.updateText()

    def change_deadzone_y(self, arg__1):
        self.tree_item.config.deadzone_y = float(arg__1) / 1000.0
        self.deadzone_y.setValue(int(self.tree_item.config.deadzone_y * 1000))
        self.deadzone_y_val.setText(str(round(self.tree_item.config.deadzone_y, 3)))
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.joystick_in.setCurrentIndex(self.tree_item.config.joystick_in)
        self.joystick_out.setCurrentIndex(self.tree_item.config.joystick_out)
        if self.tree_item.config.invert_x:
            self.invert_x.setCheckState(Qt.Checked)
        else:
            self.invert_x.setCheckState(Qt.Unchecked)
        if self.tree_item.config.invert_y:
            self.invert_y.setCheckState(Qt.Checked)
        else:
            self.invert_y.setCheckState(Qt.Unchecked)
        self.deadzone_x.setValue(int(self.tree_item.config.deadzone_x * 1000))
        self.deadzone_x_val.setText(str(round(self.tree_item.config.deadzone_x, 3)))
        self.deadzone_y.setValue(int(self.tree_item.config.deadzone_y * 1000))
        self.deadzone_y_val.setText(str(round(self.tree_item.config.deadzone_y, 3)))
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingJoystickAsKeyboard(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        joystick_outputs = ["Left Joystick", "Right Joystick"]
        axis_outputs = ["X", "Y"]
        pos_negs = ["Positive", "Negative"]

        self.joystick_lr_label = QLabel("Input Joystick")
        self.layout.addWidget(self.joystick_lr_label, 0, 0, Qt.AlignRight)

        self.joystick_lr = QComboBox(self)
        self.joystick_lr.addItems(joystick_outputs)
        self.joystick_lr.currentIndexChanged.connect(self.change_joystick_lr)
        self.layout.addWidget(self.joystick_lr, 0, 1)

        self.axis_xy_label = QLabel("Input Axis")
        self.layout.addWidget(self.axis_xy_label, 1, 0, Qt.AlignRight)

        self.axis_xy = QComboBox(self)
        self.axis_xy.addItems(axis_outputs)
        self.axis_xy.currentIndexChanged.connect(self.change_axis_xy)
        self.layout.addWidget(self.axis_xy, 1, 1)

        self.pos_neg_label = QLabel("Positive/Negative")
        self.layout.addWidget(self.pos_neg_label, 2, 0, Qt.AlignRight)

        self.pos_neg = QComboBox(self)
        self.pos_neg.addItems(pos_negs)
        self.pos_neg.currentIndexChanged.connect(self.change_pos_neg)
        self.layout.addWidget(self.pos_neg, 2, 1)

        self.invert_label = QLabel("Invert Input Axis")
        self.layout.addWidget(self.invert_label, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.change_invert)
        self.layout.addWidget(self.invert, 3, 1)

        self.threshold_label = QLabel("Threshold")
        self.layout.addWidget(self.threshold_label, 4, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.change_threshold)
        self.threshold.setRange(0, 1000)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 4, 1)

        self.threshold_val = QLabel("")
        self.threshold_val.setMinimumWidth(50)
        self.layout.addWidget(self.threshold_val, 4, 2, Qt.AlignLeft)

        self.keypress_label = QLabel("Keypress")
        self.layout.addWidget(self.keypress_label, 5, 0, Qt.AlignRight)

        self.keypress = QLineEdit(self)
        self.keypress.setText("")
        self.keypress.textChanged.connect(self.change_string)
        self.layout.addWidget(self.keypress, 5, 1)

    def change_joystick_lr(self, index):
        self.tree_item.config.joystick_in = index
        self.tree_item.updateText()

    def change_axis_xy(self, index):
        self.tree_item.config.axis_xy = index
        self.tree_item.updateText()

    def change_pos_neg(self, index):
        self.tree_item.config.pos_neg = index
        self.tree_item.updateText()

    def change_invert(self, arg__1):
        self.tree_item.config.invert = arg__1
        self.tree_item.updateText()

    def change_threshold(self, arg__1):
        self.tree_item.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3)))
        self.tree_item.updateText()

    def change_string(self, arg__1):
        self.tree_item.config.string = arg__1
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.joystick_lr.setCurrentIndex(self.tree_item.config.joystick_in)
        self.axis_xy.setCurrentIndex(self.tree_item.config.axis_xy)
        self.pos_neg.setCurrentIndex(self.tree_item.config.pos_neg)
        if self.tree_item.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3)))
        self.keypress.setText(self.tree_item.config.string)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingJoystickAsTrigger(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        joystick_outputs = ["Left Joystick", "Right Joystick"]
        axis_outputs = ["X", "Y"]
        pos_negs = ["Positive", "Negative"]
        trigger_lrs = ["Left Trigger", "Right Trigger"]

        self.joystick_lr_label = QLabel("Input Joystick")
        self.layout.addWidget(self.joystick_lr_label, 0, 0, Qt.AlignRight)

        self.joystick_lr = QComboBox(self)
        self.joystick_lr.addItems(joystick_outputs)
        self.joystick_lr.currentIndexChanged.connect(self.change_joystick_lr)
        self.layout.addWidget(self.joystick_lr, 0, 1)

        self.axis_xy_label = QLabel("Input Axis")
        self.layout.addWidget(self.axis_xy_label, 1, 0, Qt.AlignRight)

        self.axis_xy = QComboBox(self)
        self.axis_xy.addItems(axis_outputs)
        self.axis_xy.currentIndexChanged.connect(self.change_axis_xy)
        self.layout.addWidget(self.axis_xy, 1, 1)

        self.pos_neg_label = QLabel("Positive/Negative")
        self.layout.addWidget(self.pos_neg_label, 2, 0, Qt.AlignRight)

        self.pos_neg = QComboBox(self)
        self.pos_neg.addItems(pos_negs)
        self.pos_neg.currentIndexChanged.connect(self.change_pos_neg)
        self.layout.addWidget(self.pos_neg, 2, 1)

        self.invert_label = QLabel("Invert Input Axis")
        self.layout.addWidget(self.invert_label, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.change_invert)
        self.layout.addWidget(self.invert, 3, 1)

        self.threshold_label = QLabel("Threshold")
        self.layout.addWidget(self.threshold_label, 4, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.change_threshold)
        self.threshold.setRange(0, 1000)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 4, 1)

        self.threshold_val = QLabel("")
        self.threshold_val.setMinimumWidth(50)
        self.layout.addWidget(self.threshold_val, 4, 2, Qt.AlignLeft)

        self.trigger_lr_label = QLabel("Output Trigger")
        self.layout.addWidget(self.trigger_lr_label, 5, 0, Qt.AlignRight)

        self.trigger_lr = QComboBox(self)
        self.trigger_lr.addItems(trigger_lrs)
        self.trigger_lr.currentIndexChanged.connect(self.change_trigger_lr)
        self.layout.addWidget(self.trigger_lr, 5, 1)

    def change_joystick_lr(self, index):
        self.tree_item.config.joystick_in = index
        self.tree_item.updateText()

    def change_axis_xy(self, index):
        self.tree_item.config.axis_xy = index
        self.tree_item.updateText()

    def change_pos_neg(self, index):
        self.tree_item.config.pos_neg = index
        self.tree_item.updateText()

    def change_invert(self, arg__1):
        self.tree_item.config.invert = arg__1
        self.tree_item.updateText()

    def change_threshold(self, arg__1):
        self.tree_item.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3)))
        self.tree_item.updateText()

    def change_trigger_lr(self, index):
        self.tree_item.config.trigger_out = index
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.joystick_lr.setCurrentIndex(self.tree_item.config.joystick_in)
        self.axis_xy.setCurrentIndex(self.tree_item.config.axis_xy)
        self.pos_neg.setCurrentIndex(self.tree_item.config.pos_neg)
        if self.tree_item.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3)))
        self.trigger_lr.setCurrentIndex(self.tree_item.config.trigger_out)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingEncoderAsButton(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        speed_baseds = ["Direction Based", "Speed Based"]
        directions = ["Clockwise", "Counter Clockwise"]
        button_nums = [i for i in range(14)]
        button_outputs = [map_output_button(i).title() for i in button_nums]

        self.speed_based_label = QLabel("Encoder Functionality")
        self.layout.addWidget(self.speed_based_label, 0, 0, Qt.AlignRight)

        self.speed_based = QComboBox(self)
        self.speed_based.addItems(speed_baseds)
        self.speed_based.currentIndexChanged.connect(self.change_speed_based)
        self.layout.addWidget(self.speed_based, 0, 1)

        self.ccw_label = QLabel("Direction")
        self.layout.addWidget(self.ccw_label, 1, 0, Qt.AlignRight)

        self.ccw = QComboBox(self)
        self.ccw.addItems(directions)
        self.ccw.currentIndexChanged.connect(self.change_ccw)
        self.layout.addWidget(self.ccw, 1, 1)

        self.invert_label = QLabel("Invert Direction")
        self.layout.addWidget(self.invert_label, 2, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.change_invert)
        self.layout.addWidget(self.invert, 2, 1)

        self.threshold_label = QLabel("Speed Threshold")
        self.layout.addWidget(self.threshold_label, 3, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.change_threshold)
        self.threshold.setRange(0, 20e3)
        self.threshold.setTickInterval(5)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 3, 1)

        self.threshold_val = QLabel("")
        self.threshold_val.setMinimumWidth(50)
        self.layout.addWidget(self.threshold_val, 3, 2, Qt.AlignLeft)

        self.trigger_lr_label = QLabel("Output Button")
        self.layout.addWidget(self.trigger_lr_label, 5, 0, Qt.AlignRight)

        self.button_out = QComboBox(self)
        self.button_out.addItems(button_outputs)
        self.button_out.currentIndexChanged.connect(self.change_button_out)
        self.layout.addWidget(self.button_out, 5, 1)

    def change_speed_based(self, index):
        self.tree_item.config.speed_based = index
        self.tree_item.updateText()

    def change_ccw(self, index):
        self.tree_item.config.ccw = index
        self.tree_item.updateText()

    def change_invert(self, arg__1):
        self.tree_item.config.invert = arg__1
        self.tree_item.updateText()

    def change_threshold(self, arg__1):
        self.tree_item.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3))+" Hz")
        self.tree_item.updateText()

    def change_button_out(self, index):
        self.tree_item.config.button_out = index
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.speed_based.setCurrentIndex(self.tree_item.config.speed_based)
        self.ccw.setCurrentIndex(self.tree_item.config.ccw)
        if self.tree_item.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3))+" Hz")
        self.button_out.setCurrentIndex(self.tree_item.config.button_out)
        self.show()

    def close_mapping(self):
        self.close()

class InputMappingEncoderAsJoystick(QWidget):
    def __init__(self, parent, tree_item):
        super().__init__(parent)
        self.parent = parent
        self.tree_item = tree_item
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        binary_baseds = ["Binary Based", "Linear Based"]
        speed_baseds = ["Direction Based", "Speed Based"]
        directions = ["Clockwise", "Counter Clockwise"]
        joystick_outputs = ["Left Joystick", "Right Joystick"]
        axis_outputs = ["X", "Y"]
        pos_negs = ["Positive", "Negative"]

        self.binary_based_label = QLabel("Binary/Linear Functionality")
        self.layout.addWidget(self.binary_based_label, 0, 0, Qt.AlignRight)

        self.binary_based = QComboBox(self)
        self.binary_based.addItems(binary_baseds)
        self.binary_based.currentIndexChanged.connect(self.change_binary_based)
        self.layout.addWidget(self.binary_based, 0, 1)

        self.speed_based_label = QLabel("Encoder Functionality")
        self.layout.addWidget(self.speed_based_label, 1, 0, Qt.AlignRight)

        self.speed_based = QComboBox(self)
        self.speed_based.addItems(speed_baseds)
        self.speed_based.currentIndexChanged.connect(self.change_speed_based)
        self.layout.addWidget(self.speed_based, 1, 1)

        self.ccw_label = QLabel("Direction")
        self.layout.addWidget(self.ccw_label, 2, 0, Qt.AlignRight)

        self.ccw = QComboBox(self)
        self.ccw.addItems(directions)
        self.ccw.currentIndexChanged.connect(self.change_ccw)
        self.layout.addWidget(self.ccw, 2, 1)

        self.invert_label = QLabel("Invert Direction")
        self.layout.addWidget(self.invert_label, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.change_invert)
        self.layout.addWidget(self.invert, 3, 1)

        self.threshold_label = QLabel("Speed Threshold")
        self.layout.addWidget(self.threshold_label, 4, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.change_threshold)
        self.threshold.setRange(0, 20e3)
        self.threshold.setTickInterval(5)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 4, 1)

        self.threshold_val = QLabel("")
        self.threshold_val.setMinimumWidth(50)
        self.layout.addWidget(self.threshold_val, 4, 2, Qt.AlignLeft)

        self.linear_middle_label = QLabel("Linear Middle")
        self.layout.addWidget(self.linear_middle_label, 5, 0, Qt.AlignRight)

        self.linear_middle = QSlider(self)
        self.linear_middle.sliderMoved.connect(self.change_linear_middle)
        self.linear_middle.setRange(0, 1000)
        self.linear_middle.setTickInterval(5)
        self.linear_middle.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.linear_middle, 5, 1)

        self.linear_middle_val = QLabel("")
        self.linear_middle_val.setMinimumWidth(50)
        self.layout.addWidget(self.linear_middle_val, 5, 2, Qt.AlignLeft)

        self.linear_deadzone_label = QLabel("Linear Deadzone")
        self.layout.addWidget(self.linear_deadzone_label, 6, 0, Qt.AlignRight)

        self.linear_deadzone = QSlider(self)
        self.linear_deadzone.sliderMoved.connect(self.change_linear_deadzone)
        self.linear_deadzone.setRange(0, 1000)
        self.linear_deadzone.setTickInterval(5)
        self.linear_deadzone.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.linear_deadzone, 6, 1)

        self.linear_deadzone_val = QLabel("")
        self.linear_deadzone_val.setMinimumWidth(50)
        self.layout.addWidget(self.linear_deadzone_val, 6, 2, Qt.AlignLeft)

        self.joystick_lr_label = QLabel("Output Joystick")
        self.layout.addWidget(self.joystick_lr_label, 7, 0, Qt.AlignRight)

        self.joystick_lr = QComboBox(self)
        self.joystick_lr.addItems(joystick_outputs)
        self.joystick_lr.currentIndexChanged.connect(self.change_joystick_out)
        self.layout.addWidget(self.joystick_lr, 7, 1)

        self.axis_xy_label = QLabel("Output Axis")
        self.layout.addWidget(self.axis_xy_label, 8, 0, Qt.AlignRight)

        self.axis_xy = QComboBox(self)
        self.axis_xy.addItems(axis_outputs)
        self.axis_xy.currentIndexChanged.connect(self.change_axis_xy)
        self.layout.addWidget(self.axis_xy, 8, 1)

        self.pos_neg_label = QLabel("Positive/Negative")
        self.layout.addWidget(self.pos_neg_label, 9, 0, Qt.AlignRight)

        self.pos_neg = QComboBox(self)
        self.pos_neg.addItems(pos_negs)
        self.pos_neg.currentIndexChanged.connect(self.change_pos_neg)
        self.layout.addWidget(self.pos_neg, 9, 1)

    def change_binary_based(self, index):
        self.tree_item.config.binary_based = index
        if self.tree_item.config.binary_based:
            self.ccw.setEnabled(True)
            self.speed_based.setEnabled(True)
            self.threshold.setEnabled(True)
            self.linear_middle.setEnabled(False)
            self.linear_deadzone.setEnabled(False)
        else:
            self.ccw.setEnabled(False)
            self.speed_based.setEnabled(False)
            self.threshold.setEnabled(False)
            self.linear_middle.setEnabled(True)
            self.linear_deadzone.setEnabled(True)
        self.tree_item.updateText()

    def change_speed_based(self, index):
        self.tree_item.config.speed_based = index
        self.tree_item.updateText()

    def change_ccw(self, index):
        self.tree_item.config.ccw = index
        self.tree_item.updateText()

    def change_invert(self, arg__1):
        self.tree_item.config.invert = arg__1
        self.tree_item.updateText()

    def change_threshold(self, arg__1):
        self.tree_item.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.tree_item.config.threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.threshold, 3))+" Hz")
        self.tree_item.updateText()

    def change_linear_middle(self, arg__1):
        self.tree_item.config.linear_middle = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.tree_item.config.linear_middle * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.linear_middle, 3)))
        self.tree_item.updateText()

    def change_linear_deadzone(self, arg__1):
        self.tree_item.config.linear_deadzone = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.tree_item.config.linear_deadzone * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.linear_deadzone, 3)))
        self.tree_item.updateText()

    def change_joystick_out(self, index):
        self.tree_item.config.joystick_out = index
        self.tree_item.updateText()

    def change_axis_xy(self, index):
        self.tree_item.config.axis_xy = index
        self.tree_item.updateText()

    def change_pos_neg(self, index):
        self.tree_item.config.pos_neg = index
        self.tree_item.updateText()

    def show_mapping(self, tree_item):
        self.tree_item = tree_item
        self.binary_based.setCurrentIndex(self.tree_item.config.binary_based)
        self.change_binary_based(self.tree_item.config.binary_based)
        self.speed_based.setCurrentIndex(self.tree_item.config.speed_based)
        self.ccw.setCurrentIndex(self.tree_item.config.ccw)
        if self.tree_item.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.tree_item.config.speed_threshold * 1000))
        self.threshold_val.setText(str(round(self.tree_item.config.speed_threshold, 3))+" Hz")
        self.linear_middle.setValue(int(self.tree_item.config.linear_middle * 1000))
        self.linear_middle_val.setText(str(round(self.tree_item.config.linear_middle, 3)))
        self.linear_deadzone.setValue(int(self.tree_item.config.linear_deadzone * 1000))
        self.linear_deadzone_val.setText(str(round(self.tree_item.config.linear_deadzone, 3)))
        self.joystick_lr.setCurrentIndex(self.tree_item.config.joystick_out)
        self.axis_xy.setCurrentIndex(self.tree_item.config.axis_xy)
        self.pos_neg.setCurrentIndex(self.tree_item.config.pos_neg)
        self.show()

    def close_mapping(self):
        self.close()

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
        for device in Serial_Controller.get_devices():
            self.addItem(device)

class MappingList(QTreeWidget):
    def __init__(self, parent, change_input_mapping_ui):
        super().__init__()
        self.parent = parent
        self.initUI()
        self.setMinimumHeight(200)
        self.change_input_mapping_ui = change_input_mapping_ui

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
        ItemRightClickMenu(item, self.parent.config, pos, self.change_input_mapping_ui, self.removeItem)

    def headerRightClicked(self, header, pos):
        HeaderRightClickMenu(header, self.parent.config, pos, self.populateTree)

    def itemLeftClicked(self, item, pos):
        self.change_input_mapping_ui(item)

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
    serial_controller = Serial_Controller()

    #Initialize the Application window
    app = QApplication()

    #Import the application styling
    with open(QSS_FILE, "r") as f:
        app_style = f.read()
        app.setStyleSheet(app_style)

    #Initialize the main window
    main = MainWindow(app, serial_controller)
    main.resize(1200, 800)
    main.show()

    app.exec()
