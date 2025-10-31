import cv2
import numpy as np
from application.entities.yolo import Yolo

yolo = Yolo()

image = cv2.imread("image-1.jpg")
x, y, w, h = cv2.selectROI("Selecionar ROI", image)

cv2.destroyWindow("Selecionar ROI")

cropped = image[y : y + h, x : x + w]

image_test = np.zeros_like(image)

image_test[y : y + h, x : x + w] = cropped

cv2.imshow("Imagem original", image)

cv2.imshow("Recorte", cropped)

cv2.imshow("Recorte na imagem preta", image_test)

label, cls_label, conf, box, filename = yolo.predict(cropped)
print(yolo.predict(cropped))

box = box.int().tolist()
cv2.circle(
    image, (box[0] + x, box[1] + y), radius=1, thickness=2, color=(255, 255, 255)
)

cv2.circle(cropped, (box[0], box[1]), radius=1, thickness=2, color=(255, 255, 255))

cv2.imshow("Imagem original", image)
cv2.imshow("Recorte", cropped)
cv2.waitKey(0)

cv2.destroyAllWindows()
