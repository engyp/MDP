import sys
sys.path.append("..")
import cv2
import numpy as numpy

img1 = cv2.imread('ImagesQuery/up.JPG',0)
img2 = cv2.imread('ImagesTrain/upTrain.JPG',0)

orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

imgKp1 = cv2.drawKeypoints(img1,kp1,None)
imgKp2 = cv2.drawKeypoints(img2,kp2,None)

cv2.imshow('Kp1',imgKp1)
cv2.imshow('Kp2',imgKp2)
cv2.imshow('img1',img1)
cv2.imshow('img2',img2)
cv2.waitKey(0)
