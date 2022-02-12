from config_classes import *

if __name__ == "__main__":
    print("Creating Default Joystick Configurations")
    config0 = Controller_Configuration(0, "GMK Controller - Default Configuration 1", [LED_COLOR_CYAN, LED_COLOR_NONE, LED_COLOR_NONE, LED_COLOR_NONE])
    config0.add_config(Button_as_Button(0, 0))
    config0.add_config(Button_as_Button(1, 1))
    config0.add_config(Button_as_Button(2, 2))
    config0.add_config(Button_as_Button(3, 3))
    config0.add_config(Button_as_Button(4, 4))
    config0.add_config(Button_as_Button(5, 5))
    config0.add_config(Button_as_Button(6, 6))
    config0.add_config(Button_as_Button(7, 7))
    config0.add_config(Button_as_Button(8, 10))
    config0.add_config(Button_as_Button(9, 11))
    config0.add_config(Button_as_Button(10, 12))
    config0.add_config(Button_as_Button(11, 13))

    config0.add_config(Button_as_Trigger(12, 0))
    config0.add_config(Button_as_Trigger(13, 1))

    config0.add_config(Joystick_as_Joystick(0, 0, 0, 0, 0.05, 0.05))
    config0.add_config(Joystick_as_Joystick(1, 0, 0, 1, 0.05, 0.05))

    config0.add_config(Encoder_as_Button(1, 0, 0, 1.0, 8))
    config0.add_config(Encoder_as_Button(1, 1, 0, 1.0, 9))

    config0.print_config_to_file("configs/")
