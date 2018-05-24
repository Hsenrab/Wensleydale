import RPi.GPIO as GPIO
import time
import Internals.Utils.wlogger as wlogger

print_debug = True

touchInputPin = 0
touchOutputPin = 0

BigLEDAOutputPinRed = 17
BigLEDAOutputPinBlue = 27
BigLEDAOutputPinGreen = 22
BigLEDBOutputPinRed = 10
BigLEDBOutputPinBlue = 9
BigLEDBOutputPinGreen = 11


def set_up_pins():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(touchInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(touchOutputPin, GPIO.OUT)
    
    GPIO.setup(BigLEDAOutputPinRed, GPIO.OUT)
    GPIO.setup(BigLEDAOutputPinBlue, GPIO.OUT)
    GPIO.setup(BigLEDAOutputPinGreen, GPIO.OUT)
    GPIO.setup(BigLEDBOutputPinRed, GPIO.OUT)
    GPIO.setup(BigLEDBOutputPinBlue, GPIO.OUT)
    GPIO.setup(BigLEDBOutputPinGreen, GPIO.OUT)
    


def set_leds_on():
    GPIO.output(BigLEDAOutputPinRed, GPIO.HIGH)
    GPIO.output(BigLEDAOutputPinBlue, GPIO.HIGH)
    GPIO.output(BigLEDAOutputPinGreen, GPIO.HIGH)
    GPIO.output(BigLEDBOutputPinRed, GPIO.HIGH)
    GPIO.output(BigLEDBOutputPinBlue, GPIO.HIGH)
    GPIO.output(BigLEDBOutputPinGreen, GPIO.HIGH)
    
    GPIO.output(touchOutputPin, GPIO.HIGH)

def set_leds_off():
    GPIO.output(BigLEDAOutputPinRed, GPIO.LOW)
    GPIO.output(BigLEDAOutputPinBlue, GPIO.LOW)
    GPIO.output(BigLEDAOutputPinGreen, GPIO.LOW)
    GPIO.output(BigLEDBOutputPinRed, GPIO.LOW)
    GPIO.output(BigLEDBOutputPinBlue, GPIO.LOW)
    GPIO.output(BigLEDBOutputPinGreen, GPIO.LOW)
    
    GPIO.output(touchOutputPin, GPIO.LOW)
    

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
                    
                is_LEDs_on = False
            else:
                set_leds_on()
                wlogger.log_info("Button press -> LEDs On, No. Presses: " + str(button_press_count))
                
                if print_debug:
                    print("Button press -> LEDs On", flush=True)
                    
                is_LEDs_on = True
            
            record_button_press()
        
        # Small time delay between each run through.
        time.sleep(0.1)
        

