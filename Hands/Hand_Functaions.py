import cv2
import time
from Hands import HanfTruckingModule as htm
import mouse as ms

class functaions():
    def __init__(self):
        self.cap = cv2.VideoCapture(0) #Setting the video cap
        self.imgToDraw = cv2.imread("whitw.PNG")# Creat a blank withe img to Free Draw function 1'
        self.set_text_on_imgToDraw()
        self.Hand_d =htm.HandDetector()

        self.first_time_in_funcation = [ #in order to know then is the first time in the function
            {"freeDraw":True}            #use for set up setting, like color for drawing
             ]                           #after the first time is will change to False until the end of running

        self.function_in_class = [
            {"1": self.freeDraw}
            ]
    #_____________________#
    # Function 1 - Free Draw - Use the center of your hand to draw!
    #you can choose the pen color from one of the option in the console:
    #V 1.0: The colors if: Black,Green,Red,Blue,Pink
    #for clean the page - inster 'CLEAN'

    def set_text_on_imgToDraw(self):
        cv2.rectangle(self.imgToDraw, (5, 5), (640, 100), (213, 86, 245))
        cv2.putText(self.imgToDraw, "CLEAN PAGE", (150
                                                   , 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255),2)
        pass

    def freeDraw(self):

        self.center_of_the_hand = self.Hand_d.getHCP()

        pixelToDraw_x = int((self.center_of_the_hand[1]/640)*946)
        pixelToDraw_y = int(946-(self.center_of_the_hand[0] / 640) * 946)

        drawin_color = \
            {
            'Black':(0,0,0),
            'Green':(0,255,0),
            'Red':(0,0,255),
            'Blue':(255,0,0),
            'Pink':(213,86,245)
            }

        if self.first_time_in_funcation[0]["freeDraw"]:
            print("free draw as been execute \n")
            print(f"choose color: {list(drawin_color.keys())}")
            self.choosen_color = input("-->")
            self.first_time_in_funcation[0]["freeDraw"] = False
        else:
            self.imgToDraw[pixelToDraw_x:pixelToDraw_x+5, pixelToDraw_y:pixelToDraw_y+5] = drawin_color[self.choosen_color] #drawing according to the center of the hand position


        self.clean_page_for_freeDraw(pixelToDraw_x,pixelToDraw_y)


    def clean_page_for_freeDraw(self,x,y):

        if (x > 4 and x < 100) and (y > 4 and y < 640):
            self.imgToDraw = cv2.imread("whitw.PNG")  # Creat a blank withe img to draw fun'
            self.set_text_on_imgToDraw()
            print("C")
        else:
            print(x,y)





    # _____________________#
    # Function 2 - Move mouse - Use the center of your hand to control the mouse!
    # V 1.0: You can only move the mouse(next V will be option to right click

    def Move_mouse(self):
        end_x = 1700-((self.center_of_the_hand[0]/640)*1700)  #
        end_y = (self.center_of_the_hand[1]/640)*955
        ms.move(end_x,end_y)


    #___# dic' of functions
    #

    #____#
    #main

    def print_functions_names(self):
        print("choose the function you want to execute:")
        i=0
        for fun_name in self.first_time_in_funcation:
            print(f"{i+1}-{list(fun_name.keys())[i]}")
            i = i +1


    # = input("choose the function you want to use: 1-Free drawing-->")
    def run(self):
        pTime = 0
        cTime = 0

        self.print_functions_names()
        fun_to_run = input("-->")
        while True:
            success, viedo_Img = self.cap.read()

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            viedo_Img = self.Hand_d.findHands(viedo_Img) #refresh the img with the new lamd mark positions
            lmList= self.Hand_d.findPosition(viedo_Img) #list of all the fingers landmarks


            if len(lmList) != 0: #only if the system detect hand(the landmarks list is not empty) run function

                self.freeDraw()

            cv2.putText(viedo_Img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) #write th FTS on the screen

            cv2.imshow("cam_video", viedo_Img)
            cv2.imshow("Image_to_draw",self.imgToDraw)
            cv2.waitKey(1)

def run_class():

    f = functaions()
    f.run()


run_class()