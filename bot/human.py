from .util import *
from . import util
import pytesseract,pyautogui,pyscreenshot,pyscreeze
import time
from .realmouse import *
from numpy.random import normal


def moveMouseToImage(name,dx=0,dy=0,dw=0,dh=0,grayscale=False,confidence=.9):
    box=util.findImage(name,grayscale,confidence)
    if dx!=0 or dy!=0: box=translate(box,dx,dy)
    if dw!=0 or dh!=0: box=transform(box,dw,dh)
    return moveMouseToBox(box)

def doubleClick(image=None,box=None,dx=0,dy=0,dw=0,dh=0):
    try:
        if image is not None:
            moveMouseToImage(image,dx,dy,dw,dh)
        if box is not None:
            moveMouseToBox(box)
        pyautogui.doubleClick()
        return True
    except pyscreeze.ImageNotFoundException as e:
        return False
    
def click(image=None,box=None,dx=0,dy=0,dw=0,dh=0,clicks=1,grayscale=True,confidence=.9):
    try:
        if image is not None:
            moveMouseToImage(image,dx,dy,dw,dh,grayscale,confidence)
        if box is not None:
            moveMouseToBox(box)
        if clicks == 1:
            pyautogui.click()
        elif clicks==2:
            pyautogui.doubleClick()
        elif clicks==3:
            pyautogui.tripleClick()
        return True
    except pyscreeze.ImageNotFoundException as e:
        return False
    
def write(text):
    pyautogui.typewrite(text)
    
def move(image=None):
    if image is not None:
        return moveMouseToImage(image)

def moveMouseToBox(box,err=.5):
    move_mouse_to(box.left+int(box.width*normal(.5,err)),box.top+int(box.height*normal(.5,err)))
    x,y=pyautogui.position()
    if util.isOutside(x,y,box):
       moveMouseToBox(box,err=err/2)

def clickBox(box):
    moveMouseToBox(box)
    pyautogui.click()

def hold(key,duration):
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)
    
def screenshot():
    return pyscreenshot.grab()

def recognize(img):
    return pytesseract.image_to_string(img)

def scrape(text,img,n):
    width,height=img.size
    w=width/n
    h=height/n
    for i in range(n-1):
        for j in range(n-1):
            box=(int(i*w),int(j*h),int((i+1)*w),int((j+1)*h))
            crop=img.crop(box)
            cypher=recognize(img.copy().crop(box))
            if text.lower() in cypher.lower(): return crop
