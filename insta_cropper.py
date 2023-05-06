from PIL import Image
import os




def cropImg(imgPath,savePath):
    img = Image.open(imgPath)
    upperLimit = 0
    bottomLimit = 0

    imgWidth = img.size[0];
    imgHeight = img.size[1];

    pix = img.load()

    for y in range(0,int(imgHeight/2)):
        row = True
        for x in range (int(imgWidth/2-200),int((img.size[0]-1)/2)+200):
            if pix[x, y] != (255, 255, 255):
                row =False
                break
        if row :
            upperLimit=  y ;

    for y in range(imgHeight-1,int(imgHeight/2),-1):
        row = True
        for x in range (int(imgWidth/2-200),int((img.size[0]-1)/2)+200):
            if pix[x, y] != (255, 255, 255):
                row =False
                break
        if row :
            bottomLimit =  y ;

    img2 = img.crop((0,upperLimit,imgWidth,bottomLimit))
    img2Path = savePath + imgPath
    img2.save(img2Path)



savePath = "cropped"

if not os.path.exists(savePath):
    os.makedirs(savePath)

for imgPath in os.listdir():
    if imgPath.endswith(".png"):
        saveImgPath = savePath + "\\" + imgPath
        cropImg(imgPath, saveImgPath)
