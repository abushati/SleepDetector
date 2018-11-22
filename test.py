from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
#ssh -R 52698:localhost:52698 pi@192.168.1.15

class video(object):
    def __init__(self):
        #self.camera = cv2.VideoCapture(0)
        
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 60
        self.rawCapture = PiRGBArray(self.camera)
        """Video streaming generator function."""
        self.thresh = 0.25	
        self.frame_check = 20

    def eye_aspect_ratio(self,eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

        

