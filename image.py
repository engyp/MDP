import cv2
import numpy as numpy

img1 = cv2.imread('ImagesQuery/up.JPG')
img2 = cv2.imread('ImagesTrain/upTrain.JPG')

cv2.imshow('img1',img1)
cv2.imshow('img2',img2)
cv2.waitKey(0)