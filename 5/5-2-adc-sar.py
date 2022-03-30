import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def bin2dec(value):
    dec = 0
    deg = 0
    for i in range(7, -1, -1):       
        dec += (2*value[i])**deg
        deg += 1

    return dec

def adc():
    bin = dec2bin(0)
    for i in range(7):
        bin[i] = 1
        GPIO.output(dac, bin)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            bin[i] = 0

    dec = bin2dec(bin)
    return dec

try:
    while True:
        dec = adc()
        print(f"{dec2bin(dec)} -> {dec} -> {(3.3 * dec) / 256} V")
finally:
    GPIO.cleanup()