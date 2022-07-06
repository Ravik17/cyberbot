import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model
import threading


class HandGest():

    def __init__(self):

        self.classID_1 = 0
        self.classID_2 = 0

        # initialize mediapipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils

        # Load the gesture recognizer model
        self.model = load_model('mp_hand_gesture')

        # Load class names
        self.f = open('gesture.names', 'r')
        self.classNames_1 = self.f.read().split('\n')
        self.classNames_2 = self.f.read().split('\n')
        self.f.close()

        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)


        # Configure thread
        loop_thread = threading.Thread(target=self.loop, args=())
        
        # Start thread
        loop_thread.start()

    #def getClassID(self):
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
            
            className_1 = ''
            className_2 = ''

            # post process the result
            if result.multi_hand_landmarks:
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


                    self.classID_1 = np.argmax(prediction)
                    self.classID_2 = np.argmax(prediction)
                    # self.classID = np.argmax(prediction, a]xis=1)
                    
                    print(self.classID_1)
                    
                    print(self.classID_2)

                    # ghosthand = np.argmax(prediction, axis=0)
                    # print(ghosthand)
                    
                    className_1 = self.classNames_1[self.classID_1]
                    className_2 = self.classNames_2[self.classID_2]

                    #print(classID)

            # show the prediction on the frame
            cv2.putText(frame, className_1, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (0,0,255), 2, cv2.LINE_AA)

            # Show the final output
            cv2.imshow("Output", frame) 

            if cv2.waitKey(1) == ord('q'):
                break
