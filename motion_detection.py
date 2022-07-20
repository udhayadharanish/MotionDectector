from datetime import datetime
import pandas
import cv2
from cv2 import destroyAllWindows

video = cv2.VideoCapture(0)
data = pandas.DataFrame(columns=["Start","End"])
status_list = [None,None]
times = []
first_frame = None

while(True):
    
    status = 0
    check,frame = video.read()

    frame = cv2.resize(frame,(500,500))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)

    
    if first_frame is None:
        first_frame = gray
        continue


    delta_frame = cv2.absdiff(first_frame,gray)

    thresh_frame = cv2.threshold(delta_frame,130,255,cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame,None,iterations=2)

    (cnts,_) = cv2.findContours(thresh_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    for counter in cnts:
        if cv2.contourArea(counter) < 8000:
            continue
        (x,y,w,h) =cv2.boundingRect(counter)
        status = 1
        cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),3)
        print("motion !!!")

    status_list.append(status)

    status_list = status_list[-2:]
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())


    
    cv2.imshow("first_frame",first_frame)
    # cv2.imshow("capturing...",guassian)
    cv2.imshow("Delta Frame",delta_frame )
    cv2.imshow("threshold frame",thresh_frame)
    cv2.imshow("motion detecting",frame)


    
    key = cv2.waitKey(1)
    if key == ord("q"):
        if status == 1:
            times.append(datetime.now())
        break
# start = []
# end = []
# for i in range(0,len(times),2):
#     start.append(times[i])
# for i in range(1,len(times),2):
#     end.append(times[i])
for i in range(0,len(times),2):
    data = data.append({"Start":times[i],"End":times[i+1]},ignore_index=True)




print(data)
data.to_csv("Times.csv")
print(times)
video.release()
cv2.destroyAllWindows
