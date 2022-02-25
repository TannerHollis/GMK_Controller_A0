import pygame
from pygame.locals import *
import time, math

RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 150)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
OFF_BLACK = (50, 50, 50)
DARK_GRAY = (100, 100, 100)
GRAY = (150, 150, 150)
LIGHT_GRAY = (200, 200, 200)
OFF_WHITE = (225, 225, 225)
WHITE = (255, 255, 255)

class Graph:
    def __init__(self, screen, pos, width, height, background):
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.background = background
        self.points = []
        self.actual_points = []
        self.dac_bits = 8
        self.d_y = 1 / (2**self.dac_bits-1)
        self.x_points = 64
        self.max_frequency = 100e3
        self.d_x_min = 1 / self.max_frequency
        self.d_x = 1 / (self.x_points)
        self.current_point = None
        self.mouse_is_down = False
        self.point_found = False
        self.show_lines = True
        self.show_actual_lines = False
        self.approx_points = False
        self.show_points = True
        self.current_waveform = None

    def change_dac_bits(self, dac_bits):
        self.dac_bits = dac_bits
        self.d_y = 1 / (2**self.dac_bits-1)

    def change_points(self, points):
        self.x_points = points
        self.d_x = 1 / (self.x_points)

    def render(self):
        self.draw_grid()
        self.rect = Rect(self.pos, (self.width, self.height))
        pygame.draw.rect(self.screen, self.background, self.rect, 2)

        if self.show_actual_lines:
            n_points = len(self.actual_points)
            if n_points > 0:
                pygame.draw.line(self.screen, DARK_GREEN, (self.pos[0], self.actual_points[0].pos[1]), self.actual_points[0].pos)
                for n in range(n_points-1):
                    pos_0 = self.actual_points[n].pos
                    pos_1 = self.actual_points[n+1].pos
                    pygame.draw.line(self.screen, DARK_GREEN, pos_0, (pos_0[0] + self.d_x*self.width, pos_0[1]))
                    pygame.draw.line(self.screen, DARK_GREEN, (pos_0[0] + self.d_x*self.width, pos_0[1]), pos_1)
                    pygame.draw.line(self.screen, DARK_GREEN, pos_1, (pos_1[0] + self.d_x*self.width, pos_1[1]))

        if self.show_lines:
            n_points = len(self.points)
            if n_points > 0:
                left = (self.pos[0], self.points[0].pos[1])
                right = (self.pos[0]+self.width, self.points[n_points-1].pos[1])
                pygame.draw.line(self.screen, BLUE, left, self.points[0].pos)
                pygame.draw.line(self.screen, BLUE, right, self.points[n_points-1].pos)
                for n in range(n_points-1):
                    pygame.draw.line(self.screen, BLUE, self.points[n].pos, self.points[n+1].pos)

        if self.show_points:
            for point in self.points:
                point.render()

    def process_actual_points(self):
        self.actual_points = []
        if len(self.points)==0:
            None
        else:
            if not self.approx_points:
                val = self.points[0].val
                for n in range(self.x_points):
                    t = n*self.d_x
                    for point in self.points:
                        if t == point.t:
                            val = point.val
                    actual_point = GraphPoint(self, t, val, BLACK, clickable=False)
                    actual_point.set_pos_from_vals(t, val)
                    self.actual_points.append(actual_point)
            else:
                n_points = len(self.points)
                point_first = self.points[0]
                point_last = self.points[n_points-1]
                for i in range(round(point_first.t/self.d_x)):
                    t = i*self.d_x
                    val = point_first.val
                    actual_point = GraphPoint(self, t, val, BLACK, clickable=False)
                    actual_point.set_pos_from_vals(t, val)
                    self.actual_points.append(actual_point)

                for i in range(0, n_points-1):
                    if not self.points[i+1].t - self.points[i].t == 0:
                        dy_dx = (self.points[i+1].val - self.points[i].val)/(self.points[i+1].t - self.points[i].t)
                        for n in range(round((self.points[i+1].t - self.points[i].t)/self.d_x)):
                            t = n*self.d_x + self.points[i].t
                            val = dy_dx*n*self.d_x + self.points[i].val
                            actual_point = GraphPoint(self, t, val, BLACK, clickable=False)
                            actual_point.set_pos_from_vals(t, val)
                            self.actual_points.append(actual_point)

                for i in range(round((1 - point_last.t)/self.d_x)):
                    t = i*self.d_x + point_last.t
                    val = point_last.val
                    actual_point = GraphPoint(self, t, val, BLACK, clickable=False)
                    actual_point.set_pos_from_vals(t, val)
                    self.actual_points.append(actual_point)

    def draw_grid(self):
        if self.width / self.x_points > 1.5:
            for n in range(self.x_points):
                x = self.d_x*n*self.width + self.pos[0]
                top = (x, self.pos[1])
                bottom = (x, self.pos[1] + self.height)
                pygame.draw.line(self.screen, OFF_WHITE, top, bottom)

        if self.height / (2**self.dac_bits-1) > 1.5:            
            for n in range(2**self.dac_bits-1):
                y = self.d_y*n*self.height + self.pos[1]
                left = (self.pos[0], y)
                right = (self.pos[0] + self.width, y)
                pygame.draw.line(self.screen, LIGHT_GRAY, left, right)

    def sort_points(self):
        self.points.sort(key=lambda x: x.t)
        self.process_actual_points()

    def process_events(self, event):
        if event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                for point in self.points:
                    if point.selected:
                        self.points.pop(self.points.index(point))
                        self.sort_points()

        if event.type == MOUSEBUTTONDOWN:
            self.mouse_is_down = True
            self.point_found = False
            self.check_click(event.pos)
                    
        if event.type == MOUSEBUTTONUP:
            self.mouse_is_down = False
            self.current_point = None

    def process_input(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.mouse_is_down and self.current_point:
            if self.check_mouse(mouse_pos):
                self.current_point.set_vals_from_pos(mouse_pos)
                self.sort_points()

    def check_click(self, click_pos):
        x_is_in_bounds = click_pos[0] >= self.pos[0] and click_pos[0] <= self.pos[0] + self.width
        y_is_in_bounds = click_pos[1] >= self.pos[1] and click_pos[1] <= self.pos[1] + self.height

        if x_is_in_bounds and y_is_in_bounds:
            if len(self.points)>0:
                for point in self.points:
                    if point.check_click(click_pos):
                        self.point_found = True
                        self.current_point = point

            if not self.point_found:
                point = GraphPoint(self, 0, 0, BLACK, clickable=True, clickable_by_radius=True, click_radius=10)
                point.set_vals_from_pos(click_pos)
                point.selected = True
                self.points.append(point)
                self.sort_points()
                self.current_point = point
        else:
            for point in self.points:
                if point.selected:
                    point.selected = False

    def check_mouse(self, mouse_pos):
        x_is_in_bounds = mouse_pos[0] >= self.pos[0] and mouse_pos[0] <= self.pos[0] + self.width
        y_is_in_bounds = mouse_pos[1] >= self.pos[1] and mouse_pos[1] <= self.pos[1] + self.height
        return x_is_in_bounds and y_is_in_bounds
        
class GraphPoint:
    def __init__(self, parent, t, val, color, clickable=False, clickable_by_radius=False, click_radius = 10, click_bounds= (0, 0)):
        self.parent = parent
        self.val = val
        self.t = t
        self.pos = (0, 0)
        self.color = color
        self.clickable = clickable
        self.clickable_by_radius = clickable_by_radius
        self.click_radius = click_radius
        self.click_bounds = click_bounds
        self.selected = False

    def render(self):
        if self.selected:
            color = RED
        else:
            color = self.color
        pygame.draw.circle(self.parent.screen, color, self.pos, 5)

    def set_vals_from_pos(self, pos):
        self.val = 1 - (pos[1] - self.parent.pos[1]) / self.parent.height
        self.check_val_bounds()
        self.t = (pos[0] - self.parent.pos[0]) / self.parent.width
        self.set_pos_from_vals(self.t, self.val)

    def set_pos_from_vals(self, t, val):
        self.t = round(t / self.parent.d_x) * self.parent.d_x
        self.val = round(val / self.parent.d_y) * self.parent.d_y
        self.check_val_bounds()
        x = self.t * self.parent.width + self.parent.pos[0]
        y = self.parent.pos[1] + self.parent.height - self.val * self.parent.height
        self.pos = (int(x), int(y))

    def check_val_bounds(self):
        if self.val > 1:
            self.val = 1
        if self.val < 0:
            self.val = 0

    def check_click(self, click_pos):
        self.selected = False
        if self.clickable:
            if self.clickable_by_radius:
                d_y = click_pos[1] - self.pos[1]
                d_x = click_pos[0] - self.pos[0]
                dist = math.sqrt(d_y*d_y + d_x*d_x)
                if dist <= self.click_radius:
                    self.selected = True
                    return True
            else:
                x_is_in_bounds = click_pos[0] >= self.pos[0] - self.click_bounds[0]/2 and click_pos[0] <= self.pos[0] + self.click_bounds[0]/2
                y_is_in_bounds = click_pos[1] >= self.pos[1] - self.click_bounds[1]/2 and click_pos[1] <= self.pos[1] + self.click_bounds[1]/2
                if x_is_in_bounds and y_is_in_bounds:
                    self.selected = True
                    return True
                
class TextController:
    def __init__(self, screen, texts):
        self.screen = screen
        self.texts = texts
        self.text_found = False
        self.current_text = None

    def process_events(self, event):
        if event.type == KEYDOWN:
            if self.current_text:
                if event.key == K_BACKSPACE and self.current_text:
                    if len(self.current_text.text)>0:
                        self.current_text.text = self.current_text.text[:-1]
                        self.current_text.validate()
                elif event.key == K_RETURN or event.key == K_KP_ENTER and self.current_text:
                    self.current_text.command()
                else:
                    self.current_text.text += event.unicode
                    self.current_text.validate()
            
        if event.type == MOUSEBUTTONDOWN:
            self.text_found = False
            self.check_click(event.pos)

    def render(self):
        for text in self.texts:
            text.render()

    def check_click(self, click_pos):
        for text in self.texts:
            if text.check_click(click_pos):
                self.current_text = text
                self.text_found = True
                
        if not self.text_found:
            self.current_text = None

class EdittableText:
    def __init__(self, parent, text, prefix, suffix, pos, color, size, font, align="L", clickable=False, entry=False, entry_length=0):
        self.parent = parent
        self.text = text
        self.prefix = prefix
        self.suffix = suffix
        self.pos = pos
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont(font, self.size)
        self.align = align
        self.clickable = clickable
        self.entry = entry
        self.entry_length = entry_length
        self.selected = False
        self.parent.texts.append(self)

    def render(self):
        pre = self.font.render("{}".format(self.prefix), True, self.color)
        pre_rect = pre.get_rect()
        text = self.font.render("{}".format(self.text), True, self.color)
        text_rect = text.get_rect()
        suff = self.font.render("{}".format(self.suffix), True, self.color)
        suff_rect = suff.get_rect()
        
        if self.align == "L": 
            pre_rect.midleft = self.pos
            text_rect.topleft = pre_rect.topright
            suff_rect.topleft = text_rect.topright
        elif self.align == "C":
            text_rect.center = self.pos
            pre_rect.topright = text_rect.topleft
            suff_rect.topleft = text_rect.topright
        else:
            suff_rect.midright = self.pos
            text_rect.topright = suff_rect.topleft
            pre_rect.topright = text_rect.topleft

        if self.entry:
            entry_rect = Rect(pre_rect.topright, (self.entry_length*self.size/2, pre_rect.height))
            pygame.draw.rect(self.parent.screen, OFF_WHITE, entry_rect)
                    
        if time.time() % 1 > 0.5 and self.selected:
            cursor = Rect(text_rect.topright, (3, text_rect.height))
            pygame.draw.rect(self.parent.screen, self.color, cursor)
            suff_rect.topleft = (text_rect.topright[0] + 3, text_rect.topright[1])
        else:
            suff_rect.topleft = text_rect.topright
        
        self.parent.screen.blit(pre, pre_rect)
        self.parent.screen.blit(text, text_rect)
        self.parent.screen.blit(suff, suff_rect)

    def check_click(self, click_pos):
        if not self.clickable:
            return False
        img = self.font.render("{}{}{}".format(self.prefix, self.text, self.suffix), True, self.color)
        rect = img.get_rect()
        if self.align == "L": 
            rect.midleft = self.pos
        elif self.align == "C":
            rect.center = self.pos
        else:
            rect.midright = self.pos

        if self.entry:
            rect = Rect(rect.topleft, (self.entry_length*self.size/3, rect.height))
            
        x_is_in_bounds = click_pos[0] >= rect.topleft[0] and click_pos[0] <= rect.topleft[0] + rect.size[0]
        y_is_in_bounds = click_pos[1] >= rect.topleft[1] and click_pos[1] <= rect.topleft[1] + rect.size[1]
        if x_is_in_bounds and y_is_in_bounds:
            self.selected = True
            return True
        else:
            self.selected = False
            return False

    def command(self):
        None

    def validate(self):
        None

class CheckBox:
    def __init__(self, parent, text, pos, color, size, font, state=False):
        self.parent = parent
        self.text = text
        self.pos = pos
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont(font, self.size)
        self.state = state
        self.parent.texts.append(self)

    def check_click(self, click_pos):
        box = Rect(self.pos, (self.size / 2, self.size / 2))
        box.midleft = self.pos
        
        x_is_in_bounds = click_pos[0] >= box.topleft[0] and click_pos[0] <= box.topleft[0] + box.size[0]
        y_is_in_bounds = click_pos[1] >= box.topleft[1] and click_pos[1] <= box.topleft[1] + box.size[1]
        if x_is_in_bounds and y_is_in_bounds:
            self.state = not self.state
            self.command()
            
            #To prevent editting text from text_controller
            return False

    def render(self):
        img = self.font.render("{}".format(self.text), True, self.color)
        rect = img.get_rect()
        rect.midleft = (self.pos[0] + self.size, self.pos[1])
        box = Rect(self.pos, (self.size / 2, self.size / 2))
        box.midleft = self.pos
        self.parent.screen.blit(img, rect)
        pygame.draw.rect(self.parent.screen, self.color, box, self.state==False)

    def command(self):
        None

class Button:
    def __init__(self, parent, text, pos, color, size, font, align="L", clickable=True):
        self.parent = parent
        self.text = text
        self.pos = pos
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont(font, self.size)
        self.align = align
        self.clickable = clickable
        self.clicked = False
        self.time_clicked = 0
        self.parent.texts.append(self)

    def check_click(self, click_pos):
        if not self.clickable:
            return False
        img = self.font.render("{}".format(self.text), True, self.color)
        rect = img.get_rect()
        box = Rect(self.pos, (rect.size[0] + 10, rect.size[1] + 10))
        if self.align == "L":
            box.midleft = self.pos
            rect.center = box.center
        elif self.align == "C":
            rect.center = self.pos
            box.center = self.pos
        else:
            box.midright = self.pos
            rect.center = box.center
        
        x_is_in_bounds = click_pos[0] >= box.topleft[0] and click_pos[0] <= box.topleft[0] + box.size[0]
        y_is_in_bounds = click_pos[1] >= box.topleft[1] and click_pos[1] <= box.topleft[1] + box.size[1]
        if x_is_in_bounds and y_is_in_bounds:
            self.clicked = True
            self.time_clicked = time.time()
            self.command()
            
            #To prevent editting text from text_controller
            return False

    def render(self):
        if self.clicked:
            color = WHITE
        else:
            color = self.color
        img = self.font.render("{}".format(self.text), True, color)
        rect = img.get_rect()
        box = Rect(self.pos, (rect.size[0] + 10, rect.size[1] + 10))
        if self.align == "L":
            box.midleft = self.pos
            rect.center = box.center
        elif self.align == "C":
            rect.center = self.pos
            box.center = self.pos
        else:
            box.midright = self.pos
            rect.center = box.center
        pygame.draw.rect(self.parent.screen, LIGHT_GRAY, box)
        self.parent.screen.blit(img, rect)

        if time.time() - self.time_clicked > 0.15 and self.clicked:
            self.clicked = False

    def command(self):
        None

def eng_note_to_str(val):
    scale = 1e-15
    i = 0
    if val == 0:
        return ("", 0)
    while val/scale > 999.99999999:
        scale = scale * 1000
        i += 1
    prefix = "None"
    if i == 0:
        prefix = "p"
    elif i == 1:
        prefix = "f"
    elif i == 2:
        prefix = "n"
    elif i == 3:
        prefix = "u"
    elif i == 4:
        prefix = "m"
    elif i == 5:
        prefix = ""
    elif i == 6:
        prefix = "k"
    elif i == 7:
        prefix = "M"
    elif i == 8:
        prefix = "G"
    return (prefix, round(val/scale, 6))

def str_to_eng_note(string):
    unit_pos = 0
    unit_found = False
    for i in range(len(string)):
        if string[i] in ["p", "f", "n", "u", "m", "k", "M", "G"]:
            unit_found = True
            unit_pos = i
            break

    if unit_found:
        unit = string[i:]
        val = float(string[:i])
    else:
        val = float(string[:i+1])
        unit = ""
    scale = None
    if unit == "p":
        scale = 1e-15
    elif unit == "f":
        scale = 1e-12
    elif unit == "n":
        scale = 1e-9
    elif unit == "u":
        scale = 1e-6
    elif unit == "m":
        scale = 1e-3
    elif unit == "":
        scale = 1
    elif unit == "k":
        scale = 1e3
    elif unit == "M":
        scale = 1e6
    elif unit == "G":
        scale = 1e9
    if scale:
        return val*scale
    else:
        return False
    
def check_char(char):
    return (char in ["p", "f", "n", "u", "m", "k", "M", "G"] or char.isdigit() or char == ".")

def check_num(char):
    return (char.isdigit() or char == ".")

def is_float(string):
    is_float = True
    if string == "." or string.count(".") > 1:
        is_float = False
    for char in string:
        if not (char.isdigit() or char == "."):
            is_float = False
    return is_float
