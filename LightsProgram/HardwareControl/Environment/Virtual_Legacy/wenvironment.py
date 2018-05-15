import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from math import *
from pyquaternion import *

# Pygame Initialisation.
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

# Default view
glMatrixMode(GL_PROJECTION)

# Set perspective
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
gluLookAt(0.0, -0.5, 8.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


# Using depth test to make sure closer colors are shown over further ones
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_LIGHTING)
glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 2.0, 5.0, 1.0])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT1, GL_POSITION, [0.0, -5.0, 12.0, 1.0])
glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
glEnable(GL_LIGHT1)
glLightfv(GL_LIGHT2, GL_POSITION, [0.0, -5.0, 5.0, -1.0])
glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
glEnable(GL_LIGHT2)


glMatrixMode(GL_MODELVIEW)



