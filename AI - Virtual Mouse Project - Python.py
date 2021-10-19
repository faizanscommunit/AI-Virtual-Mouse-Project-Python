
#**** ---- Note --- ****#
# AI - Virtual Mouse Project - Python
# By Faizanscommunit
# MIT Licensed

#**** --- Algorithm --- ****#

# 1. Find Hand Landmarks
# 2. Get the tip of the index and middle finger
# 3. Check which fingers are up
# 4. Only index finger: Moving mode
# 5. Convert Coordinates
# 6. Smoothen values
# 7. Move Mouse
# 8. Both index and middle fingers are up so it is in clicking mode
# 9. Find distance b/w fingers
# 10. Click mouse if distance is short
# 11. Frame Rate
# 12. Display

#**** --- Source Code --- ****#

# Imports
import cv2
import autopy
import numpy as np
import time
from cvzone.HandTrackingModule import HandDetector
# Variables
frameR = 100
wCam, hCam = 640, 480
smoothening = 10
plocX, plocY = 0, 0
clocX, clocY = 0, 0
pTime = 0
cap = cv2.VideoCapture(1)
cap.set(3, wCam)
cap.set(4, hCam)
wScreen, hScreen = autopy.screen.size()
# Detecting Hands
detector = HandDetector(maxHands=1)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList)!=0: # If there is a hand
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # Rectangle which will act as a mouse pad
        cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0,255),2)
        #  Detecting Fingers
        fingers = detector.fingersUp()
        # Moving mouse if 1st finger is up
        if fingers[1] == 1 and fingers[2]==0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScreen))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScreen))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # Moving Mouse
            autopy.mouse.move(wScreen-clocX, clocY)
            # Detecting finger tip
            cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
            plocX, plocY = clocX, clocY
        # Click Functionality
        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)
            if length<30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
    # FPS (Frames Per Second)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    # Showing FPS
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)
    # Creating Window
    cv2.imshow("AI - Virtual Mouse ", img)
    # Quit Functionality
    if cv2.waitKey(10) == ord('q'):
        break

#**** --- Social Links --- ****#
#  Github: https://github.com/faizanscommunit
#  Website: https://faizanscommunit.pythonanywhere.com/
#  Instagram: https://www.instagram.com/faizanscommunit/
