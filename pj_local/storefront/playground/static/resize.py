import cv2

img=cv2.imread("004-alert.png")
im2=cv2.resize(img,(100,100),interpolation=cv2.INTER_AREA)
cv2.imwrite("alert2.png", im2)