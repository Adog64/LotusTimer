import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import pygame
from pygame.locals import *
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

def main():
   pygame.display.init()

   window = pygame.display.set_mode((500, 200), DOUBLEBUF)
   window.fill((51, 51, 51))

   fig = pylab.figure(figsize=[5, 2], dpi=100)
   fig.patch.set_visible(False)
   ax = fig.gca()
   ax.patch.set_visible(False)
   for i in ax.spines.values():
      i.set_visible(False)
   ax.xaxis.set_visible(False)
   ax.tick_params(axis='y', colors=(122/255, 28/255, 1))
   
   x = np.array(range(1,11))
   y = np.array([21.85, 23.27, 19.82, 28.13, 23.92, 21.22, 29.35, 31.44, 19.32, 24.47])

   xnew = np.linspace(x.min(), x.max(), 200) 
   spl = make_interp_spline(x, y, k=3)
   y_smooth = spl(xnew)

   ax.plot(xnew, y_smooth, linewidth=2, color=(122/255, 28/255, 1), aa=True) 

   canvas = agg.FigureCanvasAgg(fig)
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