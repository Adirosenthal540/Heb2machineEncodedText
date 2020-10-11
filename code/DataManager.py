import Main
import os
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
import cv2 as cv

GRAYSHADE =150
MINPERCENT = 25

# *** The data is combination of TIF image (tif) of one line of text and txt Image (gt.txt) which is the lable of the image
# *** The name of the tif and the matching txt file should be the same - becouse there are lot of diffrent handwrite
# *** the user will insert his own ID and the name of each image will be calculate from uniqe ID of the image (integer)
# *** and the user ID - like: 1-316550797.tif, 1-316550797.gt.txt, 2-316550797.tif, 2-316550797.gt.txt etc.

DataFolder = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\DataBase"
infoFile = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\code\info.txt"


def Insert_to_database(images_processed):
    f = open(infoFile, "r")
    list_of_lines = f.readlines()
    numImage = list_of_lines[0].split(" ")[-1]
    numStart = int(numImage)
    list_of_lines[0] = list_of_lines[0][:-(len(numImage))]
    numImage = int(numImage)
    image_path_list = []
    for imageP in images_processed:
        if CheckImageBeforeDatabase(imageP):
            nameImage = imageP.handwrite_ID +"_"+ str(numImage)
            pathNewImage = os.path.join(DataFolder, nameImage+".tif")
            image_path_list.append(pathNewImage)
            im = Image.fromarray(imageP.imageArray)
            im.save(pathNewImage, 'TIFF')
            f = open(os.path.join(DataFolder, nameImage+".gt.txt"), "w+", encoding="utf-8")
            f.write(imageP.Label)
            f.close()
            numImage += 1

    list_of_lines[0] = list_of_lines[0] + str(numImage)
    a_file = open(infoFile, "w", encoding="utf-8")
    a_file.writelines(list_of_lines)
    a_file.close()

    top = Toplevel()
    top.title("check database")

    bad_Image = Main.checkData(image_path_list, top)
    delete_from_database(bad_Image)
    return (numStart, numImage)

def delete_from_database(images_list_paths):
    for image_path in images_list_paths:
        os.remove(image_path)
        txt_file_path = image_path[:-4]+".gt.txt"
        os.remove(txt_file_path)

def CheckImageBeforeDatabase(imageP):
    imageArray = imageP.imageArray
    numDarkPixels = np.sum(imageArray < GRAYSHADE)
    numPixelsInImage = imageArray.size
    percent = (numDarkPixels / numPixelsInImage) * 100
    if percent > MINPERCENT:
        return False
    else:
        return True

def list_image_path_database():
    path_list = []
    for file in os.listdir(DataFolder):
        if file.endswith(".tif") or file.endswith(".png"):
            path_list.append(os.path.join(DataFolder, file))
    return path_list

def getLabelFromDatabase(path_image):
    try :
        text_file = path_image[:-4]+".gt.txt"
        if os.path.exists(path_image):
            txt_file = open(text_file, "r", encoding="utf-8")
            text = txt_file.read()
            txt_file.close()
            return text
        else:
            return -1

    except :
        return -1

