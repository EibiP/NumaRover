import time
import cv2
import pickle
import socket
import struct
import threading
import torch
import numpy as np

from PIL import Image
from tensorflow import keras
from PIL import Image, ImageOps


class NewPrimaryServerCode():

    rover_ip = '0.0.0.0'
    server_ip = '0.0.0.0'
    rover_port_webcam_movement = 0
    server_port_movement = 0
    origin = ""
    destination = ""
    drive_model_name = ""
    checkpoint_model_name = ""
    checkpoint_passed = set()
    is_pass_dest = False

    def __init__(self, rover_ip, server_ip, rover_port_webcam_movement, server_port_movement, origin, destination, drive_model_name, checkpoint_model_name):
        threading.Thread.__init__(self)
        self.rover_ip = rover_ip
        self.server_ip = server_ip
        self.rover_port_webcam_movement = rover_port_webcam_movement
        self.server_port_movement = server_port_movement
        self.origin = origin
        self.destination = destination
        self.drive_model_name = drive_model_name
        self.checkpoint_model_name = checkpoint_model_name

    def run(self):
        self.receive_webcam()

    def receive_webcam(self):
        try:
            drive_model = keras.models.load_model(self.drive_model_name)
            checkpoint_model = torch.hub.load('yolov7', 'custom', self.checkpoint_model_name, source='local')
            server_socket_webcam_movement = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket_webcam_movement.connect((self.rover_ip, self.rover_port_webcam_movement))
            data = b""
            payload_size = struct.calcsize("Q")
            print("****** Connecting to Rover IP:", self.rover_ip, "Port:", self.rover_port_webcam_movement, "*****")

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.server_ip, self.server_port_movement))
            server_socket.listen(1)
            print("***** Listening Server IP:", self.server_ip, "Port:", self.server_port_movement, "*****")
            rover_socket, addr = server_socket.accept()
            print("Connected:", addr)
            msg = rover_socket.recv(1024).decode('utf-8')
            print(msg)

            while server_socket_webcam_movement:
                while len(data) < payload_size:
                    packet = server_socket_webcam_movement.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack('Q', packed_msg_size)[0]

                while len(data) < msg_size:
                    data += server_socket_webcam_movement.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)

                # **************************************************
                t1 = threading.Thread(target=self.predict_movement, args=(drive_model, frame, rover_socket))
                t2 = threading.Thread(target=self.checkpoint_position, args=(checkpoint_model, frame))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
                
                if self.is_pass_dest == False:
                    if self.destination in self.checkpoint_passed:
                        rover_socket.send("DESTINATION REACHED".encode('utf-8'))
                        break_msg = rover_socket.recv(1024).decode('utf-8')
                        if break_msg == "PACKAGE GOTTEN":
                            self.is_pass_dest = True
                            self.checkpoint_passed.clear()
                            print("")
                else:
                    if self.origin in self.checkpoint_passed:
                        rover_socket.send("ORIGIN REACHED".encode('utf-8'))
                        break

                cv2.imshow("PrimaryServerCode", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # time.sleep(1)
                # **************************************************

            rover_socket.close()
            server_socket.close()
            server_socket_webcam_movement.close()
            cv2.destroyAllWindows()
            print("***** NewPrimaryServerCode stop *****")
        except Exception as e:
            print(e)
            print('***** NewPrimaryServerCode connection failed *****')
            time.sleep(1)
            print('Reconnecting in:', 5, 'seconds')
            time.sleep(5)
            self.receive_webcam()
    
    def checkpoint_position(self, checkpoint_model, frame):
        results = checkpoint_model(frame)
        if results.pandas().xyxy[0]['name'].size > 0:
            # print(type(results.pandas().xyxy[0]['confidence'][0]))
            first_detect = results.pandas().xyxy[0]['name'][0]
            if first_detect not in self.checkpoint_passed:
                self.checkpoint_passed.add(first_detect)
                print(first_detect)

    def predict_movement(self, drive_model, frame, rover_socket):
        image = frame
        image = self.preprocess(image)
        output = drive_model.predict(image, verbose = 0)
        # print(output[0][0])
        output = float(output[0][0])
        adjust_val = (((output + 1) * 300) / 2) + 350
        adjust_val = str(round(adjust_val))
        rover_socket.send(adjust_val.encode('utf-8'))

    def preprocess(self, img):
        # images = [np.asarray(Image.fromarray(img).resize([256, 256]), dtype='float32') / 255]
        images = np.asarray(ImageOps.grayscale(Image.fromarray(img)).resize([256,256]), dtype = 'float32')/255
        images = np.asarray(images)
        images = images.reshape(-1, 256, 256, 1)
        return images


if __name__ == "__main__":
    rover_ip = '192.168.1.3'
    server_ip = '192.168.1.4'
    rover_port_webcam_movement = 50002
    server_port_movement = 50004
    origin = "Checkpoint 1"
    destination = "Checkpoint 3"
    drive_model_name = "model_2"
    checkpoint_model_name = "best.pt"
    ssm = NewPrimaryServerCode(rover_ip, server_ip, rover_port_webcam_movement, server_port_movement, origin, destination, drive_model_name, checkpoint_model_name)
    ssm.run()
