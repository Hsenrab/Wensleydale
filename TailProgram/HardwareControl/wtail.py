import RPi.GPIO as GPIO
import time
import Internals.Utils.wlogger as wlogger
import Main.config as config

from Adafruit_PCA9685 import PCA9685 
import Internals.Utils.wgloballock as wgloballock

print_debug = True




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
        self.lock.acquire()
        successful_move = False
        while not successful_move:
            try:
                self.motor.set_pwm(self.forward_ch, 0, 2250) # Calibrated
                self.motor.set_pwm(self.backwards_ch, 0, 0)
                successful_move = True
            except IOError as e:
                if print_debug:
                    print("ExceptionCaught")
                wlogger.log_info("Exceptioin Caught")
                wlogger.log_info(e)
                successful_move = False
                pass
        
        self.lock.release()
        wlogger.log_info("Set Tail On")
    
    def set_tail_off(self):
        
        if print_debug:
            print("Tail Off")
        GPIO.output(config.touchOutputPin, GPIO.LOW)
        self.lock.acquire()
        self.motor.set_pwm(self.forward_ch, 0, 0)
        self.motor.set_pwm(self.backwards_ch, 0, 0)
        self.lock.release()
        wlogger.log_info("Set Tail Off")
        
    
    def record_button_press(self):
        if config.button_press_count % 100 == 0:
            with open('TailButtonCount.log', 'w+') as f:
                f.write(str(config.button_press_count))
            
    
    
    # This function listens to the button and turns the LEDs on and off.
    def control_tail(self):
    
        # Set up touch pad pins.
        self.set_up_pins()

        # Set tail off to start.
        self.set_tail_off()
        is_tail_on = False
        
        continue_control = True
        button_already_pressed = False
        
        while continue_control:
            
            # Assume this cycles has no button press. This will be reset to
            # zero if a button is pressed.
            config.cycles_without_button_press += 1

            # Determine whether a random change is needed. 
        
            if config.cycles_without_button_press > config.num_cycles_before_random_wag:
                if config.cycles_without_button_press % config.random_wag_frequency < config.random_wag_length:
            
                    wlogger.log_info("Random Wag -> Tail On")
                    
                    if print_debug:
                        print("Random Wag -> Tail On", flush=True)
                        
                    is_tail_on = True
                    
                    
                else:
                    
                    wlogger.log_info("Random Wag -> Tail Off")
                    
                    if print_debug:
                        print("Random Wag -> Tail Off", flush=True)
                        
                    is_tail_on = False
                
            
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
            

