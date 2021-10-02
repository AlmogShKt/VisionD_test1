import cv2
import mediapipe as mp
from matplotlib import pyplot as plt
import time
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

coord_x = []
coord_y = []

def draw_coord_graph(x,y):
    coord_x.append(x)
    coord_y.append(y)
    if len(coord_y) % 100 == 0 :
        plt.cla()
        plt.scatter(coord_x,coord_y)
        plt.show()
        print(f"x:{coord_x}")
        print(f"Y:{coord_y}")



def GetFingerIdAndXY(id):
    if id != None:
        return fingerL[id]
    else:
        return fingerL


    pass


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
    results = hands.process(imgRGB)
    fingerL = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm  in enumerate(handLms.landmark):
                lmX = lm.x
                lmY = lm.y
                h,w,c = img.shape
                cx,cy = int(lmX*w) , int(lmY*h)
                cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
                fingerL.append((id,(cx,cy)))
                print(f"ID:{id}, {cx,cy}")


                # if id == 0:
                #
                #     #print(f"ID:{id}| lmX:{lmX} |lmY:{lmY}")
                #     draw_coord_graph(lmX,lmY)
                #     # ani = FuncAnimation(plt.gcf(),draw_coord_graph(lmX,lmY))
                #     # plt.tight_layout()
                #     # plt.show()


            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)




    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)