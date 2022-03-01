from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ConfigClasses import *

BUTTON_INPUTS = ["Button {}".format(i) for i in [i for i in range(14)]]
BUTTON_OUTPUTS = [mapOutputButton(i).title() for i in [i for i in range(14)]]
JOYSTICK_OUTPUTS = ["Left Joystick", "Right Joystick"]
AXES = ["X", "Y"]
POLARITY = ["Positive", "Negative"]
TRIGGER_OUTPUTS = ["Left Trigger", "Right Trigger"]
ENCODER_FUNCTION_0 = ["Linear Based", "Binary Based (On/Off)"]
ENCODER_FUNCTION_1 = ["Direction Based", "Speed Based"]
ENCODER_DIRECTIONS = ["Clockwise", "Counter Clockwise"]

class InputMappingDefault(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)
        self.label = QLabel("Select an input mapping or create a new one to get started.")
        self.layout.addWidget(self.label, 0, 0, Qt.AlignCenter)

    def showMapping(self, treeItem):
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingButtonAsButton(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)
        self.layout.setVerticalSpacing(0)

        self.buttonInLabel = QLabel("Input Button")
        self.layout.addWidget(self.buttonInLabel, 0, 0, Qt.AlignRight)
        
        self.buttonIn = QComboBox(self)
        self.buttonIn.addItems(BUTTON_INPUTS)
        self.buttonIn.currentIndexChanged.connect(self.changeButtonIn)
        self.layout.addWidget(self.buttonIn, 0, 1)

        self.buttonOutLabel = QLabel("Output Button")
        self.layout.addWidget(self.buttonOutLabel, 1, 0, Qt.AlignRight)

        self.buttonOut = QComboBox(self)
        self.buttonOut.addItems(BUTTON_OUTPUTS)
        self.buttonOut.currentIndexChanged.connect(self.changeButtonOut)
        self.layout.addWidget(self.buttonOut, 1, 1)

    def changeButtonIn(self, index):
        self.treeItem.config.buttonIn = index
        self.treeItem.updateText()

    def changeButtonOut(self, index):
        self.treeItem.config.buttonOut = index
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.buttonIn.setCurrentIndex(self.treeItem.config.buttonIn)
        self.buttonOut.setCurrentIndex(self.treeItem.config.buttonOut)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingButtonAsJoystick(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.buttonInLabel = QLabel("Input Button")
        self.layout.addWidget(self.buttonInLabel, 0, 0, Qt.AlignRight)
        
        self.buttonIn = QComboBox(self)
        self.buttonIn.addItems(BUTTON_INPUTS)
        self.buttonIn.currentIndexChanged.connect(self.changeButtonIn)
        self.layout.addWidget(self.buttonIn, 0, 1)

        self.joystickOutLabel = QLabel("Output Joystick")
        self.layout.addWidget(self.joystickOutLabel, 1, 0, Qt.AlignRight)

        self.joystickOut = QComboBox(self)
        self.joystickOut.addItems(JOYSTICK_OUTPUTS)
        self.joystickOut.currentIndexChanged.connect(self.changeJoystickOut)
        self.layout.addWidget(self.joystickOut, 1, 1)

        self.axisXYLabel = QLabel("Output Axis")
        self.layout.addWidget(self.axisXYLabel, 2, 0, Qt.AlignRight)

        self.axisXY = QComboBox(self)
        self.axisXY.addItems(AXES)
        self.axisXY.currentIndexChanged.connect(self.changeAxisXY)
        self.layout.addWidget(self.axisXY, 2, 1)

        self.posNegLabel = QLabel("Positive/Negative")
        self.layout.addWidget(self.posNegLabel, 3, 0, Qt.AlignRight)

        self.posNeg = QComboBox(self)
        self.posNeg.addItems(POLARITY)
        self.posNeg.currentIndexChanged.connect(self.changePosNeg)
        self.layout.addWidget(self.posNeg, 3, 1)

    def changeButtonIn(self, index):
        self.treeItem.config.buttonIn = index
        self.treeItem.updateText()

    def changeJoystickOut(self, index):
        self.treeItem.config.joystickOut = index
        self.treeItem.updateText()

    def changeAxisXY(self, index):
        self.treeItem.config.axisXY = index
        self.treeItem.updateText()

    def changePosNeg(self, index):
        self.treeItem.config.posNeg = index
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.buttonIn.setCurrentIndex(self.treeItem.config.buttonIn)
        self.joystickOut.setCurrentIndex(self.treeItem.config.joystickOut)
        self.axisXY.setCurrentIndex(self.treeItem.config.axisXY)
        self.posNeg.setCurrentIndex(self.treeItem.config.posNeg)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingButtonAsKeyboard(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.buttonInLabel = QLabel("Input Button")
        self.layout.addWidget(self.buttonInLabel, 0, 0, Qt.AlignRight)
        
        self.buttonIn = QComboBox(self)
        self.buttonIn.addItems(BUTTON_INPUTS)
        self.buttonIn.currentIndexChanged.connect(self.changeButtonIn)
        self.layout.addWidget(self.buttonIn, 0, 1)

        self.keypressLabel = QLabel("Keypress")
        self.layout.addWidget(self.keypressLabel, 1, 0, Qt.AlignRight)

        self.keypress = QLineEdit(self)
        self.keypress.textChanged.connect(self.changeString)
        self.layout.addWidget(self.keypress, 1, 1)
        

    def changeButtonIn(self, index):
        self.treeItem.config.buttonIn = index
        self.treeItem.updateText()

    def changeString(self, arg__1):
        self.treeItem.config.string = arg__1
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.buttonIn.setCurrentIndex(self.treeItem.config.buttonIn)
        self.keypress.setText(self.treeItem.config.string)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingButtonAsTrigger(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.buttonInLabel = QLabel("Input Button")
        self.layout.addWidget(self.buttonInLabel, 0, 0, Qt.AlignRight)
        
        self.buttonIn = QComboBox(self)
        self.buttonIn.addItems(BUTTON_INPUTS)
        self.buttonIn.currentIndexChanged.connect(self.changeButtonIn)
        self.layout.addWidget(self.buttonIn, 0, 1)

        self.triggerOutLabel = QLabel("Output Trigger")
        self.layout.addWidget(self.triggerOutLabel, 1, 0, Qt.AlignRight)

        self.triggerOut = QComboBox(self)
        self.triggerOut.addItems(TRIGGER_OUTPUTS)
        self.triggerOut.currentIndexChanged.connect(self.changeTriggerOut)
        self.layout.addWidget(self.triggerOut, 1, 1)
        

    def changeButtonIn(self, index):
        self.treeItem.config.buttonIn = index
        self.treeItem.updateText()

    def changeTriggerOut(self, index):
        self.treeItem.config.triggerOut = index
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.buttonIn.setCurrentIndex(self.treeItem.config.buttonIn)
        self.triggerOut.setCurrentIndex(self.treeItem.config.triggerOut)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingJoystickAsButton(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.joystickInLabel = QLabel("Input Joystick")
        self.layout.addWidget(self.joystickInLabel, 0, 0, Qt.AlignRight)

        self.joystickIn = QComboBox(self)
        self.joystickIn.addItems(JOYSTICK_OUTPUTS)
        self.joystickIn.currentIndexChanged.connect(self.changeJoystickIn)
        self.layout.addWidget(self.joystickIn, 0, 1)

        self.axisXYLabel = QLabel("Input Axis")
        self.layout.addWidget(self.axisXYLabel, 1, 0, Qt.AlignRight)

        self.axisXY = QComboBox(self)
        self.axisXY.addItems(AXES)
        self.axisXY.currentIndexChanged.connect(self.changeAxisXY)
        self.layout.addWidget(self.axisXY, 1, 1)

        self.posNegLabel = QLabel("Positive/Negative")
        self.layout.addWidget(self.posNegLabel, 2, 0, Qt.AlignRight)

        self.posNeg = QComboBox(self)
        self.posNeg.addItems(POLARITY)
        self.posNeg.currentIndexChanged.connect(self.changePosNeg)
        self.layout.addWidget(self.posNeg, 2, 1)

        self.invertLabel = QLabel("Invert Input Axis")
        self.layout.addWidget(self.invertLabel, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.changeInvert)
        self.layout.addWidget(self.invert, 3, 1)

        self.thresholdLabel = QLabel("Threshold")
        self.layout.addWidget(self.thresholdLabel, 4, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.changeThreshold)
        self.threshold.setRange(0, 1000)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 4, 1)

        self.thresholdVal = QLabel("")
        self.thresholdVal.setMinimumWidth(50)
        self.layout.addWidget(self.thresholdVal, 4, 2, Qt.AlignLeft)

        self.buttonOutLabel = QLabel("Output Button")
        self.layout.addWidget(self.buttonOutLabel, 5, 0, Qt.AlignRight)

        self.buttonOut = QComboBox(self)
        self.buttonOut.addItems(BUTTON_OUTPUTS)
        self.buttonOut.currentIndexChanged.connect(self.changeButtonOut)
        self.layout.addWidget(self.buttonOut, 5, 1)

    def changeJoystickIn(self, index):
        self.treeItem.config.joystickIn = index
        self.treeItem.updateText()

    def changeAxisXY(self, index):
        self.treeItem.config.axisXY = index
        self.treeItem.updateText()

    def changePosNeg(self, index):
        self.treeItem.config.posNeg = index
        self.treeItem.updateText()

    def changeInvert(self, arg__1):
        self.treeItem.config.invert = arg__1
        self.treeItem.updateText()

    def changeThreshold(self, arg__1):
        self.treeItem.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.treeItem.config.threshold * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.threshold, 3)))
        self.treeItem.updateText()

    def changeButtonOut(self, index):
        self.treeItem.config.buttonOut = index
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.joystickIn.setCurrentIndex(self.treeItem.config.joystickIn)
        self.axisXY.setCurrentIndex(self.treeItem.config.axisXY)
        self.posNeg.setCurrentIndex(self.treeItem.config.posNeg)
        if self.treeItem.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.treeItem.config.threshold * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.threshold, 3)))
        self.buttonOut.setCurrentIndex(self.treeItem.config.buttonOut)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingJoystickAsJoystick(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.joystickINLabel = QLabel("Input Joystick")
        self.layout.addWidget(self.joystickINLabel, 0, 0, Qt.AlignRight)

        self.joystickIn = QComboBox(self)
        self.joystickIn.addItems(JOYSTICK_OUTPUTS)
        self.joystickIn.currentIndexChanged.connect(self.changeJoystickIn)
        self.layout.addWidget(self.joystickIn, 0, 1)

        self.invertXLabel = QLabel("Invert X Axis")
        self.layout.addWidget(self.invertXLabel, 1, 0 ,Qt.AlignRight)

        self.invertX = QCheckBox(self)
        self.invertX.stateChanged.connect(self.changeInvertX)
        self.layout.addWidget(self.invertX, 1, 1)

        self.invertYLabel = QLabel("Invert Y Axis")
        self.layout.addWidget(self.invertYLabel, 2, 0 ,Qt.AlignRight)

        self.invertY = QCheckBox(self)
        self.invertY.stateChanged.connect(self.changeInvertY)
        self.layout.addWidget(self.invertY, 2, 1)

        self.deadzoneXLabel = QLabel("X Deadzone")
        self.layout.addWidget(self.deadzoneXLabel, 3, 0, Qt.AlignRight)

        self.deadzoneX = QSlider(self)
        self.deadzoneX.sliderMoved.connect(self.changeDeadzoneX)
        self.deadzoneX.setRange(0, 1000)
        self.deadzoneX.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.deadzoneX, 3, 1)

        self.deadzoneXVal = QLabel("")
        self.deadzoneXVal.setMinimumWidth(50)
        self.layout.addWidget(self.deadzoneXVal, 3, 2, Qt.AlignLeft)

        self.deadzoneYLabel = QLabel("Y Deadzone")
        self.layout.addWidget(self.deadzoneYLabel, 4, 0, Qt.AlignRight)

        self.deadzoneY = QSlider(self)
        self.deadzoneY.sliderMoved.connect(self.changeDeadzoneY)
        self.deadzoneY.setRange(0, 1000)
        self.deadzoneY.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.deadzoneY, 4, 1)

        self.deadzoneYVal = QLabel("")
        self.deadzoneYVal.setMinimumWidth(50)
        self.layout.addWidget(self.deadzoneYVal, 4, 2, Qt.AlignLeft)

        self.joystickOutLabel = QLabel("Output Joystick")
        self.layout.addWidget(self.joystickOutLabel, 5, 0, Qt.AlignRight)

        self.joystickOut = QComboBox(self)
        self.joystickOut.addItems(JOYSTICK_OUTPUTS)
        self.joystickOut.currentIndexChanged.connect(self.changeJoystickOut)
        self.layout.addWidget(self.joystickOut, 5, 1)

    def changeJoystickIn(self, index):
        self.treeItem.config.joystickIn = index
        self.treeItem.updateText()

    def changeInvertX(self, index):
        self.treeItem.config.invertX = index
        self.treeItem.updateText()

    def changeInvertY(self, index):
        self.treeItem.config.invertY = index
        self.treeItem.updateText()

    def changeJoystickOut(self, index):
        self.treeItem.config.joystickOut = index
        self.treeItem.updateText()

    def changeDeadzoneX(self, arg__1):
        self.treeItem.config.deadzoneX = float(arg__1) / 1000.0
        self.deadzoneX.setValue(int(self.treeItem.config.deadzoneX * 1000))
        self.deadzoneXVal.setText(str(round(self.treeItem.config.deadzoneX, 3)))
        self.treeItem.updateText()

    def changeDeadzoneY(self, arg__1):
        self.treeItem.config.deadzoneY = float(arg__1) / 1000.0
        self.deadzoneY.setValue(int(self.treeItem.config.deadzoneY * 1000))
        self.deadzoneYVal.setText(str(round(self.treeItem.config.deadzoneY, 3)))
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.joystickIn.setCurrentIndex(self.treeItem.config.joystickIn)
        self.joystickOut.setCurrentIndex(self.treeItem.config.joystickOut)
        if self.treeItem.config.invertX:
            self.invertX.setCheckState(Qt.Checked)
        else:
            self.invertX.setCheckState(Qt.Unchecked)
        if self.treeItem.config.invertY:
            self.invertY.setCheckState(Qt.Checked)
        else:
            self.invertY.setCheckState(Qt.Unchecked)
        self.deadzoneX.setValue(int(self.treeItem.config.deadzoneX * 1000))
        self.deadzoneXVal.setText(str(round(self.treeItem.config.deadzoneX, 3)))
        self.deadzoneY.setValue(int(self.treeItem.config.deadzoneY * 1000))
        self.deadzoneYVal.setText(str(round(self.treeItem.config.deadzoneY, 3)))
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingJoystickAsKeyboard(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.joystickInLabel = QLabel("Input Joystick")
        self.layout.addWidget(self.joystickInLabel, 0, 0, Qt.AlignRight)

        self.joystickIn = QComboBox(self)
        self.joystickIn.addItems(JOYSTICK_OUTPUTS)
        self.joystickIn.currentIndexChanged.connect(self.changeJoystickIn)
        self.layout.addWidget(self.joystickIn, 0, 1)

        self.axisXYLabel = QLabel("Input Axis")
        self.layout.addWidget(self.axisXYLabel, 1, 0, Qt.AlignRight)

        self.axisXY = QComboBox(self)
        self.axisXY.addItems(AXES)
        self.axisXY.currentIndexChanged.connect(self.changeAxisXY)
        self.layout.addWidget(self.axisXY, 1, 1)

        self.posNegLabel = QLabel("Positive/Negative")
        self.layout.addWidget(self.posNegLabel, 2, 0, Qt.AlignRight)

        self.posNeg = QComboBox(self)
        self.posNeg.addItems(POLARITY)
        self.posNeg.currentIndexChanged.connect(self.changePosNeg)
        self.layout.addWidget(self.posNeg, 2, 1)

        self.invertLabel = QLabel("Invert Input Axis")
        self.layout.addWidget(self.invertLabel, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.changeInvert)
        self.layout.addWidget(self.invert, 3, 1)

        self.thresholdLabel = QLabel("Threshold")
        self.layout.addWidget(self.thresholdLabel, 4, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.changeThreshold)
        self.threshold.setRange(0, 1000)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 4, 1)

        self.thresholdVal = QLabel("")
        self.thresholdVal.setMinimumWidth(50)
        self.layout.addWidget(self.thresholdVal, 4, 2, Qt.AlignLeft)

        self.keypressLabel = QLabel("Keypress")
        self.layout.addWidget(self.keypressLabel, 5, 0, Qt.AlignRight)

        self.keypress = QLineEdit(self)
        self.keypress.setText("")
        self.keypress.textChanged.connect(self.changeString)
        self.layout.addWidget(self.keypress, 5, 1)

    def changeJoystickIn(self, index):
        self.treeItem.config.joystickIn = index
        self.treeItem.updateText()

    def changeAxisXY(self, index):
        self.treeItem.config.axisXY = index
        self.treeItem.updateText()

    def changePosNeg(self, index):
        self.treeItem.config.posNeg = index
        self.treeItem.updateText()

    def changeInvert(self, arg__1):
        self.treeItem.config.invert = arg__1
        self.treeItem.updateText()

    def changeThreshold(self, arg__1):
        self.treeItem.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.treeItem.config.threshold * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.threshold, 3)))
        self.treeItem.updateText()

    def changeString(self, arg__1):
        self.treeItem.config.string = arg__1
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.joystickIn.setCurrentIndex(self.treeItem.config.joystickIn)
        self.axisXY.setCurrentIndex(self.treeItem.config.axisXY)
        self.posNeg.setCurrentIndex(self.treeItem.config.posNeg)
        if self.treeItem.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.treeItem.config.threshold * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.threshold, 3)))
        self.keypress.setText(self.treeItem.config.string)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingJoystickAsTrigger(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.joystickInLabel = QLabel("Input Joystick")
        self.layout.addWidget(self.joystickInLabel, 0, 0, Qt.AlignRight)

        self.joystickIn = QComboBox(self)
        self.joystickIn.addItems(JOYSTICK_OUTPUTS)
        self.joystickIn.currentIndexChanged.connect(self.changeJoystickIn)
        self.layout.addWidget(self.joystickIn, 0, 1)

        self.axisXYLabel = QLabel("Input Axis")
        self.layout.addWidget(self.axisXYLabel, 1, 0, Qt.AlignRight)

        self.axisXY = QComboBox(self)
        self.axisXY.addItems(AXES)
        self.axisXY.currentIndexChanged.connect(self.changeAxisXY)
        self.layout.addWidget(self.axisXY, 1, 1)

        self.posNegLabel = QLabel("Positive/Negative")
        self.layout.addWidget(self.posNegLabel, 2, 0, Qt.AlignRight)

        self.posNeg = QComboBox(self)
        self.posNeg.addItems(POLARITY)
        self.posNeg.currentIndexChanged.connect(self.changePosNeg)
        self.layout.addWidget(self.posNeg, 2, 1)

        self.invertLabel = QLabel("Invert Input Axis")
        self.layout.addWidget(self.invertLabel, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.changeInvert)
        self.layout.addWidget(self.invert, 3, 1)

        self.thresholdLabel = QLabel("Threshold")
        self.layout.addWidget(self.thresholdLabel, 4, 0, Qt.AlignRight)

        self.threshold = QSlider(self)
        self.threshold.sliderMoved.connect(self.changeThreshold)
        self.threshold.setRange(0, 1000)
        self.threshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.threshold, 4, 1)

        self.thresholdVal = QLabel("")
        self.thresholdVal.setMinimumWidth(50)
        self.layout.addWidget(self.thresholdVal, 4, 2, Qt.AlignLeft)

        self.triggerOutLabel = QLabel("Output Trigger")
        self.layout.addWidget(self.triggerOutLabel, 5, 0, Qt.AlignRight)

        self.triggerOut = QComboBox(self)
        self.triggerOut.addItems(TRIGGER_OUTPUTS)
        self.triggerOut.currentIndexChanged.connect(self.changeTriggerOut)
        self.layout.addWidget(self.triggerOut, 5, 1)

    def changeJoystickIn(self, index):
        self.treeItem.config.joystickIn = index
        self.treeItem.updateText()

    def changeAxisXY(self, index):
        self.treeItem.config.axisXY = index
        self.treeItem.updateText()

    def changePosNeg(self, index):
        self.treeItem.config.posNeg = index
        self.treeItem.updateText()

    def changeInvert(self, arg__1):
        self.treeItem.config.invert = arg__1
        self.treeItem.updateText()

    def changeThreshold(self, arg__1):
        self.treeItem.config.threshold = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.treeItem.config.threshold * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.threshold, 3)))
        self.treeItem.updateText()

    def changeTriggerOut(self, index):
        self.treeItem.config.triggerOut = index
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.joystickIn.setCurrentIndex(self.treeItem.config.joystickIn)
        self.axisXY.setCurrentIndex(self.treeItem.config.axisXY)
        self.posNeg.setCurrentIndex(self.treeItem.config.posNeg)
        if self.treeItem.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.threshold.setValue(int(self.treeItem.config.threshold * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.threshold, 3)))
        self.triggerOut.setCurrentIndex(self.treeItem.config.triggerOut)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingEncoderAsButton(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.speed_basedLabel = QLabel("Encoder Functionality")
        self.layout.addWidget(self.speed_basedLabel, 0, 0, Qt.AlignRight)

        self.speedBased = QComboBox(self)
        self.speedBased.addItems(ENCODER_FUNCTION_1)
        self.speedBased.currentIndexChanged.connect(self.changeSpeedBased)
        self.layout.addWidget(self.speedBased, 0, 1)

        self.ccwLabel = QLabel("Direction")
        self.layout.addWidget(self.ccwLabel, 1, 0, Qt.AlignRight)

        self.ccw = QComboBox(self)
        self.ccw.addItems(ENCODER_DIRECTIONS)
        self.ccw.currentIndexChanged.connect(self.changeCcw)
        self.layout.addWidget(self.ccw, 1, 1)

        self.invertLabel = QLabel("Invert Direction")
        self.layout.addWidget(self.invertLabel, 2, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.changeInvert)
        self.layout.addWidget(self.invert, 2, 1)

        self.speedThresholdLabel = QLabel("Speed Threshold")
        self.layout.addWidget(self.speedThresholdLabel, 3, 0, Qt.AlignRight)

        self.speedThreshold = QSlider(self)
        self.speedThreshold.sliderMoved.connect(self.changeSpeedThreshold)
        self.speedThreshold.setRange(0, 20e3)
        self.speedThreshold.setTickInterval(5)
        self.speedThreshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.speedThreshold, 3, 1)

        self.speedThresholdVal = QLabel("")
        self.speedThresholdVal.setMinimumWidth(50)
        self.layout.addWidget(self.speedThresholdVal, 3, 2, Qt.AlignLeft)

        self.buttonOutLabel = QLabel("Output Button")
        self.layout.addWidget(self.buttonOutLabel, 5, 0, Qt.AlignRight)

        self.buttonOut = QComboBox(self)
        self.buttonOut.addItems(BUTTON_OUTPUTS)
        self.buttonOut.currentIndexChanged.connect(self.changeButtonOut)
        self.layout.addWidget(self.buttonOut, 5, 1)

    def changeSpeedBased(self, index):
        self.treeItem.config.speedBased = index
        self.treeItem.updateText()

    def changeCcw(self, index):
        self.treeItem.config.ccw = index
        self.treeItem.updateText()

    def changeInvert(self, arg__1):
        self.treeItem.config.invert = arg__1
        self.treeItem.updateText()

    def changeSpeedThreshold(self, arg__1):
        self.treeItem.config.speedThreshold = float(arg__1) / 1000.0
        self.speedThreshold.setValue(int(self.treeItem.config.speedThreshold * 1000))
        self.speedThresholdVal.setText(str(round(self.treeItem.config.speedThreshold, 3))+" Hz")
        self.treeItem.updateText()

    def changeButtonOut(self, index):
        self.treeItem.config.buttonOut = index
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.speedBased.setCurrentIndex(self.treeItem.config.speedBased)
        self.ccw.setCurrentIndex(self.treeItem.config.ccw)
        if self.treeItem.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.speedThreshold.setValue(int(self.treeItem.config.speedThreshold * 1000))
        self.speedThresholdVal.setText(str(round(self.treeItem.config.speedThreshold, 3))+" Hz")
        self.buttonOut.setCurrentIndex(self.treeItem.config.buttonOut)
        self.show()

    def closeMapping(self):
        self.close()

class InputMappingEncoderAsJoystick(QWidget):
    def __init__(self, parent, treeItem):
        super().__init__(parent)
        self.parent = parent
        self.treeItem = treeItem
        self.initUI()
        self.close()

    def initUI(self):
        self.layout = QGridLayout(self)

        self.binaryBasedLabel = QLabel("Binary/Linear Functionality")
        self.layout.addWidget(self.binaryBasedLabel, 0, 0, Qt.AlignRight)

        self.binaryBased = QComboBox(self)
        self.binaryBased.addItems(ENCODER_FUNCTION_0)
        self.binaryBased.currentIndexChanged.connect(self.changeBinaryBased)
        self.layout.addWidget(self.binaryBased, 0, 1)

        self.speedBasedLabel = QLabel("Encoder Functionality")
        self.layout.addWidget(self.speedBasedLabel, 1, 0, Qt.AlignRight)

        self.speedBased = QComboBox(self)
        self.speedBased.addItems(ENCODER_FUNCTION_0)
        self.speedBased.currentIndexChanged.connect(self.changeSpeedBased)
        self.layout.addWidget(self.speedBased, 1, 1)

        self.ccwLabel = QLabel("Direction")
        self.layout.addWidget(self.ccwLabel, 2, 0, Qt.AlignRight)

        self.ccw = QComboBox(self)
        self.ccw.addItems(ENCODER_DIRECTIONS)
        self.ccw.currentIndexChanged.connect(self.changeCcw)
        self.layout.addWidget(self.ccw, 2, 1)

        self.invertLabel = QLabel("Invert Direction")
        self.layout.addWidget(self.invertLabel, 3, 0 ,Qt.AlignRight)

        self.invert = QCheckBox(self)
        self.invert.stateChanged.connect(self.changeInvert)
        self.layout.addWidget(self.invert, 3, 1)

        self.speedThresholdLabel = QLabel("Speed Threshold")
        self.layout.addWidget(self.speedThresholdLabel, 4, 0, Qt.AlignRight)

        self.speedThreshold = QSlider(self)
        self.speedThreshold.sliderMoved.connect(self.changeSpeedThreshold)
        self.speedThreshold.setRange(0, 20e3)
        self.speedThreshold.setTickInterval(5)
        self.speedThreshold.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.speedThreshold, 4, 1)

        self.speedThresholdVal = QLabel("")
        self.speedThresholdVal.setMinimumWidth(50)
        self.layout.addWidget(self.speedThresholdVal, 4, 2, Qt.AlignLeft)

        self.linearMiddleLabel = QLabel("Linear Middle")
        self.layout.addWidget(self.linearMiddleLabel, 5, 0, Qt.AlignRight)

        self.linearMiddle = QSlider(self)
        self.linearMiddle.sliderMoved.connect(self.changeLinearMiddle)
        self.linearMiddle.setRange(0, 1000)
        self.linearMiddle.setTickInterval(5)
        self.linearMiddle.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.linearMiddle, 5, 1)

        self.linearMiddleVal = QLabel("")
        self.linearMiddleVal.setMinimumWidth(50)
        self.layout.addWidget(self.linearMiddleVal, 5, 2, Qt.AlignLeft)

        self.linearDeadzoneLabel = QLabel("Linear Deadzone")
        self.layout.addWidget(self.linearDeadzoneLabel, 6, 0, Qt.AlignRight)

        self.linearDeadzone = QSlider(self)
        self.linearDeadzone.sliderMoved.connect(self.changeLinearDeadzone)
        self.linearDeadzone.setRange(0, 1000)
        self.linearDeadzone.setTickInterval(5)
        self.linearDeadzone.setOrientation(Qt.Horizontal)
        self.layout.addWidget(self.linearDeadzone, 6, 1)

        self.linearDeadzoneVal = QLabel("")
        self.linearDeadzoneVal.setMinimumWidth(50)
        self.layout.addWidget(self.linearDeadzoneVal, 6, 2, Qt.AlignLeft)

        self.joystickOutLabel = QLabel("Output Joystick")
        self.layout.addWidget(self.joystickOutLabel, 7, 0, Qt.AlignRight)

        self.joystickOut = QComboBox(self)
        self.joystickOut.addItems(JOYSTICK_OUTPUTS)
        self.joystickOut.currentIndexChanged.connect(self.changeJoystickOut)
        self.layout.addWidget(self.joystickOut, 7, 1)

        self.axisXYLabel = QLabel("Output Axis")
        self.layout.addWidget(self.axisXYLabel, 8, 0, Qt.AlignRight)

        self.axisXY = QComboBox(self)
        self.axisXY.addItems(AXES)
        self.axisXY.currentIndexChanged.connect(self.changeAxisXY)
        self.layout.addWidget(self.axisXY, 8, 1)

        self.posNegLabel = QLabel("Positive/Negative")
        self.layout.addWidget(self.posNegLabel, 9, 0, Qt.AlignRight)

        self.posNeg = QComboBox(self)
        self.posNeg.addItems(POLARITY)
        self.posNeg.currentIndexChanged.connect(self.changePosNeg)
        self.layout.addWidget(self.posNeg, 9, 1)

    def changeBinaryBased(self, index):
        self.treeItem.config.binaryBased = index
        if self.treeItem.config.binaryBased:
            self.ccw.setEnabled(True)
            self.speedBased.setEnabled(True)
            self.speedThreshold.setEnabled(True)
            self.linearMiddle.setEnabled(False)
            self.linearDeadzone.setEnabled(False)
        else:
            self.ccw.setEnabled(False)
            self.speedBased.setEnabled(False)
            self.speedThreshold.setEnabled(False)
            self.linearMiddle.setEnabled(True)
            self.linearDeadzone.setEnabled(True)
        self.treeItem.updateText()

    def changeSpeedBased(self, index):
        self.treeItem.config.speedBased = index
        self.treeItem.updateText()

    def changeCcw(self, index):
        self.treeItem.config.ccw = index
        self.treeItem.updateText()

    def changeInvert(self, arg__1):
        self.treeItem.config.invert = arg__1
        self.treeItem.updateText()

    def changeSpeedThreshold(self, arg__1):
        self.treeItem.config.speedThreshold = float(arg__1) / 1000.0
        self.speedThreshold.setValue(int(self.treeItem.config.speedThreshold * 1000))
        self.speedThresholdVal.setText(str(round(self.treeItem.config.speedThreshold, 3))+" Hz")
        self.treeItem.updateText()

    def changeLinearMiddle(self, arg__1):
        self.treeItem.config.linearMiddle = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.treeItem.config.linearMiddle * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.linearMiddle, 3)))
        self.treeItem.updateText()

    def changeLinearDeadzone(self, arg__1):
        self.treeItem.config.linearDeadzone = float(arg__1) / 1000.0
        self.threshold.setValue(int(self.treeItem.config.linearDeadzone * 1000))
        self.thresholdVal.setText(str(round(self.treeItem.config.linearDeadzone, 3)))
        self.treeItem.updateText()

    def changeJoystickOut(self, index):
        self.treeItem.config.joystickOut = index
        self.treeItem.updateText()

    def changeAxisXY(self, index):
        self.treeItem.config.axisXY = index
        self.treeItem.updateText()

    def changePosNeg(self, index):
        self.treeItem.config.posNeg = index
        self.treeItem.updateText()

    def showMapping(self, treeItem):
        self.treeItem = treeItem
        self.binaryBased.setCurrentIndex(self.treeItem.config.binaryBased)
        self.changeBinaryBased(self.treeItem.config.binaryBased)
        self.speedBased.setCurrentIndex(self.treeItem.config.speedBased)
        self.ccw.setCurrentIndex(self.treeItem.config.ccw)
        if self.treeItem.config.invert:
            self.invert.setCheckState(Qt.Checked)
        else:
            self.invert.setCheckState(Qt.Unchecked)
        self.speedThreshold.setValue(int(self.treeItem.config.speedThreshold * 1000))
        self.speedThresholdVal.setText(str(round(self.treeItem.config.speedThreshold, 3))+" Hz")
        self.linearMiddle.setValue(int(self.treeItem.config.linearMiddle * 1000))
        self.linearMiddleVal.setText(str(round(self.treeItem.config.linearMiddle, 3)))
        self.linearDeadzone.setValue(int(self.treeItem.config.linearDeadzone * 1000))
        self.linearDeadzoneVal.setText(str(round(self.treeItem.config.linearDeadzone, 3)))
        self.joystickOut.setCurrentIndex(self.treeItem.config.joystickOut)
        self.axisXY.setCurrentIndex(self.treeItem.config.axisXY)
        self.posNeg.setCurrentIndex(self.treeItem.config.posNeg)
        self.show()

    def closeMapping(self):
        self.close()




