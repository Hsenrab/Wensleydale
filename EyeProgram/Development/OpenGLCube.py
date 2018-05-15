import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


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

    # Set perspective
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    # Set origin as 5 units back from screen. So we can see origin.
    glTranslatef(0.0, 0.0, -5)

    # Pygame loop.
    while True:

        # Check if we should end game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Rotates matrix by rotation matrix  (angle, x, y, z)
        glRotatef(1, 3, 1, 1)

        # Clear canvas.
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        # Set up the cube.
        Cube()

        # Refresh display
        pygame.display.flip()

        # Wait
        pygame.time.wait(10)


main()