import time
import socket
import threading
import subprocess
import RPi.GPIO as GPIO

class RoverReceiveMovementClass(threading.Thread):

    server_ip = '0.0.0.0'
    server_port_movement = 0
    is_going = False
       
    def __init__(self, server_ip, server_port_movement):
        threading.Thread.__init__(self)
        self.server_ip = server_ip
        self.server_port_movement = server_port_movement

    def run(self):
        self.receive_text()
    
    def receive_text(self):
        try:
            rover_socket_movement = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rover_socket_movement.connect((self.server_ip, self.server_port_movement))
            print('***** Connecting to Server IP:', self.server_ip, 'Port:', self.server_port_movement, "*****")
            password = 'jetson'
            subprocess.call("echo {} | sudo -S sh bashWheel.sh 0".format(password), shell=True)
            subprocess.call("echo {} | sudo -S sh bashTurn.sh 500".format(password), shell=True)
            try:
                while rover_socket_movement:
                    if self.is_going == False:
                        self.sensor_start()
                        rover_socket_movement.send('connected'.encode('utf-8'))
                        subprocess.call("echo {} | sudo -S sh newForward.sh".format(password), shell=True)
                        self.is_going = True

                    msg = rover_socket_movement.recv(1024).decode('utf-8')

                    if "DESTINATION REACHED" in msg :
                        subprocess.call("echo {} | sudo -S sh bashWheel.sh 0".format(password), shell=True)
                        subprocess.call("echo {} | sudo -S sh bashTurn.sh 500".format(password), shell=True)
                        self.sensor_start()
                        rover_socket_movement.send('PACKAGE GOTTEN'.encode('utf-8'))
                        subprocess.call("echo {} | sudo -S sh newForward.sh".format(password), shell=True)
                    elif "ORIGIN REACHED" in msg:
                        subprocess.call("echo {} | sudo -S sh bashWheel.sh 0".format(password), shell=True)
                        subprocess.call("echo {} | sudo -S sh bashTurn.sh 500".format(password), shell=True)
                        break
                    else:
                        subprocess.call("echo {} | sudo -S sh bashTurn.sh {}".format(password, msg), shell=True)
                    print(msg)
            finally:
                rover_socket_movement.close()
                print("***** RoverReceiveMovementClass stop *****")
        except Exception as e:
            password = 'jetson'
            subprocess.call("echo {} | sudo -S sh bashWheel.sh 0".format(password), shell=True)
            subprocess.call("echo {} | sudo -S sh bashTurn.sh 500".format(password), shell=True)
            print(f"***** RoverReceiveMovementClass connection failed {self.server_ip} {str(self.server_port_movement)} *****")
            print(e)
            time.sleep(1)
            print('Reconnecting in:', 5, 'seconds')
            time.sleep(5)
            self.receive_text()
            
    def sensor_start(self):
        GPIO.setmode(GPIO.BOARD)
        PIN_TRIGGER = 16
        PIN_ECHO = 18
        sample_intervals = 1
        count = 0
        print("sensor_start: WAITING FOR USER INPUT")
        while True:
            GPIO.setup(PIN_TRIGGER, GPIO.OUT)
            GPIO.setup(PIN_ECHO, GPIO.IN)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            time.sleep(sample_intervals)
            GPIO.output(PIN_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(PIN_TRIGGER, GPIO.LOW)

            while GPIO.input(PIN_ECHO)==0:
                pulse_start_time = time.time()
            while GPIO.input(PIN_ECHO)==1:
                pulse_end_time = time.time()

            pulse_duration = pulse_end_time - pulse_start_time
            distance = round((pulse_duration * 17150)*0.0328084, 2)
            if distance < 1:
                print ("Distance:",distance,"ft")
                count = count + 1
                if count == 5:
                    print("sensor_start: USER INPUT ACCEPTED")
                    GPIO.cleanup()
                    break
