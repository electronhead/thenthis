import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin=17
print(f"pin {pin} set to {GPIO.input(pin)}")
pin=18
print(f"pin {pin} set to {GPIO.input(pin)}")