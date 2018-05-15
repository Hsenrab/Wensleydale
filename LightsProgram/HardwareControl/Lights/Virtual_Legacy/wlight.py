
import Internals.Utils.wlogger as wlogger
import pygame
from pygame.locals import *
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from pyquaternion import *
import numpy


#if not config.real_hardware:
import HardwareControl.Environment.Virtual.wenvironment as wenvironment

#else:
#    import HardwareControl.Environment.Physical.environment as environment


class LightController:
    """ This class contains the various subcontrollers and routines to combine them"""

    def __init__(self):
        """
        Create Controller
        """

        wlogger.log_info("Initialising Light Controller")
        self.LightStripArray = []

        self.led_size = 0.1
        self.led_spacing = 0.11
        self.led_row_length = 50
        self.led_row_spacing = 1

    def redraw(self):
        wlogger.log_info("Redraw Lights")
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        # Translate to face location.
        glTranslatef(0.0, 0.0, -0.5)
        glColor(0.0, 0.3, 0.1)

        glBegin(GL_QUADS)  # start drawing a rectangle
        glVertex2f(-3, -3)  # bottom left point
        glVertex2f(3, -3)  # bottom right point
        glVertex2f(3, 3)  # top right point
        glVertex2f(-3, 3)  # top left point
        glEnd()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-2.8, 2.8, -0.47)

        for strip in self.LightStripArray:
            glPushMatrix()
            self.drawStrip(strip)
            glPopMatrix()
            glTranslate(0.0, -self.led_row_spacing, 0.0)

        glPopMatrix()

        # Refresh display
        pygame.display.flip()

    def drawStrip(self, current_strip):

        num_rows = int(math.ceil(current_strip.num_led/self.led_row_length))
        current_led = 0

        for j in range(0, num_rows):
            glTranslate(0.0, -self.led_spacing, 0.0)

            for i in range(0, self.led_row_length):

                if (j % 2) == 0:
                    glTranslate(self.led_spacing, 0, 0)
                else:
                    glTranslate(-self.led_spacing, 0, 0)

                red = current_strip.leds[4 * current_led + 1]
                green = current_strip.leds[4 * current_led + 2]
                blue = current_strip.leds[4 * current_led + 3]

                glColor(red, green, blue)
                self.drawLED()
                current_led += 1

                if current_led >= current_strip.num_led:
                    break

            if current_led < current_strip.num_led:
                glTranslate(0.0, -self.led_spacing, 0.0)
                glColor(current_strip.leds[4 * current_led + 1], current_strip.leds[4 * current_led + 2],
                        current_strip.leds[4 * current_led + 3])
                self.drawLED()
                current_led += 1
                if (j % 2) == 0:
                    glTranslate(self.led_spacing, 0, 0)
                else:
                    glTranslate(-self.led_spacing, 0, 0)

            if current_led >= current_strip.num_led:
                break

    def drawLED(self):
        glBegin(GL_QUADS)  # start drawing a rectangle
        glVertex2f(0, 0)  # bottom left point
        glVertex2f(self.led_size, 0)  # bottom right point
        glVertex2f(self.led_size, self.led_size)  # top right point
        glVertex2f(0, self.led_size)  # top left point
        glEnd()


lightController = LightController()







