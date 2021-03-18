import pygame
from settings import *
from collections.abc import Iterable

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
        pass

    def deselect(self):
        pass

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
    def __init__(self, center, size, enabled=False, image=None, text='', mode='t', toggle=True, when_pressed=print, when_unpressed=print, text_font=None):
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
        if toggle:
            self.functions['off'] = when_unpressed
        

    def set_when_pressed(self, function=print):
        self.functions['on'] = function
    
    def when_unpressed(self, function=print):
        self.functions['off'] = function

    def select(self):
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
    def __init__(self, center, size, font, text_color, text, enabled):
        super().__init__(center=center, size=size, enabled=enabled)
        self.font = font
        self.text = text
        self.text_color = text_color

    def render(self, window):
        lbl = pygame.Surface(self.size, pygame.SRCALPHA, 32).convert_alpha()
        y = 0
        lineSpacing = -2
        text = self.text
        bottom = 0

        # get the height of the font
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > self.size[1]:
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
            lbl.blit(surface, (lbl.get_width()/2 - sr.width/2, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]
        window.blit(lbl, (self.rect.left, self.rect.top + (self.rect.height/2 - bottom)))
        return text


class Panel(AppComponent):
    def __init__(self, center, size, enabled, font, items=[]):
        super().__init__(center=center, size=size, enabled=enabled)
        super().__init__(center=center, size=size, enabled=enabled)
        self.surface = pygame.Surface(size)
        self.items = items
        self.font = font
    
    def render(self, window):
        y = 25
        c = 0
        for i in self.items:
            row = pygame.Surface((self.width, 20))
            if isinstance(i, Iterable):
                for j in i:
                    pass                  
            c += 1
        window.blit(self.surface, self.rect)
            


class ScrollBox(AppComponent):
    def __init__(self, center=(0,0), size=(0,0), enabled=True, items=[]):
        super().__init__(center=center, size=size, enabled=enabled)
        self.surface = pygame.Surface(size)
        self.items = items
    
    def render(self, window):
        for i in self.items:
            row = pygame.Surface((self.width, 20))
            if isinstance(i, Iterable):             
                for j in i:
                    j.render(row)
