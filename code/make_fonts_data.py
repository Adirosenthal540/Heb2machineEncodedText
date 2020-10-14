from difflib import SequenceMatcher as SQ
import ImageProcessing
import config
from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
from pdf2image import convert_from_path
POPPLER_PATH = config.get_poppler_path()
import docx, os, time
NUMPIXELS = 20

names_of_fonts = []
def convert_wordDocx_to_x_words_in_line_txtFile(x, doc, outputPathForTextFile):
    j=0
    f = open(outputPathForTextFile, "w+", encoding="utf-8")
    for paragraph in doc.paragraphs:
        list_words = paragraph.text.split(" ")
        list_words = [word for word in list_words if word!="" and word!="\n" and word!="\t" and ('\xa0' not in word) and len(word)<18 and len(word)>1]
        numword = 0
        while numword< len(list_words) and len(list_words)>0:
            line = ""
            for i in range(x):
                # numword += 1
                if numword < len(list_words):
                    if i==0:
                        line = list_words[numword]
                    else:
                        line= line+" "+list_words[numword]
                else:
                    break
                numword += 1
            if i>1:
                f.write(line+"\n")
            print(list(line))
            print(len(list_words))
            print(numword)

    f.close

# input: folder path with pdf's files
# output: make a new folder with the fonts name and paste each page of the pdf as an image into the folder
def convert_pdf_to_tif_images(folder):
    files = os.listdir(folder)
    for file in files:
        if file[-4:].lower() ==".pdf":
            outputpath, namefile = os.path.split(file)
            os.mkdir(os.path.join(folder, namefile[:-4])+"_images_")
            output_folder = os.path.join(folder, namefile[:-4])+"_images_"
            pdf_file = os.path.join(folder, file)
            try:
                images = convert_from_path(pdf_file, fmt="jpeg", poppler_path=POPPLER_PATH)
                namefile = os.path.basename(pdf_file)
                name = os.path.splitext(namefile)[0]
                i = 0
                for image in images:
                    # image = Image.open(im)
                    new_path_image = os.path.join(output_folder, name + "_" + str(i) + ".tif")
                    i += 1
                    image.save(new_path_image, 'TIFF')
            except MemoryError as error:
                print ("error : "+str(i))


def Insert_to_folder(images_processed, folderSave):
    numImage = 0
    image_path_list = []
    files = os.listdir(folderSave)
    for imageP in images_processed:
        nameImage = imageP.handwrite_ID +"_"+ str(numImage)
        while nameImage+".tif" in files:
            numImage +=1
            nameImage = imageP.handwrite_ID + "_" + str(numImage)
        pathNewImage = os.path.join(folderSave, nameImage+".tif")
        image_path_list.append(pathNewImage)
        im = Image.fromarray(imageP.imageArray)
        im.save(pathNewImage, 'TIFF')
        f = open(os.path.join(folderSave, nameImage+".gt.txt"), "w+", encoding="utf-8")
        f.write(imageP.Label)
        f.close()
        numImage += 1

def extract_ines_of_text_from_images_and_match_labels(folder, txtfile):
    font_name = os.path.basename(folder)[:-8] #remove "docx_" and "_images_"
    font_origin = font_name
    if len(font_name)>5:
        font_name = font_name[0:10]
        while font_name in names_of_fonts:
            font_name= font_name+"a"
    names_of_fonts.append(font_name)
    files = os.listdir(folder)

    if font_name in files:
        #shutil.rmtree(os.path.join(folder, font_name))
        return

    os.mkdir(os.path.join(folder, font_name))
    folderSave = os.path.join(folder, font_name)

    till_page = len(files)
    print(till_page )

    txt_file = open(txtfile, "r" , encoding="utf-8")
    text = txt_file.read()
    txt_file.close()

    lines_txt = text.split('\n')
    num_lines_txt = len(lines_txt)
    print(num_lines_txt)

    num_line=0
    newImagesForTrain = []
    num_lines_images = 0

    for i in range(till_page-1):
        print(i)
        image = os.path.join(folder, font_origin+"_"+str(i)+".tif")

        print(image)
        imageArray = cv.imread(image, 0)
        width = imageArray.shape[1]
        height = imageArray.shape[0]
        boundries = ImageProcessing.GetLineBounds(imageArray)
        #print(boundries)
        print(len(boundries))
        thispageSnum = num_lines_images
        num_lines_images += len(boundries)

        for i in range(len(boundries)):
            x, y, w, h = boundries[i]
            cutImage = imageArray[max(0, min(y, y+h)-NUMPIXELS):min(max(y, y+h)+NUMPIXELS,height) , max(0, min(x, x+w)-NUMPIXELS) :min(width, max(x, x+w)+NUMPIXELS)]
            while lines_txt[num_line]=="" or lines_txt[num_line]==" " and num_line<num_lines_txt-1:
                num_line+=1
            if num_line<=num_lines_txt-1:
                Label = lines_txt[num_line]
                print(Label)
                #cv.imshow("bb", cutImage)
                #cv.waitKey(0)
                num_line += 1
                print(thispageSnum+i)
                print(num_line)
                newImagesForTrain.append(ImageProcessing.ImageProcessing(cutImage, imagePath=None, handwrite_ID=font_name, Label = Label))
    Insert_to_folder(newImagesForTrain, folderSave)
    print(num_line, num_lines_images)

def extract_ines_of_text_from_image_and_match_label(imageArray, text,fontname, folderSave):
    lines_txt = text.split('\n')
    num_lines_txt = len(lines_txt)
    print(num_lines_txt)
    num_line=0
    newImagesForTrain = []

    width = imageArray.shape[1]
    height = imageArray.shape[0]
    boundries = ImageProcessing.GetLineBounds(imageArray)

    print(len(boundries))
    num_lines_image = len(boundries)
    for i in range(len(boundries)):
        x, y, w, h = boundries[i]
        cutImage = imageArray[max(0, min(y, y+h)-NUMPIXELS):min(max(y, y+h)+NUMPIXELS,height) , max(0, min(x, x+w)-NUMPIXELS) :min(width, max(x, x+w)+NUMPIXELS)]
        while lines_txt[num_line]=="" or lines_txt[num_line]==" " and num_line<num_lines_txt-1:
            num_line+=1
        if num_line<=num_lines_txt-1:
            Label = lines_txt[num_line]
            num_line += 1
            newImagesForTrain.append(ImageProcessing.ImageProcessing(cutImage, imagePath=None, handwrite_ID=fontname, Label = Label))

    Insert_to_folder(newImagesForTrain, folderSave)




def main():
    # doc = docx.Document(r"C:\Users\Adi Rosental\Documents\shecode_final_project\handwriteDoc\trainFonts\hebrew_text2-cahol_lavan.docx")
    # outputPathForTextFile = r"C:\Users\Adi Rosental\Documents\shecode_final_project\handwriteDoc\trainFonts"
    #
    # convert_wordDocx_to_x_words_in_line_txtFile(6, doc, os.path.join(outputPathForTextFile,  "test_word_file21.txt"))
    #
    # folder = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\fonts\fontsForTrain\nagla3"
    # convert_pdf_to_tif_images(folder)
    # #
    # txtfile = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\fonts\chaniFont\chani2_images_\2.txt"
    # folderSave = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\fonts\chaniFont\chani2_images_\chani2"
    # folder = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\fonts\chaniFont"
    # files = os.listdir(folder)
    # for file in files:
    #     if file[-8:] == "_images_":
    #          print(file)
    # txtfile = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\fonts\fontsForTrain\nagla3\fonts_text.txt"
    # extract_ines_of_text_from_images_and_match_labels(r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\fonts\fontsForTrain\nagla3\fonts_text3_images_", txtfile)
    #
    # imageArray = cv.imread(r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\fonts\chaniFont\chani2_images_\chani2_1.tif", 0)
    # txt_file = open(txtfile, "r" , encoding="utf-8")
    # text = txt_file.read()
    # txt_file.close()
    # extract_ines_of_text_from_image_and_match_label(imageArray, text,"chani2", folderSave)
    text1 = "ואיך שלא אפנה לראות  תמיד איתה ארצה\
\n    להיות, שומרת לי היא אמונים לא מסתובבת\
\n    בגנים. וגם אני בין הבריות לא מתפתה לאחרות.\
\n    והיא הייתה יפה קצת משונה וגם הכוכבים דולקים\
\n    על אש קטנה.\
\n    תשירו שיר לשלום אל תלחשו תפילה\
\n    שלומית בונה סוכה מוארת וירוקה על כן היא עסוקה\
    "
    text2 = "ואיך שלא אופנה לראות תמיד אתה ארצה\
\n    להיות, שומרת לי ה4ן אלמונים עטו מסתובבת\
\n    ג הבריות לא מתפתה לאחרת.\
\n    \
\n    והא בייתה יפה קלת משונה ועם הכוכבים דולקים\
\n    אש קטנב\
\n    \
\n    תשירו שה לשלום אל תלחשו תפשה\
\n    שלומתבונה סוכה מויות וירקה לעל כן הש עשקה\
    "
    print(calcMatchLine(text1, text2))
if __name__ == "__main__":
    main()

