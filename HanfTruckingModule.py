import cv2
import mediapipe as mp
import time


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
        self.countForAVG = self.countForAVG + 1
        # print(self.countForAVG)
        return self.HCP

    def disBetFin(self, f1, f2):
        return ((((f2[0] - f1[0]) ** 2) + ((f2[1] - f1[1]) ** 2)) ** 0.5)

    def under5sec(self):
        if self.FristTimeIn:
            self.SratTime = time.time()
            self.FristTimeIn = False
        else:
            d = time.time() - self.SratTime
            if d > 5:
                return False
            else:
                return True

    def itsACloseHand(self):
        f0 = self.lmList[0][1:3]
        f4 = self.lmList[4][1:3]
        f8 = self.lmList[8][1:3]
        f9 = self.lmList[9][1:3]
        f12 = self.lmList[12][1:3]
        f16 = self.lmList[16][1:3]
        f20 = self.lmList[20][1:3]
        if self.disBetFin(f4, f8) < 50 and self.disBetFin(f8, f12) < 30 and self.disBetFin(f12,
                                                                                           f16) < 25 and self.disBetFin(
            f16, f20) < 25 and self.disBetFin(f4, f20) < 83:
            # print(f"Your Hand is Close!")
            return True
        else:  # In case the hand is open
            if self.disBetFin(f9, f0) > 160 or self.disBetFin(f9,
                                                              f0) < 65:  # if the hand is open, check if is too far or too close to the camera
                if self.under5sec():
                    print("under 5 sec")
                else:
                    print("your hand is to far more then 5 sec!")
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
