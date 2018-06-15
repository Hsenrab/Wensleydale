import RPi.GPIO as GPIO
import time
import Internals.Utils.wlogger as wlogger
import Main.config as config
import random
print_debug = True




def set_up_pins():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.touchInputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(config.touchOutputPin, GPIO.OUT)
    
    GPIO.setup(config.BigLEDAOutputPinRed, GPIO.OUT)
    GPIO.setup(config.BigLEDAOutputPinBlue, GPIO.OUT)
    GPIO.setup(config.BigLEDAOutputPinGreen, GPIO.OUT)
    GPIO.setup(config.BigLEDBOutputPinRed, GPIO.OUT)
    GPIO.setup(config.BigLEDBOutputPinBlue, GPIO.OUT)
    GPIO.setup(config.BigLEDBOutputPinGreen, GPIO.OUT)
    


def set_leds_on():
    
    set_leds_off() #Clear previous colours
    
    #Set the rbg of each LED to randomly be on or off to generate a
    # random colour.
    
    red1 = (random.randint(0,1) == 1)
    blue1 = (random.randint(0,1) == 1)
    green1 = (random.randint(0,1) == 1)
    red2 = (random.randint(0,1) == 1)
    blue2 = (random.randint(0,1) == 1)
    green2 = (random.randint(0,1) == 1)
    
    # If all are off make both LEDs red.
    if not red1 and not red2 and not blue1 and not blue2 and \
        not green1 and not green2:
            red1 = True
            red2 = True
            
    if red1:
        GPIO.output(config.BigLEDAOutputPinRed, GPIO.HIGH)
    if blue1:
        GPIO.output(config.BigLEDAOutputPinBlue, GPIO.HIGH)
    if green1:
        GPIO.output(config.BigLEDAOutputPinGreen, GPIO.HIGH)
    if red2:
        GPIO.output(config.BigLEDBOutputPinRed, GPIO.HIGH)
    if blue2:
        GPIO.output(config.BigLEDBOutputPinBlue, GPIO.HIGH)
    if green2:
        GPIO.output(config.BigLEDBOutputPinGreen, GPIO.HIGH)

def set_leds_off():
    GPIO.output(config.BigLEDAOutputPinRed, GPIO.LOW)
    GPIO.output(config.BigLEDAOutputPinBlue, GPIO.LOW)
    GPIO.output(config.BigLEDAOutputPinGreen, GPIO.LOW)
    GPIO.output(config.BigLEDBOutputPinRed, GPIO.LOW)
    GPIO.output(config.BigLEDBOutputPinBlue, GPIO.LOW)
    GPIO.output(config.BigLEDBOutputPinGreen, GPIO.LOW)
    

def record_button_presses(button_press_count)
 
    file_path = '/home/pi/BigLEDButtonPresses.csv'
    if not os.path.isfile(file_path):
        with open(file_path, 'a') as buttonFile:
            wrtr = csv.writer(buttonFile, delimiter=',', quotechar='"')
            wrtr.writerow(['Pi Time',
                            'Total Count'])
                            
    with open(file_path, 'a') as buttonFile:
        wrtr = csv.writer(buttonFile, delimiter=',', quotechar='"')
        timestamp = time.time()
        wrtr.writerow([datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                        button_press_count)
        


# This function listens to the button and turns the LEDs on and off.
def control_big_leds():

    # Set up pins.
    set_up_pins()
    
    # Set LEDs on to start.
    set_leds_on()
    is_LEDs_on = True
    
    continue_control = True
    button_already_pressed = False
    button_press_count = 0
    
    while continue_control:    
        # Gather button input
        inputButton = GPIO.input(config.touchInputPin)

        # Change BigLED if button is pressed.
        if inputButton and not button_already_pressed:
            GPIO.output(config.touchOutputPin, GPIO.HIGH)
            button_press_count += 1
            button_already_pressed = True
            
            if False: 
                set_leds_off()
                wlogger.log_info("Button press -> LEDs Off, No. Presses: " + str(config.button_press_count))
                
                if print_debug:
                    print("Button press -> LEDs Off", flush=True)
                    
                is_LEDs_on = False
            else:
                set_leds_on()
                wlogger.log_info("Button press -> LEDs On, No. Presses: " + str(config.button_press_count))
                
                if print_debug:
                    print("Button press -> LEDs On", flush=True)
                    
                is_LEDs_on = True

                 
        elif not inputButton:
            GPIO.output(config.touchOutputPin, GPIO.LOW)
            button_already_pressed = False
                
       
        try:
            if count % config.num_cycles_between_button_recording == 0:
                record_button_presses(button_press_count)   
                button_press_count = 0
                
        except Exception as e:
            print("Recording Error")
            wlogger.log_info(e)
            pass
            
        # Small time delay between each run through.
        time.sleep(0.1)
        

