
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
from flask import Flask, render_template, Response
from test import video


app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming"""
    return render_template('index.html')

def gen(test):
        video1 = video()
        detect = dlib.get_frontal_face_detector()
        predict = dlib.shape_predictor("/home/pi/Camera/shape_predictor_68_face_landmarks.dat")
        #file path on pi /home/pi/Camera/shape_predictor_68_face_landmarks.dat
        # Dat file is the crux of the code
        flag=0
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
        
        for frames in video1.camera.capture_continuous(video1.rawCapture, format="bgr", use_video_port=True):
                frame = frames.array
                #ret, frame  = video1.camera.read()
                frame = imutils.resize(frame, width=450)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                subjects = detect(gray, 0)
                for subject in subjects:
                        shape = predict(gray, subject)
                        shape = face_utils.shape_to_np(shape)
                        #converting to NumPy Array
                        leftEye = shape[lStart:lEnd]
                        rightEye = shape[rStart:rEnd]
                        leftEAR = video1.eye_aspect_ratio(leftEye)
                        rightEAR = video1.eye_aspect_ratio(rightEye)
                        ear = (leftEAR + rightEAR) / 2.0
                        leftEyeHull = cv2.convexHull(leftEye)
                        rightEyeHull = cv2.convexHull(rightEye) 
                        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                        if ear < video1.thresh:
                                flag += 1
                        print (flag)
                        if flag >= video1.frame_check:
                                cv2.putText(frame, "****************ALERT!****************", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                                cv2.putText(frame, "****************ALERT!****************", (10,325),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        #print ("Drowsy")
                        else:
                                flag = 0
                #
            #cv2.imshow('frame',frame)
                #cv2.imwrite('t.jpg', frame)
                ret, jpeg = cv2.imencode('.jpg', frame)
                uploadFrame = jpeg.tobytes()
                video1.rawCapture.truncate(0)
           
        #thisFrame = video1.updatedFrame()
        #yield expression is directly sent to the browser
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + uploadFrame + b'\r\n')#open('t.jpg', 'rb').read()
        #opens the saved jpg file

        
        #yield expression is directly sent to the browser
        yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #opens the saved jpg file


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	app.run(host="0.0.0.0")