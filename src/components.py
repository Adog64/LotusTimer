import pygame
from .settings import *
from collections.abc import Iterable
#import numpy as np
#import matplotlib
#matplotlib.use("Agg")
#import matplotlib.backends.backend_agg as agg
#import pylab

class Enterable:
    def __init__(self):
        pass

    def enter(self, char):
        pass

class AppComponent:
    def __init__(self,center=(0,0), size=(0,0), enabled=True):
        self.size = size
        self.center = center
        self.enabled = enabled
        self.selected = False
        self.updated = False
        self.rect = pygame.Rect(center[0]-size[0]/2, center[1]-size[1]/2, size[0], size[1])

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def render(self, window):
        pass

    def set_rect(self, rect):
        self.rect = rect

    def get_coord(self):
        return self.coord
    
    def select(self):
        self.selected = True

    def update(self):
        self.updated = False

    def deselect(self):
        self.selected = False
    @classmethod
    def valid(cls, *n):
        return True

    
class TextBox(AppComponent, Enterable):
    def __init__(self, font, text_color=(0,0,0), center=(0,0), size=(0,0),
                 enterable=False, text='',enabled=True, bordered=False,
                 border_color=(255,255,255), fill_color=(100,100,100),
                 is_valid_entry=AppComponent.valid, invalid_color=(255,0,0)):
        super().__init__(center=center, size=size, enabled=enabled)
        self.font = font
        self.enterable = enterable
        self.text = text
        self.text_color = text_color
        self.bordered = bordered
        self.border_color = border_color
        self.invalid_color = invalid_color
        self.box = Box(self.center, self.size, enabled=enabled, bordered=enterable, visible=bordered, border_color=border_color, fill_color=box_fill_color)
        self.is_valid_entry = is_valid_entry

    def select(self):
        self.selected = True
        self.box.select()
        self.update()
    
    def deselect(self):
        self.selected = False
        self.box.deselect()
        self.update()

    def render(self, window):
        if not self.updated:
            if self.text != '' and not self.valid():
                self.box.border_color = self.invalid_color
            else:
                self.box.border_color = self.border_color
            self.surface = self.font.render(self.text, True, self.text_color)
            if self.surface.get_rect().width > self.size[0]:
                self.surface = pygame.transform.scale(self.surface, self.size)
            self.surface_rect = self.surface.get_rect()
            self.surface_rect.center = self.center
            if self.bordered:
                self.box.rect.center = self.center
                self.box.render(window)
            if self.text != '':
                window.blit(self.surface, self.surface_rect)
            self.updated = True
        else:
            self.box.render(window)
            window.blit(self.surface, self.surface_rect)
    
    def valid(self):
        return self.is_valid_entry(self.text)

    def enter(self, char):
        self.text += char
        self.update()

    def clear(self):
        self.text = ""
        self.update()

    def backspace(self):
        self.text = self.text[:-1]
        self.update()

#display an image on the screen or another component
class Image(AppComponent):
    def __init__(self, center, size, image):
        super().__init__(center=center, size=size, enabled=True)
        self.image = pygame.transform.smoothscale(image, self.size)

    def render(self, window):
        window.blit(self.image, self.rect)


#a toggle switch with similar to a button
class Switch(AppComponent):
    pass


class Box(AppComponent):
    def __init__(self, center=(0,0), size=(0,0), enabled=True, bordered=False, visible=False, border_color=border_color, fill_color=box_fill_color):
        super().__init__(center=center, size=size, enabled=enabled)
        self.bordered = bordered
        self.visible = visible
        self.color = box_fill_color
        self.default_border_color = border_color
        self.border_color = border_color

    def render(self, window):
        if self.visible:
            pygame.draw.rect(window, self.color, self.rect, width=0, border_radius=10)
            if self.bordered:
                pygame.draw.rect(window, self.border_color, self.rect, width=1, border_radius=10)

    def lighten(self):
        color = []
        lighten_x = 15
        for x in self.color:
            if x < 255 - lighten_x:
                color.append(x+lighten_x)
        self.color = (color[0], color[1], color[2])

    def select(self):
        self.border_color = (255, 255, 0)
    
    def deselect(self):
        self.border_color = self.default_border_color

    def darken(self):
        color = []
        darken_x = 15
        for x in self.color:
            if x >= 0 + darken_x:
                color.append(x-darken_x)
            else:
                color.append(x)
        self.color = (color[0], color[1], color[2])


class Button(AppComponent):
    def __init__(self, center, size, enabled=False, image=None, text='', mode='t', toggle=True, when_pressed=print, when_unpressed=print, text_font=None, wp_arg=None, text_color=(0,0,0)):
        super().__init__(center=center, size=size, enabled=enabled)
        if image != None and mode == 'i':
            self.image = Image(center=center, size=(size[0] - 2*button_img_gap, size[1] - 2*button_img_gap), image=image)
        if mode == 't':
            self.text = TextBox(text_font, text_color, self.center, size=(self.size[0] - 2*button_img_gap, self.size[1] - 2*button_img_gap), text=text, bordered=False)
            self.text.box.darken()
        self.box = Box(center=center, size=size, visible=True)
        self.mode = mode
        self.functions = {'on':when_pressed}
        self.toggle = toggle
        self.wp_arg = wp_arg
        if toggle:
            self.functions['off'] = when_unpressed
        

    def set_when_pressed(self, function=print):
        self.functions['on'] = function
    
    def when_unpressed(self, function=print):
        self.functions['off'] = function

    def select(self):
        if self.wp_arg != None:
            self.functions['on'](self.wp_arg)
        else:
            self.functions['on']()

    def render(self, window):
        self.box.render(window)
        if self.mode == 't':
            self.text.render(window)
        elif self.mode == 'i':
            self.image.render(window)


class Screen(AppComponent):
    def __init__(self, center=(0,0), size=(0,0), enabled=True, components={}):
        super().__init__(center=center, size=size, enabled=enabled)
        self.components = components

    def add_component(self, name, component):
        self.components[name] = component

    def resize_component(self, name, size):
        if name in self.components:
            self.components[name].resize(size)
     
    def disable_component(self, name):
        if name in self.components:
            self.components[name].disable()
    
    def enable_component(self, name):
        if name in self.components:
            self.components[name].enable()
    
    def get_components(self):
        return self.components

    def render(self, window):
        for component in self.components.values():
            component.render(window)
    
    def clicks(self, mouse):
        for component in self.components.values():
            if component.rect.collidepoint(mouse) and component.selected == False:
                component.select()
            elif component.selected == True:
                component.deselect()

    def get_selected(self):
        selections = []
        for component in self.components:
            if self.components[component].selected:
                selections.append(component)
        return selections

    def keys(self, char):
        for component in self.components.values():
            if component.selected and isinstance(component, Enterable):
                component.enter(char)


class Label(AppComponent):
    def __init__(self, center, size, font, text_color, text, enabled=True, just='c', scaling=False):
        super().__init__(center=center, size=size, enabled=enabled)
        self.font = font
        self.text = text
        self.text_color = text_color
        self.fontHeight = self.font.size("Tg")[1]
        self.height = self.fontHeight
        self.just = just
        self.scaling = scaling
    
    def set_text(self, text):
        self.text = text
        self.update()

    def render(self, window):
        if not self.updated:
            if not self.scaling:
                lbl = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
                y = 0
                lineSpacing = -2
                text = self.text
                bottom = 0

                while text:
                    i = 1

                    # determine if the row of text will be outside our area
                    if y + self.fontHeight > self.size[1]:
                        break

                    # determine maximum width of line
                    while self.font.size(text[:i])[0] < self.rect.width and i < len(text):
                        i += 1

                    # if we've wrapped the text, then adjust the wrap to the last word      
                    if i < len(text): 
                        i = text.rfind(" ", 0, i) + 1

                    surface = self.font.render(text[:i], True, self.text_color)
                    sr = surface.get_rect()
                    bottom += sr.bottom
                    if self.just == 'c':
                        lbl.blit(surface, (lbl.get_width()/2 - sr.width/2, y))
                    elif self.just == 'l':
                        lbl.blit(surface, self.rect)
                    y += self.fontHeight + lineSpacing

                    # remove the text we just blitted
                    text = text[i:]
                self.lbl = lbl
                self.lblpos = (self.rect.left, self.rect.top + (self.rect.height/2 - bottom))
                window.blit(lbl, self.lblpos)
                self.updated = True
                return text
            else:
                self.lbl = pygame.transform.smoothscale(self.font.render(self.text, True, self.text_color), self.size)
                self.lblpos = self.rect.topleft  
                window.blit(self.lbl, self.lblpos)
                self.updated = True
        else:
            window.blit(self.lbl, self.lblpos)


class Panel(AppComponent):
    def __init__(self, center, size, enabled=True, items=[], columns=1, column_width=100):
        super().__init__(center=center, size=size, enabled=enabled)
        super().__init__(center=center, size=size, enabled=enabled)
        self.surface = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
        self.items = items
        self.scrolled = 0
        self.items_top = 0
        self.items_bottom = 0
        self.items_height = 0
        self.columns = columns
        self.column_width = column_width

    def set_items(self, items=[]):
        self.items = items
        self.update()
    
    def render(self, window):
        self.surface.fill((0,0,0,0))
        y = self.scrolled
        c = 0
        spacing = 10
        col = 0
        ipc = int(len(self.items)/self.columns)
        row = 0
        if len(self.items)%2 != 0:
            row -= 1
        for i in self.items:
            if not self.updated:
                if isinstance(i, Iterable): 
                    left = i[0].rect.left
                    right = i[0].rect.right
                    top = i[0].rect.top
                    bottom = i[0].rect.bottom
                    for j in i:
                        left = min(j.rect.left, left)
                        right = max(j.rect.right, right)
                        top = min(j.rect.top, top)
                        bottom = max(j.rect.bottom, bottom)
                    s = pygame.Surface((right-left, bottom-top), pygame.SRCALPHA, 32).convert_alpha()
                    for j in i:
                        j.render(s)
                        self.surface.blit(s, (j.rect.left + col*self.column_width, y))
                        y += bottom-top + spacing                
                else:
                    # top = i.rect.top
                    # bottom = i.rect.bottom
                    # if bottom > self.rect.top or top < self.rect.bottom:
                    #     y += i.height + spacing
                    #     continue
                    s = pygame.Surface(i.size, pygame.SRCALPHA, 32).convert_alpha()
                    i.render(s)
                    self.surface.blit(s, (i.rect.left + col*self.column_width, y))
                    y += i.height + spacing
                self.items_bottom = y
                self.items_height = min(y, self.size[1])
                row += 1
                if row == ipc:
                    col += 1
                    row = 0
                    y = self.scrolled
        window.blit(self.surface, self.rect)
            

class ScrollBox(Panel):
    def __init__(self, center, size, enabled, scroll_speed=5, items=[]):
        super().__init__(center, size, enabled=enabled, items=items)
        self.scroll_speed = scroll_speed

    def scroll_up(self):
        if self.selected and self.items_bottom > self.items_height:
            self.scrolled -= self.scroll_speed
            self.update()
    
    def scroll_down(self):
        if self.selected and self.scrolled < 0:
            self.scrolled += self.scroll_speed
            self.update()


# class LineGraph(AppComponent):
#     def __init__(self, center, size, data, domain=None, linecolor=(0,0,0)):
#         super().__init__(center, size, enabled=True)
#         self.data = [item/1000 for item in data]
#         if domain == None:
#             domain = [0, len(data)]
#         self.domain = np.array(range(domain[0], domain[1]))
#         self.line_color = [item/255 for item in linecolor]

#     def update(self, data, domain=None):
#         self.data = [item/1000 for item in data]
#         if domain == None:
#             domain = [0, len(data)]
#         self.domain = np.array(range(domain[0], domain[1]))
#         self.updated = False
     
#     def render(self, window):
#         #Don't bother recreating the graph if the data hasn't changed
#         if not self.updated:
#             if len(self.data) > 0:
#                 #Configure the graph settings
#                 fig = pylab.figure(figsize=[self.size[0]/100, self.size[1]/100], dpi=100)
#                 fig.patch.set_visible(False)
#                 ax = fig.gca()
#                 ax.patch.set_visible(False)
#                 for i in ax.spines.values():
#                     i.set_visible(False)
#                 ax.xaxis.set_visible(False)
#                 ax.tick_params(axis='y', colors=self.line_color) 

#                 #Convert datapoints into a polynomial
#                 y = np.array(self.data)
#                 x = np.array(range(len(y)))
#                 xs = np.linspace(0, len(y) - 1, self.size[1])

#                 poly_deg = min(len(y) - 1, 30)
#                 coefs = np.polyfit(x, y, poly_deg)
#                 y_poly = np.polyval(coefs, xs)
#                 #Plot the data
#                 ax.plot(xs, y_poly, linewidth=2, color=(122/255, 28/255, 1), aa=True) 
#                 #Convert the plot into a image string and get its size
#                 canvas = agg.FigureCanvasAgg(fig)
#                 canvas.draw()
#                 renderer = canvas.get_renderer()
#                 raw_data = renderer.tostring_rgb()
#                 size = canvas.get_width_height()

#                 image = pygame.image.fromstring(raw_data, size, "RGB").convert_alpha()
#                 for x in range(image.get_width()):
#                     for y in range(image.get_height()):
#                         if image.get_at((x, y)) == (255, 255, 255, 255):
#                             image.set_at((x, y), (255, 255, 255, 0))
#                 #Save the image object
#                 self.surface = image
#                 self.updated = True        
#         #Draw the surface
#         window.blit(self.surface, self.rect)