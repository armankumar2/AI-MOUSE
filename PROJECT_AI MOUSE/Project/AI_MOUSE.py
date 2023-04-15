# Imported Libraries....
import cv2 # This libray is use to access the camera and to do the tweaks on the camera.
import time # This library helps to get the all types of time related things here use to show the fps
import hand_tracking_module as htm # This library helps to track the hand movement and helps in hand-gesture recognition
import pyautogui # This library helps to do the task of giving the size of system screen.
import numpy as np # This library helps in making arrays,and give the correct measures
import mouse # This library helps to control the mouse functions i.e. to click , left-right-double click , drag and drop , etc.\import threading
import threading
#_________________________________________ACCESSING CAMERA_____________________________________

pTime = 0 # Previous Time

plocX , plocY = 0,0 # Previous loc
clocX , clocY = 0,0 # Current loc

#______ ><________

W = 640 # Shows the width
H = 360 # Shows the height

#_______________________________________LEFT , RIGHT AND DOUBLE CLICK DELAY___________________________________________________

l_delay = 0

def l_clk_delay():
    global l_delay
    global l_clk_thread

    time.sleep(1)
    l_delay = 0
    l_clk_thread = threading.Thread(target=l_clk_delay)

l_clk_thread = threading.Thread(target=l_clk_delay)


r_delay = 0

def r_clk_delay():
    global r_delay
    global r_clk_thread

    time.sleep(1)
    r_delay = 0
    r_clk_thread = threading.Thread(target=r_clk_delay)

r_clk_thread = threading.Thread(target=r_clk_delay)


double_delay = 0

def double_clk_delay():
    global double_delay
    global double_clk_thread

    time.sleep(2)
    double_delay = 0
    double_clk_thread = threading.Thread(target=double_clk_delay)

double_clk_thread = threading.Thread(target=double_clk_delay)





frameR = 100 #Frame Reduction
smoothning = 5 # It helps to smoothen the hand gesture.
cap = cv2.VideoCapture(0) # It help to access the main and primary camera
cap.set(3,W) # It sets the value and adjustment of camera for width
cap.set(4,H) # It sets the value and adjusment of camera for height
detector = htm.handDetector(maxHands=1) # it helps to detect the hand max is 1 so 1 hand will be controlled.
wScr,hScr = pyautogui.size() # It gives the width and height of the system(Lappy,Comp.) screen.
# print(wScr,hScr)
while True : # It starts looping so that camera never ends until and unless the user destroy the whole window.
    sucess , IMG = cap.read() # It reads the camera and show us in computer screen.

#_____________________________________________HAND TRACKING________________________________________
    # IMG = cv2.flip(IMG,1) # It helps to flip the camera so that AI detect the right positions.
    IMG = detector.findHands(IMG) # It detects the hand movement in image I mean real view.
    lmList,bbox = detector.findPosition(IMG) # It helps to find the position of image I mean real view.
    
#___________________________________TO GET THE TIP OF INDEX AND MIDDLE FINGER_______________________

    if len(lmList) != 0 : # It checks the position to get the tip info

        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]
        x4,y4 = lmList[4][1:]

        # print(x1,y1,x2,y2)

#_____________________________________CHECK WITH FINGERS UP__________________________________

        fingers = detector.fingersUp() # Now it helps to detect the fingers
        Totalfingers = fingers.count(1)
        print(fingers)

        #____________________________MAKING BOUNDARY______________________________________

        cv2.rectangle(IMG, (frameR , frameR), (W-frameR , H-frameR) , (255,0,255), 2) # Makes a rect. boundary for right positions

#_______________________________________ONLY INDEX FINGER_____________________________________

        if fingers[1]== 1 and fingers[2] == 0: # It is true only for index finger.

            #__________________CONVERT COORDINATES______________________________________

            x3 = np.interp(x1, (frameR,W-frameR),(0,wScr)) # It gives the x coordinate of I.F.
            y3 = np.interp(y1, (frameR,H-frameR),(0,hScr)) # It gives the y coordinates of I.F.

            #________________SMOOTHNING THE VALUES TO GET BETTER RESULT_________________

            clocX = plocX + (x3 - plocX) / smoothning # It helps to smoothen of cursor in x direction
            clocY = plocY + (y3 - plocY) / smoothning # It helps to smoothen the value of cursor in y direction


            #____________________________TO MOVE THE MOUSE_____________________________

            mouse.move(wScr-clocX,clocY) # It helps to move the cursor
            cv2.circle(IMG, (x1,y1), 15, (255,0,255), cv2.FILLED) # It creates a circle in index finger so that it can be recognisable
            cv2.putText(IMG, str("CURSOR MODE"),(W-490,H-(-40)),cv2.FONT_HERSHEY_PLAIN , 3, (0,0,255),3)

            plocX , plocY = clocX, clocY # It changes the previous locations to the current location.

#_______________________________IF BOTH INDEX AND MIDDLE FINGER UP : CLICK MODE______________________


        # Left Click
        # If Index finger is open and thumb is open it act as a left click
        if fingers[1] == 1 and fingers[2] == 0  and fingers[0] == 1:
            if l_delay == 0 :
                mouse.click(button="left")
                print("left click")
                l_delay = 1
                l_clk_thread.start()
        

        # Right Click
        # if Index finger and pinky finger is open it act as a right click
        if fingers[1] == 1 and fingers[2] == 0  and fingers[4] == 1:
            if r_delay == 0 :
                mouse.click(button="right")
                cv2.putText(IMG, str("RIGHT CLICK"),(W-490,H-(-40)),cv2.FONT_HERSHEY_PLAIN , 3, (0,0,255),3)
                print("right click")
                r_delay = 1
                r_clk_thread.start()

        # Double click
        # if Index, thumb and middle is open it act as a double click
        if fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 1 :
            if abs(x1-x2) < 25 :
                if double_delay == 0 :
                    mouse.double_click(button="left")
                    cv2.putText(IMG, str("DOUBLE CLICK"),(W-490,H-(-40)),cv2.FONT_HERSHEY_PLAIN , 3, (0,0,255),3)
                    print("double click")
                    double_delay = 1
                    double_clk_thread.start()

        #Scroll
        # if the distance b/w index and middle finger is less than 25 it act as a lower scroll
        if fingers[1] == 1 and fingers[2] == 1  :
            if abs(x1-x2) < 25 and fingers[4] == 0 :
                mouse.wheel(delta= -1)
                print("lower scroll")
        # if the distance b/w index and middle finger is less than 25 and pinky finger is open it act as a upper scroll
        if fingers[1] == 1 and fingers[2] == 1 :
            if abs(x1-x2) < 25 and fingers[4] == 1 :
                mouse.wheel(delta= 1)
                print("upper scroll")


        #Drag and for Drop use the left click gesture
        if Totalfingers == 0 :
            print("Drag")
            pyautogui.sleep(1)
            pyautogui.mouseDown(button="left")


#____________________________________________FRAME RATE___________________________________________

    cTime = time.time() # It shows the time for frame rate
    fps = 1/(cTime-pTime) # Fornula to calculate the frame rate.
    pTime = cTime # Changes to previous time to current time.
    cv2.putText(IMG, str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN , 3, (0,0,255),3) # It creates a responsive text for fps in camera screen

    #____________________________________________DISPLAY___________________________________________

    cv2.imshow("AI MOUSE v.2.0", IMG) # It helps to display the heading of software or in simple words name of software.

    if cv2.waitKey(1) == ord("q"): # This checks the camera and wait until the user response.
        break 

  
