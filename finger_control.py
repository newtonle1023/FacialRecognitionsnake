import cv2
import numpy as np
import copy
import math


class FingerControls:
	def __init__(self, args):
		self.args = args
		self.cap_region_x_begin=0.5 
		self.cap_region_y_end=0.8 
		self.threshold = 60	 
		self.blurValue = 41	 
		self.bgSubThreshold = 50
		self.learningRate = 0
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.camera = cv2.VideoCapture(0)
		self.camera.set(10,200)
		self.isBgCaptured = 0	# bool, whether the background captured
		self.triggerSwitch = False	# if true, keyborad simulator works
		self.setupCam()
		self.camLoop()

	def getArg(self):
		return self.args[0]

	def setArg(self, val):
		self.args[0] = val

	def FindDistance(self, A,B): 
		return np.sqrt(np.power((np.absolute(A[0]-B[0])),2) + np.power(np.absolute((A[1]-B[1])),2)) 

	def removeBG(self, frame):
		fgmask = self.bgModel.apply(frame,learningRate=0)
		# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
		# res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
		kernel = np.ones((3, 3), np.uint8)
		fgmask = cv2.erode(fgmask, kernel, iterations=1)
		res = cv2.bitwise_and(frame, frame, mask=fgmask)
		return res

	def calculateFingers(self, res,drawing):  # -> finished bool, cnt: finger count
		#  convexity defect
		hull = cv2.convexHull(res, returnPoints=False)
		points = []
		if len(hull) > 3:
			defects = cv2.convexityDefects(res, hull)
			if type(defects) != type(None):	 # avoid crashing.	 (BUG not found)
				cnt = 0
				for i in range(defects.shape[0]):
					s, e, f, d = defects[i, 0]
					end = tuple(res[e][0])
					points.append(end)
				return True, cnt
			return False, 0

	def setupCam(self):
		self.bgModel = cv2.createBackgroundSubtractorMOG2(0, self.bgSubThreshold)

	def camLoop(self):
		while self.camera.isOpened():
			ret, frame = self.camera.read()
			img = self.removeBG(frame)
			img = img[0:int(self.cap_region_y_end * frame.shape[0]),
						int(self.cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
			cv2.imshow('test', img)

			# convert the image into binary image
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			blur = cv2.GaussianBlur(gray, (self.blurValue, self.blurValue), 0)
			ret, thresh = cv2.threshold(blur, self.threshold, 255, cv2.THRESH_BINARY)

			# get the coutours
			thresh1 = copy.deepcopy(thresh)
			contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			length = len(contours)
			maxArea = -1
			if length > 0:
				for i in range(length):	 # find the biggest contour (according to area)
					temp = contours[i]
					area = cv2.contourArea(temp)
					if area > maxArea:
						maxArea = area
						ci = i
				res = contours[ci]
				hull = cv2.convexHull(res)
				drawing = np.zeros(img.shape, np.uint8)
				cx, cy = 0, 0
				M = cv2.moments(hull)
				if(M['m00'] != 0):
					cx = M['m10']/M['m00']
					cy = M['m01']/M['m00']
				centroid = (int(cx),int(cy))
				cv2.putText(drawing, 'Center', centroid, self.font, 2, (255,255,0) ,2)
				#get all points from contour hull, append them to the list probable fingertips::
				finger = []
				for i in range(0, len(hull) - 1):
					finger.append(hull[i][0])
				indexFinger = []
				max = self.FindDistance(finger[0], centroid)

				#getting the extrema in the convex Hull, furthest away from the contour centroid::
				for i in range(1,len(finger)):
					if (self.FindDistance(finger[i], centroid) > max):
						indexFinger = finger[i]
						max = self.FindDistance(finger[i], centroid)
				indexFinger = np.array(indexFinger, np.uint16)
				if(len(indexFinger) > 0):
					tipAndCenterEuclidean = np.sqrt(np.power(indexFinger[0] - centroid[0], 2) + np.power(indexFinger[1] - centroid[1], 2))
					print(tipAndCenterEuclidean)
					if(tipAndCenterEuclidean < 90):
						cv2.putText(drawing,'Fist Closed',(100,100),self.font,2,(0,0,255),2)  
					else:
						if(indexFinger[0] - centroid[0] > 60):							
							cv2.putText(drawing,'Right',(100,100),self.font,2,(0,0,255),2)
							self.setArg(0)
						elif (indexFinger[0] - centroid[0] < -60):
							cv2.putText(drawing,'Left',(100,100),self.font,2,(0,0,255),2)
							self.setArg(2)
						elif(indexFinger[1] - centroid[1] > 60):						  
							cv2.putText(drawing,'Down',(100,100),self.font,2,(0,0,255),2)
							self.setArg(1)
						elif(indexFinger[1] - centroid[1] < -60):						   
							cv2.putText(drawing,'Up',(100,100),self.font,2,(0,0,255),2)
							self.setArg(3)
						cv2.circle(frame, tuple(indexFinger),5,(0,0,255),-1)


				cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
				cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

				isFinishCal,cnt = self.calculateFingers(res, drawing)
				if self.triggerSwitch is True:
					if isFinishCal is True and cnt <= 2:
						print (cnt)