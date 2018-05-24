import RPi.GPIO as GPIO
import time
import Internals.Utils.wlogger as wlogger

print_debug = True

BigLEDinputPin = 0
BigLEDOutputPinRed = 1
BigLEDOutputPinBlue = 1
BigLEDOutputPinGreen = 1

def set_up_pins():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BigLEDinputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BigLEDOutputPinRed, GPIO.OUT)
    GPIO.setup(BigLEDOutputPinBlue, GPIO.OUT)
    GPIO.setup(BigLEDOutputPinGreen, GPIO.OUT)

def set_leds_on():
    GPIO.output(BigLEDOutputPinRed, GPIO.HIGH)
    GPIO.output(BigLEDOutputPinBlue, GPIO.HIGH)
    GPIO.output(BigLEDOutputPinGreen, GPIO.HIGH)

def set_leds_off():
    GPIO.output(BigLEDOutputPinRed, GPIO.LOW)
    GPIO.output(BigLEDOutputPinBlue, GPIO.LOW)
    GPIO.output(BigLEDOutputPinGreen, GPIO.LOW)
    

def record_button_press():
    if config.button_press_count % 1000 == 0:
        with open('BigLEDsButtonCount.log') as f:
            f.write(config.button_press_count)
        


# This function listens to the button and turns the LEDs on and off.
def control_big_leds():

    # Set up pins.
    set_up_pins()
    
    # Set LEDs on to start.
    set_leds_on()
    is_LEDs_on = True
    
    continue_control = True
    
    while continue_control:    
        # Gather button input
        inputButton = GPIO.input(BigLEDinputPin)

        # Change BigLED if button is pressed.
        if inputButton:
            config.button_press_count += 1
            
            if is_LEDs_on: 
                set_leds_off()
                wlogger.log_info("Button press -> LEDs Off, No. Presses: " + str(button_press_count))
                
                if print_debug:
                    print("Button press -> LEDs Off", flush=True)
                
            else:
                set_leds_on()
                wlogger.log_info("Button press -> LEDs On, No. Presses: " + str(button_press_count))
                
                if print_debug:
                    print("Button press -> LEDs On", flush=True)
            
            record_button_press()
        
        # Small time delay between each run through.
        time.sleep(0.1)
        

