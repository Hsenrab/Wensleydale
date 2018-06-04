import RPi.GPIO as GPIO
import time
import Internals.Utils.wlogger as wlogger
import Main.config as config

from Adafruit_PCA9685 import PCA9685 

print_debug = True




class Tail:
    def set_up_pins(self):
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config.touchInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(config.touchOutputPin, GPIO.OUT)
    
        self.touchInputPin = 0
        self.touchOutputPin = 0
        self.forward_ch = 0
        self.backwards_ch = 1
        
        # PWM Setup Variables
        self.motor = PCA9685(0x40) # Always use the default i2c address for the PWM hats. This call turns off any pwm signal currently being sent.
        self.pwm_freq = 5000
        self.motor.set_pwm_freq(self.pwm_freq)
    
        self.pwm_bitres = 4096
        self.pwm_scaler = self.pwm_bitres / (1/self.pwm_freq)
    
    
    def set_tail_on(self):
        if print_debug:
            print("Tail On")
        GPIO.output(config.touchOutputPin, GPIO.HIGH)
        self.motor.set_pwm(self.forward_ch, 0, 2000) # needs calibrating - changes speed of tail.
        self.motor.set_pwm(self.backwards_ch, 0, 0)
    
    def set_tail_off(self):
        
        if print_debug:
            print("Tail Off")
        GPIO.output(config.touchOutputPin, GPIO.LOW)
        self.motor.set_pwm(self.forward_ch, 0, 0)
        self.motor.set_pwm(self.backwards_ch, 0, 0)
        
    
    def record_button_press(self):
        if config.button_press_count % 1000 == 0:
            with open('TailButtonCount.log', 'w+') as f:
                f.write(str(config.button_press_count))
            
    
    
    # This function listens to the button and turns the LEDs on and off.
    def control_tail(self):
    
        # Set up touch pad pins.
        self.set_up_pins()

        # Set tail off to start.
        self.set_tail_on() #TODO
        is_tail_on = True
        
        continue_control = True
        button_already_pressed = False
        
        while continue_control:    
            # Gather button input
            inputButton = GPIO.input(config.touchInputPin)
    
            # Change BigLED if button is pressed.
            if inputButton and not button_already_pressed:
                button_already_pressed = True
                config.button_press_count += 1
                
                if is_tail_on: 
                    wlogger.log_info("Button press -> Tail Off, No. Presses: " + str(config.button_press_count))
                    
                    if print_debug:
                        print("Button press -> Tail Off", flush=True)
                        
                    is_tail_on = False
                    
                else:
                    wlogger.log_info("Button press -> Tail On, No. Presses: " + str(config.button_press_count))
                    
                    if print_debug:
                        print("Button press -> Tail On", flush=True)
                        
                    is_tail_on = True
                
                self.record_button_press()
            elif not inputButton:
                button_already_pressed = False
                
            print(is_tail_on)
            if is_tail_on: 
                self.set_tail_on()
            else:
                self.set_tail_off()

            
            self.record_button_press()
            
            # Small time delay between each run through.
            time.sleep(0.1)
            

