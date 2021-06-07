import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin=17
GPIO.setup(pin, GPIO.IN)
print(f"pin {pin} set to {GPIO.input(pin)})
pin=18
GPIO.setup(pin, GPIO.IN)
print(f"pin {pin} set to {GPIO.input(pin)})