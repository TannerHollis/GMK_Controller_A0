import serial
import pygame
import struct
import numpy
from classes import *
import time

VID = 1155
PID = 22336
PORT = "COM5"

s = serial.Serial()
s.baudrate = 192000
s.port = PORT
s.parity = "N"

def open_device():
    s.port = PORT
    try:
        s.open()
        print("Successfully opened device on port: " + PORT)
    except:
        print("Failed to acces device on port: " + PORT)

def test_send():
    if s.isOpen():
        s.write(r"0"*65)
        time.sleep(1)
        print(s.read())

def test_read():
    if s.isOpen():
        s.write(r"1" + r"0"*64)
        time.sleep(1)
        print(s.read())
    
def validate_port():
    com_port.text = com_port.text[0:com_port.entry_length]
    PORT = com_port.text
    s.port = PORT
    open_device_button.text = "Open Device on: " + PORT

pygame.font.init()
font = pygame.font.SysFont("Consolas", 10)

window_size = (500, 220)
screen = pygame.display.set_mode(window_size)
text_controller = TextController(screen, [])

title = EdittableText(text_controller, "GMK Controller Serial Test", "", "", (window_size[0]/2, 20), BLACK, 24, None, align="C", entry=False, clickable=False)

test_send_button = Button(text_controller, "Test Device (Send 0x00)", (window_size[0]/2, 50), BLACK, 24, None, align="C", clickable=True)
test_send_button.command = test_send

test_read_config_button = Button(text_controller, "Test Read Config (Send 0x01)", (window_size[0]/2, 80), BLACK, 24, None, align="C", clickable=True)
test_read_config_button.command = test_read

open_device_button = Button(text_controller, "Open Device on: " + PORT, (window_size[0]/4, 200), BLACK, 24, None, align="C", clickable=True)
open_device_button.command = open_device

com_port = EdittableText(text_controller, PORT, "Port: ", "", (window_size[0]*3/4, 200), BLACK, 24, None, align="C", entry=True, clickable=True, entry_length=6)
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

    
