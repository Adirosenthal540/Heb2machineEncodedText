import Controller
import ImageProcessing
import HandwrittenDoc
import ModelTesseract
import DataManager
import config
import cv2 as cv
import numpy as np
import os, math
from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image

def Status_program(i):
    switcher={
        0: "Create data" ,
        1: "Extract text" ,
        }
    return switcher.get(i, " ")

def maessage_type(i):
    switcher={
        0: "information" ,
        1: "warning" ,
        2: "error"
        }
    return switcher.get(i, " ")

def insertDocuments(i):
    switcher={
        "Scanned":0  ,
        "Labeled":1 ,
        }
    return switcher.get(i, " ")

HOME_DIRECTORY = config.get_home_directory()
HELP_TEXT_DOC_CREATE = os.path.join(HOME_DIRECTORY, "code\help_create.txt")
HELP_TEXT_DOC_EXTRACT = os.path.join(HOME_DIRECTORY, "code\help_extract.txt")
IMAGE_WIDTH_TO_SHOW = 600
IMAGE_HEIGHT_TO_SHOW = 600

INPUT_NUM_TRYS = 2
POPPLER_PATH = config.get_poppler_path()

original_image_array_show = []
images_numpy_array = []
images_numpy_array_show = []
imageTK_list = []
images_path_list = []
original_image_array = []
LABEL = ":תיוג"
TEXT_ENTRY_LABEL = "כתוב את הטקסט שבתמונה :"
writerID = ""
points = []
images_path_list = []
images = []
txt_file = []
delete_files = []
modelName = None
controller_program = None
global root

def reset_global_parameters():
    global folder_selected, markTextArea, markTextArea, images, original_image_array_show, images_numpy_array
    global images_numpy_array_show, imageTK_list, original_image_array
    global  scannedInsertDocuments, delete_files, txtFiles, points,images_path_list, status_program
    folder_selected = ""
    markTextArea = False
    status_program = None
    scannedInsertDocuments = None
    txtFiles = []
    points = []
    images =[]
    images_path_list = []
    original_image_array_show = []
    images_numpy_array = []
    images_numpy_array_show = []
    imageTK_list = []
    original_image_array = []


def popup_message(message, type):
    if type.lower() == "information":
        response = messagebox.showinfo("information", message)
    elif type.lower() == "error":
        response = messagebox.showerror("ERROR", message)
    elif type.lower() == "warning":
        response = messagebox.showwarning("WARNING", message)


def foward_label():
    global entrylabel, newLabeleForTrain, numImageLine, button_foward, statuslabel, my_image_line, button_backward, root_setLabel
    global image_list_tolabel, countImageGotLabel, button_saveImage

    entrylabel.delete(0, END)
    numImageLine += 1

    if newLabeleForTrain[numImageLine] != "":
        entrylabel.insert(0, newLabeleForTrain[numImageLine])
        button_saveImage = Button(root_setLabel, text="Save the image with this label", padx=70, pady=20,
                                  command=saveImagelabel, bg="medium sea green")
        button_saveImage.grid(row=4, column=1)
    else:
        button_saveImage = Button(root_setLabel, text="Save the image with this label", padx=70, pady=20,
                                  command=saveImagelabel)
        button_saveImage.grid(row=4, column=1)

    my_image_line = Label(root_setLabel, image=image_list_tolabel[numImageLine], width=IMAGE_WIDTH_TO_SHOW, height = IMAGE_HEIGHT_TO_SHOW/2)
    my_image_line.grid(row=2, column=1, columnspan=1)

    statuslabel = Label(root_setLabel, text="Image "+str(numImageLine+1)+" of " + str(len(newLabeleForTrain))+", "+str(countImageGotLabel)+" images got labeled", bd=1, relief=SUNKEN)
    statuslabel.grid(row=6, column=0, columnspan=3)

    if numImageLine < len(newLabeleForTrain)-1:
        button_foward = Button(root_setLabel, text=">>", padx=70, pady=20, command= foward_label, fg="black")
    else:
        button_foward = Button(root_setLabel, text=">>", padx=70, pady=20, state = DISABLED)
    button_backward = Button(root_setLabel, text="<<", padx=70, pady=20, command=backward_label, fg="black")
    button_foward.grid(row=2, column=2)
    button_backward.grid(row=2, column=0)


def backward_label():
    global entrylabel, newLabeleForTrain, numImageLine, button_backward, statuslabel, my_image_line, button_foward, root_setLabel
    global image_list_tolabel, newLabeleForTrain, countImageGotLabel, button_saveImage, newLabeleForTrain

    numImageLine -= 1
    entrylabel.delete(0, END)
    if newLabeleForTrain[numImageLine] != "":
        entrylabel.insert(0, newLabeleForTrain[numImageLine])
        button_saveImage = Button(root_setLabel, text="Save the image with this label", padx=70, pady=20,
                                  command=saveImagelabel, bg="medium sea green")
        button_saveImage.grid(row=4, column=1)
    else:
        button_saveImage = Button(root_setLabel, text="Save the image with this label", padx=70, pady=20,
                                  command=saveImagelabel)
        button_saveImage.grid(row=4, column=1)


    my_image_line = Label(root_setLabel, image=image_list_tolabel[numImageLine], width=IMAGE_WIDTH_TO_SHOW, height = IMAGE_HEIGHT_TO_SHOW/2)
    my_image_line.grid(row=2, column=1, columnspan=1)

    statuslabel = Label(root_setLabel, text="Image "+str(numImageLine+1)+" of " + str(len(newLabeleForTrain))+", "+str(countImageGotLabel)+" images got labeled", bd=1, relief=SUNKEN)
    statuslabel.grid(row=6, column=0, columnspan=3)

    if numImageLine > 0:
        button_backward = Button(root_setLabel, text="<<", padx=70, pady=20, command=backward_label, fg="black")
    else:
        button_backward = Button(root_setLabel, text="<<", padx=70, pady=20, state=DISABLED)
    button_foward = Button(root_setLabel, text=">>", padx=70, pady=20, command= foward_label, fg="black")
    button_foward.grid(row=2, column=2)
    button_backward.grid(row=2, column=0)


def saveImagelabel():
    global entrylabel, newLabeleForTrain, numImageLine, root_setLabel, image_list_tolabel, button_saveImage
    global countImageGotLabel, statuslabel
    if entrylabel.get()!="":
        if newLabeleForTrain[numImageLine] == "":
            countImageGotLabel += 1
        newLabeleForTrain[numImageLine] = entrylabel.get()
    else:
        popup_message("ERROR - didn't insert any label for the image, try again", maessage_type(2))
        return
    button_saveImage = Button(root_setLabel, text="Save the image with this label", padx=70, pady=20, command = saveImagelabel, bg = "medium sea green")
    button_saveImage.grid(row=4, column=1)

    statuslabel = Label(root_setLabel, text="Image "+str(numImageLine+1)+" of " + str(len(newLabeleForTrain))+", "+str(countImageGotLabel)+" images got labeled", bd=1, relief=SUNKEN)
    statuslabel.grid(row=6, column=0, columnspan=3)

def insert_new_labeled_image():
    global newLabeleForTrain, root_setLabel, image_list_tolabel, origin_line_images_array, controller_labeled
    handwrite_ID = controller_labeled.image_processing_list[0].handwrite_ID
    print(handwrite_ID)
    imagesInsertDatabase =[]
    count = 0
    for i in range(len(newLabeleForTrain)):
        if newLabeleForTrain[i] != "":
            count += 1
            root_setLabel.destroy()
            imagesInsertDatabase.append(ImageProcessing.ImageProcessing(origin_line_images_array[i], Label = newLabeleForTrain[i] ,imagePath = None, handwrite_ID = handwrite_ID))
    if count >0 :
        controller_labeled.insert_data_to_dataBase(imagesInsertDatabase)
    else:
        popup_message("No data to insert", maessage_type(2))

    root_setLabel.destroy()


def userSetLabel(line_images_array, controller):
    global image_list_tolabel, imageTK, origin_line_images_array, entrylabel, numImageLine
    global newLabeleForTrain, root_setLabel, button_saveImage, controller_labeled
    global label_title, label_description, countImageGotLabel, statuslabel
    top = Toplevel()
    top.title("Set labels for new handwriting lines")
    controller_labeled = controller
    numImageLine = 0
    countImageGotLabel = 0
    print(len(line_images_array))
    print(controller.labels)
    if controller.labels!=None:
        lines_txt = controller.labels.split('\n')
        while "" in lines_txt:
            lines_txt.remove("")
        print(lines_txt)
        print(lines_txt)
        if len(line_images_array) == len(lines_txt):
            newLabeleForTrain = lines_txt
            countImageGotLabel =  len(lines_txt)
        else:
            newLabeleForTrain = [""] * len(line_images_array)
    else:
        newLabeleForTrain = [""] * len(line_images_array)
    print(newLabeleForTrain)
    print(len(line_images_array))
    image_list_tolabel =[]

    origin_line_images_array = line_images_array.copy()
    root_setLabel = top

    for image_array in line_images_array:
        widthImage_edit, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
        image_array = cv.resize(image_array, (widthImage_edit, height))
        imageTK = ImageTk.PhotoImage(Image.fromarray(image_array))
        image_list_tolabel.append(imageTK)

    label_title = Label(root_setLabel, text="write the label for this handwrite line", font=("Ariel", 16))
    label_title.grid(row=0, column=0, columnspan=3)
    label_description = Label(root_setLabel, text="***Be sure to write without errors and pay attention to punctuation***" )
    label_description.grid(row=1, column=0, columnspan=3)

    my_image_line = Label(root_setLabel, image=image_list_tolabel[0], width=IMAGE_WIDTH_TO_SHOW, height = IMAGE_HEIGHT_TO_SHOW/2)
    my_image_line.grid(row=2, column=1, columnspan=1)

    if numImageLine < len(line_images_array)-1:
        button_foward = Button(root_setLabel, text=">>", padx=70, pady=20, command= foward_label, fg="black")
    else:
        button_foward = Button(root_setLabel, text=">>", padx=70, pady=20, state = DISABLED)

    button_backward = Button(root_setLabel, text="<<", padx=70, pady=20, state = DISABLED, fg="black")

    button_foward.grid(row=2, column=2)
    button_backward.grid(row=2, column=0)

    entrylabel = Entry(root_setLabel, borderwidth=5, justify='right', width = 80)
    entrylabel.grid(row=3, column=0, columnspan = 2, sticky= E )
    label_entery = Label(root_setLabel, text=TEXT_ENTRY_LABEL, anchor = "w")
    label_entery.grid(row=3, column=3)

    if newLabeleForTrain[numImageLine] != "":
        entrylabel.insert(0, newLabeleForTrain[numImageLine])
    button_saveImage = Button(root_setLabel, text="Save the image with this label", padx=70, pady=20,command=saveImagelabel)
    button_saveImage.grid(row=4, column=1)


    button_insert_labeled_images = Button(root_setLabel, text="Insert into database", padx=70, pady=20, command = insert_new_labeled_image)
    button_insert_labeled_images.grid(row=5, column=0, columnspan = 3)

    statuslabel = Label(root_setLabel, text="Image 1 of " + str(len(line_images_array))+", "+str(countImageGotLabel)+" images got labeled", bd=1, relief=SUNKEN)
    statuslabel.grid(row=6, column=0, columnspan=3)

    root_setLabel.mainloop()




def CheckImage(file):
    valid_images = [".jpg", ".gif", ".png", ".tif", ".tiff"]
    ext = os.path.splitext(file)[1]
    if ext.lower() not in valid_images:
        return False
    else:
        return True

# check if the path has chars in hebrew
def checkPath(path):
    for chr in path:
        if ord(chr) > 1488 and ord(chr) < 1514:
            popup_message("Error - the path has chars in hebrew", maessage_type(2))
            return False
    return True

def CheckPDF(file):
    ext = os.path.splitext(file)[1]
    if ext.lower() =='.pdf':
        return True
    else:
        return False

# The Image of the training will be extract to same path where it save
def ExtractImagesFromPDF(file, files):
    global delete_files, writerID
    order = HandwrittenDoc.check_PDF_name(file)
    if POPPLER_PATH!= None:
        images = convert_from_path(file, fmt="jpeg", poppler_path =POPPLER_PATH)
    else:
        images = convert_from_path(file, fmt="jpeg")
    outputpath, namefile = os.path.split(file)
    i = 0
    for image in images:
        # image = Image.open(im)
        new_path_image = os.path.join(outputpath, writerID +"_"+ str(order[i]) + ".tif")
        j=0
        while (new_path_image in files):
            new_path_image = os.path.join(outputpath, writerID + "_"+str(j)+"_" + str(order[i]) + ".tif")
            j += 1
        i += 1
        image.save(new_path_image, 'TIFF')
        files.append(new_path_image)
        delete_files.append(new_path_image)
    return files

# the func save all the paths of the images and text files(optional)
# input: path of a folder,  scanned = false if want to find also text files
# output: list of all the images ans text files
def Extract_files_from_folder(folder):
    imagesInFolder = []
    txtFiles = []
    files = os.listdir(folder)
    flag = 0
    for file in files:
        if (CheckImage(file) == False) :
            if (CheckPDF(file) == True ):
                files = files + ExtractImagesFromPDF(os.path.join(folder,file), files)
            continue
        else:
            if not HandwrittenDoc.Check_image_name(file):
                namefile = os.path.basename(file)
                popup_message("WRONG INPUT IMAGE NAME - "+namefile,  maessage_type(1))
                continue
        imagesInFolder.append(os.path.join(folder, file))

    return imagesInFolder, txtFiles


def deleteFiles():
    global delete_files
    for file in delete_files:
        os.remove(file)
    delete_files = []

def openFolder():
    global frame_scanned_label, folder_selected, frame, root, run_Button, frameMarkRun, selectfolder_Button
    frameMarkRun = Frame(root,  bg= "steel blue")
    frameMarkRun.grid(row=5, column=0, columnspan=2)

    selectfolder_Button = Button(frame_scanned_label, text="Open Folder with your scanned pages (PDF \ Image formats)",
                                 font=("Ariel,12"), bg = "medium sea green", width=45, padx=10, pady=20, state = DISABLED)
    selectfolder_Button.grid(row=1, column=0, columnspan=2)

    root.withdraw()
    folder_selected = filedialog.askdirectory()
    root.deiconify()
    if not checkPath(folder_selected):
        Select_train_test(0)
    mylabel_folder = Label(frame_scanned_label, text=folder_selected,  bg= "steel blue")
    mylabel_folder.grid(row=2, column=0, columnspan = 2)
    run_Button = Button(frameMarkRun, text = "RUN", command = run_program, font=("Ariel,14"),width = 40, pady=5).grid(row=1, column=0, columnspan = 2)


def checkID(writerID):
    if writerID == "":
        return False
    if len(writerID)>9 or ord(writerID[0]) < 49 or ord(writerID[0]) >= 60:
        return False
    return True

def enterID():
    global e, writerID
    writerID =  e.get()
    if not checkID(writerID):
        popup_message("You enter wrong ID, Try Again", maessage_type(2))
        return -1
    #popup_message("succeeded", maessage_type(0))
    return e.get()


def clicked_Radiobutton(value):
    global frame, frame_scanned_label, folder_selected, open_image_Button, images, Radiobutton1, Radiobutton2
    global folder_selected, scannedInsertDocuments, frameExtract, frameMarkRun, e, selectfolder_Button
    images = []
    frameMarkRun.destroy()
    frameExtract.destroy()
    frame_text.destroy()

    frame_scanned_label.destroy()
    frame_scanned_label = Frame(frame,  bg= "steel blue")
    frame_scanned_label.grid(row=4, column=0, columnspan=2)

    folder_selected = ""

    if value ==insertDocuments("Scanned"):

        scannedInsertDocuments = True
        selectfolder_Button = Button(frame_scanned_label, text="Open Folder with your scanned pages (PDF \ Image formats)",font=("Ariel,12"),width = 45,padx = 10, pady = 20,  command=openFolder)
        selectfolder_Button.grid(row=1, column=0, columnspan=2)
    elif value ==insertDocuments("Labeled"):
        scannedInsertDocuments = False
        open_image_Button = Button(frame_scanned_label, text="Open Image of your handwrite ", font=("Ariel,12"), width = 40, pady=20, command=get_image)
        open_image_Button.grid(row=1, column=0, columnspan=2)

    Radiobutton1 = Radiobutton(frame, text = "Scanned handwrite images",  bg= "steel blue",font = ("Ariel", 12), value = 0, state = DISABLED)
    Radiobutton2 = Radiobutton(frame, text = "Create your labeled handwrite data",  bg= "steel blue", font = ("Ariel", 12), value = 1, state = DISABLED)
    Radiobutton1.grid(row=3, column=0)
    Radiobutton2.grid(row=3, column=1)
    e = Entry(frame_scanned_label, width=40, borderwidth=5)
    enterIDLabel = Label(frame_scanned_label, text="Enter writer ID :", fg="black",font=("Ariel,10"), bg = "steel blue", width=15, padx=10, pady=10,)
    enterIDLabel.grid(row=3,column = 0, sticky = "e")
    e.grid(row=3, column=1)
    mainloop()

def Popup_Mark_the_text():
    global markTextArea
    response = messagebox.askyesno("Mark the text", "Do you wont to select the area of the text on the documents?")
    markTextArea = response

def chooseScannedOrLabeled():
    global mylabel_radio, clicked, frame, frame_scanned_label
    frame_scanned_label = Frame(frame,  bg= "steel blue")
    frame_scanned_label.grid(row=4, column =0, columnspan = 2)
    r = IntVar()
    r.set("1")
    myLabel = Label(frame, text="Colecting data for training tesseract",  bg= "steel blue", font = ("Ariel", 14))
    Radiobutton1 = Radiobutton(frame, text = "Scanned handwrite images",  bg= "steel blue",font = ("Ariel", 12), variable = r, value = 0, command = lambda:clicked_Radiobutton(r.get()))
    Radiobutton2 = Radiobutton(frame, text = "Create your labeled handwrite data",  bg= "steel blue", font = ("Ariel", 12), variable = r, value = 1, command = lambda:clicked_Radiobutton(r.get()))
    Radiobutton1.grid(row=3, column=0)
    Radiobutton2.grid(row=3, column=1)
    myLabel.grid(row=0, column=0, columnspan =2)
    frame.mainloop()

# show the image that was selecr=ted for "extract text" process
def show_image():
    global frameExtract, flag_show, canvas_image, images_path_list, imageTK_list, show_image_butten, hide_image_butten
    imageTK = imageTK_list[0]
    canvas_image = Canvas(frameExtract, width = imageTK.width(), height = imageTK.height())
    canvas_image.grid(row=1, column=0, columnspan=2)

    canvas_image.create_image((0,0) , image = imageTK, anchor="nw")
    flag_show = 0

    show_image_butten = Button(frameExtract, text="show image", state=DISABLED, font=("Ariel,10"), width = 20, pady=5).grid(row=0, column=0)
    hide_image_butten = Button(frameExtract, text="hide image", command=hide_image, font=("Ariel,10"), width = 20, pady=5).grid(row=0, column=1)

def hide_image():
    global frameExtract, canvas_image, show_image_butten, hide_image_butten
    canvas_image.delete('all')
    canvas_image.grid_forget()
    show_image_butten = Button(frameExtract, text="show image", command=show_image, font=("Ariel,10"), width = 20, pady=5).grid(row=0, column=0)
    hide_image_butten = Button(frameExtract, text="hide image", state=DISABLED, font=("Ariel,10"), width = 20, pady=5).grid(row=0, column=1)

# def slide_uper_th( root):
#     global imageTK_, my_label2, horizontal2, btn_THRESH_BINARY_uper, choosenImage, choosenImage_originsize
#     global my_image_label, original
#
#     image_array = original.copy()
#     width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
#     image_array = cv.resize(image_array, (width, height))
#
#     _, th = cv.threshold(image_array, horizontal2.get(), 255, cv.THRESH_BINARY)
#     _, th2 = cv.threshold(original.copy(), horizontal2.get(), 255, cv.THRESH_BINARY)
#     image_array = cv.bitwise_xor(choosenImage, th, mask=None)
#     choosenImage_originsize = cv.bitwise_xor(choosenImage_originsize, th2, mask=None)
#
#     image_fromarray = Image.fromarray(image_array)
#     imageTK_ = ImageTk.PhotoImage(image_fromarray)
#     my_image_label = Label(root, image=imageTK_)
#     my_image_label.grid(row=1, column=0, rowspan = 5)

def slide_threshold(image_array, root):
    global imageTK_, my_image_label, choosenImage, horizontal, btn_dilation, btn_opening, btn_closing, choosenImage_originsize
    global my_label2, horizontal2, btn_THRESH_BINARY_uper, images_numpy_array, btn_removeNoise, btn_erosion

    _, th = cv.threshold(image_array, horizontal.get(), 255, cv.THRESH_BINARY)
    choosenImage_originsize = images_numpy_array[0].copy()
    _, choosenImage_originsize = cv.threshold(choosenImage_originsize, horizontal.get(), 255, cv.THRESH_BINARY)

    image_array = th.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    choosenImage = image_array.copy()

    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

    # horizontal2 = Scale(root, from_ = horizontal.get(), to =  255, orient = HORIZONTAL)
    # horizontal2.grid(row = 2, column = 2)
    # my_label2 = Label(root, text = "Choose uper value :")
    # my_label2.grid(row = 2, column = 1)
    # btn_THRESH_BINARY_uper = Button(root, text = "click", command = lambda: slide_uper_th( root)).grid(row = 2, column = 3)

    btn_dilation = Button(root, text = "dilation", command = lambda: dilation(root)).grid(row = 4, column = 3)
    btn_opening = Button(root, text = "opening", command = lambda: opening(root)).grid(row = 4, column = 2)
    btn_closing = Button(root, text = "closing", command = lambda: closing(root)).grid(row = 4, column = 1)
    btn_removeNoise = Button(root, text = "remove noise", command = lambda: removeNoise(root)).grid(row = 3, column = 1)
    btn_erosion = Button(root, text="erosion", command=lambda: erosion(root)).grid(row=3, column=2)

def get_original(root):
    global my_image_label, original, imageTK_, choosenImage, choosenImage_originsize, images_numpy_array, top_edit
    choosenImage_originsize = images_numpy_array[0].copy()

    image_array = original.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    choosenImage = image_array.copy()

    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)

    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

def save_edit_image():
    global choosenImage, top_edit, isTrain, root, scannedInsertDocuments, writerID, controller_program
    global images_numpy_array_show, images_numpy_array, imageTK_list, choosenImage_originsize
    print (choosenImage)
    images_numpy_array_show[0] = choosenImage
    images_numpy_array[0] = choosenImage_originsize

    imageTK_list[0] = ImageTk.PhotoImage(Image.fromarray(images_numpy_array_show[0]))
    if isTrain:
        images.append(ImageProcessing.ImageProcessing(images_numpy_array[0], imagePath=images_path_list[0],handwrite_ID=writerID))
    else:
        images.append(ImageProcessing.ImageProcessing(images_numpy_array[0], imagePath=images_path_list[0],handwrite_ID="result"))

    controller_program = Controller.Controller(isTrain, images, root, isScanned = scannedInsertDocuments, modelName=modelName)
    top_edit.destroy()
    result = controller_program.main()

    showResults(root, result)


def dilation(root):
    global my_image_label, original, imageTK_, choosenImage, btn_dilation, choosenImage_originsize, top_edit
    image_array = choosenImage.copy()
    kernal = np.ones((2, 2), np.uint8)
    dilation = cv.dilate(image_array, kernal, iterations=1)

    choosenImage_originsize = cv.dilate(choosenImage_originsize, kernal, iterations=3)
    image_array = dilation.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))

    choosenImage = image_array.copy()
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

def opening(root):
    global my_image_label, original, imageTK_, choosenImage, btn_dilation, btn_opening, choosenImage_originsize, top_edit
    image_array = choosenImage.copy()
    kernal = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(image_array, cv.MORPH_OPEN, kernal)
    choosenImage_originsize = cv.morphologyEx(choosenImage_originsize, cv.MORPH_OPEN, kernal)
    image_array = opening.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    choosenImage = image_array.copy()
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

def closing(root):
    global my_image_label, original, imageTK_, choosenImage, btn_closing, choosenImage_originsize, top_edit
    image_array = choosenImage.copy()
    kernal = np.ones((2, 2), np.uint8)
    closing = cv.morphologyEx(image_array, cv.MORPH_CLOSE, kernal)
    choosenImage_originsize = cv.morphologyEx(choosenImage_originsize, cv.MORPH_CLOSE, kernal)
    image_array = closing.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    choosenImage = image_array.copy()
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

def removeNoise(root):
    global my_image_label, original, imageTK_, choosenImage, btn_removeNoise, choosenImage_originsize, top_edit
    image_array = choosenImage.copy()
    remove_noise = cv.medianBlur(image_array, 3)
    choosenImage_originsize = cv.medianBlur(choosenImage_originsize, 3)
    image_array = remove_noise.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    choosenImage = image_array.copy()
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

def erosion(root):
    global my_image_label, original, imageTK_, choosenImage, btn_removeNoise, choosenImage_originsize, top_edit, btn_erosion
    image_array = choosenImage.copy()
    kernal = np.ones((2, 2), np.uint8)
    erode = cv.erode(image_array, kernal, iterations=1)
    choosenImage_originsize = cv.medianBlur(choosenImage_originsize, 3)
    image_array = erode.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    choosenImage = image_array.copy()
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan=5)

def userChooseTresholds(image_array, root):
    global horizontal, choosenImage, choosenImage_originsize, original, my_image_label, imageTK_, get_original_button
    global btn_dilation, btn_opening, btn_closing, top_edit, images_numpy_array, btn_THRESH_BINARY_uper, btn_removeNoise, btn_erosion

    horizontal = Scale(root, from_ =  0, to =  255, orient = HORIZONTAL)
    horizontal.grid(row = 1, column = 2)
    my_label = Label(root, text = "choose value for\n THRESH_BINARY: ")
    my_label.grid(row = 1, column = 1)

    #image_array = cv.imread(image_path, 0)
    choosenImage_originsize = images_numpy_array[0].copy()

    original = image_array.copy()

    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    choosenImage = image_array.copy()

    root.geometry(str(width + 300) + "x" + str(height + 100))

    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_title = Label(root, text = "Find the best variation of your image to extracting text", font=("Ariel", 16))
    my_title.grid(row = 0, column = 0, columnspan = 5)

    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

    btn_THRESH_BINARY = Button(root, text = "click", command = lambda: slide_threshold(original.copy(), root)).grid(row = 1, column = 3)

    btn_dilation = Button(root, text = "dilation", state = DISABLED).grid(row = 4, column = 3)
    btn_opening = Button(root, text = "opening", state = DISABLED).grid(row = 4, column = 2)
    btn_closing = Button(root, text = "closing", state = DISABLED).grid(row = 4, column = 1)
    btn_removeNoise = Button(root, text = "remove noise", state = DISABLED).grid(row = 3, column = 1)
    btn_erosion = Button(root, text = "erosion", state = DISABLED).grid(row = 3, column = 2)
    get_original_button = Button(root, text = "click to original", command = lambda: get_original(root), width = 25).grid(row = 5, column = 1, columnspan = 3)
    save_image_button = Button(root, text="Click here to run program on this image", command=save_edit_image).grid(row=8, column=0, columnspan = 4)
    root.mainloop()

def EditImage():
    global images_numpy_array_show, images_numpy_array
    global choosenImage, original, root, top_edit
    top_edit = Toplevel()
    top_edit.title("Edit you image")
    userChooseTresholds(images_numpy_array[0].copy(), top_edit)


def get_image():
    global root, frame, clicked, options, flag_show, frameExtract, frameMarkRun, imageTK_list, images_path_list, open_image_Button, insert_image_button
    global original_image_array, images_numpy_array, images_numpy_array_show, show_image_button, hide_image_button, original_image_array_show, isTrain
    images_path_list = []
    imageTK_list = []
    images_numpy_array_show = []
    images_numpy_array =[]
    frameExtract.destroy()
    frameExtract = Frame(frame,  bg= "steel blue")
    frameMarkRun = Frame(root,  bg= "steel blue")

    frameMarkRun.grid(row=6, column=0, columnspan=2)
    frameExtract.grid(row=5, column=0, columnspan=2)

    if status_program == Status_program(0):
        open_image_Button = Button(frame_scanned_label, text="Open Image of your handwrite ",font=("Ariel,12"),width = 40,
                                   padx=10, pady=20, state = DISABLED, bg = "medium sea green", bd = 5, relief = RIDGE)
        open_image_Button.grid(row=1,column = 0, columnspan=2)
    else:
        insert_image_button = Button(frame, text="Open image", bg = "medium sea green",font=("Ariel,12"),
                                     width = 40, bd = 5, relief = RIDGE, padx=10, pady=20,  state = DISABLED).grid(row=2, column=0, columnspan=2)
    flag_show = 1
    root.filename = filedialog.askopenfilename(title="select a file", filetype=(("ALL FILES", "*.*"),("JPEG", "*.jpg"),("PNG", "*.png"), ("TIF", "*.tif")))

    if not checkPath(root.filename):
        Select_train_test(0)
    images_path_list.append(root.filename)

    image_array = cv.imread(images_path_list[0], 0)
    original_image_array.append(image_array.copy())
    images_numpy_array.append(image_array.copy())
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    images_numpy_array_show.append(image_array)
    original_image_array_show = images_numpy_array_show.copy()
    imageTK_list.append(ImageTk.PhotoImage(Image.fromarray(image_array)))

    show_image_button = Button(frameExtract, text="show image", command=show_image, font=("Ariel,10"), width = 20, pady=5).grid(row=0, column=0)
    hide_image_button = Button(frameExtract, text="hide image", state=DISABLED, font=("Ariel,10"), width = 20, pady=5).grid(row=0, column=1)
    run_Button = Button(frameMarkRun, text="RUN", command=run_program, font=("Ariel,14"),width = 40, pady=5).grid(row=1, column=0, columnspan = 2)


def Select_train_test(var):
    global myLabel, clicked, frame, options, root, status_program, image_label, frameExtract, frameMarkRun, frame_text
    global insert_image_button
    reset_global_parameters()
    frame.destroy()
    frameMarkRun.destroy()
    frameExtract.destroy()
    frame_text.destroy()
    value = clicked.get()
    frame = Frame(root,  bg= "steel blue")
    frame.grid(row=3, column=0, columnspan=2)

    if value == Status_program(0):

        status_program = Status_program(0)
        myLabel = Label(frame, text="Collecting data for training tesseract").grid(row=0, column =0, columnspan = 2)

        drop = OptionMenu(root, clicked, *options, command=Select_train_test)
        drop.config(width=30, font=('Ariel, 14'))
        drop.grid(row=1, column=0, columnspan = 2)
        chooseScannedOrLabeled()

    if value == Status_program(1):
        status_program = Status_program(1)
        myLabel = Label(frame, text="Run tesseract on the lateset training machine", bg= "steel blue",
                        font = ("Ariel", 14)).grid(row=0,  column =0, columnspan = 2)
        drop = OptionMenu(root, clicked, *options, command=Select_train_test)
        drop.config(width=30, font=('Ariel, 14'))
        drop.grid(row=1, column=0, columnspan = 2)
        insert_image_button = Button(frame, text="Open image", command=get_image, font=("Ariel,12"), width = 40, padx=10,
                                     pady=20).grid(row=2, column=0, columnspan = 2)
    frame.mainloop()



def remove_checkData():
    global my_image_check_data, button_eccept, button_remove, status, bad_Images_num, image_list, root_checkData
    global num_image_checkData, path_list_checkData
    if num_image_checkData not in bad_Images_num:
        bad_Images_num.append(num_image_checkData)

    button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=remove_checkData, fg="black", bg="red", bd = 5, relief = RIDGE)
    button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=eccept_checkData, fg="black",bg="medium sea green")
    button_remove.grid(row = 5, column = 1)
    button_eccept.grid(row = 5, column = 2)

def eccept_checkData():
    global my_image_check_data, button_eccept, button_remove, status, good_Image, bad_Images_num, image_list, root_checkData
    global num_image_checkData, path_list_checkData

    if num_image_checkData in bad_Images_num:
        bad_Images_num.remove(num_image_checkData)

    button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=remove_checkData, fg="black", bg="red")
    button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=eccept_checkData, fg="black",bg="medium sea green", bd = 5, relief = RIDGE)
    button_remove.grid(row = 5, column = 1)
    button_eccept.grid(row = 5, column = 2)

def foward_check():
    global my_image_check_data, button_eccept, button_remove, status, image_list, root_checkData, num_image_checkData
    global path_list_checkData

    num_image_checkData += 1

    my_image_check_data.grid_forget()
    my_image_check_data = Label(root_checkData, image=image_list[num_image_checkData], width  = IMAGE_WIDTH_TO_SHOW)
    my_image_check_data.grid(row = 0, column = 1, columnspan = 2)
    if num_image_checkData == len(image_list)-1 :
        foward_check_btn = Button(root_checkData, text=">>", padx=70, pady=20, state=DISABLED, fg="black")
    else:
        foward_check_btn = Button(root_checkData, text=">>", padx=70, pady=20, command= foward_check,
                             fg="black")

    backward_check_btn = Button(root_checkData, text="<<", padx=70, pady=20, command = backward_check, fg="black")
    foward_check_btn.grid(row = 0, column = 3)
    backward_check_btn.grid(row = 0, column = 0)

    button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=remove_checkData, fg="black", bg="red")
    button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=eccept_checkData, fg="black",bg="medium sea green")
    button_remove.grid(row = 5, column = 1)
    button_eccept.grid(row = 5, column = 2)

    label_image_name = DataManager.getLabelFromDatabase(path_list_checkData[num_image_checkData])
    if label_image_name == -1:
        popup_message("The text file of image - " + os.path.basename(path_list_checkData[num_image_checkData]) + " not found",
                      maessage_type(2))
        label_image_name = "ERROR"

    my_label_check_data = Label(root_checkData, text=label_image_name, anchor=CENTER)
    my_label_check_data.grid(row=4, column=0, columnspan=4, sticky="ew")

    status = Label(root_checkData, text="Image "+str(num_image_checkData+1)+" of " + str(len(image_list)), bd=1, relief=SUNKEN)
    status.grid(row=6, column=0, columnspan=4)


def backward_check():
    global my_image_check_data, button_eccept, button_remove, status, image_list, root_checkData, num_image_checkData
    global path_list_checkData

    num_image_checkData -= 1

    my_image_check_data.grid_forget()
    my_image_check_data = Label(root_checkData, image=image_list[num_image_checkData], width=IMAGE_WIDTH_TO_SHOW)
    my_image_check_data.grid(row=0, column=1, columnspan=2)
    if num_image_checkData == 0:
        backward_check_btn = Button(root_checkData, text="<<", padx=70, pady=20, state=DISABLED, fg="black")
    else:
        backward_check_btn = Button(root_checkData, text="<<", padx=70, pady=20, command=backward_check, fg="black")

    foward_check_btn = Button(root_checkData, text=">>", padx=70, pady=20, command=foward_check,fg="black")

    foward_check_btn.grid(row=0, column=3)
    backward_check_btn.grid(row=0, column=0)

    button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=remove_checkData, fg="black", bg="red")
    button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=eccept_checkData, fg="black",bg="medium sea green")
    button_remove.grid(row = 5, column = 1)
    button_eccept.grid(row = 5, column = 2)

    label_image_name = DataManager.getLabelFromDatabase(path_list_checkData[num_image_checkData])
    if label_image_name == -1:
        popup_message(
            "The text file of image - " + os.path.basename(path_list_checkData[num_image_checkData]) + " not found",
            maessage_type(2))
        label_image_name = "ERROR"

    my_label_check_data = Label(root_checkData, text=label_image_name, anchor=CENTER)
    my_label_check_data.grid(row=4, column=0, columnspan=4, sticky="ew")

    status = Label(root_checkData, text="Image " + str(num_image_checkData + 1) + " of " + str(len(image_list)), bd=1,
                   relief=SUNKEN)
    status.grid(row=6, column=0, columnspan=4)

def exit_program(root):
    root.destroy()
    exit()

def exit_check_data(root):
    global bad_Images_num, path_list_checkData
    root.destroy()
    imageToDel = []
    for i in range (len(bad_Images_num)):
        imageToDel.append(path_list_checkData[bad_Images_num[i]])

    if imageToDel!=[]:
        popup_message("Deleted "+str(len(imageToDel))+" images, thank you", maessage_type(0))
        DataManager.delete_from_database(imageToDel)


    else:
        popup_message("All the Images got into the database, THANK YOU :)", maessage_type(0))
    deleteFiles()

def checkData(path_list, top):
    global my_image_check_data, good_Image, bad_Images_num, image_list, status, root_checkData, backward_check_btn, foward_check_btn
    global my_label_check_data, button_eccept, button_remove, button_exit, num_image_checkData, path_list_checkData
    good_Image = []
    bad_Images_num = []
    image_list = []
    num_image_checkData = 0
    path_list_checkData = path_list
    root_checkData = top
    for image_path in path_list:
        image_array = cv.imread(image_path, 0)
        width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
        image_array = cv.resize(image_array, (width, height))
        imageTK = ImageTk.PhotoImage(Image.fromarray(image_array))

        image_list.append(imageTK)


    my_image_check_data = Label(root_checkData, image = image_list[num_image_checkData], width  = IMAGE_WIDTH_TO_SHOW)
    my_image_check_data.grid(row = 0, column = 1, columnspan = 2)
    if 0 == len(path_list)-1:
        foward_check_btn = Button(root_checkData, text=">>", padx=70, pady=20, state=DISABLED, fg="black")
    else:
        foward_check_btn = Button(root_checkData, text=">>", padx=70, pady=20, command= foward_check, fg="black")

    backward_check_btn = Button(root_checkData, text="<<", padx=70, pady=20, state = DISABLED, fg="black")
    foward_check_btn.grid(row = 0, column = 3)
    backward_check_btn.grid(row = 0, column = 0)
    label_image_name = DataManager.getLabelFromDatabase(path_list[num_image_checkData])
    if label_image_name == -1:
        popup_message("The text file of image - " + os.path.basename(path_list[num_image_checkData]) + " not found", maessage_type(2))
        label_image_name = "ERROR"
    label_title = Label(root_checkData, text = LABEL, anchor = CENTER)
    my_label_check_data = Label(root_checkData, text = label_image_name, anchor = CENTER)
    label_title.grid(row=3, column=0, columnspan=4, sticky = "ew", pady=5)
    my_label_check_data.grid(row=4, column=0, columnspan=4, sticky = "ew")

    button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command= eccept_checkData, fg="black", bg="medium sea green")
    button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command= remove_checkData, fg="black", bg="red")
    button_eccept.grid(row = 5, column = 2)
    button_remove.grid(row = 5, column = 1)

    button_exit = Button(root_checkData, text = "Save and Exit",padx = 30, pady = 20, command = lambda: exit_check_data(root_checkData))
    button_exit.grid(row = 5, column = 0)

    status = Label(root_checkData, text="Image 1 of " + str(len(image_list)), bd=1, relief=SUNKEN)
    status.grid(row=6, column = 0 , columnspan = 4)

    root_checkData.mainloop()
    #return bad_Image

    # if len(image_list) - 1 == 1:
    #     button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=lambda: eccept(1, path_list), fg="black",
    #                            bg="green")
    #     button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=lambda: remove(1, path_list),
    #                            fg="black", bg="red")
    # else:
    #     button_eccept = Button(root_checkData, text="OK", padx=70, pady=20, command=lambda: foward(True, 1, path_list), fg="black", bg="green")
    #     button_remove = Button(root_checkData, text="Error", padx=70, pady=20, command=lambda: foward(False, 1, path_list), fg="black", bg="red")



def new_window_check_database(root):
    path_list = DataManager.list_image_path_database()
    top = Toplevel()
    top.title("check database")
    checkData(path_list, top)


def covert_points_from_resize_to_original(points, resizeImage, originalImage):
    width_resizeImage = resizeImage.shape[1]
    height_resizeImage = resizeImage.shape[0]

    width_originalImage = originalImage.shape[1]
    height_originalImage = originalImage.shape[0]

    new_points = []
    if width_resizeImage == width_originalImage:
        return points
    coeff = width_originalImage / width_resizeImage
    for point in points:
        new_points.append((math.floor(point[0]*(width_originalImage / width_resizeImage)), math.floor(point[1] *coeff)))
    return new_points

def click_CutImage(num_image) :
    global points, file, top2, w, num_image_to_cut, imageTK_list, original_image_array_show, img_toCut, cv_array
    top2 = Toplevel()
    top2.title("Cut image window")
    points = []
    num_image_to_cut = num_image
    w = Canvas(top2, width=IMAGE_WIDTH_TO_SHOW, height=IMAGE_HEIGHT_TO_SHOW)
    cv_array = original_image_array_show[num_image_to_cut].copy()
    img_toCut = ImageTk.PhotoImage(Image.fromarray(cv_array))
    w.create_image(0, 0, image=img_toCut, anchor="nw")
    w.grid(row=0)
    top2.bind("<Button 1>", CutImage)

def CutImage(eventorigin):
    global x, y, points, top2, w, images_path_list, images_numpy_array_show, num_image_to_cut, root_window, img_toCut, cv_array
    global original_image_array, original_image_array_show, my_image
    while(len(points)<4):
        x = eventorigin.x
        y = eventorigin.y
        cv_array = cv.circle(cv_array, (x, y), 3, 0, -1)
        points.append((x, y))
        if len(points) >= 2:
            cv_array = cv.line(cv_array, points[-1], points[-2], 50, 3)

        img_toCut = ImageTk.PhotoImage(Image.fromarray(cv_array))
        w.create_image(0, 0, image=img_toCut, anchor="nw")
        top2.bind("<Button 1>", CutImage)
        top2.mainloop()

    top2.destroy()

    fixed_points = covert_points_from_resize_to_original(points, resizeImage = original_image_array_show[num_image_to_cut], originalImage = original_image_array[num_image_to_cut])
    print(fixed_points)
    print(points)

    images_numpy_array_show[num_image_to_cut] = ImageProcessing.WrapImage(original_image_array_show[num_image_to_cut], np.array(points[0:4]))
    images_numpy_array[num_image_to_cut] = ImageProcessing.WrapImage(original_image_array[num_image_to_cut] , np.array(fixed_points[0:4]))
    imageTK_list[num_image_to_cut] = ImageTk.PhotoImage(Image.fromarray(images_numpy_array_show[num_image_to_cut]))

    status = Label(root_window, text = "Image "+str(num_image_to_cut+1)+" of " + str(len(imageTK_list)), bd =1, relief = SUNKEN)
    my_image.grid_forget()
    my_image = Label(root_window, image = imageTK_list[num_image_to_cut])
    my_image.grid(row = 0, column = 1, columnspan = 3)
    button_exit = Button(root_window, text = "Continue",padx = 70, pady = 20, command = exit_wrap)
    button_wrap = Button(root_window, text = "try again Cut Image",padx = 70, pady = 20, command = lambda: click_CutImage(num_image_to_cut))
    if num_image_to_cut == len(imageTK_list)-1:
        button_next = Button(root_window, text=">>", padx=70, pady=20, state=DISABLED, fg="black")
    else:
        button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(num_image_to_cut + 1),
                             fg="black")

    if num_image_to_cut ==0:
        button_previous = Button(root_window, text="<<", padx=70, pady=20, state = DISABLED, fg="black")
    else:
        button_previous = Button(root_window, text="<<", padx=70, pady=20, command=lambda: back(num_image_to_cut - 1),
                                 fg="black")

    button_exit.grid(row = 1, column = 0)
    button_wrap.grid(row = 1, column = 1,  columnspan = 2)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row = 0, column = 0)
    status.grid(row=3, column = 0 , columnspan = 3)
    root_window.mainloop()

def next( image_number):
    global my_image, button_next, button_previous, status, good_Image, bad_Image, imageTK_list, images_path_list, root_window, button_wrap

    my_image.grid_forget()

    my_image = Label(root_window, image=imageTK_list[image_number])

    if image_number == len(images_path_list) - 1:
        button_next = Button(root_window, text=">>", padx=70, pady=20, state=DISABLED, fg="black")
    else:
        button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(image_number + 1),fg="black")

    button_previous = Button(root_window, text="<<", padx=70, pady=20,command=lambda: back(image_number -1), fg="black")

    status = Label(root_window, text="Image " + str(image_number+1) + " of " + str(len(imageTK_list)), bd=1, relief=SUNKEN)
    button_wrap = Button(root_window, text="Cut Image", padx=70, pady=20, command=lambda: click_CutImage(image_number))

    button_wrap.grid(row=1, column=1, columnspan=2)
    my_image.grid(row=0, column=1, columnspan=3)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row=0, column=0)
    status.grid(row=3, column=0, columnspan=3)


def back( image_number):
    global my_image, button_next, button_previous, status, good_Image, bad_Image, imageTK_list, images_path_list, root_window
    my_image.grid_forget()

    my_image = Label(root_window, image=imageTK_list[image_number])
    button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(image_number + 1), fg="black")

    if image_number == 0:
        button_previous = Button(root_window, text="<<", padx=70, pady=20,state = DISABLED, fg="black")
    else:
        button_previous = Button(root_window, text="<<", padx=70, pady=20, command=lambda: back(image_number - 1), fg="black")

    button_wrap = Button(root_window, text="Cut Image", padx=70, pady=20, command=lambda: click_CutImage(image_number))
    status = Label(root_window, text="Image " + str(image_number +1) + " of " + str(len(imageTK_list)), bd=1, relief=SUNKEN)

    button_wrap.grid(row=1, column=1, columnspan=2)
    my_image.grid(row=0, column=1, columnspan=3)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row=0, column = 0)
    status.grid(row=3, column=0, columnspan=3)

def exit_wrap():
    global root_window
    root_window.destroy()
    run_program(finishWrop = True)

def wrap_data():
    global my_image, imageTK_list, status, root_window, images_numpy_array_show, root_window
    global original_image_array
    root_window = Toplevel()
    root_window.title("Cropp the image")

    status = Label(root_window, text = "Image 1 of " + str(len(imageTK_list)), bd =1, relief = SUNKEN)

    my_image = Label(root_window, image = imageTK_list[0])
    my_image.grid(row = 0, column = 1, columnspan = 3)

    button_exit = Button(root_window, text = "Continue",padx = 70, pady = 20, command = exit_wrap)
    button_wrap = Button(root_window, text = "Cut Image",padx = 70, pady = 20, command = lambda: click_CutImage(0))
    button_next = Button(root_window, text=">>", padx=70, pady=20, command=lambda: next(1), fg="black")
    button_previous = Button(root_window, text="<<", padx=70, pady=20, state = DISABLED, fg="black")

    button_exit.grid(row = 1, column = 0)
    button_wrap.grid(row = 1, column = 1,  columnspan = 2)
    button_next.grid(row = 0, column =4)
    button_previous.grid(row = 0, column = 0)
    status.grid(row=3, column = 0 , columnspan = 3)
    root.mainloop()


def calculate_width_height(image_array, max_width_to_show, max_height_to_show):
    width_original = image_array.shape[1]
    height_original = image_array.shape[0]
    if width_original < max_width_to_show and height_original  < max_height_to_show:
        return width_original, height_original

    if width_original > height_original:
        new_width = max_width_to_show
        new_height = math.floor(height_original * (max_width_to_show / width_original))
    else:
        new_height = max_height_to_show
        new_width = math.floor(width_original * (max_height_to_show / height_original))

    return new_width, new_height

def extractResult(result):
    root.withdraw()
    file_to_save = filedialog.asksaveasfile(mode = "w", defaultextension=".txt", title="insert handriting image")
    if file_to_save is None:
        return
    root.deiconify()
    file_to_save.close()
    print(str(file_to_save.name))
    file_to_save = open(file_to_save.name, "w", encoding="utf-8")
    file_to_save.write(result)
    file_to_save.close()


    popup_message("Secceeded, hope to see you again :)", maessage_type(0))

def showResults(root, result):
    global frame_scanned_label, frame, frame_text, frameMarkRun
    frameMarkRun.destroy()
    if  status_program == Status_program(0):
        popup_message("Data insert into the database, goodbye", maessage_type(0))
    else:
        frame_text = Frame(root, relief =  SUNKEN)

        xscrollbar = Scrollbar(frame_text, orient = HORIZONTAL)
        xscrollbar.grid(row = 2, column = 0, sticky = E+W)

        yscrollbar = Scrollbar(frame_text)
        yscrollbar.grid(row = 0, column = 6, sticky = N + S)
        my_result = Text(frame_text, bg = "lavender", bd = 4, width = 50, height = 10, xscrollcommand = xscrollbar.set )
        my_result.tag_configure('tag-right', justify='right')
        my_result.insert('end', str(result) , 'tag-right')

        scrl = Scrollbar(root, command=my_result.yview)
        my_result.config(yscrollcommand=scrl.set)
        my_result.grid(row=0, column=0, sticky = N+S+E+W)

        frame_text.grid(row=5, column=0, columnspan=2)

        if status_program == Status_program(0) and scannedInsertDocuments:
            popup_message("Secceeded reading the scanned pages and insert into the Database", maessage_type(0))
        elif status_program == Status_program(0):
            popup_message("Secceeded insert the labeled data into the database", maessage_type(0))
        else:
            popup_message("Finish the export of the text from the image - look at the results :)", maessage_type(0))

        try_again_Button = Button(frame_text, text="Try again", command=tryagain).grid(row=1, column=0,columnspan=2,sticky=W + E)
        save_Button = Button(frame_text, text="Extract result", command=lambda: extractResult(result)).grid(row=2, column=0,columnspan=2,sticky=W + E)
        compare_to_real_label_Button = Button(frame_text, text="Compare to real Label", command=lambda: compare_to_real_label(result)).grid(row=3, column=0,columnspan=2,sticky=W + E)

def compare_to_real_label(result):
    global frame_text, insert_real_text, compare_label, root_compare
    root_compare = Toplevel()
    root_compare.title("Compare result to the real label")
    root_compare.geometry(str(IMAGE_WIDTH_TO_SHOW)+"x550")
    root_compare.configure(background = "steel blue")
    compare_label = Label(root_compare, text="Write the real Label for the image:",
                    bg="steel blue", font=("Ariel", 16), width=50, anchor = CENTER)
    compare_label.grid(row = 0, column = 0, columnspan = 3)
    tesseract_result_l = Label(root_compare, text=f"Result using trained tesseract model:",
                    bg="steel blue", font=("Ariel", 10), width=50)
    tesseract_result_l.grid(row = 1, column = 0,  columnspan = 3)
    frame_tesseract_text = Frame(root_compare, relief=SUNKEN)
    yscrollbar = Scrollbar(frame_tesseract_text)
    yscrollbar.grid(row=0, column=6, sticky=N + S)
    my_result = Text(frame_tesseract_text, bg="lavender", bd=4, width=50, height=10)
    my_result.tag_configure('tag-right', justify='right')
    my_result.insert('end', str(result), 'tag-right')
    scrl = Scrollbar(root, command=my_result.yview)
    my_result.config(yscrollcommand=scrl.set)
    my_result.grid(row=0, column=0, sticky=N + S + E + W)
    frame_tesseract_text.grid(row=2, column=0, columnspan=3)
    label_write_real = Label(root_compare, text="Please write the real label of the text :",
                    bg="steel blue", font=("Ariel", 10), width=50)
    label_write_real.grid(row = 3, column = 0, columnspan = 3)
    frame_realtext = Frame(root_compare, relief=SUNKEN)
    xscrollbar = Scrollbar(frame_realtext, orient=HORIZONTAL)
    xscrollbar.grid(row=2, column=0, sticky=E + W)
    yscrollbar = Scrollbar(frame_realtext)
    yscrollbar.grid(row=0, column=6, sticky=N + S)
    insert_real_text = Text(frame_realtext, bg="lavender", bd=4, width=50,height =  10, xscrollcommand=xscrollbar.set)
    #insert_real_text.tag_configure('tag-right', justify='right')
    scrl = Scrollbar(root, command=insert_real_text.yview)
    insert_real_text.config(yscrollcommand=scrl.set)
    insert_real_text.grid(row=0, column=0, sticky=N + S + E + W)
    frame_realtext.grid(row=4, column=0, columnspan = 3)
    calculate_match_btn = Button(root_compare, text="Calculate match", relief=SUNKEN, width = 20, pady = 10,
                                 command=lambda: calcMatch(result))
    calculate_match_btn.grid(row=5, column=1,sticky=W + E)
    root_compare.mainloop()

def insertresult():
    global root_compare, controller_program, userInserLabel
    root_compare.destroy()
    controller_program.setLabels(userInserLabel)
    controller_program.processLabeledImages()

def calcMatch(result):
    global root_compare, insert_real_text, compare_label, userInserLabel
    userInserLabel = insert_real_text.get("1.0",END)
    print(userInserLabel)
    print(result)
    precentMatch = ModelTesseract.calcMatch(userInserLabel, result)
    compare_label = Label(root_compare, text="The match precent according similarity - "+str(round(precentMatch,2))+"%",
                    bg="steel blue", font=("Ariel", 16), fg = "red",bd = 5, width=50, anchor = CENTER)
    compare_label.grid(row = 6, column = 0, columnspan = 3)
    compare_label = Button(root_compare, text="Want to insert your true label into database?",
                           command= insertresult, font=("Ariel", 12), bd = 5, width=40, anchor = CENTER)
    compare_label.grid(row = 7, column = 0, columnspan = 3)

def tryagain():
    global frame_text
    frame_text.destroy
    Select_train_test(0)

def open_help_window(type):
    top = Toplevel()
    top.geometry("400x400")
    if type == Status_program(0):
        top.title("help "+str(Status_program(0)))
        txt_file = open(HELP_TEXT_DOC_CREATE, "r", encoding="utf-8")
        text = txt_file.read()
        txt_file.close()
    elif type == Status_program(1):
        top.title("help "+str(Status_program(1)))
        txt_file = open(HELP_TEXT_DOC_EXTRACT, "r", encoding="utf-8")
        text = txt_file.read()
        txt_file.close()
    numCharLine  = [len(line) for line in text.split("\n")]
    top.geometry(str(max(numCharLine)*6)+"x400")

    my_help = Label(top, text=text, justify='right')
    my_help.pack()
    top.mainloop()

def setmodel():
    global entrylabel, modelName, root_model
    if entrylabel.get()!= "":
        modelName = entrylabel.get()
        popup_message("Switch model name, thank you", maessage_type(0))
        root_model.destroy()

def new_window_selectModel(root):
    global entrylabel, root_model
    root_model = Toplevel()
    root_model.title("Choose your traineddata model - make sure it is in the tessdata folder")
    root_model.geometry(str(IMAGE_WIDTH_TO_SHOW)+"x150")

    title_label_model = Label(root_model, text="Choose your traineddata model - make sure it is in the tessdata folder",
                     font=("Ariel", 12), width=70, anchor = CENTER)
    title_label_model.grid(row = 0, column = 0, columnspan = 3)

    label_model = Label(root_model, text="Insert traineddata name:", font=("Ariel", 10))
    label_model.grid(row = 1, column = 0, columnspan = 3)

    entrylabel = Entry(root_model, borderwidth=5, width = 30)
    entrylabel.grid(row=2, column=0, columnspan = 3 )

    button_save = Button(root_model, text="Save",width = 20, padx=5, pady=5, command = setmodel)
    button_save.grid(row=3, column=1)
    root_model.mainloop()

def run_program(finishWrop = False, finishEdit = False):
    global folder_selected, markTextArea, scannedInsertDocuments, root, original_image_array_show
    global images, txtFiles, points, delete_files, images_path_list, images_numpy_array, writerID, isTrain

    isTrain = status_program == Status_program(0)
    if isTrain:
        writerID = str(enterID())
        #print ("writerID"+str(writerID))
        if writerID == "-1":
            Select_train_test(Status_program(0))

    if not finishWrop:
        if status_program == Status_program(0):
            if scannedInsertDocuments:
                images_path_list, txtFiles = Extract_files_from_folder(folder_selected)
                if images_path_list == []:
                    popup_message("ERROR NO GOOD FILES TO CREATE DATA - CHECK 'help'", maessage_type(2))
                    exit_program(root)

                for image_path in images_path_list:
                    image_array = cv.imread(image_path, 0)
                    original_image_array.append(image_array.copy())
                    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
                    image_array = cv.resize(image_array, (width, height))
                    images_numpy_array_show.append(image_array)
                    imageTK_list.append(ImageTk.PhotoImage(Image.fromarray(image_array)))
                images_numpy_array = original_image_array.copy()
                original_image_array_show = images_numpy_array_show.copy()
                wrap_data()
            else:
                wrap_data()

        elif status_program == Status_program(1):
            wrap_data()

    # after cropp of the images
    else:
        if status_program == Status_program(0):
            for i in range(len(images_path_list)):
                if scannedInsertDocuments:
                    images.append(ImageProcessing.ImageProcessing(images_numpy_array[i], imagePath=images_path_list[i], handwrite_ID=writerID))
                else:
                    EditImage()
                    #images.append(ImageProcessing.ImageProcessing(images_numpy_array[i], imagePath=images_path_list[0], handwrite_ID=writerID))
        elif status_program == Status_program(1):
            EditImage()
            #images.append(ImageProcessing.ImageProcessing(images_numpy_array[0], imagePath=images_path_list[0]))

    print(len(images))

    print("isTrain"+str(isTrain))
    print("scannedInsertDocuments "+str(scannedInsertDocuments))
    controller = Controller.Controller(isTrain, images, root, isScanned = scannedInsertDocuments, modelName = modelName)
    result = controller.main()
    showResults(root, result)

def main():
    global folder_selected, markTextArea, scannedInsertDocuments
    global txtFiles, points, delete_files, clicked, root, options, frame , frameExtract, frame_text, frameMarkRun

    reset_global_parameters()
    root = Tk()

    # bgImage = Canvas(root, height = IMAGE_HEIGHT_TO_SHOW, width = IMAGE_WIDTH_TO_SHOW)
    # backgroung_array = cv.imread(r"C:\Users\Adi Rosental\Documents\shecode_final_project\code\tesseractIcon.png")
    # backgroung_array = cv.resize(backgroung_array, (IMAGE_WIDTH_TO_SHOW-50, IMAGE_HEIGHT_TO_SHOW))
    # imagebg = Image.fromarray(backgroung_array)
    # fileImage = ImageTk.PhotoImage(imagebg)
    # backgroundimage_label = Label(root, image = fileImage)
    # backgroundimage_label.place(x=0, y=0, relwidth = 1, relheight = 1)

    root.configure(background = "steel blue")

    root.geometry(str(IMAGE_WIDTH_TO_SHOW) + "x" + str(IMAGE_HEIGHT_TO_SHOW+100))
    root.title("convert a picture in Hebrew to machine encoded text - Adi Rosenthal")

    frame = Frame(root,  bg= "steel blue")
    frame.grid(row=3, column=0,  columnspan = 2 )
    frameExtract = Frame(frame,  bg= "steel blue")
    frameExtract.grid(row=5, column=0, columnspan=2)
    frameMarkRun = Frame(root,  bg= "steel blue")
    frameMarkRun.grid(row=6, column=0, columnspan=2)
    frame_text = Frame(root, relief=SUNKEN)
    frame_text.grid(row=6, column=0, columnspan=2)
    menubar = Menu(root)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command = lambda: exit_program(root))
    menubar.add_cascade(label="File", menu=filemenu)

    datamenu = Menu(menubar, tearoff=0)
    datamenu.add_command(label="Check Data", command=lambda: new_window_check_database(root))
    menubar.add_cascade(label="Data", menu=datamenu)

    modelmenu = Menu(menubar, tearoff=0)
    modelmenu.add_command(label="Select Model", command=lambda: new_window_selectModel(root))
    menubar.add_cascade(label="Model", menu=modelmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label = "Help - create data", command = lambda: open_help_window(Status_program(0)))
    helpmenu.add_command(label = "Help - extract text", command = lambda: open_help_window(Status_program(1)))
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    options = ["please choose", Status_program(0),Status_program(1)]

    clicked = StringVar()
    clicked.set(options[0])
    myLabel = Label(root, text="Choose one of the options - "+Status_program(0)+" or "+Status_program(1) +":", bg= "steel blue",font=("Ariel", 16), width = 50)
    drop = OptionMenu(root, clicked, *options, command=Select_train_test)
    drop.config(width = 30, font=('Ariel, 14'))

    myLabel.grid(row=0, column=0, columnspan = 2)
    drop.grid(row=1, column=0, columnspan = 2)

    deleteFiles()
    root.mainloop()

if __name__ == "__main__":
    main()



    # 1) switch case : enum - with all the values
    # 2) print errors with the gui
    # 3) work on the power point - vm, docker ,  vedio -


