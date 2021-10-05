import cv2
import mediapipe as mp
import time
import pyautogui
import os
import glob

class HandDetector():  # Setting the class
    def __init__(self, mode=False, maxHands=2, detectaionCon=0.5, TruckCon=0.5):
        self.mode = mode
        self.maxHand = maxHands
        self.detectaionCon = detectaionCon
        self.TruckCon = TruckCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHand, self.detectaionCon, self.TruckCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.countForAVG = 0

        self.FristTimeIn = True  # use for make sure when the hand is too far for more then 5 sec. a flag, if the hand is too far its became False. is in 'itsACloseHand'
        self.SratTime = time.time()  # Setting the beginning run time. use for claca. in 'itsACloseHand'
        self.removefiles()

    def removefiles(self):

        files = glob.glob("C:\\Users\\ashta\\PycharmProjects\\VisionD_test1\\screenshots\\*")
        if len(files) > 0:
            for f in files:
                os.remove(f)

    def findHands(self, img, draw=True): #Find the hands in the img
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True): # finding and converting the hand location in the img

        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHans = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHans.landmark):

                lmX = lm.x  # landmark X axes
                lmY = lm.y  # landmark Y axes
                h, w, c = img.shape
                cx, cy = int(lmX * w), int(lmY * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    if len(self.lmList) > 9:
                        xHandCenter = int((self.lmList[9][1] + self.lmList[0][1]) / 2)
                        yHandCenter = int((self.lmList[9][2] + self.lmList[0][2]) / 2)
                        self.HCP = (xHandCenter, yHandCenter)
                        cv2.circle(img, (self.HCP), 7, (255, 0, 255), cv2.FILLED)  # Circel the center of the hand

        return self.lmList

    def getHCP(self):
       # self.countForAVG = self.countForAVG + 1
        # print(self.countForAVG)
        return self.HCP

    def disBetFin(self, f1, f2):
        return ((((f2[0] - f1[0]) ** 2) + ((f2[1] - f1[1]) ** 2)) ** 0.5)




    def under5sec(self):
        if self.FristTimeIn:
            self.SratTime = time.time()
            self.FristTimeIn = False
            #print("firt if under 5")
            return True
        else:
            d = time.time() - self.SratTime #d is the time has passed from the moment the hand was too far/close until time.time()
            if d > 5:
                print(d)
                return False # if is more then 5 sec return False - the hand is too far/closr and its not a "jump" of hand lendmarks
            else:
                #print("else under 5")
                return True
    def do_scrrenshot(self): #screenshot for checking the hand jumps
        screenshot = pyautogui.screenshot()
        screenshot.save(f"C:\\Users\\ashta\\PycharmProjects\\VisionD_test1\\screenshots\\screen{self.countForAVG}.png")
    def set_fingers(self): #setting finger lendmarks
        self.f0 = self.lmList[0][1:3]
        self.f2 = self.lmList[2][1:3]
        self.f4 = self.lmList[4][1:3]
        self.f3 = self.lmList[3][1:3]
        self.f5 = self.lmList[5][1:3]
        self.f8 = self.lmList[8][1:3]
        self.f9 = self.lmList[9][1:3]
        self.f12 = self.lmList[12][1:3]
        self.f13 = self.lmList[13][1:3]
        self.f16 = self.lmList[16][1:3]
        self.f17 = self.lmList[17][1:3]
        self.f20 = self.lmList[20][1:3]
    def print_for_checks(self):
        print("___")
        print(f"3-4- {round(self.disBetFin(self.f3, self.f4))}")
        print(f"5-9- {round(self.disBetFin(self.f5, self.f9))}")
        print(f"9-13- {round(self.disBetFin(self.f9, self.f13))}")
        print(f"13-17- {round(self.disBetFin(self.f13, self.f17))}")
        print("___")
    def itsACloseHand(self):
        self.set_fingers()

        if self.disBetFin(self.f5, self.f9) < 20 or self.disBetFin(self.f9, self.f13) < 15 or self.disBetFin(self.f13,self.f17) < 12 or (self.disBetFin(self.f3,self.f4) < 15 and self.disBetFin(self.f2,self.f3) < 15):
            self.countForAVG = self.countForAVG + 1
            self.print_for_checks()
            self.do_scrrenshot()
            # print(f"JUMP! {self.countForAVG}")


        if self.disBetFin(self.f4, self.f8) < 50 and self.disBetFin(self.f8, self.f12) < 30 and self.disBetFin(self.f12,self.f16) < 25 and self.disBetFin(
                                                                                    self.f16, self.f20) < 25 and self.disBetFin(self.f4, self.f20) < 83:
            #print(f"Your Hand is Close!")
            return True
        else:  # In case the hand is open
            if self.disBetFin(self.f9, self.f0) > 160 or self.disBetFin(self.f9,self.f0) < 65:  # if the hand is open, check if is too far or too close to the camera
                if self.under5sec():
                    pass
                    #print("under 5 sec")
                else:
                    #print("your hand is to far more then 5 sec!")
                    pass
            else:
                self.FristTimeIn = True
            return False


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    dete = HandDetector()

    while True:
        success, img = cap.read()

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        img = dete.findHands(img)
        lmList = dete.findPosition(img)
        if len(lmList) != 0:
            # print(lmList[4])
            pass

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
