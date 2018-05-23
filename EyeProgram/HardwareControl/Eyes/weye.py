import numpy
import math
from pyquaternion import *
import time
import Internals.Utils.wlogger as wlogger

from Adafruit_PCA9685 import PCA9685 


class Eye:

# Constructor for the eye class
    def __init__(self, radius = 0, centre = 0, vertical_channel = 0, horizontal_channel = 1):
        """ The constructor takes a horizontal and vertical channel as input, which correspond to which channel each servomotor is connected to on the Raspberry PI PWM Hat. 
        The 'radius' and 'centre' arguments are for the simulation model, which is currently not included in this codebase. 
        """

        # PWM Setup Variables
        self.eye                = PCA9685(0x40) # Always use the default i2c address for the PWM hats. This call turns off any pwm signal currently being sent.
        self.vert_ch            = vertical_channel
        self.horiz_ch           = horizontal_channel
        self.pwm_freq = 50.0 
        
        self.eye.set_pwm_freq(int(self.pwm_freq))

        self.pwm_bitres = 4096.0
        self.pwm_scaler = self.pwm_bitres / (1/self.pwm_freq)
        # The PWM periods for a typical servomotor is between 1ms and 2ms, with 1.5ms being the middle of the useable range.        
        self.pwm_period_min   = 10e-4 * self.pwm_scaler # This is the minimum angle (1ms) These will need to be calibrated.
        self.pwm_period_zero  = 15e-4 * self.pwm_scaler # This angle is the middle of the servo range (1.5ms)
        self.pwm_period_max   = 20e-4 * self.pwm_scaler # This is the maximum angle (2ms)
        self.pwm_period_range = self.pwm_period_max - self.pwm_period_min
        self.servo_angle_max  = 70 # This is the range of the unrestricted servo movement
        self.servo_angle_min  = -70 # This is the range of the unrestricted servo movement and will need to be calibrated.
        self.servo_angle_range = self.servo_angle_max - self.servo_angle_min
        self.eye_movement_max_radius = 70
        self.eye_movement_corner_angle = math.sqrt((self.eye_movement_max_radius**2)/2)

        # Servo Position Tracking Variables (degrees)
        self.eye_vert_angle   = 0
        self.eye_horiz_angle  = 0
        
        # Note that unless move_to(0, 0) is called the initial position will
        # be wrong. This is called in the controller as calling PCA9685(0x40)
        # turns off any pwm signal being sent so this must be done after the
        # eyes have each been constructed.
        

        # Eye Simulation
        self.radius = radius
        self.centre = centre
        
        self.use_mapping = True
        self.use_centring = True
        
        # Mapping up front calibration computations.
        # Currently no mapping will be Calibrated values for v2 eyes
        extreme_up_vert = self.eye_movement_max_radius #Calibrate
        extreme_up_horiz = 0 #Calibrate
        mag = math.sqrt(extreme_up_vert**2 + extreme_up_horiz**2)
        self.normalised_extreme_up_vert = extreme_up_vert/mag
        self.normalised_extreme_up_horiz = extreme_up_horiz/mag
        
        extreme_down_vert = -self.eye_movement_max_radius #Calibrate
        extreme_down_horiz = 25 #Calibrate
        mag = math.sqrt(extreme_down_vert**2 + extreme_down_horiz**2)
        self.normalised_extreme_down_vert = extreme_down_vert/mag
        self.normalised_extreme_down_horiz = extreme_down_horiz/mag
        
        extreme_left_vert = 0 #Calibrate
        extreme_left_horiz = -self.eye_movement_max_radius #Calibrate
        mag = math.sqrt(extreme_left_vert**2 + extreme_left_horiz**2)
        self.normalised_extreme_left_vert = extreme_left_vert/mag
        self.normalised_extreme_left_horiz = extreme_left_horiz/mag
        
        extreme_right_vert = -15 #Calibrate
        extreme_right_horiz = self.eye_movement_max_radius #Calibrate
        mag = math.sqrt(extreme_right_vert**2 + extreme_right_horiz**2)
        self.normalised_extreme_right_vert = extreme_right_vert/mag
        self.normalised_extreme_right_horiz = extreme_right_horiz/mag
        
        self.zero_position_vert = 15 #Calibrate
        self.zero_position_horiz = 15 #Calibrate
        
    def unsafe_move_to_mapped_position(self, horiz_angle, vert_angle):
        # Map the new angle against a correction matrix, which accounts for the mechanism of the eye.
        servo_angle_horiz, servo_angle_vert = self.map_eye_to_servo(horiz_angle, vert_angle);

        # Convert the corrected angle into a PWM tick count and therefore duty cycle
        servo_pwm_period_vert = self.conv_servo_angle_ms(int(servo_angle_vert))
        servo_pwm_period_horiz = self.conv_servo_angle_ms(int(servo_angle_horiz))
        
        #print("Servo PWM period Vert: " + str(servo_pwm_period_vert))
        #print("Servo PWM period Horiz: " + str(servo_pwm_period_horiz))

        # Apply this new duty cycle to the servomotor
        self.eye.set_pwm(self.vert_ch, 0, int(servo_pwm_period_vert))
        self.eye.set_pwm(self.horiz_ch, 0, int(servo_pwm_period_horiz))
        
        #Update the positions
        self.eye_horiz_angle = horiz_angle
        self.eye_vert_angle = vert_angle
        
        
    def is_valid_position(self, horiz_angle, vert_angle):
        
        if horiz_angle**2 + vert_angle**2 < self.eye_movement_max_radius**2:
            return True
        else:
            return False
        
        
    def make_valid_position(self, horiz_angle, vert_angle):
        # Move the position to the closest valid point by moving it
        # to the most extreme valid point on the line between the given
        # points and the centre.
        
        tol = 0.01
        
        
        if horiz_angle**2 + vert_angle**2 > 0:
            current_radius = math.sqrt(horiz_angle**2 + vert_angle**2)
        else:
            current_radius = 0
        
        if current_radius <= self.eye_movement_max_radius + tol:
            return horiz_angle, vert_angle
        
        print("Warning eye bound hit")
        wlogger.log_warning("Eye bound hit")
        norm_horiz_angle = horiz_angle / current_radius
        norm_vert_angle = vert_angle / current_radius
        
        valid_horiz_angle = norm_horiz_angle* self.eye_movement_max_radius
        valid_vert_angle = norm_vert_angle* self.eye_movement_max_radius
        
        return valid_horiz_angle, valid_vert_angle


    def step_vert_angle(self, step_size):
        """Advances the eye position by the "step_size" argument"""

        # First calculate the new angle
        target_vert_angle = self.eye_vert_angle + step_size
        #print("Target Vert: " + str(target_vert_angle))

        
        # Make the target position valid if needed
        target_horiz_angle, target_vert_angle = self.make_valid_position(self.eye_horiz_angle, target_vert_angle)
        #print("Step to")
        #print("Horiz: " + str(target_horiz_angle))
        #print("Vert: " + str(target_vert_angle))

        # Now move to given angle
        self.unsafe_move_to_mapped_position(target_horiz_angle, target_vert_angle)

        
    def step_horiz_angle(self, step_size):
        """Advances the eye position by the "step_size" argument"""

        # First calculate the new angle
        target_horiz_angle = self.eye_horiz_angle + step_size
        #print("Target Horiz: " + str(target_horiz_angle))
        
        # Make the target position valid if needed
        target_horiz_angle, target_vert_angle = self.make_valid_position(target_horiz_angle, self.eye_vert_angle)
        #print("Step to")
        #print("Horiz: " + str(target_horiz_angle))
        #print("Vert: " + str(target_vert_angle))

        # Now move to given angle
        self.unsafe_move_to_mapped_position(target_horiz_angle, target_vert_angle)
        
    def move_to(self, target_horiz_angle, target_vert_angle):
        
        valid_horiz_angle, valid_vert_angle = self.make_valid_position(target_horiz_angle, target_vert_angle)
        
        self.unsafe_move_to_mapped_position(target_horiz_angle, target_vert_angle)

        
    def get_vert_angle(self):
        return self.eye_vert_angle
    def get_horiz_angle(self):
        return self.eye_horiz_angle    

        
    def conv_servo_angle_ms(self, angle):
        """ Maps a servo angle to a number of ms PWM period required to move it to that position.
        A typical servo positioning system moves between -90 and 90 degress with periods between 1 and 2 ms.
        However, this library automatically takes the input angle and scales it to a position between the max
        servo range variables """

        scaled_angle = (float(angle) - float(self.servo_angle_min)) / float(self.servo_angle_range)
        return float(self.pwm_period_min + (scaled_angle * self.pwm_period_range))

    
    def map_eye_to_servo(self, horiz_angle, vert_angle):
        """ This function maps the given angles to the servo angles required to get the eye at that position. 
        This is required because of the linkage to the eye itself, which creates a mapping between the servo and eye angles. 
        """
        
        if self.use_centring == False:
            return horiz_angle, vert_angle
        
        if self.use_mapping == False:
            mapped_horiz_angle = horiz_angle + self.zero_position_vert
            mapped_vert_angle = vert_angle + self.zero_position_horiz
            return mapped_horiz_angle, mapped_vert_angle
        

        # Currently linearly interpolating results based on the quadrant
        # the target co ordinate lies in.
        
        #TODO finish this.
        
        #if horiz_angle > 0 and vert_angle > 0:
            #mapped_horiz_angle = horiz_angle*self.normalised_extreme_up_horiz
            #mapped_horiz_angle = horiz_angle*self.normalised_extreme_up_horiz
        #elif horiz_angle < 0 and vert_angle > 0:
            
        #elif horiz_angle < 0 and vert_angle < 0:
        
        #else:
        
        # Basic zero calibration for eyes v2
        mapped_horiz_angle = horiz_angle + self.zero_position_vert
        mapped_vert_angle = vert_angle + self.zero_position_horiz
        return mapped_horiz_angle, mapped_vert_angle


    def vert_test(self):
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))

        for i in range(0, 10):
            self.eye.set_pwm(self.vert_ch, 0, int(self.pwm_period_min))
            time.sleep(0.3)
            self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
            time.sleep(0.3)
            self.eye.set_pwm(self.vert_ch, 0, int(self.pwm_period_max))
            time.sleep(0.3)
            self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
            time.sleep(0.3)
            
    def horiz_test(self):
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))

        for i in range(0, 10):
            self.eye.set_pwm(self.horiz_ch, 0, int(self.pwm_period_min))
            time.sleep(0.3)
            self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
            time.sleep(0.3)
            self.eye.set_pwm(self.horiz_ch, 0, int(self.pwm_period_max))
            time.sleep(0.3)
            self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
            time.sleep(0.3)
            
    def vert_angle_test(self):    
        step = 1
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
        
        for i in range(0, 10):
            print(i)
            self.step_vert_angle(step)
            print(self.eye_vert_angle)
            time.sleep(0.3)
            self.step_vert_angle(-step)
            print(self.eye_vert_angle)
            time.sleep(0.3)
            self.step_vert_angle(-step)
            print(self.eye_vert_angle)
            time.sleep(0.3)
            self.step_vert_angle(step)
            print(self.eye_vert_angle)
            time.sleep(0.3)
            print(self.eye_vert_angle)
        
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
        
    def horiz_angle_test(self):
        step = 1
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
        
        for i in range(0, 10):
            print(i)
            self.step_horiz_angle(step)
            time.sleep(0.3)
            self.step_horiz_angle(-step)
            time.sleep(0.3)
            self.step_horiz_angle(-step)
            time.sleep(0.3)
            self.step_horiz_angle(step)
            time.sleep(0.3) 
       
        
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
        
        
    def recentre_servo(self):
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
        
                
    def recentre_angle(self):
        self.move_to(0, 0)
        
    def vert_test_increasing_steps(self):
        minimum_step = 2
        print(minimum_step)
        
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
        
        
        for j in range(0, 5):
            print("Step:")
            step = minimum_step*j
            print(step)
            
            for i in range(0, 2):
                self.step_vert_angle(step)
                print("Angles")
                print(self.eye_vert_angle)
                time.sleep(0.3)
                self.step_vert_angle(-step)
                print(self.eye_vert_angle)
                time.sleep(0.3)
                self.step_vert_angle(-step)
                print(self.eye_vert_angle)
                time.sleep(0.3)
                self.step_vert_angle(step)
                print(self.eye_vert_angle)
                time.sleep(0.3)
                print(self.eye_vert_angle)
                
                self.step_horiz_angle(step)
                print(self.eye_horiz_angle)
                time.sleep(0.3)
                self.step_horiz_angle(-step)
                print(self.eye_horiz_angle)
                time.sleep(0.3)
                self.step_horiz_angle(-step)
                print(self.eye_horiz_angle)
                time.sleep(0.3)
                self.step_horiz_angle(step)
                print(self.eye_horiz_angle)
                time.sleep(0.3)
                
            
        self.eye.set_pwm(self.horiz_ch, 0, int( self.pwm_period_zero))
        self.eye.set_pwm(self.vert_ch, 0, int( self.pwm_period_zero))
        
        
        
    def multistep_horiz(self, num_steps, angle, sleep_time):
        
        for i in range(0, num_steps):
            self.step_horiz_angle(angle)   
            time.sleep(sleep_time)
            
            
    def multistep_vert(self, num_steps, angle, sleep_time):
        
        for i in range(0, num_steps):
            self.step_vert_angle(angle)
            time.sleep(sleep_time)
            
    def multistep_both(self, num_steps, vert_angle, horiz_angle, sleep_time):
        
        for i in range(0, num_steps):
            self.step_vert_angle(vert_angle) 
            self.step_horiz_angle(horiz_angle)   
            time.sleep(sleep_time)

        

