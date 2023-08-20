import time
import RoverSendWebcam as rsw
import RoverReceiveMovement as rrm

rover_ip = '192.168.1.3'
server_ip = '192.168.1.4'
rover_port_webcam_movement = 50002
server_port_movement = 50004

if __name__ == "__main__":
    t2 = rsw.RoverSendWebcamClass(rover_ip, rover_port_webcam_movement)
    t4 = rrm.RoverReceiveMovementClass(server_ip, server_port_movement)
    thread_list = [t2, t4]
    for threads in thread_list:
        threads.daemon = True
    for threads in thread_list:
        threads.start()
    try:
        while True:
            if not t4.is_alive():
                t2.kill()
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("********** STOPPING PrimaryRoverCode.py **********")

