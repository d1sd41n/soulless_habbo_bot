import cv2
from mss import mss
from PIL import Image
import numpy as np
import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller

def convert_rgb_to_bgr(img):
        return img[:, :, ::-1]


mouse = MouseController()
keyboard = Controller()

resolution = mss().monitors[0]  #get the screen resolution
# print(resolution)
monitor = {'top': 0, 'left': 0, 'width': resolution['width'], 'height': resolution['height']}
screen = mss()
frame = None

sct_img = screen.grab(monitor)
img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
img = np.array(img)
img_bgr = convert_rgb_to_bgr(img)
img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

chair_1 = cv2.imread('assets/habbo/givedrink1.png',0)
print(chair_1)
w, h = chair_1.shape[::-1] # weight height

res = cv2.matchTemplate(img_gray, chair_1, cv2.TM_CCOEFF_NORMED)

threshold = 0.9
loc = np.where( res >= threshold)
loczip = list(zip(*loc[::-1]))
coor = loczip[0]
mouse.position = (coor[0]+int(w/2), coor[1]+int(h/2))
mouse.click(Button.left)
print(loczip)
# keyboard.type('.')
# keyboard.press(Key.enter)
# keyboard.release(Key.enter)

for pt in zip(*loc[::-1]):
    # print(pt)
    # print(type(pt))
    cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (255,255,255), 4)

cv2.imshow('img_bgr', img_gray)
# # cv2.imshow('habbo', habbo_avatar_1)
cv2.waitKey(0)
cv2.destroyAllWindows()
