import numpy as np
import cv2
import os
import math
import pyautogui


sep = os.sep
face_cas = cv2.CascadeClassifier(
    cv2.__path__[0]+f"{sep}data{sep}haarcascade_frontalface_alt.xml")

hand_css = cv2.CascadeClassifier("test.xml")


cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = hand_css.detectMultiScale(gray, scaleFactor=2.5, minNeighbors=5)
    x_sum = 0
    y_sum = 0
    for (x, y, h, w) in faces:
        print(x, y)
        x_sum += x
        y_sum += y
        color = (255, 0, 0)
        stoke = 2
        width = x+w
        height = y+h
        print(x, y)
        cv2.rectangle(frame, (x, y), (width, height), color, stoke)
    c = len(faces)
    if c == 0:
        continue
    x = int(x_sum/len(faces))
    y = int(y_sum/len(faces))
    weight_x = 0
    weight_y = 0
    total_weight = 0
    W = 1
    for (lx, ly, h, w) in faces:
        try:
            W = 1/math.sqrt((x-lx)**2+(y-ly)**2)
        except:
            continue
        weight_x += lx*W
        weight_y += ly*W
        total_weight += W
    try:
        x = int(weight_x/total_weight)
        y = int(weight_y/total_weight)
    except:
        continue
    color = (0, 255, 0)
    stoke = 2
    width = x+10
    height = y+10
    cv2.rectangle(frame, (x, y), (width, height), color, stoke)
    cv2.imshow("frame", frame)
    pyautogui.moveTo(x*5, y*5)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


cam.release()
cam.destroyAllWindows()
