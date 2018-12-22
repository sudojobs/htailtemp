#Program asks for user input to determine color to shine.

import time, sys
import RPi.GPIO as GPIO

redPin = 15   #Set to appropriate GPIO
greenPin = 13 #Should be set in the 
bluePin = 11  #GPIO.BOARD format

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    
def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
def redOn():
    blink(redPin)

def redOff():
    turnOff(redPin)

def greenOn():
    blink(greenPin)

def greenOff():
    turnOff(greenPin)

def blueOn():
    blink(bluePin)

def blueOff():
    turnOff(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)


def whiteZero():
        whiteOn()

def cyanSlow():
        cyanOn()

def cyanFast():
        cyanOn()

def sequence():
    while True:
       redOn()
       time.sleep(2)
       redOff()
       time.sleep(1)
       greenOn()
       time.sleep(2)
       greenOff()
       time.sleep(1)
       blueOn()
       time.sleep(2)
       blueOff()
       time.sleep(1)
       yellowOn()
       time.sleep(2)
       yellowOff()
       time.sleep(1)
       cyanOn()
       time.sleep(2)
       cyanOff()
       time.sleep(1)
       magentaOn()
       time.sleep(2)
       magentaOff()
       time.sleep(1)
       whiteOn()
       time.sleep(2)
       whiteOff()
       time.sleep(1)
    return
    

def main():
    while True:
        cmd = raw_input("-->")


        if cmd == "red on":
            redOn()
        elif cmd == "red off":
            redOff()
        elif cmd == "green on":
            greenOn()
        elif cmd == "green off":
            greenOff()
        elif cmd == "blue on":
            blueOn()
        elif cmd == "blue off":
            blueOff()
        elif cmd == "yellow on":
            yellowOn()
        elif cmd == "yellow off":
            yellowOff()
        elif cmd == "cyan on":
            cyanOn()
        elif cmd == "cyan off":
            cyanOff()
        elif cmd == "magenta on":
            magentaOn()
        elif cmd == "magenta off":
            magentaOff()
        elif cmd == "white on":
            whiteOn()
        elif cmd == "white off":
            whiteOff()
        else:
            print("Not a valid command")
        
        
    return

#try:
#    main()
#except:
#    GPIO.cleanup()
    
