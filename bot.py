from bot import moveMouse,mouseClick,getMouseImage,clickImage
moveMouse(1000,1000)
mouseClick()
# w is the width of the image in pixel (it is a square)
# save saves to the current directory.
getMouseImage(label='mylabel', w=100, save=True) #saves like "mylabel_23451.png"

# To customize save do this:
img=getMouseImage(w=50)
img.save('mypig.png')
#img.show()
moveMouse(10,10)
# You can click images  on the screen doing stuff like this
if clickImage(img):
    print("Sucessfully clicked on that image.")
else:
    print("Failed to find and click on that image.")
