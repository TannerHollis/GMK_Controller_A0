import struct
import os

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

#Define configuration output byte formatting
CONFIGURATION_SIZE = 2048
CONFIG_NAME_LENGTH = 64
BYTE_ENCODING = "utf-8"

#Define LED colors
LED_COLOR_NONE = 0
LED_COLOR_RED = 1
LED_COLOR_GREEN = 2
LED_COLOR_YELLOW = 3
LED_COLOR_BLUE = 4
LED_COLOR_PURPLE = 5
LED_COLOR_CYAN = 6
LED_COLOR_WHITE = 7

class Controller_Configuration():
    def __init__(self, profile_number, config_name, led_colors):
        self.profile_number = profile_number
        self.config_name = config_name
        self.led_colors = led_colors
        self.led_colors_bytes = self.set_led_colors(led_colors)
        self.configurations = []

    def add_config(self, configuration):
        self.configurations.append(configuration)

    def delete_config(self, configuration):
        self.configurations.pop(configuration)

    def get_number_of_configurations(self):
        return len(self.configurations)

    def set_led_colors(self, led_colors):
        self.led_colors = led_colors
        b0 = 0x00
        b0 |= self.led_colors[0] << 5
        b0 |= self.led_colors[1] << 2
        b0 |= self.led_colors[2] >> 1
        b1 = 0x00
        b1 |= self.led_colors[2] << 7
        b1 |= self.led_colors[3] << 1
        self.led_colors_bytes = bytes([b0, b1])
        return self.led_colors_bytes

    def get_led_colors_bytes(self):
        return bytes(self.led_colors_bytes)

    def print_config_to_file(self, path):
        #Check if folder exists
        if not os.path.isdir(path):
            os.makedirs(path)
            print("Created folder : ", path)
        file_path = os.path.join(path, self.config_name + ".cfg")

        #Write to file
        with open(file_path, "wb") as f:
            print("Writing to file: {}.cfg".format(file_path))
            f.write(bytes([self.profile_number]))
            f.write(self.get_led_colors_bytes())
            f.write(self.config_name[:64].ljust(64, chr(0)).encode(BYTE_ENCODING))
            for config in self.configurations:
                config_bytes = config.to_bytes()
                f.write(config_bytes)
                f.write(bytes([0xff]))

        #Report file size
        byte_cnt = os.path.getsize(file_path)
        print("Total bytes used in configuration: {} of {}. ({:0.2f}%)".format(byte_cnt, CONFIGURATION_SIZE, 100 * byte_cnt / CONFIGURATION_SIZE))

class Button_as_Button():
    def __init__(self, button_in, button_out):
        self.button_in = button_in
        self.button_out = button_out
        self.type = INPUT_BUTTON_AS_BUTTON
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack(">BBB", self.type, self.button_in, self.button_out)
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
        self.struct = struct.pack(">BBB", self.type, self.button_in, b1)
        return self.struct

class Button_as_Keyboard():
    def __init__(self, button_in, string):
        self.button_in = button_in
        self.string = string
        self.type = INPUT_BUTTON_AS_KEYBOARD
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack(">BB{}s".format(len(self.string)), self.type, self.button_in, bytes(self.string, BYTE_ENCODING))
        return self.struct

class Button_as_Trigger():
    def __init__(self, button_in, trigger_lr):
        self.button_in = button_in
        self.trigger_lr = trigger_lr
        self.type = INPUT_BUTTON_AS_TRIGGER
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack(">BBB", self.type, self.button_in, self.trigger_lr)
        return self.struct

class Joystick_as_Button():
    def __init__(self, joystick_lr, axis_xy, invert, pos_neg, threshold, button_out):
        self.joystick_lr = joystick_lr
        self.axis_xy = axis_xy
        self.invert = invert
        self.pos_neg = pos_neg
        self.threshold = float(threshold)
        self.button_out = button_out
        self.type = INPUT_JOYSTICK_AS_BUTTON
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.joystick_lr << 0
        b0 |= self.axis_xy << 1
        b0 |= self.invert << 2
        b0 |= self.pos_neg << 3
        self.struct = struct.pack(">BBfB", self.type, b0, self.threshold, self.button_out)
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
        self.struct = bytearray(10)

    def to_bytes(self):
        b0 = 0
        b0 |= self.joystick_in << 0
        b0 |= self.invert_x << 1
        b0 |= self.invert_y << 2
        b0 |= self.joystick_out << 3
        self.struct = struct.pack(">BBff", self.type, b0, self.deadzone_x, self.deadzone_y)
        return self.struct

class Joystick_as_Keyboard():
    def __init__(self, joystick_in, axis_xy, invert, pos_neg, threshold, string):
        self.joystick_in = joystick_in
        self.axis_xy = axis_xy
        self.invert = invert
        self.pos_neg = pos_neg
        self.threshold = float(threshold)
        self.type = INPUT_JOYSTICK_AS_KEYBOARD
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.joystick_in << 0
        b0 |= self.axis_xy << 1
        b0 |= self.invert << 2
        b0 |= self.pos_neg << 3
        self.struct = struct.pack(">BBf{}s".format(len(self.string)), self.type, b0, self.threshold, bytes(self.string, BYTE_ENCODING))
        return self.struct

class Joystick_as_Trigger():
    def __init__(self, joystick_in, axis_xy, invert, pos_neg, trigger_out, threshold):
        self.joystick_in = joystick_in
        self.axis_xy = axis_xy
        self.invert = invert
        self.pos_neg = pos_neg
        self.trigger_out = trigger_out
        self.threshold = float(threshold)
        self.type = INPUT_JOYSTICK_AS_TRIGGER
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.joystick_in << 0
        b0 |= self.axis_xy << 1
        b0 |= self.invert << 2
        b0 |= self.pos_neg << 3
        b0 |= self.trigger_out << 4
        self.struct = struct.pack(">BBf".format(len(self.string)), self.type, b0, self.threshold)
        return self.struct

class Encoder_as_Button():
    def __init__(self, speed_based, ccw, invert, threshold, button_out):
        self.speed_based = speed_based
        self.ccw = ccw
        self.invert = invert
        self.threshold = float(threshold)
        self.button_out = button_out
        self.type = INPUT_ENCODER_AS_BUTTON
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.speed_based << 0
        b0 |= self.ccw << 1
        b0 |= self.invert << 2
        self.struct = struct.pack(">BBfB", self.type, b0, self.threshold, self.button_out)
        return self.struct

class Encoder_as_Joystick():
    def __init__(self, binary_based, speed_based, ccw, invert, speed_threshold, linear_middle, linear_deadzone, joystick_out, axis_xy, pos_neg):
        self.binary_based = binary_based
        self.speed_based = speed_based
        self.ccw = ccw
        self.invert = invert
        self.speed_threshold = float(speed_threshold)
        self.linear_middle = float(linear_middle)
        self.linear_deadzone = float(linear_deadzone)
        self.joystick_out = joystick_out
        self.axis_xy = axis_xy
        self.pos_neg = pos_neg
        self.type = INPUT_ENCODER_AS_JOYSTICK
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.binary_based << 0
        b0 |= self.speed_based << 1
        b0 |= self.ccw << 2
        b0 |= self.invert << 3
        b13 = 0
        b13 |= joystick_out << 0
        b13 |= axis_xy << 1
        b13 |= pos_neg << 2
        self.struct = struct.pack(">BBfffB".format(len(self.string)), self.type, b0, self.speed_threshold, self.linear_middle, self.linear_deadzone, b13)
        return self.struct

class Encoder_as_Trigger():
    def __init__(self, binary_based, speed_based, ccw, invert, speed_threshold, linear_middle, linear_deadzone, trigger_out):
        self.speed_based = speed_based
        self.ccw = ccw
        self.invert = invert
        self.speed_threshold = float(speed_threshold)
        self.linear_middle = float(linear_middle)
        self.linear_deadzone = float(linear_deadzone)
        self.trigger_out = trigger_out
        self.type = INPUT_ENCODER_AS_TRIGGER
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.binary_based << 0
        b0 |= self.speed_based << 1
        b0 |= self.ccw << 2
        b0 |= self.invert << 3
        self.struct = struct.pack(">BBfffB", self.type, b0, self.speed_threshold, self.linear_middle, self.linear_deadzone, self.trigger_out)
        return self.struct
    
