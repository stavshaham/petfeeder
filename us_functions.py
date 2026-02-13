import machine
import time
from pico_i2c_lcd import I2cLcd
import servo_functions as sf

# Ultrasonic sensor
us_trig = machine.Pin(17, machine.Pin.OUT)
us_echo = machine.Pin(16, machine.Pin.IN)
us_pot = machine.ADC(26)

# Make sure we don't return errors, makes better calculations, might be worse for a few moments in big changes of distance
history = []

# Timer
start_timer = None
food_dispensed = False
time_to_stay = 5000 # 5 seconds
timer = None

# Potentiometer
POT_MAX = 60

# Display
lcd = None

def init_lcd(lcd_instance):
    global lcd
    lcd = lcd_instance

# This function gets the distance from the ultrasonic sensor
def get_distance():
    # Ensure TRIG is low
    us_trig.low()
    time.sleep_us(2)

    # Send 10 µs HIGH pulse
    us_trig.high()
    time.sleep_us(10)
    us_trig.low()

    # Measure pulse width on ECHO
    duration = machine.time_pulse_us(us_echo, 1, 30000)  # timeout 30ms

    if duration < 0:
        return None  # echo failed

    # Convert to cm
    distance = duration * 0.034 / 2
    return distance

# This function gets a stable distance from the sensor, eliminating errors using an array
# Taking last 5 measurements
def get_stable_distance():
    distance = get_distance()
    if distance is not None:
        history.append(distance)
        if len(history) > 5:  # average last 5 readings
            history.pop(0)
        return sum(history) / len(history)
    return None

# This function gets the threshold from the potentiometer
def get_threshold():
    threshold_binary = us_pot.read_u16()
    # Dividing the current value in the maximum value, multiplying it by the maximum distance allowed
    threshold = int(threshold_binary / 65535 * POT_MAX)
    return threshold

# This funcion resets the timer
def reset_timer(t1):
    global food_dispensed, timer, start_timer
    food_dispensed = False
    start_timer = None
    timer.deinit()
    lcd.clear()
    lcd.putstr("Can drop food.")

# This function starts the reset timer
def start_reset_timer(delay_time):
    global timer
    timer = machine.Timer(-1)
    timer.init(mode=machine.Timer.ONE_SHOT, period = delay_time, callback = reset_timer)
    lcd.clear()
    lcd.putstr("Food dispense is")
    lcd.move_to(0, 1)
    lcd.putstr("on timeout.")

# This function checks if the pet is within the threshold for the time_to_stay
def distance_to_timer(distance, threshold, seconds, delay_time):
    global start_timer, food_dispensed
    if food_dispensed:
        return
    
    if distance is not None and distance > 0 and distance <= threshold:
        if start_timer is None:
            start_timer = time.ticks_ms() # Current time in ms
        else:
            # Checking how long has been passed from the timer
            elapsed = time.ticks_diff(time.ticks_ms(), start_timer)
            if elapsed >= time_to_stay and not food_dispensed:
                sf.dispense_food(seconds)
                food_dispensed = True
                start_reset_timer(delay_time)
                
    else:
        start_timer = None                
        
    