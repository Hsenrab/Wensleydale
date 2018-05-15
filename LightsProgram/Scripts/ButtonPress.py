import RPi.GPIO as GPIO
import time

inputPinA = 24
inputPinB = 25
inputPinC = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(inputPinA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(inputPinB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(inputPinC, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
  inputValueA = GPIO.input(inputPinA)
  inputValueB = GPIO.input(inputPinB)
  inputValueC = GPIO.input(inputPinC)

  if(inputValueA == True):
    print("Button press - A")
    time.sleep(0.3)

  if(inputValueB == True):
    print("Button press - B")
    time.sleep(0.3)

  if(inputValueC == True):
    print("Button press - C")
    time.sleep(0.3)
