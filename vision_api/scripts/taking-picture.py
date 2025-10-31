import os
from datetime import datetime

import cv2

folders_name = [
    "images/conical_ring/",
    "images/cuboid/",
    "images/cylinder/",
    "images/dumbbell/",
    "images/hollow-cilinder/",
    "images/round_base_cuboid/",
]

cap = cv2.VideoCapture(2)

ret, frame = cap.read()
roi_coords = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
x, y, w, h = roi_coords

print(x, y, w, h)

for folder_name in folders_name:
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    while True:
        ret, frame = cap.read()

        roi_frame = frame[y : y + h, x : x + w]

        cv2.imshow("ROI Frame", roi_frame)

        key = cv2.waitKey(2)

        if key & 0xFF == ord("q"):
            file_name = f"image_{datetime.now()}.jpg"
            cv2.imwrite(folder_name + file_name, roi_frame)
        if key & 0xFF == ord("e"):
            break

cap.release()
cv2.destroyAllWindows()
