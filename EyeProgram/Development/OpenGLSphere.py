# Draw sphere with QUAD_STRIP
# Controls: UP/DOWN - scale up/down
#           LEFT/RIGHT - rotate left/right
#           F1 - Toggle surface as SMOOTH or FLAT

# Python imports
from math import *
import sys
import pygame
from pygame.locals import *

# OpenGL imports for python
try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print("OpenGL wrapper for python not found")

# Last time when sphere was re-displayed
last_time = 0


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

        # Direction of light
        self.direction0 = [0.0, 2.0, -1.0, 1.0]
        self.direction1 = [0.0, -2.0, 1.0, 1.0]

        # Intensity of light
        self.intensity = [0.5, 0.5, 0.5, 1.0]

        # Intensity of ambient light
        self.ambient_intensity = [0.3, 0.3, 0.3, 1.0]

        # The surface type(Flat or Smooth)
        self.surface = GL_FLAT

    # Initialize
    def init(self):

        # Set background color to black
        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.compute_location()

        # Set OpenGL parameters
        glEnable(GL_DEPTH_TEST)

        # Enable lighting
        glEnable(GL_LIGHTING)

        # Set light model
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)

        # Enable light number 0
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)

        # Set position and intensity of light
        glLightfv(GL_LIGHT0, GL_POSITION, self.direction0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.intensity)

        glLightfv(GL_LIGHT1, GL_POSITION, self.direction1)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, self.intensity)
        glLightfv(GL_LIGHT1, GL_AMBIENT, self.ambient_intensity)

        # Setup the material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

    # Compute location
    def compute_location(self):
        x = 2 * cos(self.user_theta)
        y = 2 * sin(self.user_theta)
        z = self.user_height
        d = sqrt(x * x + y * y + z * z)

        # Set matrix mode
        glMatrixMode(GL_MODELVIEW)

        # Reset matrix
        glLoadIdentity()
        glFrustum(-d * 0.5, d * 0.5, -d * 0.5, d * 0.5, d - 1.1, d + 1.1)

        # Set camera
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

    # Display the sphere
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set color to white
        glColor3f(1.0, 1.0, 1.0)

        # Set shade model
        glShadeModel(self.surface)

        self.draw()
        glutSwapBuffers()

    # Draw the sphere
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
                glNormal3f(x * zr0, y * zr0, z0)
                glVertex3f(x * zr0, y * zr0, z0)
                glNormal3f(x * zr1, y * zr1, z1)
                glVertex3f(x * zr1, y * zr1, z1)

            glEnd()

    # Keyboard controller for sphere
    def special(self, key, x, y):

        # Scale the sphere up or down
        if key == GLUT_KEY_UP:
            self.user_height += 0.1
        if key == GLUT_KEY_DOWN:
            self.user_height -= 0.1

        # Rotate the cube
        if key == GLUT_KEY_LEFT:
            self.user_theta += 0.1
        if key == GLUT_KEY_RIGHT:
            self.user_theta -= 0.1

        # Toggle the surface
        if key == GLUT_KEY_F1:
            if self.surface == GL_FLAT:
                self.surface = GL_SMOOTH
            else:
                self.surface = GL_FLAT

        self.compute_location()
        glutPostRedisplay()

    # The idle callback
    def idle(self):
        global last_time
        time = glutGet(GLUT_ELAPSED_TIME)

        if last_time == 0 or time >= last_time + 40:
            last_time = time
            glutPostRedisplay()

    # The visibility callback
    def visible(self, vis):
        if vis == GLUT_VISIBLE:
            glutIdleFunc(self.idle)
        else:
            glutIdleFunc(None)


# The main function
def main():

     # Pygame initialisation.
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # Set perspective
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    # Set origin as 5 units back from screen. So we can see origin.
    glTranslatef(0.0, 0.0, -5)

     # Set perspective
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)


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

         # Instantiate the sphere object
        s = Sphere(1.0)

        s.init()

        # Refresh display
        pygame.display.flip()

        # Wait
        pygame.time.wait(10)

# Call the main function
if __name__ == '__main__':
    main()