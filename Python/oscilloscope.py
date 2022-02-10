import serial
import pygame
import struct
import numpy
import Controller_Data

unpack_format = "ff"
unpack_length = 8

data_labels = ["JS0_X", "JS0_Y"]
data_colors = ((0, 255, 0), (255, 0, 0))
data_length = 512
data_nums = len(data_labels)
data_points = numpy.zeros((data_nums, data_length))
data_write = 0

scale = 5

VID = 1155
PID = 22336
PORT = "COM5"

s = serial.Serial()
s.baudrate = 192000
s.port = PORT
s.parity = "N"
s.open()

pygame.font.init()
font = pygame.font.SysFont("Consolas", 10)

size = width, height = 900, 600
screen = pygame.display.set_mode(size)
delta_x = width / data_length

QUIT = False
while not QUIT:
    raw_bytes = s.read(unpack_length)
    data_in = struct.unpack(unpack_format, raw_bytes)
    for i in range(data_nums):
        data_points[i, data_write] = -data_in[i]*scale + height * (i*2 + 1) / (data_nums + data_nums)
    if data_write == data_length - 1:
        data_write = 0
    else:
        data_write = data_write + 1

    screen.fill((0,0,0))
    for i in range(data_nums):
        text = font.render(data_labels[i], True, data_colors[i])
        screen.blit(text, (width / 2.0, height * (i) / (data_nums)))
        x = 0
        for j in range(data_write, data_length - 1):
            point0 = (delta_x * x, data_points[i, j])
            point1 = (delta_x * (x + 1), data_points[i, j+1])
            pygame.draw.line(screen, data_colors[i], point0, point1, 1)
            x = x + 1
        for j in range(0, data_write - 1):
            point0 = (delta_x * x, data_points[i, j])
            point1 = (delta_x * (x + 1), data_points[i, j+1])
            pygame.draw.line(screen, data_colors[i], point0, point1, 1)
            x = x + 1
            
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            QUIT = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            scale += 5
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            scale -= 5

pygame.quit()

    
