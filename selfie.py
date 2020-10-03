from scipy.spatial import distance as dist
from imutils.video import VideoStream, FPS
from imutils import face_utils
import imutils
import numpy as np
import time
import dlib
import cv2
import os
from datetime import datetime

def smile(mouth):
    corner_A = dist.euclidean(mouth[3], mouth[9])
    corner_B = dist.euclidean(mouth[2], mouth[10])
    corner_C = dist.euclidean(mouth[4], mouth[8])
    avg = (corner_A + corner_B + corner_C)/3
    corner_D = dist.euclidean(mouth[0], mouth[6])
    ratio = avg / corner_D
    return ratio

def selfie():
    
    save_folder = 'selfies'
    try:
        os.mkdir(save_folder)
    except OSError as os_e:
        pass

    count = 0
    current_time = 0

    shape_predictor = 'data/shape_predictor_68_face_landmarks.dat' 
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    (mouth_start, mouth_end) = face_utils.FACIAL_LANDMARKS_IDXS['mouth']

    vs = VideoStream(src=0).start()
    fileStream = False
    time.sleep(1.0)

    fps= FPS().start()
    cv2.namedWindow('test')

    while True:
        frame = vs.read()
        frame = imutils.resize(frame, width=450, height=300)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        anchors = detector(gray, 0)
        for anchor in anchors:
            landmark = predictor(gray, anchor)
            landmark = face_utils.shape_to_np(landmark)
            mouth = landmark[mouth_start:mouth_end]
            ratio = smile(mouth)
            mouthHull = cv2.convexHull(mouth)
            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
        
            if ratio >= .2 and ratio < .25 :
                count += 1
            else:
                if count >= 15:
                    current_time = datetime.now().strftime('%b %d, %Y %Hh%Mm%Ss')
                    frame = vs.read()
                    time.sleep(.3)
                    frame2= frame.copy()
                    img_name = '{}.png'.format(current_time)
                    cv2.imwrite(os.path.join(save_folder, img_name), frame)
                    print('{} written!'.format(img_name))
                count = 0

            cv2.putText(frame, 'MAR: %.2f' % (ratio), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.imshow('Frame', frame)
        fps.update()

        key2 = cv2.waitKey(1) & 0xFF
        if key2 == ord('q'):
            break

    fps.stop()

    cv2.destroyAllWindows()
    vs.stop()

if __name__ == '__main__':
    selfie()