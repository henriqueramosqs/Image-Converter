import numpy as np
import cv2 as cv
import os

BGR2YUV = np.array([
    [0.615, -0.515, -0.100],
    [-0.147, -0.289, 0.436],
    [0.299, 0.587, 0.114]
],dtype=np.float32)

BGR2YCbCr_mul = np.array([
    [0.5, -0.419, -0.081],
    [-0.169, -0.331, 0.500],
    [0.299, 0.587, 0.114]
],dtype=np.float32)

BGR2YCbCr_const =np.array([
    128,
    128,
    0
],dtype=np.uint8)

colormap_1 = np.array([[[i,255-i,0] for i in range(256)]],dtype=np.uint8)
colormap_2 = np.array([[[0,255-i,i] for i in range(256)]],dtype=np.uint8)

toConvertPath = os.path.join(os.curdir,"To Convert")
convertedPath = os.path.join(os.curdir,"Converted")

def splitBGR(img:np.ndarray):
    imgDimensions = img.shape
    auxMat = np.zeros(imgDimensions[:2],np.uint8)
    B,G,R = cv.split(img)
    blueChannel = np.stack((B,auxMat,auxMat),axis=2)
    greenChannel = np.stack((auxMat,G,auxMat),axis=2)
    redChannel = np.stack((auxMat,auxMat,R),axis=2)

    return (redChannel,greenChannel,blueChannel)

def convertToYUV(img:np.ndarray):
    imgDimensions = img.shape
    result = np.zeros(imgDimensions,dtype=np.uint8)

    for row in range(imgDimensions[0]):
        for column in range(imgDimensions[1]):
            result[row,column,:] = np.dot(BGR2YUV,img[row,column,:])

    Y,U,V = cv.split(result)

    yChannel = cv.cvtColor(Y,cv.COLOR_GRAY2BGR)
    uChannel = cv.cvtColor(U,cv.COLOR_GRAY2BGR)
    vChannel = cv.cvtColor(V,cv.COLOR_GRAY2BGR)

    uChannel = cv.LUT(uChannel,colormap_1)
    vChannel = cv.LUT(vChannel,colormap_2)

    
    return(yChannel,uChannel,vChannel)

def convertToYCbCr(img:np.ndarray):
    imgDimensions = img.shape
    result = np.zeros(imgDimensions,dtype=np.uint8)

    for row in range(imgDimensions[0]):
        for column in range(imgDimensions[1]):
            result[row,column,:] = np.dot(BGR2YCbCr_mul,img[row,column,:])
            result[row,column,:]+=BGR2YCbCr_const

    Y,Cb,Cr = cv.split(result)

    yChannel = cv.cvtColor(Y,cv.COLOR_GRAY2BGR)
    cbChannel = cv.cvtColor(Cb,cv.COLOR_GRAY2BGR)
    crChannel = cv.cvtColor(Cr,cv.COLOR_GRAY2BGR)

    cbChannel = cv.LUT(cbChannel,colormap_1)
    crChannel = cv.LUT(crChannel,colormap_2)
    
    return(yChannel,cbChannel,crChannel)

def isValidInput(string:str)->bool:
    if(string=="1" or string =="2" or string=="3"):
        return True
    return 

if(not os.path.isdir(convertedPath)):
    raise Exception("Destiny path unnavailable! Please add a \"Converted\" folder to this directory!")

if(not os.path.isdir(toConvertPath)):
    raise Exception("Origin path unnavailable! Please add a \"To Convert\" folder to this directory!")

print("Hi! Please, put your images in \"To Convert\" file and indicate the desired operation:")
print("1 - Split R, G and B channels")
print("2 - Convert Image to YUV")
print("3 - Convert image to YCbCr\n")

operation = 0

while(not isValidInput(operation)):
    operation = input()

    if (operation=="1"):
        print("\nSpliting R, G ans B Channels...\n")
        break
    if (operation=="2"):
        print("\nConverting to YUV format...\n")
        break
    if (operation=="3"):
        print("\nConverting to YCbCr format...\n")
        break

    print("Please, select a valid operation")


for rawImgName in os.listdir(toConvertPath):
    if rawImgName==".DS_Store":
        continue

    print(f"Converting {rawImgName}...")
    imgName = rawImgName.strip()
    imgName = imgName[:imgName.find('.')]
    imgOrgLoc = os.path.join(toConvertPath,rawImgName)
    imgDestLoc = os.path.join(convertedPath,imgName)
    img = cv.imread(imgOrgLoc)

    if not os.path.isdir(imgDestLoc):
        os.mkdir(imgDestLoc)

    if(operation=="1"):
        res = splitBGR(img)

        bName = imgName + "BlueChannel.jpeg"
        bDestiny = os.path.join(imgDestLoc,bName)
        cv.imwrite(bDestiny,res[0])

        gName = imgName + "GreenChannel.jpeg"
        gDestiny = os.path.join(imgDestLoc,gName)
        cv.imwrite(gDestiny,res[1])

        rName = imgName + "RedChannel.jpeg"
        rDestiny = os.path.join(imgDestLoc,rName)
        cv.imwrite(rDestiny,res[2])
    
    if(operation=="2"):
        res = convertToYUV(img)

        yName = imgName + "YChannel.jpeg"
        yDestiny = os.path.join(imgDestLoc,yName)
        cv.imwrite(yDestiny,res[0])

        uName = imgName + "UChannel.jpeg"
        uDestiny = os.path.join(imgDestLoc,uName)
        cv.imwrite(uDestiny,res[1])

        vName = imgName + "VChannel.jpeg"
        vDestiny = os.path.join(imgDestLoc,vName)
        cv.imwrite(vDestiny,res[2])

    if(operation=="3"):
        res = convertToYCbCr(img)

        yName = imgName + "YChannel.jpeg"
        yDestiny = os.path.join(imgDestLoc,yName)
        cv.imwrite(yDestiny,res[0])

        cbName = imgName + "CbChannel.jpeg"
        cbDestiny = os.path.join(imgDestLoc,cbName)
        cv.imwrite(cbDestiny,res[1])

        crName = imgName + "CrChannel.jpeg"
        crDestiny = os.path.join(imgDestLoc,crName)
        cv.imwrite(crDestiny,res[2])

print("Done!")