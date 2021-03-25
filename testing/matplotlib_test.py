import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import pygame
from pygame.locals import *
import numpy as np

def main():
   pygame.display.init()

   window = pygame.display.set_mode((700, 225), DOUBLEBUF)
   window.fill((51, 51, 51))

   fig = pylab.figure(figsize=[7, 2.25], dpi=100)
   fig.patch.set_visible(False)
   ax = fig.gca()
   ax.patch.set_visible(False)
   for i in ax.spines.values():
      i.set_visible(False)
   ax.xaxis.set_visible(False)
   ax.tick_params(axis='y', colors=(122/255, 28/255, 1))
   
   y = np.array([21.85, 23.27, 19.82])
   x = np.array(range(len(y)))
   xs = np.linspace(0, len(y) - 1, 1000)

   poly_deg = len(y) - 1
   coefs = np.polyfit(x, y, poly_deg)
   y_poly = np.polyval(coefs, xs)

   ax.plot(xs, y_poly, linewidth=2, color=(122/255, 28/255, 1), aa=True) 

   canvas = agg.FigureCanvasAgg(fig)
   print(canvas)
   canvas.draw()
   renderer = canvas.get_renderer()
   raw_data = renderer.tostring_rgb()

   screen = pygame.display.get_surface()
   size = canvas.get_width_height()

   image = pygame.image.fromstring(raw_data, size, "RGB").convert_alpha()
   for x in range(image.get_width()):
        for y in range(image.get_height()):
            if image.get_at((x, y)) == (255, 255, 255, 255):
                image.set_at((x, y), (255, 255, 255, 0))

   screen.blit(image, (0,0))
   pygame.display.flip()

   crashed = False
   while not crashed:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            crashed = True

if __name__ == '__main__':
   main()