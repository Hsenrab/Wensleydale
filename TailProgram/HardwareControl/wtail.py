import RPi.GPIO as GPIO
import time
import Internals.Utils.wlogger as wlogger
import Main.config as config
import os
import datetime
import csv
from Adafruit_PCA9685 import PCA9685 
import Internals.Utils.wgloballock as wgloballock

print_debug = False




class Tail:
    def set_up_pins(self):
        
        # Set up file lock.
        self.lock = wgloballock.WFileLock("my_lock.txt", dir="/home/pi/temp")
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.touchInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(config.touchOutputPin, GPIO.OUT)
    
        self.touchInputPin = 0
        self.touchOutputPin = 0
        self.forward_ch = 0
        self.backwards_ch = 1
        
        # PWM Setup Variables
        self.lock.acquire()
        self.motor = PCA9685(0x41) # Always use the default i2c address for the PWM hats. This call turns off any pwm signal currently being sent.
        self.pwm_freq = 5000
        self.motor.set_pwm_freq(self.pwm_freq)
        self.lock.release()
    
        self.pwm_bitres = 4096
        self.pwm_scaler = self.pwm_bitres / (1/self.pwm_freq)
    
    
    def set_tail_on(self):
        if print_debug:
            print("Tail On")
        GPIO.output(config.touchOutputPin, GPIO.HIGH)
        
        successful_move = False
        num_tries = 0
        while not successful_move and num_tries < 1000:
            try:
                self.motor.set_pwm(self.forward_ch, 0, 2250) # Calibrated
                self.motor.set_pwm(self.backwards_ch, 0, 0)
                successful_move = True
            except IOError as e:
                if print_debug:
                    print("ExceptionCaught")
                wlogger.log_info("Exception Caught")
                wlogger.log_info(e)
                successful_move = False
                num_tries += 1
                pass
                
        if num_tries >= 1000:
            wlogger.log_info("Num Tries Reached")
                
        wlogger.log_info("Set Tail On")
    
    def set_tail_off(self):
        
        if print_debug:
            print("Tail Off")
        GPIO.output(config.touchOutputPin, GPIO.LOW)
        successful_move = False
        num_tries = 0
        while not successful_move and num_tries < 1000:
            try:
                self.motor.set_pwm(self.forward_ch, 0, 0) # Calibrated
                self.motor.set_pwm(self.backwards_ch, 0, 0)
                successful_move = True
            except IOError as e:
                if print_debug:
                    print("ExceptionCaught")
                wlogger.log_info("Exception Caught")
                wlogger.log_info(e)
                successful_move = False
                num_tries += 1
                pass
        wlogger.log_info("Set Tail Off")
        
    
    def record_button_presses(self, button_press_count):
 
        file_path = '/home/pi/TailButtonPresses.csv'
        if not os.path.isfile(file_path):
            with open(file_path, 'a') as buttonFile:
                wrtr = csv.writer(buttonFile, delimiter=',', quotechar='"')
                wrtr.writerow(['Pi Time',
                                'Total Count'])
                                
        with open(file_path, 'a') as buttonFile:
            wrtr = csv.writer(buttonFile, delimiter=',', quotechar='"')
            timestamp = time.time()
            wrtr.writerow([datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'), button_press_count])
            
    
    
    # This function listens to the button and turns the LEDs on and off.
    def control_tail(self):
    
        # Set up touch pad pins.
        self.set_up_pins()

        # Set tail off to start.
        self.set_tail_on()
        is_tail_on = True
        
        continue_control = True
        button_already_pressed = False
        
        config.cycles_without_button_press = 0
        button_press_count = 0
        count = 0
        
        while continue_control:
            count +=1
            
            # Assume this cycle has no button press.
            config.cycles_without_button_press += 1
            
             # Determine whether a random wag is needed. 
            if config.cycles_without_button_press > config.num_cycles_before_random_wag:
                if config.cycles_without_button_press % config.random_wag_frequency == 0:
            
                    wlogger.log_info("Random Wag -> Tail On")
                    
                    if print_debug:
                        print("Random Wag -> Tail On", flush=True)
                        
                    is_tail_on = True
                    
                    
                elif config.cycles_without_button_press % config.random_wag_frequency == config.random_wag_length:
                    
                    wlogger.log_info("Random Wag -> Tail Off")
                    
                    if print_debug:
                        print("Random Wag -> Tail Off", flush=True)
                        
                    is_tail_on = False


            # Gather button input
            inputButton = GPIO.input(config.touchInputPin)
    
            # Change BigLED if button is pressed.
            if inputButton and not button_already_pressed:
                button_already_pressed = True
                button_press_count += 1
                config.cycles_without_button_press = 0
                
                if is_tail_on: 
                    wlogger.log_info("Button press -> Tail Off")
                    
                    if print_debug:
                        print("Button press -> Tail Off", flush=True)
                        
                    is_tail_on = False
                    
                else:
                    wlogger.log_info("Button press -> Tail On")
                    
                    if print_debug:
                        print("Button press -> Tail On", flush=True)
                        
                    is_tail_on = True
                

            elif not inputButton:
                button_already_pressed = False
                

            if is_tail_on: 
                self.set_tail_on()
            else:
                self.set_tail_off()

            
            try:
                if count % config.num_cycles_between_button_recording == 0:
                    self.record_button_presses(button_press_count)   
                    button_press_count = 0
                
            except Exception as e:
                print("Recording Error")
                wlogger.log_info(e)
                pass
            
            # Small time delay between each run through.
            time.sleep(0.1)
            

