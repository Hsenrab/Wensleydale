import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
from math import *
from pyquaternion import *
import Internals.Utils.wlogger as wlogger


class Eye:

    # Constructor for the eye class
    def __init__(self, radius, centre):

        wlogger.log_info("Initialising Eye")

        # Radius of eye
        self.radius = radius

        # Centre of the eye
        self.centre = centre

        # Number of latitudes in sphere
        self.lats = 20

        # Number of longitudes in sphere
        self.longs = 20

        self.user_theta = 0
        self.user_height = 0

        # The surface type(Flat or Smooth)
        self.surface = GL_FLAT

        self.eye_vert_angle = 0
        self.eye_horiz_angle = 0
        self.eye_movement_max_radius = 0.7
        self.rotation_to_centre = Quaternion(axis=[1.0, 0.0, 0.0], angle=pi/2)
        self.current_quaternion = self.rotation_to_centre

    def draw(self):

        glPushMatrix()

        # Translate to eye location.
        glTranslatef(self.centre[0], self.centre[1], self.centre[2])

        # Rotate by accumulative matrix.
        glMultMatrixf(self.current_quaternion.transformation_matrix)

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

        glPopMatrix()

    def step_vert_angle(self, step_size):
        print("Virtual Eye")

        self.eye_vert_angle += step_size

        if self.eye_vert_angle > self.eye_movement_max_radius:
            self.eye_vert_angle = self.eye_movement_max_radius
        elif self.eye_vert_angle < -self.eye_movement_max_radius:
            self.eye_vert_angle = -self.eye_movement_max_radius

        rad_vert_angle = self.eye_vert_angle*pi/180
        rad_horiz_angle = self.eye_horiz_angle*pi/180
        rot_x = Quaternion(axis=[1.0, 0.0, 0.0], angle=self.eye_vert_angle).normalised
        rot_y = Quaternion(axis=[0.0, 1.0, 0.0], angle=self.eye_horiz_angle).normalised
        self.current_quaternion = self.rotation_to_centre * rot_x * rot_y

    def step_horiz_angle(self, step_size):
        print("Virtual Eye")

        self.eye_horiz_angle += step_size

        if self.eye_horiz_angle > self.eye_movement_max_radius:
            self.eye_horiz_angle = self.eye_movement_max_radius
        elif self.eye_horiz_angle < -self.eye_movement_max_radius:
            self.eye_horiz_angle = -self.eye_movement_max_radius
        rad_vert_angle = self.eye_vert_angle*pi/180
        rad_horiz_angle = self.eye_horiz_angle*pi/180
        rot_x = Quaternion(axis=[1.0, 0.0, 0.0], angle=rad_vert_angle).normalised
        rot_y = Quaternion(axis=[0.0, 1.0, 0.0], angle=rad_horiz_angle).normalised
        self.current_quaternion = self.rotation_to_centre * rot_x * rot_y


