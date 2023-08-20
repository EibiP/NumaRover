# RoverSendWebcam
import cv2
import imutils
import pickle
import socket
import struct
import threading

class TestWebcamRover(threading.Thread):

    rover_ip = '127.0.0.1'
    rover_port = 50001
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.send_webcam()

    def send_webcam(self):
        try:
            rover_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            rover_socket.bind((self.rover_ip, self.rover_port))
            print("********** Rover IP:", self.rover_ip, "Port:", self.rover_port, "**********")
            rover_socket.listen(1)
            print("********** Listening... **********")

            while True:
                server_socket, addr = rover_socket.accept()
                print("********** Connected:", addr, "**********")
                if server_socket:
                    vid = cv2.VideoCapture(0)
                    
                    while vid.isOpened():
                        img, frame = vid.read()
                        frame = imutils.resize(frame, width=480)
                        a = pickle.dumps(frame)
                        message = struct.pack('Q', len(a)) + a
                        server_socket.sendall(message)
                        
                        cv2.imshow("********** Sending Rover Video **********", frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            server_socket.close()
        finally:
            rover_socket.close()
            print("********** Stop Sending Rover Video **********")


if __name__ == "__main__":
    rsw = TestWebcamRover()
    rsw.send_webcam()
