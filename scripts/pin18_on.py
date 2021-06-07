import RPi.GPIO as GPIO
level=1
pin=18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin,level)
print(f"pin {pin} set to {GPIO.input(pin)})