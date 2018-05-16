import Internals.Utils.wlogger as wlogger
import math
from pyquaternion import *
import numpy
import time
import Main.config as config


if not config.real_hardware:
    import HardwareControl.Environment.Virtual.wenvironment as wenvironment
    import HardwareControl.Eyes.Virtual.weye as weye
    import pygame
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLU import *

else:
    import HardwareControl.Eyes.Physical.weye as weye


class Controller:
    """ This class contains the various subcontrollers and routines to combine them"""

    def __init__(self):
        """
        Create Controller
        """

        wlogger.log_info("Initialising Controller")
        self.LeftEye  = weye.Eye(1, ( 1, 0, 0), 4, 5)
        self.RightEye = weye.Eye(1, (-1, 0, 0), 6, 7)
        
        # Set up initial position - this would make more sense to do internally
        # but calling PCA9685(0x40) resets the signals to zero.
        
        self.LeftEye.move_to(0, 0)
        self.RightEye.move_to(0, 0)
        self.redraw()

    def redraw(self):
        if not config.real_hardware:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            # Translate to face location.
            glTranslatef(0.0, 0.0, -0.5)
            glColor(1.0, 0.9, 0.7)
            self.draw_circle(5, 20)
            glPopMatrix()

            self.LeftEye.draw()
            self.RightEye.draw()

            # Refresh display
            pygame.display.flip()
            
    def move_to(self, horiz_angle, vert_angle):
            self.LeftEye.move_to(horiz_angle, vert_angle)
            self.RightEye.move_to(horiz_angle, vert_angle)


    def extreme_left(self, stepSize):
        """ This function moves the eyes to the extreme left position. It only affects the Y Axis (left to right)"""
        wlogger.log_info("Performing Extreme Left")

        while (self.LeftEye.eye_horiz_angle - stepSize) > -self.LeftEye.eye_movement_max_radius and (self.RightEye.eye_horiz_angle - stepSize) > -self.LeftEye.eye_movement_max_radius:
            self.LeftEye.step_horiz_angle(-stepSize)
            self.RightEye.step_horiz_angle(-stepSize)
            self.redraw()

    def extreme_right(self, stepSize):
        """ This function moves the eyes to the extreme right position. It only affects the Y Axis (left to right)"""
        wlogger.log_info("Performing Extreme Right")

        while (self.LeftEye.eye_horiz_angle + stepSize) < self.LeftEye.eye_movement_max_radius and (self.RightEye.eye_horiz_angle + stepSize) < self.RightEye.eye_movement_max_radius:
            self.LeftEye.step_horiz_angle(stepSize)
            self.RightEye.step_horiz_angle(stepSize)
            self.redraw()

    def extreme_up(self, stepSize):
        """ This function moves the eyes to the extreme up position. It only affects the X Axis (up and down)"""
        wlogger.log_info("Performing Extreme Up")

        while (self.LeftEye.eye_vert_angle + stepSize) < self.LeftEye.eye_movement_max_radius and (self.RightEye.eye_vert_angle + stepSize) < self.RightEye.eye_movement_max_radius:
            self.LeftEye.step_vert_angle(stepSize)
            self.RightEye.step_vert_angle(stepSize)
            self.redraw()

    def extreme_down(self, stepSize):
        """ This function moves the eyes to the extreme down position. It only affects the X Axis (up and down)"""
        wlogger.log_info("Performing Extreme Down")

        while (self.LeftEye.eye_vert_angle - stepSize) > -self.LeftEye.eye_movement_max_radius and (self.RightEye.eye_vert_angle - stepSize) > -self.RightEye.eye_movement_max_radius:
            self.LeftEye.step_vert_angle(-stepSize)
            self.RightEye.step_vert_angle(-stepSize)
            self.redraw()

    def cross_eyes_checker(self):
        """ This function checks the current positions of the eyes in relation to each other and returns an integer
        symbolising how to proceed with crossing the eyes"""
        wlogger.log_info("Performing Eye Position Check")

        if self.LeftEye.eye_horiz_angle < self.LeftEye.eye_movement_max_radius and self.RightEye.eye_horiz_angle > -self.RightEye.eye_movement_max_radius:
            return 1
        elif self.LeftEye.eye_horiz_angle < self.LeftEye.eye_movement_max_radius and self.RightEye.eye_horiz_angle == -self.RightEye.eye_movement_max_radius:
            return 2
        elif self.LeftEye.eye_horiz_angle == self.LeftEye.eye_movement_max_radius and self.RightEye.eye_horiz_angle > -self.RightEye.eye_movement_max_radius:
            return 3
        else:
            return 0

    def cross_eyes(self, stepSize):
        """ This function makes Gromit go cross-eyed and the returns to centre"""
        wlogger.log_info("Performing Cross-Eyes")

        while self.cross_eyes_checker() == 1:
            self.LeftEye.step_horiz_angle(stepSize)
            self.RightEye.step_horiz_angle(-stepSize)
            self.redraw()

        while self.cross_eyes_checker() == 2:
            self.LeftEye.step_horiz_angle(stepSize)
            self.redraw()

        while self.cross_eyes_checker() == 3:
            self.RightEye.step_horiz_angle(-stepSize)
            self.redraw()

        while self.LeftEye.eye_horiz_angle > 0 > self.RightEye.eye_horiz_angle:
            self.LeftEye.step_horiz_angle(-stepSize)
            self.RightEye.step_horiz_angle(stepSize)
            self.redraw()

    def StepTowardsCentre(self, eye, stepSize):
        """ This function moves the given eye a step closer to the centre in either axis depending on which is further away"""
        wlogger.log_info("Performing Step Towards Centre")

        if abs(eye.eye_vert_angle) > abs(eye.eye_horiz_angle):
            print("Vertical Step")
            if eye.eye_vert_angle > 0:
                eye.step_vert_angle(-stepSize)
            else:
                eye.step_vert_angle(stepSize)
        else:
            print("Horizontal Step")
            if eye.eye_horiz_angle > 0:
                eye.step_horiz_angle(-stepSize)
            else:
                eye.step_horiz_angle(stepSize)

        self.redraw()
        
    def calculate_small_step_size(self, stepSize, bigDistance, smallDistance):
        """This function calculates a stepsize for the smaller distance to be travelled"""
        wlogger.log_info("calculating small step size")
        
        smallStepSize = (abs(smallDistance) * stepSize)/abs(bigDistance)
        
        print(smallStepSize)
        
        if (smallDistance < 0 and bigDistance < 0):
            return -smallStepSize
        else:
            return smallStepSize
        
    def straight_to_point(self, stepSize, X, Y):
        """ This function moves each eye to the centre in a straight line"""
        wlogger.log_info("Performing Straight Recentre")
        
        #calculate distance from given point of Left Eye
        leftVertChange = Y - self.LeftEye.eye_vert_angle
        leftHorizChange = X - self.LeftEye.eye_vert_angle
        leftDistance = math.sqrt((leftVertChange**2)+(leftHorizChange**2))
        
        #calculate distance from given point of Right Eye
        rightVertChange = Y - self.RightEye.eye_vert_angle
        rightHorizChange = X - self.RightEye.eye_horiz_angle
        rightDistance = math.sqrt((rightVertChange**2)+(rightHorizChange**2))
        
        #Determine large distance,and calculate smaller step size accordingly
        if(leftDistance > rightDistance):
            rightStepSize = self.calculate_small_step_size(stepSize, leftDistance, rightDistance)
            leftStepSize = stepSize
            steps = math.floor(leftDistance/stepSize)
            
        elif(rightDistance > leftDistance):
            leftStepSize = self.calculate_small_step_size(stepSize, rightDistance, leftDistance)
            rightStepSize = stepSize
            steps = math.floor(rightDistance/stepSize)
        
        else:
            leftStepSize = stepSize
            rightStepSize = stepSize
            steps = math.floor(leftDistance/stepSize)
            print("The Eyes are moving the same distance")
            print(steps)
        
        #determine which axis has a large distance for each eye, and calculate step sizes accordingly
        if (leftVertChange == leftHorizChange):
            leftVertStepSize = leftStepSize
            leftHorizStepSize =leftStepSize
            
        elif (leftVertChange > leftHorizChange):
            leftHorizStepSize = self.calculate_small_step_size(leftStepSize, leftVertChange, leftHorizChange)
            leftVertStepSize = leftStepSize
        
        elif (leftHorizChange > leftVertChange):
            leftVertStepSize = self.calculate_small_step_size(leftStepSize, leftHorizChange, leftVertChange)
            leftHorizStepSize = leftStepSize
            
        if (rightVertChange == rightHorizChange):
            rightVertStepSize = rightStepSize
            rightHorizStepSize = rightStepSize
            
        elif (rightVertChange > rightHorizChange):
            rightHorizStepSize = self.calculate_small_step_size(rightStepSize, rightVertChange, rightHorizChange)
            rightVertStepSize = rightStepSize
        
        elif (rightHorizChange > rightVertChange):
            rightVertStepSize = self.calculate_small_step_size(rightStepSize, rightHorizChange, rightVertChange)
            rightHorizStepSize = rightStepSize
            
        # take required number of steps to get as close to the area as possible    
        for i in range(steps):
            print("Step " + str(i))
            self.LeftEye.step_vert_angle(leftVertStepSize)
            self.LeftEye.step_horiz_angle(leftHorizStepSize)
            self.RightEye.step_vert_angle(rightVertStepSize)
            self.RightEye.step_horiz_angle(rightHorizStepSize)
        

    def re_centre(self, stepSize):
        """ This function calculates which eye is further from the centre and then calls the StepTowardsCentre function to move that eye closer to the centre"""
        wlogger.log_info("Performing Recentre")
        
        
        
        tol= 0.01


        while ((-tol > abs(self.RightEye.eye_vert_angle) 
                    or abs(self.RightEye.eye_vert_angle) > tol) 
                    or (-tol > abs(self.RightEye.eye_horiz_angle) 
                    or abs(self.RightEye.eye_horiz_angle) > tol) 
                    or (-tol > abs(self.LeftEye.eye_vert_angle) 
                    or abs(self.LeftEye.eye_vert_angle) > tol) 
                    or (-tol > abs(self.LeftEye.eye_horiz_angle) 
                    or abs(self.LeftEye.eye_horiz_angle) > tol)):
                        
            

            right_eye_distance_sq = self.RightEye.eye_vert_angle**2 + self.RightEye.eye_horiz_angle**2
            left_eye_distance_sq = self.LeftEye.eye_vert_angle**2 + self.LeftEye.eye_horiz_angle**2            
            
            
            # If the step size is bigger than the distance remaining there is a chance of overstepping
            # - only step the smaller distance.
            if right_eye_distance_sq > left_eye_distance_sq:
                if stepSize**2 > right_eye_distance_sq:
                    self.StepTowardsCentre(self.RightEye, math.sqrt(right_eye_distance_sq))
                else:
                    self.StepTowardsCentre(self.RightEye, stepSize)
            else:
                if stepSize**2 > left_eye_distance_sq:
                    self.StepTowardsCentre(self.LeftEye, math.sqrt(left_eye_distance_sq))
                else:
                    self.StepTowardsCentre(self.LeftEye, stepSize)

        
                    
    def zero_angles(self):
        self.LeftEye.move_to(0, 0)
        self.RightEye.move_to(0, 0)
        
        print("Centred")
        print("left Vert Angle: " + str(self.LeftEye.eye_vert_angle))
        print("left Horiz Angle: " + str(self.LeftEye.eye_horiz_angle))
        
        print("right Vert Angle: " + str(self.RightEye.eye_vert_angle))
        print("right Horiz Angle: " + str(self.RightEye.eye_horiz_angle))
        
        
    def zero_pwm(self):
        self.LeftEye.recentre_servo()
        self.RightEye.recentre_servo()
        

    def Straight_Eye_Roll(self, stepSize):
        """ This function represents one of Gromits animated eye rolls."""
        wlogger.log_info("Performing Straight Eye Roll")
        
        while ((self.LeftEye.eye_vert_angle + stepSize) < self.LeftEye.eye_movement_corner_angle
               and (self.LeftEye.eye_horiz_angle + stepSize) < self.LeftEye.eye_movement_corner_angle
               and (self.RightEye.eye_vert_angle + stepSize) < self.RightEye.eye_movement_corner_angle
               and (self.RightEye.eye_horiz_angle + stepSize) < self.RightEye.eye_movement_corner_angle):
                   self.LeftEye.step_vert_angle(stepSize)
                   self.RightEye.step_vert_angle(stepSize)
                   self.LeftEye.step_horiz_angle(stepSize)
                   self.RightEye.step_horiz_angle(stepSize)
                   

        for i in range(45, 110):  
            angle_rad = (i*math.pi)/180
            horiz_angle = self.LeftEye.eye_movement_max_radius * math.cos(angle_rad)
            vert_angle = self.LeftEye.eye_movement_max_radius * math.sin(angle_rad)            
            self.move_to(horiz_angle, vert_angle)
            time.sleep(0.01)
        
        self.re_centre(1)
                    
            
    def Low_Cross_Eyes(self, stepSize):
        """This function represents Gromit's eyes focussing on his nose"""
        wlogger.log_info("Performing Low Cross Eyes")
                
        while ((self.LeftEye.eye_vert_angle - stepSize) > -self.LeftEye.eye_movement_corner_angle
               and (self.LeftEye.eye_horiz_angle + stepSize) < self.LeftEye.eye_movement_corner_angle
               and (self.RightEye.eye_vert_angle - stepSize) > -self.RightEye.eye_movement_corner_angle
               and (self.RightEye.eye_horiz_angle - stepSize) > -self.RightEye.eye_movement_corner_angle):
                   self.LeftEye.step_vert_angle(-stepSize)
                   self.RightEye.step_vert_angle(-stepSize)
                   self.LeftEye.step_horiz_angle(stepSize)
                   self.RightEye.step_horiz_angle(-stepSize)
                   
            
    def Eye_Roll(self):
        """Performs a full circle of the eyes."""
        wlogger.log_info("Performing Eye Roll")
        for i in range(0, 360):  
            angle_rad = (i*math.pi)/180
            horiz_angle = self.LeftEye.eye_movement_max_radius * math.cos(angle_rad)
            vert_angle = self.LeftEye.eye_movement_max_radius * math.sin(angle_rad)
            
            self.move_to(horiz_angle, vert_angle)
            time.sleep(0.01)
            
            

    def draw_circle(self, radius, side_num):
        if not config.real_hardware:
            glBegin(GL_POLYGON)
            for vertex in range(0, side_num):
                angle = float(vertex) * 2.0 * numpy.pi / side_num
                glVertex3f(numpy.cos(angle) * radius,  numpy.sin(angle) * radius, 0.0)
            glEnd()

    def test_move(self):
        for i in range(0, 4):
            self.LeftEye.step_vert_angle(0.05)
            self.redraw()

        for i in range(0, 4):
            self.LeftEye.step_horiz_angle(0.05)
            self.redraw()

        for i in range(0, 4):
            self.RightEye.step_vert_angle(0.05)
            self.redraw()

        for i in range(0, 4):
            self.RightEye.step_horiz_angle(0.05)
            self.redraw()

    def continue_game(self):
        if not config.real_hardware:
            accum = Quaternion(axis=[1.0, 0.0, 0.0], angle=1)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == pygame.KEYDOWN:

                        glMatrixMode(GL_PROJECTION)
                        if event.key == pygame.K_LEFT:
                            glTranslatef(-1, 0, 0)
                        if event.key == pygame.K_RIGHT:
                            glTranslatef(1, 0, 0)

                        if event.key == pygame.K_UP:
                            glTranslatef(0, 1, 0)
                        if event.key == pygame.K_DOWN:
                            glTranslatef(0, -1, 0)

                        if event.key == pygame.K_w:
                            glRotatef(3, 1.0, 0.0, 0.0)
                        if event.key == pygame.K_a:
                            glRotatef(3, 0.0, 1.0, 0.0)
                        if event.key == pygame.K_s:
                            glRotatef(-3, 1.0, 0.0, 0.0)
                        if event.key == pygame.K_d:
                            glRotatef(-3, 0.0, 1.0, 0.0)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 4:
                            glTranslatef(0, 0, 1.0)

                        if event.button == 5:
                            glTranslatef(0, 0, -1.0)

                self.redraw()

                # Refresh display
                pygame.display.flip()

                # Wait
                pygame.time.wait(10)

