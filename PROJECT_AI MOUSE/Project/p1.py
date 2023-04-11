import cv2
import time
import hand_tracking_module as htm
import pyautogui
import numpy as np
# import autopy
import mouse
#_________________________________________ACCESSING CAMERA_____________________________________

pTime = 0 # Previous Time

plocX , plocY = 0,0 # Previous loc
clocX , clocY = 0,0 # Current loc


#______ ><________

W = 640
H = 360
frameR = 100 #Frame Reduction
smoothning = 5
cap = cv2.VideoCapture(1)
cap.set(3,W)
cap.set(4,H)
detector = htm.handDetector(maxHands=1)
wScr,hScr = pyautogui.size()
# print(wScr,hScr)
while True :
    sucess , IMG = cap.read()

#_____________________________________________HAND TRACKING________________________________________
    IMG = cv2.flip(IMG,1)
    IMG = detector.findHands(IMG)
    lmList,bbox = detector.findPosition(IMG)
    
#___________________________________TO GET THE TIP OF INDEX AND MIDDLE FINGER_______________________

    if len(lmList) != 0 :

        x1,y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        # print(x1,y1,x2,y2)

#_____________________________________CHECK WITH FINGERS UP__________________________________

        fingers = detector.fingersUp()
        # print(fingers)

        #____________________________MAKING BOUNDARY______________________________________

        cv2.rectangle(IMG, (frameR , frameR), (W-frameR , H-frameR) , (255,0,255), 2)

#_______________________________________ONLY INDEX FINGER_____________________________________

        if fingers[1]== 1 and fingers[2] == 0 :

            #__________________CONVERT COORDINATES______________________________________

            x3 = np.interp(x1, (frameR,W-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR,H-frameR),(0,hScr))

            #________________SMOOTHNING THE VALUES TO GET BETTER RESULT_________________

            clocX = plocX + (x3 - plocX) / smoothning
            clocY = plocY + (y3 - plocY) / smoothning


            #____________________________TO MOVE THE MOUSE_____________________________

            mouse.move(wScr-clocX,clocY)
            cv2.circle(IMG, (x1,y1), 15, (255,0,255), cv2.FILLED)
            plocX , plocY = clocX, clocY

#_______________________________IF BOTH INDEX AND MIDDLE FINGER UP : CLICK MODE______________________

        if fingers[1] == 1 and fingers[2] == 1 :
            # Checking the distance
            length , IMG , lineInfo = detector.findDistance(8,12,IMG)
            print(length)

            # Clicking the mouse
            if length < 40 : 
                cv2.circle(IMG, (lineInfo[4],lineInfo[5]), 15, (0,255,0), cv2.FILLED)

                mouse.click()
                print("click")
            


#____________________________________________FRAME RATE___________________________________________

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(IMG, str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN , 3, (0,0,255),3)

    #____________________________________________DISPLAY___________________________________________

    cv2.imshow("AI MOUSE v.1.0", IMG)
    cv2.waitKey(1)