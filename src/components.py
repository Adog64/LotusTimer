import pygame
from src.settings import *
from collections.abc import Iterable
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
from scipy.interpolate import make_interp_spline
import pylab

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
        self.box = Box(self.center, self.size, enabled=enabled, bordered=enterable, visible=bordered, border_color=border_color, fill_color=background_color)
        self.is_valid_entry = is_valid_entry

    def select(self):
        self.selected = True
        self.box.select()
    
    def deselect(self):
        self.selected = False
        self.box.deselect()

    def render(self, window):
        if not self.valid():
            self.box.border_color = self.invalid_color
        else:
            self.box.border_color = self.border_color
        surface = self.font.render(self.text, True, self.text_color)
        if surface.get_rect().width > self.size[0]:
            surface = pygame.transform.scale(surface, self.size)
        surface_rect = surface.get_rect()
        surface_rect.center = self.center
        if self.bordered:
            self.box.rect.center = self.center
            self.box.render(window)
        if self.text != '':
            window.blit(surface, surface_rect)
    
    def valid(self):
        return self.is_valid_entry(self.text)

    def enter(self, char):
            self.text += char

    def clear(self):
        self.text = ""

    def backspace(self):
        self.text = self.text[:-1]

#display an image on the screen or another component
class Image(AppComponent):
    def __init__(self, center, size, image):
        super().__init__(center=center, size=size, enabled=True)
        self.image = pygame.transform.scale(image, self.size)

    def render(self, window):
        window.blit(self.image, self.rect)


#a toggle switch with similar to a button
class Switch(AppComponent):
    pass

#provides a padded border for other components
#@param bordered - draws a solid line around the box drawn
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


#pressable button capable of executing commands when pressed
#@param image - image displayed on button
#@param text - text displayed on button
#@param mode - either 'i' or 't' for image and text modes respectively
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
    def __init__(self, center, size, font, text_color, text, enabled=True, just='c'):
        super().__init__(center=center, size=size, enabled=enabled)
        self.font = font
        self.text = text
        self.text_color = text_color
        self.fontHeight = self.font.size("Tg")[1]
        self.height = self.fontHeight
        self.just = just

    def render(self, window):
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
        window.blit(lbl, (self.rect.left, self.rect.top + (self.rect.height/2 - bottom)))
        return text


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
    
    def scroll_down(self):
        if self.selected and self.scrolled < 0:
            self.scrolled += self.scroll_speed

class LineGraph(AppComponent):
    def __init__(self, center, size, data, domain, linecolor=(0,0,0)):
        self.data = np.array(data)
        self.domain = np.array(range(domain[0], domain[1]+1))
        self.updated = False
        self.line_color = pygame.Color.normalize(linecolor)

    def update(self, data, domain):
        self.data = np.arange(data)
        self.domain = np.array(range(domain[0], domain[1]+1))
        self.updated = True
    
    def render(self, window):
        #Don't bother recreating the graph if the data hasn't changed
        if not self.updated:
            #Configure the graph settings
            fig = pylab.figure(figsize=[5, 2], dpi=100)
            ax = fig.gca()
            for i in ax.spines.values():
                i.set_visible(False)
            ax.xaxis.set_visible(False)
            ax.tick_params(axis='y', colors=self.line_color) 
            #Convert datapoints into an interpolated smooth curve
            xnew = np.linspace(self.domain.min(), self.domain.max(), 5*len(self.domain)) 
            spl = make_interp_spline(self.domain, self.data, k=3)
            y_smooth = spl(xnew)
            #Plot the data
            ax.plot(xnew, y_smooth, linewidth=2, color=self.line_color, aa=True)
            #Convert the plot into a image string and get its size
            canvas = agg.FigureCanvasAgg(fig)
            canvas.draw()
            renderer = canvas.get_renderer()
            raw_data = renderer.tostring_rgb()
            size = canvas.get_width_height()            
            #Turn graph string into a pygame image object and convert all white pixels to transparent
            surface = pygame.image.fromstring(raw_data, size, "RGB").convert_alpha()
            for x in range(surface.get_width()):
                for y in range(surface.get_height()):
                    if surface.get_at((x, y)) == (255, 255, 255, 255):
                        surface.set_at((x, y), (0, 0, 0, 0))
            #Save the image object
            self.surface = surface
            self.updated = True        
        #Draw the surface
        window.blit(self.surface, self.rect)