import cv2
import torch
import numpy as np

# model = torch.hub.load('yolov7', 'custom', 'best.pt', source='local') 
model = torch.hub.load('yolov7', 'custom', 'yolov7.pt', source='local') 
vid = cv2.VideoCapture(0)

checkpoint_passed = set()

while vid.isOpened():
    ret, frame = vid.read()
    results = model(frame)
    if results.pandas().xyxy[0]['name'].size > 0:
        first_detect = results.pandas().xyxy[0]['name'][0]
        if first_detect not in checkpoint_passed:
            checkpoint_passed.add(first_detect)
            print(first_detect)
    cv2.imshow("SimpleYoloWebcam", np.squeeze(results.render()))
    # break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

vid.release()
cv2.destroyAllWindows()
