import struct

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

BYTE_ENCODING = "hex"

class Button_as_Button():
    def __init__(self, button_in, button_out):
        self.button_in = button_in
        self.button_out = button_out
        self.type = INPUT_BUTTON_AS_BUTTON
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack("BBB", self.type, self.button_in, self.button_out)
        return self.struct

class Button_as_Joystick():
    def __init__(self, button_in, joystick_lr, axis_xy, pos_neg):
        self.button_in = button_in
        self.joystick_lr = joystick_lr
        self.axis_xy
        self.pos_neg
        self.type = INPUT_BUTTON_AS_JOYSTICK
        self.struct = b""

    def to_bytes(self):
        b1 = 0
        b1 |= self.joystick_lr << 0
        b1 |= self.axis_xy << 1
        self.struct = struct.pack("BBB", self.type, self.button_in, b1)
        return self.struct

class Button_as_Keyboard():
    def __init__(self, button_in, string):
        self.button_in = button_in
        self.string = string
        self.type = INPUT_BUTTON_AS_KEYBOARD
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack("BB{}s".format(len(self.string)), self.type, self.button_in, bytes(self.string, BYTE_ENCODING))
        return self.struct

class Button_as_Trigger():
    def __init__(self, button_in, trigger_lr):
        self.button_in = button_in
        self.trigger_lr = trigger_lr
        self.type = INPUT_BUTTON_AS_TRIGGER
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack("BBB", self.type, self.button_in, self.trigger_lr)
        return self.struct

class Joystick_as_Button():
    def __init__(self, joystick_lr, axis_xy, invert, pos_neg, threshold, button_out):
        self.joystick_lr = joystick_lr
        self.axis_xy = axis_xy
        self.invert = invert
        self.pos_neg = pos_neg
        self.threshold = float(threshold)
        self.type = INPUT_JOYSTICK_AS_BUTTON
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.joystick_lr << 0
        b0 |= self.axis_xy << 1
        b0 |= self.invert << 2
        b0 |= self.pos_neg << 3
        self.struct = struct.pack("BBfB", self.type, b0, self.threshold, self.button_out)
        return self.struct

class Joystick_as_Joystick():
    def __init__(self, joystick_in, invert_x, invert_y, joystick_out, deadzone_x, deadzone_y):
        self.joystick_in = joystick_in
        self.invert_x = invert_x
        self.invert_y = invert_y
        self.joystick_out = joystick_out
        self.deadzone_x = float(deadzone_x)
        self.deadzone_y = float(deadzone_y)
        self.type = INPUT_JOYSTICK_AS_JOYSTICK
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.joystick_in << 0
        b0 |= self.invert_x << 1
        b0 |= self.invert_y << 2
        b0 |= self.joystick_out << 3
        self.struct = struct.pack("BBff", self.type, b0, self.deadzone_x, self.deadzone_y)
        return self.struct
