from handpose_id import HandGest
import time

def main():

    init = HandGest()


    while True:
        if init.set_handDetected():
            time.sleep(0.1)
            poseID = init.getClassID()

        print(poseID)



if __name__ == "__main__":
    main()

    

#def motor_cmd(poseID):


    #if poseID == 2:
        #go = "g"
    #print(go + "Driving forward")


    #motor_cmd(poseID)



    








