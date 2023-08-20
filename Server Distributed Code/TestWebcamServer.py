# ServerReceiveWebcam
import time
import cv2
import pickle
import socket
import struct
import threading


class TestWebcamServerClass(threading.Thread):

    rover_ip = '127.0.0.1'
    rover_port = 50001
    time_to_reconnect = 5

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.receive_webcam()

    def receive_webcam(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((self.rover_ip, self.rover_port))
            data = b""
            payload_size = struct.calcsize("Q")
            print("********** Connecting to Rover IP:", self.rover_ip, "Port:", self.rover_port, "**********")
        except:
            print('********** Connecting to rover webcam failed **********')
            time.sleep(1)
            for i in range(self.time_to_reconnect):
                print('***** Reconnecting in:', (self.time_to_reconnect-i), '*****')
                time.sleep(1)
            print('********** Reconnecting... **********')
            time.sleep(1)
            self.receive_webcam()

        try:
            while True:
                while len(data) < payload_size:
                    packet = server_socket.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack('Q', packed_msg_size)[0]

                while len(data) < msg_size:
                    data += server_socket.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("********** Getting Rover Video **********", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            server_socket.close()
            print("********** Stop Receiving Rover Video **********")


if __name__ == "__main__":
    srw = TestWebcamServerClass()
    srw.receive_webcam()
