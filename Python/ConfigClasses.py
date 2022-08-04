import struct
import os

DEFAULT_CFG_FILE = "GMK Controller - Default Configuration 1"

#Define Input Mapping Configurations
INPUT_BUTTON_AS_BUTTON = 0
INPUT_BUTTON_AS_JOYSTICK = 1
INPUT_BUTTON_AS_KEYBOARD = 2
INPUT_BUTTON_AS_TRIGGER = 3
INPUT_JOYSTICK_AS_BUTTON = 4
INPUT_JOYSTICK_AS_JOYSTICK = 5
INPUT_JOYSTICK_AS_KEYBOARD = 6
INPUT_JOYSTICK_AS_TRIGGER = 7
INPUT_ENCODER_AS_BUTTON = 8
INPUT_ENCODER_AS_JOYSTICK = 9
INPUT_ENCODER_AS_KEYBOARD = 10
INPUT_ENCODER_AS_TRIGGER = 11
INPUT_NOT_CONFIGURED = 12

#Define Input Button Mappings
BUTTON_IN_0 = 0
BUTTON_IN_1 = 1
BUTTON_IN_2 = 2
BUTTON_IN_3 = 3
BUTTON_IN_4 = 4
BUTTON_IN_5 = 5
BUTTON_IN_6 = 6
BUTTON_IN_7 = 7
BUTTON_IN_8 = 8
BUTTON_IN_9 = 9
BUTTON_IN_10 = 10
BUTTON_IN_11 = 11
BUTTON_IN_12 = 12
BUTTON_IN_13 = 13
JOYSTICK_IN_0 = 0
JOYSTICK_IN_1 = 1

#Define Output Button Mappings
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3
BUTTON_LB = 4
BUTTON_RB = 5
BUTTON_LTH = 6
BUTTON_RTH = 7
BUTTON_UP = 8
BUTTON_DOWN = 9
BUTTON_LEFT = 10
BUTTON_RIGHT = 11
BUTTON_START = 12
BUTTON_BACK = 13
JOYSTICK_LEFT = 0
JOYSTICK_RIGHT = 1
AXIS_X = 0
AXIS_Y = 1
AXIS_POSITIVE = 0
AXIS_NEGATIVE = 1
AXIS_NON_INVERTED = 0
AXIS_INVERTED = 1
TRIGGER_LEFT = 0
TRIGGER_RIGHT = 1
ENCODER_LINEAR_BASED = 0
ENCODER_BINARY_BASED = 1
ENCODER_DIRECTION_BASED = 0
ENCODER_SPEED_BASED = 1
ENCODER_DIR_CLOCKWISE = 0
ENCODER_DIR_COUNTERCLOCKWISE = 1

#Define configuration output byte formatting
CONFIGURATION_SIZE = 2048
CONFIG_NAME_LENGTH = 64
BYTE_ENCODING = "utf-8"

def mapOutputButton(buttonOut):
    if buttonOut == BUTTON_A:
        return "a"
    if buttonOut == BUTTON_B:
        return "b"
    if buttonOut == BUTTON_X:
        return "x"
    if buttonOut == BUTTON_Y:
        return "y"
    if buttonOut == BUTTON_LB:
        return "left bumper"
    if buttonOut == BUTTON_RB:
        return "right bumper"
    if buttonOut == BUTTON_LTH:
        return "left thumbstick"
    if buttonOut == BUTTON_RTH:
        return "right thumbstick"
    if buttonOut == BUTTON_UP:
        return "up"
    if buttonOut == BUTTON_DOWN:
        return "down"
    if buttonOut == BUTTON_LEFT:
        return "left"
    if buttonOut == BUTTON_RIGHT:
        return "right"
    if buttonOut == BUTTON_START:
        return "start"
    if buttonOut == BUTTON_BACK:
        return "back"

def mapOutputJoystick(joystickLR, axisXY=-1, posNeg=-1):
    string = ""
    if joystickLR == JOYSTICK_LEFT:
        string += "left joystick"
    if joystickLR == JOYSTICK_RIGHT:
        string += "right joystick"
    if axisXY == AXIS_X:
        string += " x"
    if axisXY == AXIS_Y:
        string += " y"
    if posNeg == AXIS_POSITIVE:
        string += " positive"
    if posNeg == AXIS_NEGATIVE:
        string += " negative"
    return string

def mapOutputTrigger(triggerOut):
    if triggerOut == TRIGGER_LEFT:
        return "left trigger"
    if triggerOut == TRIGGER_RIGHT:
        return "right trigger"

class ControllerOutput():
    def __init__(self, a, b, x, y, lb, rb, lth, rth, up, down, left, right, start, back, joystickLx, joystickLy, joystickRx, joystickRy, triggerL, triggerR):
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.lb = lb
        self.rb = rb
        self.lth = lth
        self.rth = rth
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.start = start
        self.back = back
        self.joystickLx = joystickLx
        self.joystickLy = joystickLy
        self.joystickRx = joystickRx
        self.joystickRy = joystickRy
        self.triggerL = triggerL
        self.triggerR = triggerR

    def toBytes(self):
        b0 = 0
        b0 |= self.a << 7
        b0 |= self.b << 6
        b0 |= self.x << 5
        b0 |= self.y << 4
        b0 |= self.lb << 3
        b0 |= self.rb << 2
        b0 |= self.lth << 1
        b0 |= self.rth << 0
        b1 = 0
        b1 |= self.up << 7
        b1 |= self.down << 6
        b1 |= self.left << 5
        b1 |= self.right << 4
        b1 |= self.start << 3
        b1 |= self.back << 2
        return struct.pack("<BBhhhhBB", b0, b1, self.joystickLx, self.joystickLy, self.joystickRx, self.joystickRy, self.triggerL, self.triggerR)

    def fromBytes(bytesIn):
        (b0, b1,  joystickLx, joystickLy, joystickRx, joystickRy, triggerL, triggerR) = struct.unpack("<BBhhhhBB", bytesIn)
        a = (b0 >> 7) & 1
        b = (b0 >> 6) & 1
        x = (b0 >> 5) & 1
        y = (b0 >> 4) & 1
        lb = (b0 >> 3) & 1
        rb = (b0 >> 2) & 1
        lth = (b0 >> 1) & 1
        rth = (b0 >> 0) & 1
        up = (b1 >> 7) & 1
        down = (b1 >> 6) & 1
        left = (b1 >> 5) & 1
        right = (b1 >> 4) & 1
        start = (b1 >> 3) & 1
        back = (b1 >> 2) & 1
        return Controller_Output(a, b, x, y, lb, rb, lth, rth, up, down, left, right, start, back, joystickLx, joystickLy, joystickRx, joystickRy, triggerL, triggerR)

    def __str__(self):
        string = ""
        string += "a: {}\n".format(self.a)
        string += "b: {}\n".format(self.b)
        string += "x: {}\n".format(self.x)
        string += "y: {}\n".format(self.y)
        string += "lb: {}\n".format(self.lb)
        string += "rb: {}\n".format(self.rb)
        string += "lth: {}\n".format(self.lth)
        string += "rth: {}\n".format(self.rth)
        string += "up: {}\n".format(self.up)
        string += "down: {}\n".format(self.down)
        string += "left: {}\n".format(self.left)
        string += "right: {}\n".format(self.right)
        string += "start: {}\n".format(self.start)
        string += "joystickLx: {}\n".format(self.joystickLx)
        string += "joystickLy: {}\n".format(self.joystickLy)
        string += "joystickRx: {}\n".format(self.joystickRx)
        string += "joystickRy: {}\n".format(self.joystickRy)
        string += "triggerL: {}\n".format(self.triggerL)
        string += "triggerR: {}\n".format(self.triggerR)
        return string

class ControllerConfigurations():
    def __init__(self, fileName):
        self.fileName = fileName
        self.controllerConfigurations = []
    
    def addControllerConfiguration(self, config):
        self.controllerConfigurations.append(config)

    def removeControllerConfiguration(self, config):
        index = self.controllerConfigurations.find(config)
        self.controllerConfigurations.pop(index)


class ControllerConfiguration():
    def __init__(self, profileNumber, configName, LEDColors, LEDBrightness):
        self.profileNumber = profileNumber
        self.configName = configName
        self.LEDColors = LEDColors
        self.LEDColorsBytes = self.setLEDColors(LEDColors)
        self.LEDBrightness = LEDBrightness
        self.configurations = []

    def addConfig(self, configuration):
        self.configurations.append(configuration)

    def delete_config(self, configuration):
        self.configurations.pop(configuration)

    def getNumberOfConfigurations(self):
        return len(self.configurations)

    def setLEDColors(self, LEDColors):
        self.LEDColorsBytes = b""
        for i in self.LEDColors:
            self.LEDColorsBytes += bytes(i)
        return self.LEDColorsBytes

    def getLEDColorsBytes(self):
        return self.LEDColorsBytes

    def LEDBytesToColors(BytesIn):
        LEDColors = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(4):
            for j in range(3):
                LEDColors[i][j] = BytesIn[i*3 + j]
        return LEDColors

    def printConfigToFile(self, filePath):
        #Write to file
        with open(filePath, "wb") as f:
            print("Writing to file: {}".format(filePath))
            f.write(self.toBytesFill(self.toBytes()))

        #Report file size
        byteCnt = len(self.toBytes())
        print("Total bytes used in configuration: {} of {}. ({:0.2f}%)".format(byteCnt, CONFIGURATION_SIZE, 100 * byteCnt / CONFIGURATION_SIZE))

        #Write text file for array initialization
        self.printConfigToTXTFile(filePath)

    def printConfigToTXTFile(self, filePath):
        #Check if folder exists
        filePath_txt = os.path.splitext(filePath)[0] + ".txt"
        filePath_cfg = filePath

        #Write to file
        with open(filePath_txt, "w") as f_txt:
            f_txt.write("{ ")
            with open(filePath_cfg, "rb") as f_cfg:
                for byte in f_cfg.read():
                    f_txt.write("{}, ".format(byte))
            f_txt.write("}")

    def fromFile(filePath):
        with open(filePath, "rb") as f:
            return ControllerConfiguration.fromBytes(f.read())

    def toBytes(self):
        bytesOut = b""
        bytesOut += bytes([self.profileNumber])
        bytesOut += self.getLEDColorsBytes()
        bytesOut += bytes([self.LEDBrightness])
        bytesOut += self.configName[:CONFIG_NAME_LENGTH].encode(BYTE_ENCODING).ljust(CONFIG_NAME_LENGTH, b" ")
        for config in self.configurations:
            configBytes = config.toBytes()
            bytesOut += configBytes
            bytesOut += bytes([0xff])

        return bytesOut

    def toBytesFill(self, bytesIn):
        bytesIn += bytes([0])*(CONFIGURATION_SIZE - len(bytesIn))
        return bytesIn
       
    def getConfigSize(self):
        return len(self.toBytes())

    def fromBytes(bytesIn):
        (profileNumber,) = struct.unpack("<B", bytesIn[0:1])
        LEDColors = ControllerConfiguration.LEDBytesToColors(struct.unpack("<{}B".format(12), bytesIn[1:13]))
        (LEDBrightness,) = struct.unpack("<B", bytesIn[13:14])
        (configName,) = struct.unpack("<{}s".format(CONFIG_NAME_LENGTH), bytesIn[14:14+CONFIG_NAME_LENGTH])
        configName = configName.decode(BYTE_ENCODING)
        cc = ControllerConfiguration(profileNumber, configName, LEDColors, LEDBrightness)
        configStart = True
        configStartAddress = 0
        for i in range(14 + CONFIG_NAME_LENGTH, len(bytesIn)):
            if(configStart):
                t = bytesIn[i]
                configStart = False
                configStartAddress = i
            if bytesIn[i] == 255:
                configStart = True
                cc.addConfig(ControllerConfiguration.configFromBytes(t, bytesIn[configStartAddress : i]))
        return cc

    def configFromBytes(t, bytesIn):
        if t == INPUT_BUTTON_AS_BUTTON:
            return ButtonAsButton.fromBytes(bytesIn)
        if t == INPUT_BUTTON_AS_JOYSTICK:
            return ButtonAsJoystick.fromBytes(bytesIn)
        if t == INPUT_BUTTON_AS_KEYBOARD:
            return ButtonAsKeyboard.fromBytes(bytesIn, len(bytesIn) - 2)
        if t == INPUT_BUTTON_AS_TRIGGER:
            return ButtonAsTrigger.fromBytes(bytesIn)
        if t == INPUT_JOYSTICK_AS_BUTTON:
            return JoystickAsButton.fromBytes(bytesIn)
        if t == INPUT_JOYSTICK_AS_JOYSTICK:
            return JoystickAsJoystick.fromBytes(bytesIn)
        if t == INPUT_JOYSTICK_AS_KEYBOARD:
            return JoystickAsKeyboard.fromBytes(bytesIn, len(bytesIn) - 6)
        if t == INPUT_JOYSTICK_AS_TRIGGER:
            return JoystickAsTrigger.fromBytes(bytesIn)
        if t == INPUT_ENCODER_AS_BUTTON:
            return EncoderAsButton.fromBytes(bytesIn)
        if t == INPUT_ENCODER_AS_JOYSTICK:
            return EncoderAsJoystick.fromBytes(bytesIn)
        if t == INPUT_ENCODER_AS_KEYBOARD:
            return EncoderAsKeyboard.fromBytes(bytes, len(bytesIn) - 6)
        if t == INPUT_ENCODER_AS_TRIGGER:
            return EncoderAsTrigger.fromBytes(bytesIn)

class ButtonAsButton():
    def __init__(self, buttonIn=0, buttonOut=0):
        self.buttonIn = buttonIn
        self.buttonOut = buttonOut
        self.type = INPUT_BUTTON_AS_BUTTON
        self.inputType = "button"
        self.outputType = "button"
        self.struct = b""

    def toBytes(self):
        self.struct = struct.pack("<BBB", self.type, self.buttonIn, self.buttonOut)
        return self.struct

    def fromBytes(bytesIn):
        (t, buttonIn, buttonOut) = struct.unpack("<BBB", bytesIn)
        return ButtonAsButton(buttonIn, buttonOut)

    def outputMapping(self):
        return mapOutputButton(self.buttonOut)

class ButtonAsJoystick():
    def __init__(self, buttonIn=0, joystickOut=0, axisXY=0, posNeg=0):
        self.buttonIn = buttonIn
        self.joystickOut = joystickOut
        self.axisXY = axisXY
        self.posNeg = posNeg
        self.type = INPUT_BUTTON_AS_JOYSTICK
        self.inputType = "button"
        self.outputType = "joystick"
        self.struct = b""

    def toBytes(self):
        b1 = 0
        b1 |= self.joystickOut << 0
        b1 |= self.axisXY << 1
        self.struct = struct.pack("<BBB", self.type, self.buttonIn, b1)
        return self.struct

    def fromBytes(bytesIn):
        (t, buttonIn, b1) = struct.unpack("<BBB", bytesIn)
        joystickOut = (b1 >> 0) & 1
        axisXY = (b1 >> 1) & 1
        posNeg = (b1 >> 2) & 1
        return ButtonAsJoystick(buttonIn, joystickOut, axisXY, posNeg)

    def outputMapping(self):
        return mapOutputJoystick(self.joystickOut, self.axisXY, self.posNeg)

class ButtonAsKeyboard():
    def __init__(self, buttonIn=0, string=""):
        self.buttonIn = buttonIn
        self.string = string
        self.type = INPUT_BUTTON_AS_KEYBOARD
        self.inputType = "button"
        self.outputType = "keyboard"
        self.struct = b""

    def toBytes(self):
        self.struct = struct.pack("<BB{}s".format(len(self.string)), self.type, self.buttonIn, bytes(self.string, BYTE_ENCODING))
        return self.struct

    def fromBytes(bytesIn, strLen):
        (t, buttonIn, string) = struct.unpack("<BB{}s".format(strLen), bytesIn)
        return ButtonAsKeyboard(buttonIn, string.decode(BYTE_ENCODING))

    def outputMapping(self):
        return "Keyboard"

class ButtonAsTrigger():
    def __init__(self, buttonIn=0, triggerOut=0):
        self.buttonIn = buttonIn
        self.triggerOut = triggerOut
        self.type = INPUT_BUTTON_AS_TRIGGER
        self.inputType = "button"
        self.outputType = "trigger"
        self.struct = b""

    def toBytes(self):
        self.struct = struct.pack("<BBB", self.type, self.buttonIn, self.triggerOut)
        return self.struct

    def fromBytes(bytesIn):
        (t, buttonIn, triggerOut) = struct.unpack("<BBB", bytesIn)
        return ButtonAsTrigger(buttonIn, triggerOut)

    def outputMapping(self):
        return mapOutputTrigger(self.triggerOut)

class JoystickAsButton():
    def __init__(self, joystickIn=0, axisXY=0, invert=0, posNeg=0, threshold=0.05, buttonOut=0):
        self.joystickIn = joystickIn
        self.axisXY = axisXY
        self.invert = invert
        self.posNeg = posNeg
        self.threshold = float(threshold)
        self.buttonOut = buttonOut
        self.type = INPUT_JOYSTICK_AS_BUTTON
        self.inputType = "joystick"
        self.outputType = "button"
        self.struct = b""

    def toBytes(self):
        b0 = 0
        b0 |= self.joystickIn << 0
        b0 |= self.axisXY << 1
        b0 |= self.invert << 2
        b0 |= self.posNeg << 3
        self.struct = struct.pack("<BBfB", self.type, b0, self.threshold, self.buttonOut)
        return self.struct

    def fromBytes(bytesIn):
        (t, b0, threshold, buttonOut) = struct.unpack("<BBfB", bytesIn)
        joystickIn = (b0 >> 0) & 1
        axisXY = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        posNeg = (b0 >> 3) & 1
        return JoystickAsButton(joystickIn, axisXY, invert, posNeg, threshold, buttonOut)

    def outputMapping(self):
        return mapOutputButton(self.buttonOut)

class JoystickAsJoystick():
    def __init__(self, joystickIn=0, invertX=0, invertY=0, joystickOut=0, deadzoneX=0.05, deadzoneY=0.05):
        self.joystickIn = joystickIn
        self.invertX = invertX
        self.invertY = invertY
        self.joystickOut = joystickOut
        self.deadzoneX = float(deadzoneX)
        self.deadzoneY = float(deadzoneY)
        self.type = INPUT_JOYSTICK_AS_JOYSTICK
        self.inputType = "joystick"
        self.outputType = "joystick"
        self.struct = bytearray(10)

    def toBytes(self):
        b0 = 0
        b0 |= self.joystickIn << 0
        b0 |= self.invertX << 1
        b0 |= self.invertY << 2
        b0 |= self.joystickOut << 3
        self.struct = struct.pack("<BBff", self.type, b0, self.deadzoneX, self.deadzoneY)
        return self.struct

    def fromBytes(bytesIn):
        (t, b0, deadzoneX, deadzoneY) = struct.unpack("<BBff", bytesIn)
        joystickIn = (b0 >> 0) & 1
        invertX = (b0 >> 1) & 1
        invertY = (b0 >> 2) & 1
        joystickOut = (b0 >> 3) & 1
        return JoystickAsJoystick(joystickIn, invertX, invertY, joystickOut, deadzoneX, deadzoneY)

    def outputMapping(self):
        return mapOutputJoystick(self.joystickOut)

class JoystickAsKeyboard():
    def __init__(self, joystickIn=0, axisXY=0, invert=0, posNeg=0, threshold=0.75, string=""):
        self.joystickIn = joystickIn
        self.axisXY = axisXY
        self.invert = invert
        self.posNeg = posNeg
        self.threshold = float(threshold)
        self.string = string
        self.type = INPUT_JOYSTICK_AS_KEYBOARD
        self.inputType = "joystick"
        self.outputType = "keyboard"
        self.struct = b""

    def toBytes(self):
        b0 = 0
        b0 |= self.joystickIn << 0
        b0 |= self.axisXY << 1
        b0 |= self.invert << 2
        b0 |= self.posNeg << 3
        self.struct = struct.pack("<BBf{}s".format(len(self.string)), self.type, b0, self.threshold, bytes(self.string, BYTE_ENCODING))
        return self.struct

    def fromBytes(bytesIn, strLen):
        (t, b0, threshold, string) = struct.unpack("<BBf{}s".format(strLen), bytesIn)
        joystickIn = (b0 >> 0) & 1
        axisXY = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        posNeg = (b0 >> 3) & 1
        return JoystickAsKeyboard(joystickIn, axisXY, invert, posNeg, threshold, string.decode(BYTE_ENCODING))

    def outputMapping(self):
        return "Keyboard"

class JoystickAsTrigger():
    def __init__(self, joystickIn=0, axisXY=0, invert=0, posNeg=0, threshold=0.75, triggerOut=0):
        self.joystickIn = joystickIn
        self.axisXY = axisXY
        self.invert = invert
        self.posNeg = posNeg
        self.triggerOut = triggerOut
        self.threshold = float(threshold)
        self.type = INPUT_JOYSTICK_AS_TRIGGER
        self.inputType = "joystick"
        self.outputType = "trigger"
        self.struct = b""

    def toBytes(self):
        b0 = 0
        b0 |= self.joystickIn << 0
        b0 |= self.axisXY << 1
        b0 |= self.invert << 2
        b0 |= self.posNeg << 3
        b0 |= self.triggerOut << 4
        self.struct = struct.pack("<BBf", self.type, b0, self.threshold)
        return self.struct

    def fromBytes(bytesIn):
        (t, b0, threshold) = struct.unpack("<BBf", bytesIn)
        joystickIn = (b0 >> 0) & 1
        axisXY = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        posNeg = (b0 >> 3) & 1
        triggerOut = (b0 >> 4) & 1
        return JoystickAsTrigger(joystickIn, axisXY, invert, posNeg, triggerOut)

    def outputMapping(self):
        return mapOutputTrigger(self.triggerOut)

class EncoderAsButton():
    def __init__(self, speedBased=0, ccw=0, invert=0, speedThreshold=5, buttonOut=0):
        self.speedBased = speedBased
        self.ccw = ccw
        self.invert = invert
        self.speedThreshold = float(speedThreshold)
        self.buttonOut = buttonOut
        self.type = INPUT_ENCODER_AS_BUTTON
        self.inputType = "encoder"
        self.outputType = "button"
        self.struct = b""

    def toBytes(self):
        b0 = 0
        b0 |= self.speedBased << 0
        b0 |= self.ccw << 1
        b0 |= self.invert << 2
        self.struct = struct.pack("<BBfB", self.type, b0, self.speedThreshold, self.buttonOut)
        return self.struct

    def fromBytes(bytesIn):
        (t, b0, speedThreshold, buttonOut) = struct.unpack("<BBfB", bytesIn)
        speedBased = (b0 >> 0) & 1
        ccw = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        return EncoderAsButton(speedBased, ccw, invert, speedThreshold, buttonOut)

    def outputMapping(self):
        return mapOutputButton(self.buttonOut)

class EncoderAsJoystick():
    def __init__(self, binaryBased=0, speedBased=0, ccw=0, invert=0, speedThreshold=5, linearMiddle=0.5, linearDeadzone=0.05, joystickOut=0, axisXY=0, posNeg=0):
        self.binaryBased = binaryBased
        self.speedBased = speedBased
        self.ccw = ccw
        self.invert = invert
        self.speedThreshold = float(speedThreshold)
        self.linearMiddle = float(linearMiddle)
        self.linearDeadzone = float(linearDeadzone)
        self.joystickOut = joystickOut
        self.axisXY = axisXY
        self.posNeg = posNeg
        self.type = INPUT_ENCODER_AS_JOYSTICK
        self.inputType = "encoder"
        self.outputType = "joystick"
        self.struct = b""

    def toBytes(self):
        b0 = 0
        b0 |= self.binaryBased << 0
        b0 |= self.speedBased << 1
        b0 |= self.ccw << 2
        b0 |= self.invert << 3
        b13 = 0
        b13 |= self.joystickOut << 0
        b13 |= self.axisXY << 1
        b13 |= self.posNeg << 2
        self.struct = struct.pack("<BBfffB", self.type, b0, self.speedThreshold, self.linearMiddle, self.linearDeadzone, b13)
        return self.struct

    def fromBytes(bytesIn):
        (t, b0, speedThreshold, linearMiddle, linearDeadzone, b13) = struct.unpack("<BBfffB", bytesIn)
        binaryBased = (b0 >> 0) & 1
        speedBased = (b0 >> 1) & 1
        ccw = (b0 >> 2) & 1
        invert = (b0 >> 3) & 1
        joystickOut = (b13 >> 0) & 1
        axisXY = (b13 >> 1) & 1
        posNeg = (b13 >> 2) & 1
        return EncoderAsJoystick(binaryBased, speedBased, ccw, invert, speedThreshold, linearMiddle, linearDeadzone, joystickOut, axisXY, posNeg)

    def outputMapping(self):
        return mapOutputJoystick(self.joystickOut, self.axisXY, self.posNeg)

class EncoderAsKeyboard():
    def __init__(self, speedBased=0, ccw=0, invert=0, speedThreshold=5, string=""):
        self.speedBased = speedBased
        self.ccw = ccw
        self.invert = invert
        self.speedThreshold = float(speedThreshold)
        self.string = string
        self.type = INPUT_ENCODER_AS_KEYBOARD
        self.inputType = "encoder"
        self.outputType = "keyboard"
        self.struct = b""

    def toBytes(self):
        b0 = 0
        b0 |= self.speedBased << 0
        b0 |= self.ccw << 1
        b0 |= self.invert << 2
        self.struct = struct.pack("<BBf{}s".format(len(self.string)), self.type, b0, self.speedThreshold, self.string)
        return self.struct

    def fromBytes(bytesIn, strLen):
        (t, b0, speedThreshold, string) = struct.unpack("<BBfB{}s".format(strLen), bytesIn)
        speedBased = (b0 >> 0) & 1
        ccw = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        return EncoderAsKeyboard(speedBased, ccw, invert, speedThreshold, string)

    def outputMapping(self):
        return "Keyboard"

class EncoderAsTrigger():
    def __init__(self, binaryBased=0, speedBased=0, ccw=0, invert=0, speedThreshold=5, linearMiddle=0.5, linearDeadzone=0.05, triggerOut=0):
        self.speedBased = speedBased
        self.ccw = ccw
        self.invert = invert
        self.speedThreshold = float(speedThreshold)
        self.linearMiddle = float(linearMiddle)
        self.linearDeadzone = float(linearDeadzone)
        self.triggerOut = triggerOut
        self.type = INPUT_ENCODER_AS_TRIGGER
        self.inputType = "encoder"
        self.outputType = "trigger"
        self.struct = b""

    def toBytes(self):
        b0 = 0
        b0 |= self.binaryBased << 0
        b0 |= self.speedBased << 1
        b0 |= self.ccw << 2
        b0 |= self.invert << 3
        self.struct = struct.pack("<BBfffB", self.type, b0, self.speedThreshold, self.linearMiddle, self.linearDeadzone, self.triggerOut)
        return self.struct

    def fromBytes(bytesIn):
        (t, b0, speedThreshold, linearMiddle, linearDeadzone, triggerOut) = struct.unpack("<BBfffB", bytesIn)
        binaryBased = (b0 >> 0) & 1
        speedBased = (b0 >> 1) & 1
        ccw = (b0 >> 2) & 1
        invert = (b0 >> 3) & 1
        return EncoderAsTrigger(binaryBased, speedBased, ccw, invert, speedThreshold, linearMiddle, linearDeadzone, triggerOut)

    def outputMapping(self):
        return mapOutputTrigger(self.triggerOut)

def test():
    print("Creating Default Joystick Configurations")
    config = ControllerConfiguration(0, DEFAULT_CFG_FILE, [[255, 0, 0], [0, 255, 0], [0, 0, 255], [90, 0, 40]], 32)
    config.addConfig(ButtonAsButton(BUTTON_IN_0, BUTTON_A))
    config.addConfig(ButtonAsButton(BUTTON_IN_1, BUTTON_B))
    config.addConfig(ButtonAsButton(BUTTON_IN_2, BUTTON_X))
    config.addConfig(ButtonAsButton(BUTTON_IN_3, BUTTON_Y))
    config.addConfig(ButtonAsButton(BUTTON_IN_4, BUTTON_LB))
    config.addConfig(ButtonAsButton(BUTTON_IN_5, BUTTON_RB))
    config.addConfig(ButtonAsButton(BUTTON_IN_6, BUTTON_LTH))
    config.addConfig(ButtonAsButton(BUTTON_IN_7, BUTTON_RTH))
    config.addConfig(ButtonAsButton(BUTTON_IN_8, BUTTON_LEFT))
    config.addConfig(ButtonAsButton(BUTTON_IN_9, BUTTON_RIGHT))
    config.addConfig(ButtonAsButton(BUTTON_IN_10, BUTTON_BACK))
    config.addConfig(ButtonAsButton(BUTTON_IN_11, BUTTON_START))

    config.addConfig(ButtonAsTrigger(BUTTON_IN_12, TRIGGER_LEFT))
    config.addConfig(ButtonAsTrigger(BUTTON_IN_13, TRIGGER_RIGHT))

    config.addConfig(JoystickAsJoystick(JOYSTICK_IN_0, AXIS_NON_INVERTED, AXIS_NON_INVERTED, JOYSTICK_LEFT, 0.05, 0.05))
    config.addConfig(JoystickAsJoystick(JOYSTICK_IN_1, AXIS_NON_INVERTED, AXIS_NON_INVERTED, JOYSTICK_RIGHT, 0.05, 0.05))

    config.addConfig(EncoderAsButton(ENCODER_SPEED_BASED, ENCODER_DIR_CLOCKWISE, AXIS_NON_INVERTED, 5.0, BUTTON_LEFT))
    config.addConfig(EncoderAsButton(ENCODER_SPEED_BASED, ENCODER_DIR_COUNTERCLOCKWISE, AXIS_NON_INVERTED, 5.0, BUTTON_RIGHT))

    #Configuration Directory
    configDir = "configs/"
    
    #Check if folder exists
    if not os.path.isdir(configDir):
        os.makedirs(configDir)
        print("Created folder : ", configDir)
    filePath = os.path.join(configDir, config.configName + ".cfg")

    config.printConfigToFile(filePath)
    return config

if __name__ == "__main__":
    config = test()
