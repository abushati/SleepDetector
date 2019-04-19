from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import time
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
#from bluetoothConnection import Bluetooth
from multiprocessing import Process
import pygame
from BluetoothConnection import Bluetooth
import time


flag = 0

def ROI (image,points):
	
	mask = np.zeros_like(image)
	cv2.fillPoly(mask,points,255)
	masked = cv2.bitwise_and(image,mask)
	return masked

def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear

def playSound(framesSoundOn):
	return
	channel.play(sound)
	# if the number of frames the sound is on for divided by 20 gives a remander of 0, increase the 
	# volume of the alarm.
	if framesSoundOn % 10 == 0:
		soundVolume += .5

def frameChecker(frame_check,framesSoundOn):
    global flag

    if flag >= frame_check:
        print('WWWWWWWAARRRRRMMMMING')

        framesSoundOn += 1
        print('Channel stat' + str(channel.get_busy()))
        communicate.autoSlowDown()
        print('sent slow down')
        flag = 0
        if channel.get_busy() == 0:
            playSound(framesSoundOn)


        cv2.putText(frame, "****************ALERT!****************", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "****************ALERT!****************", (10,325),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)



if __name__=="__main__":
    pygame.init()

#create Bluetooth communicate
    communicate = Bluetooth()


    sound = pygame.mixer.Sound("/home/pi/Camera/danger.wav")
    channel = pygame.mixer.Channel(0)
    #Pool = multiprocessing.Pool
    points = np.array([[150,0],[200,281],[300,281],[350,0]],np.int32)
    
    
    soundVolume = .3
    framesSoundOn = 0 
    testCounter = 0
    thresh = 0.225
    frame_check = 3
    detect = dlib.get_frontal_face_detector()
    predict = dlib.shape_predictor("/home/pi/Camera/shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
    #For PC's only
    #cap=cv2.VideoCapture(0)

    #For PI
    camera = PiCamera()	
    rawCapture = PiRGBArray(camera)
    camera.resolution = (640, 480)
    camera.framerate = 32
    
    while True:
        print('start of main loop')
        moving = communicate.isMoving().decode().strip()
        print(moving)

        
        if moving == 'moving':
       # if True:    
            #print(pygame.mixer.Channel.get_sound())
            print('this is the flag: ' +str(flag))
            #print('it is running')
            #print(f'this is the number of frames sound is on {framesSoundOn} and this is the volume {soundVolume}')
            print ('this is the number of frames sound is on {} and this is the volume {}'.format(str(framesSoundOn),str(soundVolume)))

            #For PC
            #ret, frame=cap.read()

            #For Pi
            frame = camera.capture(rawCapture, format="bgr", use_video_port=True)
            frame = rawCapture.array

            #orginal size of the image is 720 by 1280
            #resizing to 281 by 500
            frame = imutils.resize(frame, width=500)
			
			
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detects all the faces that are capture by the camera
            # and it returns the position of the faces,rectangles[[(120, 37) (245, 162)]]

            #pick the area of interest
            gray = ROI(gray,[points])


            subjects = detect(gray , 1)
            print(' this is the len of subjects '+str(len(subjects)))            #this is returned ----> [rectangle(187,104,294,211)]


            # if a face is not detected, increase the flag

            #if len(subjects) == 0:
                #print('there is no face detected ')
                #flag += 1
                #frameChecker(frame_check,framesSoundOn)
                #rawCapture.truncate(0)
                #continue

            #for each face that is detected in the frame, perfrom this 
            #for loop
            #print('not cont')
            for subject in subjects:

                #this predicts all the different facial landmarks
                shape = predict(gray, subject)
                #print (time.time()-last_time)
                shape = face_utils.shape_to_np(shape)
                #converts the landmarks detected into an array
                #shape = Pool.map(face_utils.shape_to_np(shape))


                #last_time = time.time()

                '''
                [[130  76]
                [132  97]
                [135 116]
                [140 136]
                '''

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                #print("--------------")
                #print(leftEye,rightEye)
                """
                P1-P6 x-y coordinates for the left eye
                [[283 155]
                    [289 150]
                    [297 151]
                    [303 155]
                    [297 156]
                    [290 156]] 
                P1-P6 x-y coordinates for the right eye
                    [[226 153]
                    [234 149]
                    [242 149]
                    [249 154]
                    [242 154]
                    [234 154]]
                """
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye) 
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 255), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
     
                if ear < thresh:
                    print('ear is gearter the thresh')
                    print(ear)
                    flag += 1
                    #print (flag)
                    frameChecker(frame_check,framesSoundOn)
                else:
                    flag = 0

                #This will run if the rccar is not trigger to slowdown
                #we dont need to send the signal multiple times
     #           elif flag > 0 and not communicate.slowDownTrigger:
      #              communicate.autoSlowDown()
       #             flag = 0
                
                
 #               else:
  #                  #if the drivers eyes are open and the alarm is on, turn it off
   #                 if channel.get_busy() == 1:
    #                    channel.stop()

                    flag = 0
            cv2.imshow('image', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            rawCapture.truncate(0)
