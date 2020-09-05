import sys
sys.path.append("..")
import cv2
import numpy as numpy

img1 = cv2.imread('ImagesQuery/up.JPG',0)
img2 = cv2.imread('ImagesTrain/upTrain.JPG',0)

orb = cv2.ORB_create(nfeatures=1000)

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# imgKp1 = cv2.drawKeypoints(img1,kp1,None)
# imgKp2 = cv2.drawKeypoints(img2,kp2,None)

# imgKp1 = img1.copy()
# for marker in kp1:
# 	imgKp1 = cv2.drawMarker(imgKp1, tuple(int(i) for i in marker.pt), color=(0, 255, 0))

# imgKp2 = img2.copy()
# for marker in kp2:
# 	imgKp2 = cv2.drawMarker(imgKp2, tuple(int(i) for i in marker.pt), color=(0, 255, 0))

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
	if m.distance < 0.75*n.distance:
		good.append([m])
print(len(good))
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)

# cv2.imshow('Kp1',imgKp1)
# cv2.imshow('Kp2',imgKp2)
cv2.imshow('img1',img1)
cv2.imshow('img2',img2)
cv2.imshow('img3',img3)
cv2.waitKey(0)
