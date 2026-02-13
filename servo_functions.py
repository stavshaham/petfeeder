import machine
import time

# Servo connected through PWM to pin 14
servo = machine.PWM(machine.Pin(14))
servo.freq(50) # 50 Hz frequency, used for calculations, gives .2s

def set_angle(angle):
    # Calculation with errors, -8% error for the min duty and -5% error for the max duty
    min_duty = 3015
    max_duty = 6225 
    duty_range = max_duty - min_duty
    
    # Calculating the final duty
    duty = int(min_duty + (angle / 90) * duty_range)
    servo.duty_u16(duty)
    
# This function is dispencing the food for x seconds
def dispense_food(seconds):
    # Open gate in 90 degrees
    set_angle(90)
    time.sleep(seconds)
    # Close gate
    set_angle(0)