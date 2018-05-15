import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
  inputValueYellow = GPIO.input(4)
  inputValueBlue = GPIO.input(22)
  inputValueGreen= GPIO.input(19)

  if(inputValueYellow == True):
    print("Button press - Yellow")
    time.sleep(0.3)

  if(inputValueBlue == True):
    print("Button press - Blue")
    time.sleep(0.3)

  if(inputValueGreen== True):
    print("Button press - Green")
    time.sleep(0.3)
