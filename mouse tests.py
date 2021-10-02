import mouse as ms
import  time
star_x = ms.get_position()[0]
star_y = ms.get_position()[1]

end_x = 1700
end_y = 955
sTime =  time.time()
eTime = 0
while True:
     eTime = time.time()
     print(eTime-sTime)