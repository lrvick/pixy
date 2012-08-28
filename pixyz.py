from smbus import SMBus
from time import sleep
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

led_pin = 4

x_dir_pin = 22
x_step_pin = 21
y_dir_pin = 18
y_step_pin = 17

speed = 0.0009

for pin in led_pin,y_step_pin,y_dir_pin,x_step_pin,x_dir_pin:
    GPIO.setup(pin, GPIO.OUT, pull_up_down=GPIO.PUD_UP)

bus = SMBus(0)

bus.write_byte_data(0x52,0x40,0x00)

sleep(0.000001)

def step(axis,direction):
    if axis == 0:
        step_pin = y_step_pin
        dir_pin = y_dir_pin
    if axis == 1:
        step_pin = x_step_pin
        dir_pin = x_dir_pin
    print('joy_x',joy_x,'joy_y',joy_y,'button_c',button_c,'button_z',button_z)
    GPIO.output(dir_pin, direction)
    GPIO.output(led_pin, True)
    GPIO.output(step_pin, True)
    sleep(speed)
    GPIO.output(led_pin, False)
    GPIO.output(step_pin, False)
    sleep(speed)

while 1:

    bus.write_byte(0x52,0x00)

    sleep(0.000001)

    data = []
    for i in xrange(6):
        data.append(bus.read_byte(0x52))

    joy_x = data[0] -121
    joy_y = data[1] -112
    if (joy_y > 119): joy_y = -90
    accel_x = (data[2] << 2) + ((data[5] & 0x0c) >> 2)
    accel_y = (data[3] << 2) + ((data[5] & 0x30) >> 4)
    accel_z = (data[4] << 2) + ((data[5] & 0xc0) >> 6)
    button_c = (data[5] & 0x1) ^ ((data[5] & 0x2) >> 1)
    button_z = (data[5] & 0x1) ^ 1

    if joy_y > 15:
        step(0,0)
    elif joy_y < -15:
        step(0,1)
    if joy_x > 15:
        step(1,0)
    elif joy_x < -15:
        step(1,1)
