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
JOYSTICK_RIGHT = 0
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

class Controller_Configuration():
    def __init__(self, profile_number, config_name, led_colors, led_brightness):
        self.profile_number = profile_number
        self.config_name = config_name
        self.led_colors = led_colors
        self.led_colors_bytes = self.set_led_colors(led_colors)
        self.led_brightness = led_brightness
        self.configurations = []

    def add_config(self, configuration):
        self.configurations.append(configuration)

    def delete_config(self, configuration):
        self.configurations.pop(configuration)

    def get_number_of_configurations(self):
        return len(self.configurations)

    def set_led_colors(self, led_colors):
        self.led_colors_bytes = b""
        for i in self.led_colors:
            self.led_colors_bytes += bytes(i)
        return self.led_colors_bytes

    def get_led_colors_bytes(self):
        return self.led_colors_bytes

    def led_bytes_to_colors(bytes_in):
        led_colors = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(4):
            for j in range(3):
                led_colors[i, j] = bytes_in[i + j]
        return led_colors

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
            f.write(bytes([self.led_brightness]))
            f.write(self.config_name[:CONFIG_NAME_LENGTH].ljust(CONFIG_NAME_LENGTH, chr(0)).encode(BYTE_ENCODING))
            for config in self.configurations:
                config_bytes = config.to_bytes()
                f.write(config_bytes)
                f.write(bytes([0xff]))

        #Report file size
        byte_cnt = os.path.getsize(file_path)
        print("Total bytes used in configuration: {} of {}. ({:0.2f}%)".format(byte_cnt, CONFIGURATION_SIZE, 100 * byte_cnt / CONFIGURATION_SIZE))

        #Write text file for array initialization
        self.print_config_to_txt_file(path)

    def print_config_to_txt_file(self, path):
        #Check if folder exists
        file_path_txt = os.path.join(path, self.config_name + ".txt")
        file_path_cfg = os.path.join(path, self.config_name + ".cfg")

        #Write to file
        with open(file_path_txt, "w") as f_txt:
            f_txt.write("{ ")
            with open(file_path_cfg, "rb") as f_cfg:
                for byte in f_cfg.read():
                    f_txt.write("{}, ".format(byte))
            f_txt.write("}")

    def from_bytes(bytes_in):
        profile_number = struct.unpack("<B", bytes_in[0])
        led_colors = Controller_Configuration.led_bytes_to_colors(struct.unpack("<BB", bytes_in[1:3]))
        config_name = struct.unpack("<{}s".format(CONFIG_NAME_LENGTH), bytes_in[3:4+CONFIG_NAME_LENGTH])
        cc = Controller_Configuration(profile_number, config_name, led_colors)
        config_start = True
        config_start_add = 0
        for i in range(4 + CONFIG_NAME_LENGTH, len(bytes_in)):
            if(config_start):
                t = bytes_in[i]
                config_start = False
                config_start_add = i
            if bytes_in[i] == 255:
                config_start = True
                cc.add_config(Controller_Configuration.parse_config_from_bytes(t, bytes_in[config_start_add : i]))

    def parse_config_from_bytes(t, bytes_in):
        if t == INPUT_BUTTON_AS_BUTTON:
            return Button_as_Button.from_bytes(bytes_in)

class Button_as_Button():
    def __init__(self, button_in, button_out):
        self.button_in = button_in
        self.button_out = button_out
        self.type = INPUT_BUTTON_AS_BUTTON
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack("<BBB", self.type, self.button_in, self.button_out)
        return self.struct

    def from_bytes(bytes_in):
        (t, button_in, button_out) = struct.unpack("<BBB", bytes_in)
        return Button_as_Button(button_in, button_out)

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
        self.struct = struct.pack("<BBB", self.type, self.button_in, b1)
        return self.struct

    def from_bytes(bytes_in):
        (t, button_in, b1) = struct.unpack("<BBB", bytes_in)
        joystick_lr = (b1 >> 0) & 1
        axis_xy = (b1 >> 1) & 1
        pos_neg = (b1 >> 2) & 1
        return Button_as_Joystick(button_in, joystick_lr, axis_xy, pos_neg)

class Button_as_Keyboard():
    def __init__(self, button_in, string):
        self.button_in = button_in
        self.string = string
        self.type = INPUT_BUTTON_AS_KEYBOARD
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack("<BB{}s".format(len(self.string)), self.type, self.button_in, bytes(self.string, BYTE_ENCODING))
        return self.struct

    def from_bytes(bytes_in, str_len):
        (t, button_in, string) = struct.unpack("<BB{}s".format(str_len), bytes_in)
        return Button_as_Keyboard(button_in, string)

class Button_as_Trigger():
    def __init__(self, button_in, trigger_lr):
        self.button_in = button_in
        self.trigger_lr = trigger_lr
        self.type = INPUT_BUTTON_AS_TRIGGER
        self.struct = b""

    def to_bytes(self):
        self.struct = struct.pack("<BBB", self.type, self.button_in, self.trigger_lr)
        return self.struct

    def from_bytes(bytes_in):
        (t, button_in, trigger_lr) = struct.unpack("<BBB", bytes_in)
        return Button_as_Trigger(button_in, trigger_lr)

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
        self.struct = struct.pack("<BBfB", self.type, b0, self.threshold, self.button_out)
        return self.struct

    def from_bytes(bytes_in):
        (t, b0, threshold, button_out) = struct.unpack("<BBfB", bytes_in)
        axis_xy = (b0 >> 0) & 1
        invert = (b0 >> 1) & 1
        pos_neg = (b0 >> 2) & 1
        return Joystick_as_Button(joystick_lr, axis_xy, invert, pos_neg, threshold, button_out)

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
        self.struct = struct.pack("<BBff", self.type, b0, self.deadzone_x, self.deadzone_y)
        return self.struct

    def from_bytes(bytes_in):
        (t, b0, deadzone_x, deadzone_y) = struct.unpack("<BBff", bytes_in)
        joystick_in = (b0 >> 0) & 1
        invert_x = (b0 >> 1) & 1
        invert_y = (b0 >> 2) & 1
        joystick_out = (b0 >> 3) & 1
        return Joystick_as_Joystick(joystick_in, invert_x, invert_y, joystick_out, deadzone_x, deadzone_y)

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
        self.struct = struct.pack("<BBf{}s".format(len(self.string)), self.type, b0, self.threshold, bytes(self.string, BYTE_ENCODING))
        return self.struct

    def from_bytes(bytes_in, str_len):
        (t, b0, threshold, string) = struct.unpack("<BBf{}s".format(str_len), bytes_in)
        joystick_in = (b0 >> 0) & 1
        axis_xy = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        pos_neg = (b0 >> 3) & 1
        return Joystick_as_Keyboard(joystick_in, axis_xy, invert, pos_neg, threshold, string)

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
        self.struct = struct.pack("<BBf".format(len(self.string)), self.type, b0, self.threshold)
        return self.struct

    def from_bytes(bytes_in):
        (t, b0, threshold) = struct.unpack("<BBf", bytes_in)
        joystick_in = (b0 >> 0) & 1
        axis_xy = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        pos_neg = (b0 >> 3) & 1
        trigger_out = (b0 >> 4) & 1
        return Joystick_as_Trigger(joystick_in, axis_xy, invert, pos_neg, trigger_out)

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
        self.struct = struct.pack("<BBfB", self.type, b0, self.threshold, self.button_out)
        return self.struct

    def from_bytes(bytes_in):
        (t, b0, threshold, button_out) = struct.unpack("<BBfB", bytes_in)
        speed_based = (b0 >> 0) & 1
        ccw = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        return Encoder_as_Button(speed_based, ccw, invert, threshold, button_out)

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
        self.struct = struct.pack("<BBfffB".format(len(self.string)), self.type, b0, self.speed_threshold, self.linear_middle, self.linear_deadzone, b13)
        return self.struct

    def from_bytes(bytes_in):
        (t, b0, speed_threshold, linear_middle, linear_deadzone, b13) = struct.unpack("<BBfffB", bytes_in)
        binary_based = (b0 >> 0) & 1
        speed_based = (b0 >> 1) & 1
        ccw = (b0 >> 2) & 1
        invert = (b0 >> 3) & 1
        joystick_out = (b13 >> 0) & 1
        axis_xy = (b13 >> 1) & 1
        pos_neg = (b13 >> 2) & 1
        return Encoder_as_Joystick(binary_based, speed_based, ccw, invert, speed_threshold, linear_middle, linear_deadzone, joystick_out, axis_xy, pos_neg)

class Encoder_as_Keyboard():
    def __init__(self, speed_based, ccw, invert, threshold, string):
        self.speed_based = speed_based
        self.ccw = ccw
        self.invert = invert
        self.threshold = float(threshold)
        self.string = string
        self.type = INPUT_ENCODER_AS_KEYBOARD
        self.struct = b""

    def to_bytes(self):
        b0 = 0
        b0 |= self.speed_based << 0
        b0 |= self.ccw << 1
        b0 |= self.invert << 2
        self.struct = struct.pack("<BBf{}s".format(len(self.string)), self.type, b0, self.threshold, self.string)
        return self.struct

    def from_bytes(bytes_in, str_len):
        (t, b0, threshold, string) = struct.unpack("<BBfB{}s".format(str_len), bytes_in)
        speed_based = (b0 >> 0) & 1
        ccw = (b0 >> 1) & 1
        invert = (b0 >> 2) & 1
        return Encoder_as_Keyboard(speed_based, ccw, invert, threshold, string)

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
        self.struct = struct.pack("<BBfffB", self.type, b0, self.speed_threshold, self.linear_middle, self.linear_deadzone, self.trigger_out)
        return self.struct

    def from_bytes(bytes_in):
        (t, b0, speed_threshold, linear_middle, linear_deadzone, trigger_out) = struct.unpack("<BBfffB", bytes_in)
        binary_based = (b0 >> 0) & 1
        speed_based = (b0 >> 1) & 1
        ccw = (b0 >> 2) & 1
        invert = (b0 >> 3) & 1
        return Encoder_as_Trigger(binary_based, speed_based, ccw, invert, speed_threshold, linear_middle, linear_deadzone, trigger_out)
    
if __name__ == "__main__":
    print("Creating Default Joystick Configurations")
    config0 = Controller_Configuration(0, "GMK Controller - Default Configuration 1", [[255, 0, 0], [0, 255, 0], [0, 0, 255], [50, 0, 50]], 32)
    config0.add_config(Button_as_Button(BUTTON_IN_0, BUTTON_A))
    config0.add_config(Button_as_Button(BUTTON_IN_1, BUTTON_B))
    config0.add_config(Button_as_Button(BUTTON_IN_2, BUTTON_X))
    config0.add_config(Button_as_Button(BUTTON_IN_3, BUTTON_Y))
    config0.add_config(Button_as_Button(BUTTON_IN_4, BUTTON_LB))
    config0.add_config(Button_as_Button(BUTTON_IN_5, BUTTON_RB))
    config0.add_config(Button_as_Button(BUTTON_IN_6, BUTTON_RTH))
    config0.add_config(Button_as_Button(BUTTON_IN_7, BUTTON_RTH))
    config0.add_config(Button_as_Button(BUTTON_IN_8, BUTTON_LEFT))
    config0.add_config(Button_as_Button(BUTTON_IN_9, BUTTON_RIGHT))
    config0.add_config(Button_as_Button(BUTTON_IN_10, BUTTON_START))
    config0.add_config(Button_as_Button(BUTTON_IN_11, BUTTON_BACK))

    config0.add_config(Button_as_Trigger(BUTTON_IN_12, TRIGGER_LEFT))
    config0.add_config(Button_as_Trigger(BUTTON_IN_13, TRIGGER_RIGHT))

    config0.add_config(Joystick_as_Joystick(JOYSTICK_IN_0, AXIS_NON_INVERTED, AXIS_NON_INVERTED, JOYSTICK_LEFT, 0.05, 0.05))
    config0.add_config(Joystick_as_Joystick(JOYSTICK_IN_1, AXIS_NON_INVERTED, AXIS_NON_INVERTED, JOYSTICK_RIGHT, 0.05, 0.05))

    config0.add_config(Encoder_as_Button(ENCODER_SPEED_BASED, ENCODER_DIR_CLOCKWISE, AXIS_NON_INVERTED, 1.0, BUTTON_LEFT))
    config0.add_config(Encoder_as_Button(ENCODER_SPEED_BASED, ENCODER_DIR_COUNTERCLOCKWISE, AXIS_NON_INVERTED, 1.0, BUTTON_RIGHT))

    config0.print_config_to_file("configs/")
