import cv2
import sys

class CameraDaemon:
	def __init__(self, args):
		self.args = args
		self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
		self.eyes_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
		self.first_read = True
		self.cap = cv2.VideoCapture(0)
		self.ret, self.image = self.cap.read()
		self.cameraLoop()

	def getArg(self):
		return self.args[0]

	def setArg(self, val):
		self.args[0] = val

	def cameraLoop(self):
		while self.ret:
			# this will keep the web-cam running and capturing the self.image for every loop
			self.ret, self.image = self.cap.read()
			# Convert the recorded self.image to grayscale
			gray_scale = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
			# Applying filters to remove impurities
			gray_scale = cv2.bilateralFilter(gray_scale, 5, 1, 1)
			# to detect face and eye
			faces = self.face_cascade.detectMultiScale(gray_scale, 1.3, 5, minSize=(100, 100))
			if len(faces) > 0:
				for (x, y, w, h) in faces:
					image = cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
					# eye_face var will be i/p to eye classifier
					eye_face = gray_scale[y:y + h, x:x + w]
					# self.image
					eye_face_clr = self.image[y:y + h, x:x + w]
					# get the eyes
					eyes = self.eyes_cascade.detectMultiScale(eye_face, 1.3, 5, minSize=(50, 50))
					if len(eyes) >= 2:
						if self.first_read:
							cv2.putText(image, "Eye's detected, press s to check blink", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
										1, (0, 255, 0), 2)
						else:
							cv2.putText(image, "Eye's Open", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
										1, (255, 255, 255), 2)
					else:
						if self.first_read:
							cv2.putText(image, "No Eye's detected", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
										1, (255, 255, 255), 2)
						else:

							cv2.putText(image, "Blink Detected.....!!!!", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
										1, (0, 255, 0), 2)
							cv2.imshow('image', self.image)
							cv2.waitKey(1)
							self.setArg(True)
							print("Blink detected......!!!")
					print("I am a fraud" if self.getArg() else "I am not a fraud")
			else:
				cv2.putText(self.image, "No Face Detected.", (70, 70), cv2.FONT_HERSHEY_SIMPLEX,
							1, (0, 255, 0), 2)
			cv2.imshow('image', self.image)
			
			a = cv2.waitKey(1)
			# press q to Quit and S to start
			# ord(ch) returns the ascii of ch
			if a == ord('q'):
				self.cap.release()
				cv2.destroyAllWindows()
				sys.exit(1);
			elif a == ord('s'):
				self.first_read = False
				self.setArg(False)