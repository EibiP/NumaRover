import cv2
import imutils
import pickle
import socket
import struct
import threading

class RoverSendWebcamClass(threading.Thread):
    
    rover_ip = '0.0.0.0'
    rover_port_webcam = 0
    
    def __init__(self, rover_ip, rover_port_webcam):
        threading.Thread.__init__(self)
        self.rover_ip = rover_ip
        self.rover_port_webcam = rover_port_webcam
    
    def kill(self):
        self.killed = True

    def run(self):
        self.send_webcam()

    def send_webcam(self):
        try:
            rover_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rover_socket.bind((self.rover_ip, self.rover_port_webcam))
            rover_socket.listen()
            print("***** Listening Rover IP:", self.rover_ip, "Port:", self.rover_port_webcam, "*****")
            
            server_socket, addr = rover_socket.accept()
            print("Connected:", addr)
            
            vid = cv2.VideoCapture(0)
            while vid.isOpened():
                img, frame = vid.read()
                frame = imutils.resize(frame, width=360)
                a = pickle.dumps(frame)
                message = struct.pack('Q', len(a)) + a
                server_socket.sendall(message)
        except Exception as e:
            print("***** BREAK INFO Rover IP:", self.rover_ip, "Port:", self.rover_port_webcam, "*****")
            print(e)
        finally:
            rover_socket.close()
            print("***** Closing Rover IP:", self.rover_ip, "Port:", self.rover_port_webcam, "*****")
