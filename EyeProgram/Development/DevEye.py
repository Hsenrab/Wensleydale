import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from math import *
from pyquaternion import *

vertices= (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


colours = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )


surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )


axis_verts = (
    (-7.5, 0.0, 0.0),
    ( 7.5, 0.0, 0.0),
    ( 0.0,-7.5, 0.0),
    ( 0.0, 7.5, 0.0),
    ( 0.0, 0.0,-7.5),
    ( 0.0, 0.0, 7.5)
    )

axes = (
    (0,1),
    (2,3),
    (4,5)
    )

axis_colors = (
    (1.0,0.0,0.0), # Red
    (0.0,1.0,0.0), # Green
    (0.0,0.0,1.0)  # Blue
    )

def Axis():
    glBegin(GL_LINES)
    for color,axis in zip(axis_colors,axes):
        glColor3fv(color)
        for point in axis:
            glVertex3fv(axis_verts[point])
    glEnd()

# The sphere class
class Sphere:

    # Constructor for the sphere class
    def __init__(self, radius):

        # Radius of sphere
        self.radius = radius

        # Number of latitudes in sphere
        self.lats = 50

        # Number of longitudes in sphere
        self.longs = 50

        self.user_theta = 0
        self.user_height = 0

        # The surface type(Flat or Smooth)
        self.surface = GL_FLAT

    def draw(self):
        for i in range(0, self.lats + 1):
            lat0 = pi * (-0.5 + float(float(i - 1) / float(self.lats)))
            z0 = sin(lat0)
            zr0 = cos(lat0)
        
            lat1 = pi * (-0.5 + float(float(i) / float(self.lats)))
            z1 = sin(lat1)
            zr1 = cos(lat1)
        
            # Use Quad strips to draw the sphere
            glBegin(GL_QUAD_STRIP)
        
            for j in range(0, self.longs + 1):
                lng = 2 * pi * float(float(j - 1) / float(self.longs))
                x = cos(lng)
                y = sin(lng)

                if z1 > -0.91 and z0 > -0.91:
                    glColor3f(0.9, 0.9, 0.9)
                else:
                    glColor3f(0.2, 0.2, 0.3)

                glNormal3f(x * zr0, z0, y * zr0)
                glVertex3f(x * zr0, z0, y * zr0)
                glNormal3f(x * zr1, z1, y * zr1)
                glVertex3f(x * zr1, z1, y * zr1)
        
            glEnd()


def Cube():
    glBegin(GL_LINES) # Notifies OpenGL that we are writing code for it. In this case line drawing code.
    
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex]) # Draws line between edge vertices.
    
    glEnd() # Ends code for OpenGL.
    
    glBegin(GL_QUADS) # Notifies OpenGL that we are writing code for it. In this case quad drawing code.
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colours[x])
            glVertex3fv(vertices[vertex])
    glEnd() # Ends code for OpenGL.



def main():

    # Pygame initialisation.
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # Default view
    glMatrixMode(GL_PROJECTION)
    # Set perspective
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    # Set origin as 5 units back from screen. So we can see origin.
    glTranslatef(0.0, 0.0, -8)


    # Using depth test to make sure closer colors are shown over further ones
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_COLOR_MATERIAL)

    glEnable (GL_LIGHTING);
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 2.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.6, 0.6, 0.6, 1.0])
    glEnable(GL_LIGHT0)

    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 0.0, 5.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
    glEnable(GL_LIGHT1)

    inc_x = 0
    inc_y = 0
    inc_z = 0

    glMatrixMode(GL_MODELVIEW)

    accum = Quaternion(axis=[1.0, 0.0, 0.0], angle=1)

    # Pygame loop.
    while True:

        inc_z = 0
        inc_x = 0
        inc_y = 0

        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    inc_z = pi/100
                if event.button == 5:
                    inc_z = -pi/100

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            inc_y = pi/100
        if keys[K_RIGHT]:
            inc_y = -pi/100

        if keys[K_UP]:
            inc_x = pi/100
        if keys[K_DOWN]:
            inc_x = -pi/100

        rot_x = Quaternion(axis=[1.0, 0.0, 0.0], angle=inc_x).normalised
        rot_y = Quaternion(axis=[0.0, 1.0, 0.0], angle=inc_y).normalised
        rot_z = Quaternion(axis=[0.0, 0.0, 1.0], angle=inc_z).normalised

        accum *= rot_x
        accum *= rot_y
        accum *= rot_z

        # Rotate by accumulative matrix.
        glLoadMatrixf(accum.transformation_matrix)


        # Clear canvas.
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Set up the cube.
        s = Sphere(1.0)
        s.draw()
        Axis()

        # Refresh display
        pygame.display.flip()

        # Wait
        pygame.time.wait(10)


main()