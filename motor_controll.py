from handpose_id import HandGest
import time

init = HandGest()

while True:
        detecting = init.set_handDetected()
        time.sleep(10)

        if detecting == "is detected":


            class motor_cmd():

                def __init__(self):


                    # Initialize class variables
                    self.poseID = init.getClassID()

                    self.cmd_forward = 0
                    self.cmd_reverse = 0
                    self.cmd_stop = 0
                    self.cmd_output = 0


                def forward(self):

                    if self.poseID == 2 and 9:
                        self.cmd_forward = "s"
                    return self.cmd_forward

                def reverse(self):
                    if self.poseID == 3:
                        self.cmd_reverse = "s"
                    return self.cmd_reverse

                def stop(self):
                    if self.poseID == 7 and 5:
                        self.cmd_stop = "s"
                    return self.cmd_stop
            

            test = motor_cmd()
            #print(test.forward())
            #print(test.reverse())
            #print(test.stop())
    #print(test.startDetection())



                

