import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import threading


class HandGest():

    def __init__(self):

        self.classID = 0

        

        # initialize mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        self.model = load_model('mp_hand_gesture')

        # Load class names
        self.f = open('gesture.names', 'r')
        self.classNames = self.f.read().split('\n')
    
        self.f.close()

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)


        # Configure thread
        loop_thread = threading.Thread(target=self.loop, args=())
        
        # Start thread
        loop_thread.start()

        # Initialize variables
        self.hand_detected = 'test'
        self.detection = 'init'

    # 
    def getClassID(self):
        #self.classID
        return  self.classID

    def is_detected(self):
        detection = 'is detection'
        return 'is detected'

    def not_detected(self):
        detection = 'not detected'
        return detection

    def set_handDetected(self):
        if self.hand_detected == 'hand':
            #print("Function reading --- WORKING")
            self.detection = self.is_detected()
        else:
            self.detection = self.not_detected()
        return self.detection

    
        #print(self.classID)

    def __del__(self):
        # release the webcam and destroy all active windows
        self.cap.release()

        cv2.destroyAllWindows()
        

    def loop(self):
        while True:
            # Read each frame from the webcam
            _, frame = self.cap.read()

            x, y, c = frame.shape

            # Flip the frame vertically
            frame = cv2.flip(frame, 1)
            framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Get hand landmark prediction
            result = self.hands.process(framergb)

            # print(result)
            
            className = ''
        
                
        
            # post process the result
            if result.multi_hand_landmarks:

                self.hand_detected = 'hand'
                #print(self.hand_detected)
                #detect.set_handDetected()

                
                # detect = HandGest('hand_detected')
                # print(detect)
                #print('Hand Detected')
                landmarks = []
                for handslms in result.multi_hand_landmarks:
                    
                    for lm in handslms.landmark:
                    
                        #print(id, lm)
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)

                        landmarks.append([lmx, lmy])

                    # Drawing landmarks on frames
                    self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)

                    # Predict gesture
                    prediction = self.model.predict([landmarks])
                    #print(prediction[0,6])
                    #print(prediction[0])
                    #print(prediction[0,0:20])
                    #print(prediction[0,11:21])


                    self.classID = np.argmax(prediction)
                    
                    # self.classID = np.argmax(prediction, a]xis=1)
                    
                    #print(self.classID)
                    
                
                    
                    className = self.classNames[self.classID]
                    # print("hand detected --- 4")

                    #print(classID)
            else:
                self.hand_detected = 0

            # show the prediction on the frame
            cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA)

            # Show the final output
            cv2.imshow("Output", frame)

            if cv2.waitKey(1) == ord('q'):
                break