import machine
import time
from pico_i2c_lcd import I2cLcd
import servo_functions as sf
import us_functions as usf
import pico_server as server

# LED
red_led = machine.Pin(15, machine.Pin.OUT)

running = False
threshold = 0
distance = 0
seconds = 2 # in seconds
delay_time = 10000 # in ms

# Real Time Clock
rtc = machine.RTC()

TARGET_HOUR = 19
TARGET_MINUTE = 57
TARGET_SEC = 30

red_led.value(0)

# Display
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
devices = i2c.scan()
if len(devices) == 0:
    print("No I2C device found")
else:
    print("I2C Address:", hex(devices[0]))
    lcd = I2cLcd(i2c, devices[0], 2, 16)
    lcd.clear()
    lcd.putstr("Connecting to")
    lcd.move_to(0, 1)
    lcd.putstr("WiFi...")
    
# Passing the LCD to the usf file
usf.init_lcd(lcd)
    
# This function return the LCD screen
def get_lcd_display():
    global lcd
    return lcd

# Toggls the LED light
def change_leds(distance):
    if distance is not None and distance > 0 and distance <= threshold:
        red_led.value(1)
    else:
        red_led.value(0)

time.sleep(2)

running = server.connect_wifi(lcd)
connection = server.open_socket()

# If the connection is None, usually means that there is a process already running on this port
if connection is not None and running:
    lcd.show("Can drop food.")
    try:
        while running:
            # Sensor logic
            threshold = usf.get_threshold()
            distance = usf.get_stable_distance()
            change_leds(distance)
            usf.distance_to_timer(distance, threshold, seconds, delay_time)

            # Network logic
            server.loop(seconds)
    except KeyboardInterrupt:
        # Catches the interrupt if it happens outside the while loop (less common)
        pass
    finally:
        server.close_socket_gracefully()

# Errors in case of WiFi cannot connect
if not running:
    lcd.show("WiFi Faild")
elif connection is None:
    lcd.show("Connection Faild")
    