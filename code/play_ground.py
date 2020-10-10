from tkinter import *
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image
import cv2 as cv
from Main import calculate_width_height
import numpy as np

IMAGE_WIDTH_TO_SHOW = 600
IMAGE_HEIGHT_TO_SHOW = 600

global choosenImage, original

root = Tk()
root.title("Edit you image")


def slide(image_array, root):
    global imageTK_, my_image_label, choosenImage, horizontal, btn_dilation, btn_opening, btn_closing
    #root.geometry(str(vertical.get())+"x500")
    _, th = cv.threshold(image_array, horizontal.get(), 255, cv.THRESH_BINARY_INV)
    choosenImage = th.copy()

    image_array = th.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))

    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

    btn_dilation = Button(root, text = "dilation", command = lambda: dilation(root)).grid(row = 2, column = 3)
    btn_opening = Button(root, text = "opening", command = lambda: opening(root)).grid(row = 2, column = 2)
    btn_closing = Button(root, text = "closing", command = lambda: closing(root)).grid(row = 2, column = 1)

def get_original(root):
    global my_image_label, original, imageTK_, choosenImage
    choosenImage = original.copy()
    image_array = original.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))

    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)

    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

def save_image():
    global choosenImage
    print (choosenImage)

def dilation(root):
    global my_image_label, original, imageTK_, choosenImage, btn_dilation
    image_array = choosenImage.copy()
    kernal = np.ones((2, 2), np.uint8)
    dilation = cv.dilate(image_array, kernal, iterations=3)

    choosenImage = dilation.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)
    btn_dilation = Button(root, text = "dilation", state = DISABLED).grid(row = 2, column = 3)

def opening(root):
    global my_image_label, original, imageTK_, choosenImage, btn_dilation, btn_opening
    image_array = choosenImage.copy()
    kernal = np.ones((2, 2), np.uint8)
    opening = cv.morphologyEx(image_array, cv.MORPH_OPEN, kernal)

    choosenImage = opening.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)
    btn_opening = Button(root, text = "opening", state = DISABLED).grid(row = 2, column = 2)

def closing(root):
    global my_image_label, original, imageTK_, choosenImage, btn_closing
    image_array = choosenImage.copy()
    kernal = np.ones((2, 2), np.uint8)
    closing = cv.morphologyEx(image_array, cv.MORPH_CLOSE, kernal)

    choosenImage = closing.copy()
    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))
    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)
    btn_closing = Button(root, text = "closing", state = DISABLED).grid(row = 2, column = 1)

def userChooseTresholds(image_path, root):
    global horizontal, choosenImage, original, my_image_label, imageTK_, get_original_button, btn_dilation, btn_opening, btn_closing
    horizontal = Scale(root, from_ =  0, to =  255, orient = HORIZONTAL)
    horizontal.grid(row = 1, column = 2)
    my_label = Label(root, text = "choose value for\n THRESH_BINARY: ")
    my_label.grid(row = 1, column = 1)

    image_array = cv.imread(image_path, 0)
    choosenImage = image_array.copy()
    original = image_array.copy()

    width, height = calculate_width_height(image_array, IMAGE_WIDTH_TO_SHOW, IMAGE_HEIGHT_TO_SHOW)
    image_array = cv.resize(image_array, (width, height))

    root.geometry(str(width + 300) + "x" + str(height + 100))

    image_fromarray = Image.fromarray(image_array)
    imageTK_ = ImageTk.PhotoImage(image_fromarray)
    my_title = Label(root, text = "Find the best variation of your image to extracting text", font=("Ariel", 16))
    my_title.grid(row = 0, column = 0, columnspan = 5)

    my_image_label = Label(root, image=imageTK_)
    my_image_label.grid(row=1, column=0, rowspan = 5)

    btn_THRESH_BINARY = Button(root, text = "click", command = lambda: slide(image_array, root)).grid(row = 1, column = 3)

    btn_dilation = Button(root, text = "dilation", state = DISABLED).grid(row = 2, column = 3)
    btn_opening = Button(root, text = "opening", state = DISABLED).grid(row = 2, column = 2)
    btn_closing = Button(root, text = "closing", state = DISABLED).grid(row = 2, column = 1)
    get_original_button = Button(root, text = "click to original", command = lambda: get_original(root), width = 25).grid(row = 5, column = 1, columnspan = 3)
    save_image_button = Button(root, text="Click here to run program on this image", command=save_image).grid(row=8, column=0, columnspan = 4, sticky=W + E)
    root.mainloop()

image_path = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\test_images\orange.jpg"
userChooseTresholds(image_path, root)