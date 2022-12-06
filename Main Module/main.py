from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import requests
import geocoder
import pyautogui
import numpy as np
import time
from playsound import playsound
import boto3
import os
#Message
message1 = "ALERT - Your family member, Oviya, is dozing off. Please contact them!"
message2 = "ALERT - After repetitive warnings, your family member has not responded. Advice to contact emergency services"

#Telegram Aravind
TOKEN = "5880592883:AAG3gvM6dwN45TGkrx9hHvIHKebdrsJ9lnw"
chat_id1 = "333341036"

#Rithvik
TOKEN2 = "5880592883:AAG3gvM6dwN45TGkrx9hHvIHKebdrsJ9lnw"
chat_id2 = "891482248"

url1a = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id1}&text={message1}"
url1b = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id1}&text={message2}"

url2a = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id2}&text={message1}"
url2b = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id2}&text={message2}"


#Location
g = geocoder.ip('me')
lati = 43.0029759
long = -78.7876123

loc1 = f"https://api.telegram.org/bot{TOKEN}/sendlocation?chat_id={chat_id1}&latitude={lati}&longitude={long}"
loc2 = f"https://api.telegram.org/bot{TOKEN}/sendlocation?chat_id={chat_id2}&latitude={lati}&longitude={long}"

#Cloud
s3 = boto3.client('s3')
Direc= "/Users/aravindbalakrishnan/Desktop/CSE 705 Final/Intelligent Driver Safety/images"

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
	


thresh = 0.25
frame_check = 20
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap=cv2.VideoCapture(0)

flag=0

filevar = 1

ctr = 0
fg = 0
while True:
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)
	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		if ear < thresh:
			flag += 1
			
			if flag >= frame_check:
				ctr +=1
				fg +=1
				cv2.putText(frame, "ALERT! WAKE UP", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "ALERT! WAKE UP", (10,325),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				

				playsound('./sound/vibration.wav')

				if fg == 1:
					requests.get(url1a).json()				
					requests.get(url2a).json()


				if ctr%5 == 0:
					image = pyautogui.screenshot()
					image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
					cv2.imwrite(f"./images/image_{filevar}.png", image)
					playsound('./sound/alarm.wav')
					requests.get(url1b).json()
					requests.get(loc1).json()
					requests.get(url2b).json()
					requests.get(loc2).json()
					filevar+=1
					fg = 1							
		else:
			flag = 0
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("p"):
		files = os.listdir(Direc)
		files = [f for f in files if os.path.isfile(Direc+'/'+f)] 
		fileid=0
		for x in files:
			s3.upload_file(
        	Filename=Direc+"//"+x,
        	Bucket="intelligent-driver-safety-system-s3-bucket",
        	Key=""+x,
    )

	if key == ord("q"):
		break
cv2.destroyAllWindows()
cap.release() 








