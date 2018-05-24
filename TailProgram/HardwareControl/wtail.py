import RPi.GPIO as GPIO
import time
import Internals.Utils.wlogger as wlogger

print_debug = True


touchInputPin = 0
touchOutputPin = 0


def set_up_pins():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(touchInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(touchOutputPin, GPIO.OUT)
    

def set_tail_on():
    # TODO - add tail move
    GPIO.output(touchOutputPin, GPIO.HIGH)

def set_tail_off():
    # TODO - add tail move
    GPIO.output(touchOutputPin, GPIO.LOW)
    

def record_button_press():
    if config.button_press_count % 1000 == 0:
        with open('TailButtonCount.log') as f:
            f.write(config.button_press_count)
        


# This function listens to the button and turns the LEDs on and off.
def control_tail():

    # Set up pins.
    set_up_pins()
    
    # Set tail off to start.
    set_tail_off()
    is_tail_on = True
    
    continue_control = True
    
    while continue_control:    
        # Gather button input
        inputButton = GPIO.input(BigLEDinputPin)

        # Change BigLED if button is pressed.
        if inputButton:
            config.button_press_count += 1
            
            if is_tail_on: 
                set_tail_off()
                wlogger.log_info("Button press -> Tail Off, No. Presses: " + str(button_press_count))
                
                if print_debug:
                    print("Button press -> Tail Off", flush=True)
                    
                is_tail_on = False
                
            else:
                set_tail_on()
                wlogger.log_info("Button press -> Tail On, No. Presses: " + str(button_press_count))
                
                if print_debug:
                    print("Button press -> Tail On", flush=True)
                    
                is_tail_on = True
            
            record_button_press()
        
        # Small time delay between each run through.
        time.sleep(0.1)
        

