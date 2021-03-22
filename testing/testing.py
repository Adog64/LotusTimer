import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import pygame
from pygame.locals import *
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline

def main():
   fig = pylab.figure(figsize=[4, 4], # Inches
                     dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                     )
   fig.patch.set_facecolor((51/255, 51/255, 51/255))

   ax = fig.gca()


   ax.set_color((122/255, 28/255, 1))

   x = np.array(range(1,11))
   y = np.array([21.85, 23.27, 19.82, 28.13, 23.92, 21.22, 29.35, 31.44, 19.32, 24.47])

   #define x as 200 equally spaced values between the min and max of original x 
   xnew = np.linspace(x.min(), x.max(), 200) 

   #define spline with degree k=7
   spl = make_interp_spline(x, y, k=3)
   y_smooth = spl(xnew)

   #create smooth line chart 
   ax.plot(xnew, y_smooth, linewidth=3, color=(122/255, 28/255, 1))  
   ax.plot(x, y,'wo')


   canvas = agg.FigureCanvasAgg(fig)
   canvas.draw()
   renderer = canvas.get_renderer()
   raw_data = renderer.tostring_rgb()

   print('rendered')

   pygame.display.init()

   window = pygame.display.set_mode((400, 400), DOUBLEBUF)
   screen = pygame.display.get_surface()

   size = canvas.get_width_height()

   surf = pygame.image.fromstring(raw_data, size, "RGB")
   screen.blit(surf, (0,0))
   pygame.display.flip()

   crashed = False
   while not crashed:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            crashed = True

if __name__ == '__main__':
   main()