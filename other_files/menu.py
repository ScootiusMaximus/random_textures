from other_files.slider import Slider
from other_files.button import Button

import pygame
pygame.init()

box = pygame.Surface((50,50))
box.fill((100,100,100))

method1box = Button(None,0,0,box)
method2box = Button(None,0,0,box)
method3box = Button(None,0,0,box)

weightslider = Slider(None,0,0,100,40)

buttons = [method1box,method2box,method3box]