import Internals.Utils.wlogger as wlogger
import math
from pyquaternion import *
import numpy
import time
import Main.config as config
import HardwareControl.Eyes.weye as weye
from operator import add


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
        
        # Calibrate
        self.sloth_step_size = 0.5
        self.tortoise_step_size = 3
        self.hare_step_size = 6
        self.cheetah_step_size = 10
        
        self.resting = [20, 0, -20, 0]

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
            
    def unsafe_move_to(self, horiz_angle, vert_angle):
        self.LeftEye.unsafe_move_to_mapped_position(horiz_angle, vert_angle)
        self.RightEye.unsafe_move_to_mapped_position(horiz_angle, vert_angle)


    def extreme_left(self, stepSize):
        """ This function moves the eyes to the extreme left position. It only affects the Y Axis (left to right)"""
        wlogger.log_info("Performing Extreme Left")

        while (self.LeftEye.eye_horiz_angle - stepSize) > -self.LeftEye.eye_movement_max_radius and (self.RightEye.eye_horiz_angle - stepSize) > -self.LeftEye.eye_movement_max_radius:
            self.LeftEye.step_horiz_angle(-stepSize)
            self.RightEye.step_horiz_angle(-stepSize)
            self.redraw()

    def extreme_right(self, stepSize):
        """ This function moves the eyes to the extreme right position. It only affects the Y Axis (left to right)
        This assumes that the eye is starting at the centre and is a test routine"""
        wlogger.log_info("Performing Extreme Right")

        while (self.LeftEye.eye_horiz_angle + stepSize) < self.LeftEye.eye_movement_max_radius and (self.RightEye.eye_horiz_angle + stepSize) < self.RightEye.eye_movement_max_radius:
            self.LeftEye.step_horiz_angle(stepSize)
            self.RightEye.step_horiz_angle(stepSize)
            self.redraw()

    def extreme_up(self, stepSize):
        """ This function moves the eyes to the extreme up position. It only affects the X Axis (up and down)
        This assumes that the eye is starting at the centre and is a test routine"""
        wlogger.log_info("Performing Extreme Up")

        while (self.LeftEye.eye_vert_angle + stepSize) < self.LeftEye.eye_movement_max_radius and (self.RightEye.eye_vert_angle + stepSize) < self.RightEye.eye_movement_max_radius:
            self.LeftEye.step_vert_angle(stepSize)
            self.RightEye.step_vert_angle(stepSize)
            self.redraw()

    def extreme_down(self, stepSize):
        """ This function moves the eyes to the extreme down position. It only affects the X Axis (up and down)
        This assumes that the eye is starting at the centre and is a test routine"""
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
        
    def calculate_StepSizes(self, stepSize, bigChange, change2, change3, change4):
        
        # Set biggest change as the the wanted step size, all other steps will be smaller.
        if(bigChange < 0):
            bigStep = -stepSize
        else:
            bigStep = stepSize
        
        # Calculate the number of steps needed. Make sure this is greater than
        # or equal to zero.
        steps = math.ceil(abs(bigChange/stepSize))
        
        if steps != 0:
            step2 = change2/steps
            step3 = change3/steps
            step4 = change4/steps
        else:
            step2 = 0
            step3 = 0
            step4 = 0
        
        return steps, bigStep, step2, step3, step4

        
    def straight_to_point(self, stepSize, coordinates):
        
        if (len(coordinates) == 2):
            LEhoriz = coordinates[0]
            LEvert = coordinates[1]
            REhoriz = coordinates[0]
            REvert = coordinates[1]
        elif (len(coordinates) == 4):
            LEhoriz = coordinates[0]
            LEvert = coordinates[1]
            REhoriz = coordinates[2]
            REvert = coordinates[3]
        else:
            return
            
        print("Start Straight")
        print(LEhoriz)
        print(LEvert)
        print(REhoriz)
        print(REvert)

        
        #calculate distance from given point of Left Eye
        leftVertChange = LEvert - self.LeftEye.eye_vert_angle
        leftHorizChange = LEhoriz - self.LeftEye.eye_horiz_angle
        leftChange = math.sqrt(leftVertChange**2 + leftHorizChange**2)
        
        #calculate distance from given point of Right Eye
        rightVertChange = REvert - self.RightEye.eye_vert_angle
        rightHorizChange = REhoriz - self.RightEye.eye_horiz_angle
        rightChange = math.sqrt(rightVertChange**2 + rightHorizChange**2)
        
        
        # Calculate the number of steps needed.
        max_change = max(leftChange, rightChange)
        num_steps = math.ceil(max_change/stepSize)
        
        LEVertStep = leftVertChange/num_steps
        LEHorizStep = leftHorizChange/num_steps
        REVertStep = rightVertChange/num_steps
        REHorizStep = rightHorizChange/num_steps
          
        
        
        for i in range(num_steps):
            leftHorizAngle = self.LeftEye.eye_horiz_angle + LEHorizStep
            leftVertAngle = self.LeftEye.eye_vert_angle + LEVertStep
            rightHorizAngle = self.RightEye.eye_horiz_angle + REHorizStep
            rightVertAngle = self.RightEye.eye_vert_angle + REVertStep
            
            self.LeftEye.move_to(leftHorizAngle, leftVertAngle)
            self.RightEye.move_to(rightHorizAngle, rightVertAngle)
            
            print("Step :" + str(i))
            print(leftHorizAngle)
            print(leftVertAngle)
            print(rightHorizAngle)
            print(rightVertAngle)
            
        # Final adjustment to correct position
        self.LeftEye.move_to(LEhoriz, LEvert)
        self.RightEye.move_to(REhoriz, REvert)
            
            

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
        
    def angular_movement(self, startAngle, endAngle, distFromCentre, angleStepSize):
        
        for i in range(startAngle, endAngle, angleStepSize):  
            angle_rad = (i*math.pi)/180
            horiz_angle = distFromCentre * math.cos(angle_rad)
            vert_angle = distFromCentre * math.sin(angle_rad)            
            self.move_to(horiz_angle, vert_angle)
            time.sleep(0.01)
        

    def Straight_Eye_Roll(self, stepSize):
        """ This function represents one of Gromits animated eye rolls."""
        wlogger.log_info("Performing Straight Eye Roll")
        restPosition = [20, 0, -20, 0]
        startPosition = [0, -25, 0, -25]
        
        
        self.straight_to_point(stepSize, startPosition)
        
        #Section for individual movements
        
        self.straight_to_point(stepSize, restPosition)
                    
            
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
                   
            
    def Eye_Roll(self, start_angle, end_angle, num_steps):
        """Performs a full circle of the eyes."""
        
        # Convert cartesian step size to an angle step. 
        interval = (end_angle - start_angle)/num_steps
        rad_interval = interval*math.pi/180
        angle_rad = start_angle*math.pi/180
        end_angle_rad = end_angle*math.pi/180
        
        # If the distance is 0 just stay in one place
        if interval == 0:
            for i in range(0, num_steps):
                horiz_angle = self.LeftEye.eye_movement_max_radius * math.cos(start_angle)
                vert_angle = self.LeftEye.eye_movement_max_radius * math.sin(start_angle)
                
                print(vert_angle)
                print(horiz_angle)
                
                
                self.move_to(horiz_angle, vert_angle)
                time.sleep(0.01)
                
                    
        wlogger.log_info("Performing Eye Roll")
        
        while angle_rad < end_angle_rad:
            horiz_angle = self.LeftEye.eye_movement_max_radius * math.cos(angle_rad)
            vert_angle = self.LeftEye.eye_movement_max_radius * math.sin(angle_rad)
            angle_rad += rad_interval
            
            print(horiz_angle)
            print(vert_angle)
            
            self.move_to(horiz_angle, vert_angle)
            time.sleep(0.01)
            
        
        horiz_angle = self.LeftEye.eye_movement_max_radius * math.cos(end_angle_rad)
        vert_angle = self.LeftEye.eye_movement_max_radius * math.sin(end_angle_rad)
        angle_rad += rad_interval
        
        print(horiz_angle)
        print(vert_angle)
        
        self.move_to(horiz_angle, vert_angle)
        time.sleep(0.01)



    def Gromit_Eye_Roll(self):
        
        # Slow move to starting position
        self.straight_to_point(self.sloth_step_size, [20, -30, -20, -30])
        
        time.sleep(5)
        
        self.straight_to_point(self.hare_step_size, [25, 0])
        
        self.straight_to_point(self.hare_step_size, [30, 10])
        
        self.straight_to_point(self.tortoise_step_size, [35, 25])
        
        self.straight_to_point(self.tortoise_step_size, [30, 50])
        
        self.straight_to_point(self.tortoise_step_size, [15, 65])
        
        self.straight_to_point(self.sloth_step_size, [0 , 70])
        
        self.straight_to_point(0.5, [-20, 65])
        
        self.straight_to_point(self.sloth_step_size, [-30, 55])
        
        self.straight_to_point(self.tortoise_step_size, [-30, 45])
        
        self.straight_to_point(self.tortoise_step_size, [-25, 35, -30, 35])
        
        self.straight_to_point(self.tortoise_step_size, [-15, 20, -30, 20])
        
        self.straight_to_point(self.hare_step_size, [0, 10, -25, 10])
        
        self.straight_to_point(self.hare_step_size, self.resting)
        
        
        
        
        
        
