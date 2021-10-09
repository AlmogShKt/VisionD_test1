import cv2
import mediapipe as mp
import time
from Hands import HanfTruckingModule as htm
import mouse as ms
#test for git


cap = cv2.VideoCapture(0)
imgToDraw = cv2.imread("whitw.PNG")

dete = htm.HandDetector()



def freeDraw():
    print("free draw as been execute")
    handcenter = dete.getHCP()

    pixelToDraw_x = int((handcenter[1]/640)*946)
    pixelToDraw_y = int(946-(handcenter[0] / 640) * 946)


    imgToDraw[pixelToDraw_x:pixelToDraw_x+5, pixelToDraw_y:pixelToDraw_y+5] = (255, 114, 30) # free drawing according to the center of the hand

    end_x = 1700-((handcenter[0]/640)*1700)
    end_y = (handcenter[1]/640)*955
    ms.move(end_x,end_y)

def DragWithHand():
    print("drag with hand as been execute")
    handcenter = dete.getHCP()
    x_start = ms.get_position()[0]
    y_start = ms.get_position()[1]
    end_x = 1700 - ((handcenter[0] / 640) * 1700)
    end_y = (handcenter[1] / 640) * 955

    if dete.itsACloseHand():
        #ms.drag(x_start,y_start,end_x,end_y)
        pass

    else:
        ms.move(end_x, end_y)

def func3():
    print("func3 as been execute")

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = dete.findHands(img)
    lmList= dete.findPosition(img)
    if len(lmList) != 0:
        DragWithHand()



    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    #cv2.imshow("Imagetodraw",imgToDraw)
    cv2.waitKey(1)
