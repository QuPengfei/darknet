#!/usr/bin/python 

import os
import xml.dom.minidom
import cv2 as cv
import numpy as np
import sys
reload(sys)

path="/home/bqu/workspace/ljhs/darknet/" 
ImgPath = "./data/VOCdevkit/VOC2007/JPEGImages/"
AnnoPath = "./data/VOCdevkit/VOC2007/Annotations/"
save_path = "/home/bqu/workspace/DL/box-image/"
txt_file = "./data/voc/2007_test.txt"

from PIL import Image, ImageDraw,ImageFont

def paint_chinese_opencv(im, chinese, pos, color):
    img_PIL = Image.fromarray(cv.cvtColor(im, cv.COLOR_BGR2RGB))
    font = ImageFont.truetype('simsun.ttc', 35)
    fillColor = color
    position = pos
    if not isinstance(chinese, unicode):
        chinese = chinese.decode('utf-8')
    draw = ImageDraw.Draw(img_PIL)
    draw.text(position, chinese, font=font, fill=fillColor)
    img = cv.cvtColor(np.asarray(img_PIL), cv.COLOR_RGB2BGR)
    return img

def file_list(txtfile):
    lines = []
    with open(txtfile,"r") as f:
        lines = f.readlines()
    return [line.strip().split("/")[-1] for line in lines]

def draw_anchor(ImgPath,AnnoPath,save_path,FileList=None,threshold=None):
    count = 0

    imagelist = FileList
    if FileList == None:
        imagelist = os.listdir(ImgPath)

    for image in imagelist:
        image_pre, ext = os.path.splitext(image)
        imgfile = ImgPath + image
        xmlfile = AnnoPath + image_pre + '.xml'
        #print(image, imgfile)

        DOMTree = xml.dom.minidom.parse(xmlfile)

        collection = DOMTree.documentElement

        img = cv.imread(imgfile)

        filenamelist = collection.getElementsByTagName("filename")
        filename = filenamelist[0].childNodes[0].data
        print(filename)
        objectlist = collection.getElementsByTagName("object")

        #if img == None: continue
 
        for objects in objectlist:
            namelist = objects.getElementsByTagName('name')
            objectname = namelist[0].childNodes[0].data
 
            bndbox = objects.getElementsByTagName('bndbox')
            #print(bndbox)
            for box in bndbox:
                x1_list = box.getElementsByTagName('xmin')
                x1 = int(x1_list[0].childNodes[0].data)
                y1_list = box.getElementsByTagName('ymin')
                y1 = int(y1_list[0].childNodes[0].data)
                x2_list = box.getElementsByTagName('xmax')  
                x2 = int(x2_list[0].childNodes[0].data)
                y2_list = box.getElementsByTagName('ymax')
                y2 = int(y2_list[0].childNodes[0].data)
		cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=2)
		img = paint_chinese_opencv(img, objectname,(x1, y1),(255, 255, 255))
                #cv.putText(img, objectname.decode('utf-8'), (x1, y1), cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),thickness=2)
                # cv.imshow('head', img)
                cv.imwrite(save_path+'/'+filename, img)   #save picture
	count += 1
	if threshold != None and count > threshold: break

if __name__ == '__main__':
    sys.setdefaultencoding('utf-8')
    print sys.getdefaultencoding()
    files = file_list(txt_file)
    draw_anchor(ImgPath,AnnoPath,save_path,FileList=files)
    #draw_anchor(ImgPath,AnnoPath,save_path,FileList=None,threshold=None)
