import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BOARD)
    PIN_TRIGGER_1 = 16
    PIN_ECHO_1 = 18
    sample_intervals = 1
    count = 0 
    while True:
        GPIO.setup(PIN_TRIGGER_1, GPIO.OUT)
        GPIO.setup(PIN_ECHO_1, GPIO.IN)
        GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
        
        time.sleep(sample_intervals)
        GPIO.output(PIN_TRIGGER_1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
        
        while GPIO.input(PIN_ECHO_1)==0:
            pulse_start_time_1 = time.time()
        while GPIO.input(PIN_ECHO_1)==1:
            pulse_end_time_1 = time.time()
            
        pulse_duration_1 = pulse_end_time_1 - pulse_start_time_1
        distance_1 = round((pulse_duration_1 * 17150)*0.0328084, 2)
        if distance_1 < 1:
            print ("Distance_1:",distance_1,"ft")
            count = count + 1
            if count == 5:
                break

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
