import serial
import pygame
import numpy
from gui_classes import *
from config_classes import *
import time

VERSION_STR_LENGTH = 24

CONFIG_FILE_NAME = "configs/GMK Controller - Default Configuration 1.cfg"

VID = 1155
PID = 22336
port_name = "COM7"

s = serial.Serial()
s.baudrate = 38400
s.port = port_name
s.parity = "N"

def open_device():
    s.port = com_port.text
    try:
        s.open()
        print("Successfully opened device on port: " + com_port.text)
    except:
        print("Failed to acces device on port: " + com_port.text)

def test_send():
    if s.isOpen():
        s.write(bytes([0]))
        print(s.read(VERSION_STR_LENGTH))

def test_read():
    if s.isOpen():
        s.write(bytes([0x40]))
        print(s.read(CONFIGURATION_SIZE))

def test_write():
    if s.isOpen():
        config = bytes([0x80])
        with open(CONFIG_FILE_NAME, "rb") as f:
            config += f.read(CONFIGURATION_SIZE)
            config += (CONFIGURATION_SIZE - len(config))*b"0"
        s.write(config)
        print("Wrote {} to Controller.".format(CONFIG_FILE_NAME))
    
def validate_port():
    com_port.text = com_port.text[0:com_port.entry_length]

pygame.font.init()
font = pygame.font.SysFont("Consolas", 10)

window_size = (500, 220)
screen = pygame.display.set_mode(window_size)
text_controller = TextController(screen, [])

title = EdittableText(text_controller, "GMK Controller Serial Test", "", "", (window_size[0]/2, 20), BLACK, 24, None, align="C", entry=False, clickable=False)

test_send_button = Button(text_controller, "Test Device (Send 0x00)", (window_size[0]/2, 50), BLACK, 24, None, align="C", clickable=True)
test_send_button.command = test_send

test_read_config_button = Button(text_controller, "Test Read Config (Send 0x40)", (window_size[0]/2, 80), BLACK, 24, None, align="C", clickable=True)
test_read_config_button.command = test_read

test_write_config_button = Button(text_controller, "Test Write Config (Send 0x80)", (window_size[0]/2, 110), BLACK, 24, None, align="C", clickable=True)
test_write_config_button.command = test_write

open_device_button = Button(text_controller, "Open Device", (window_size[0]/4, 200), BLACK, 24, None, align="C", clickable=True)
open_device_button.command = open_device

com_port = EdittableText(text_controller, port_name, "Port: ", "", (window_size[0]*3/4, 200), BLACK, 24, None, align="C", entry=True, clickable=True, entry_length=6)
com_port.validate = validate_port

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        text_controller.process_events(event)

    screen.fill(WHITE)

    text_controller.render()
    
    pygame.display.update()

pygame.quit()

    
