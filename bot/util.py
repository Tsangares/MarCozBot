from .human import screenshot
import pyautogui
import os,time,math
from pyscreeze import Box
from random import randint
from PIL.Image import Image
CWD=os.getcwd()
OUTPUT=CWD

def mlData(img,label,outputDir=OUTPUT):
    output=outputDir
    if not os.path.isdir(output): os.mkdir(output)
    name="%s_%d.png"%(label,)
    filepath=os.path.join(output,name)
    img.save(filepath)

def saveImage(img,label=None):
    if label is None:
        label='mouse_image'
    filename=os.path.join(OUTPUT,'{}_{:05d}.png'.format(label,randint(1,99999)))
    img.save(filename)
    
def getGameCenterMouse(label=None,w=100,save=False):
    x,y=pyautogui.position()
    box=Box(x-w/2,y-w/2,w,w)
    img=getImage(box=box)
    if save: saveImage(img,label)
    return img

def getGameCenter(label=None):
    img=getGameScreen(offX=150,offY=50)
    if label is not None: mlData(img,label)
    return img

def getGameScreen(offX=0,offY=0):
    tr=findImage('exit',confidence=.8)
    bl=findImage('all_chat',confidence=.8)
    top=tr.top
    left=bl.left+offX/2-80
    right=tr.left+offY/2
    bottom=bl.top
    height=bottom-top-100-offY
    width=right-left-275-offX
    box=Box(left,top,width,height)
    return getImage(box=box)
    
def camera(label,wait=3,count=10,lens=getGameCenterMouse):
    for i in range(wait):
        time.sleep(.5)
        print(wait-i)
    for i in range(count):
        lens(label)
        time.sleep(.5)
        print("Snap!")
    print('Finished')
    

def img(name):
    return r'Tools/screenshots/%s.png'%name

def center(box):
    return (int(box[0]+box[2]/2),int(box[1]+box[3]/2))

def locate(name,grayscale=True,confidence=.9):
    try:
        return pyautogui.locateCenterOnScreen(img(name),grayscale=grayscale,confidence=confidence)
    except Exception as e:
        return None

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)
def horizontal(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**4)
def verticle(a,b):
    return math.sqrt((a[0]-b[0])**4+(a[1]-b[1])**2)

def nearest(source,obj,d=distance):
    if type(source) is Box:
        point=center(source)
    elif type(source) is str:
        point=locate(source)
    else:
        raise("Unknown type source", type(source),source)
    boxes=pyautogui.locateAllOnScreen(img(obj))
    try:
        distances=[(d(center(box),point),box) for box in boxes]
    except Exception as e:
        raise(Exception(e,source,obj,d))
        
    return sorted(distances)[0][1]

def findImage(name,grayscale=True,confidence=.9):
    if issubclass(type(name),Image):
        print("Looking for image on the screen.")
        return pyautogui.locateOnScreen(name,grayscale=grayscale)
    return pyautogui.locateOnScreen(img(name),grayscale=grayscale)

def getImage(image=None,box=None,grayscale=True,confidence=.9):
    if image is not None:
        box=findImage(image,grayscale=grayscale,confidence=confidence)
    if box is not None:
        crop=(box.left,box.top,box.left+box.width,box.top+box.height)
        return screenshot().crop(crop)
    return None

def isOutside(x,y,box):
    return x < box.left or x > box.left+box.width or y < box.top or y > box.top+box.height
def isInside(x,y,box):
    return not isOutside(x,y,box)

def translate(box,dx=0,dy=0):
    return Box(box.left+dx,box.top+dy,box.width,box.height)

def transform(box,dw=0,dh=0):
    return Box(box.left,box.top,box.width+dw,box.height+dh)

#This is probably right.x 
def scale(box,x=1,y=1):
    xOffset=(box.width-box.width*x)/2
    yOffset=(box.height-box.height*y)/2
    return Box(box.left+offset,box.top+offset,box.width*x,box.height*y)

