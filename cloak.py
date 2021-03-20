import cv2 
import numpy as np
import time
video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
time.sleep(3)
#capturing the background
for i in range(30):
    check,background = video.read()
background = np.flip(background, axis=1)

while(video.isOpened()):
    check,img=video.read()
    if check==False:
        break
    img=np.flip(img,axis=1)
    #setting up the HSV values 
    #cnvrt BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #seperating the cloak part
    #to change the color adjust the hsv values
    lower_hsv = np.array([0,120,60])
    upper_hsv = np.array([10,255,255])
    mask1 = cv2.inRange(hsv,lower_hsv,upper_hsv)
    #exept the cloak evrthing will be there
    lower_hsv = np.array([170,120,70])
    upper_hsv = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_hsv,upper_hsv)

    mask1 = mask1+mask2
    #i/p img Noise removal
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8),iterations=1)
     #evrthing exept the cloak  
    mask2 = cv2.bitwise_not(mask1)

    #used to substitute the cloak or red part with background
    res1 = cv2.bitwise_and(img,img, mask=mask2)

    #differentiating the cloak from rest of the background
    res2 = cv2.bitwise_and(background,background, mask=mask1)

    final = cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("invisibility by Midhun",final)  #Displays the final output image

    key = cv2.waitKey(1)
    if key == ord('q'):
      break

video.release()
cv2.destroyAllWindows() 
 


