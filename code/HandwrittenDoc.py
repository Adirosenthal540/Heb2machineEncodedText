import numpy as np
import cv2 as cv
import os
from ImageProcessing import ImageProcessing
from PIL import Image
import tempfile

THRESHOLDTIGHT = 110
MINPIXELLETTER = 10 # MIN PIXEL NUM FOR LETTER \ LINE
MAXNUMLINES = 9
NUMPAGES = 4

def check_PDF_name(namefile):
    order_list = []
    namefile = namefile[:-4]
    orderPages = namefile.split("_")[-1]
    for num in orderPages:
        min_page_ord = 49
        max_page_ord = min_page_ord + NUMPAGES
        if ord(num) < min_page_ord or ord(num) >= max_page_ord:
            print ("ERROR - Wrong name for the PDF")
            return -1
        else:
            order_list.append(int(num))
    print("The order of the pages in your pdf - " + os.path.basename(namefile) + " are: " +orderPages)
    return order_list

def Check_image_page(namefile):
    num_page = namefile[-5]
    min_page_ord = 49
    max_page_ord = min_page_ord + NUMPAGES
    if ord(num_page) < min_page_ord or ord(num_page) >= max_page_ord:
        print("ERROR - Wrong name for the image")
        return -1
    return (int(num_page))

def Check_image_name(image_path):
    flag = 0
    image_name = os.path.basename(image_path)
    ext = os.path.splitext(image_name)[1]
    image_name = image_name[:-(len(ext))]
    if not ("_" in image_name):
        flag = 1
    else:
        numPges = image_name.split("_")[-1]
        if numPges!="":
            min_page_ord = 49
            max_page_ord = min_page_ord + NUMPAGES
            for num in numPges:
                if ord(num) < min_page_ord or ord(num) >= max_page_ord:
                    flag = 1
                    break
        else:
            flag = 1
    if flag == 1:
        return False
    else:
        return True


def FindSquaresHandwriteDoc(image):
    thresh = cv.threshold(image, 160, 255, cv.THRESH_BINARY_INV)[1]
    #thresh = cv.threshold(gray, 255 - mean + std, 255, cv.THRESH_BINARY_INV)[1]
    cnts = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # min and max area for square, given the fact that there are 10 square in row
    min_area = (image.shape[0] / 30) * image.shape[1] * 0.75
    max_area = (image.shape[0] / 10) * image.shape[1]

    boundries = []
    for c in cnts:
        area = cv.contourArea(c)

        if area > min_area and area < max_area:
            x, y, w, h = cv.boundingRect(c)

            fix = int(h * 0.2)
            x = x + fix
            y = y + fix
            w = w - fix*2
            h = h - fix*2
            boundries.append((x,y,w,h))
            # cv2.imwrite('ROI_{}.png'.format(image_number), ROI)
            cv.rectangle(image, (x, y), (x + w, y + h), 255, 5)
    # boundries = np.array(boundries)
    # cv.imshow("image", image)
    # cv.waitKey(0)
    if len(boundries) < MAXNUMLINES:
        print("ERROR - did'nt recognize all the sqares need to take a picture again or to wrap it")
        return -1
    elif len(boundries) > MAXNUMLINES:
        print("ERROR - there are noises, need to take a picture again or to wrap it")
        return -1
    return boundries

def reorderBoundries(boundries):
    reorderBoundries = []
    lenList = len(boundries)
    for i in range(lenList):
        reorderBoundries.append(boundries[lenList - 1 - i])
    return reorderBoundries


def ExportHandriteLinesFromScannedDoc(image, pageNum):
    handwrittenDic = HandwrittenDic()
    newImagesForTrain = []
    boundries = FindSquaresHandwriteDoc(image.imageArray) # The boundries are order from the bottom of the page up.
    boundries = reorderBoundries(boundries)

    for i in range(len(boundries)):
        x, y, w, h =  boundries[i]
        cutImage = image.cutImage(image.imageArray, x, y, x + w, y + h)
        Label = handwrittenDic.FindLabelForLine(page = pageNum, lineNum = i+1)
        newImagesForTrain.append(ImageProcessing(cutImage, imagePath = None, Label = Label, handwrite_ID = image.handwrite_ID))

    return newImagesForTrain

class HandwrittenDic():
    def __init__(self):
        self.dicPageLineLabel = self.createLabelForPageAndLine()

    # The function given a line it's Label im hebrew
    def createLabelForPageAndLine(self):
        dic = {}
        for page in range(1, 5):
            if page == 1:
                dic[(page, 1)] = "בשמלה אדומה ושתי צמות,"
                dic[(page, 2)] = "ילדה קטנה, יחידה ותמה"
                dic[(page, 3)] = "עמדה ושאלה – למה?"
                dic[(page, 4)] = "וכל הרי הגעש וכל הסערות"
                dic[(page, 5)] = "עמדו מזעפם ולא מצאו תשובה."
                dic[(page, 6)] = "יונתן הקטן רץ בבוקר אל הגן"
                dic[(page, 7)] = "הוא טיפס על העץ אפרוחים חיפש"
                dic[(page, 8)] = "אוי ואבוי לו לשובב, חור גדול במכנסיו"
                dic[(page, 9)] = "מן העץ התגלגל ועונשו קיבל"
            elif page == 2:
                dic[(page, 1)] = "אני אוהב שוקולד ועוגות גבינה"
                dic[(page, 2)] = "וארטיק וסוכריות ותות גינה"
                dic[(page, 3)] = "אני אוהב ימי הולדת ושקיות עם דברים טובים"
                dic[(page, 4)] = "ואת השמש ואת הירח וגם כמה כוכבים."
                dic[(page, 5)] = "אפונה וגזר ישבו במקרר "
                dic[(page, 6)] = "ויחד עם בטטה התחילו לקטר:"
                dic[(page, 7)] = "\"קר לי ברגליים, תדליק ת'מנורה בקיר,"
                dic[(page, 8)] = "כי חושך מצרים, אז בואו נשיר\"."
                dic[(page, 9)] = "תנו לגדול בשקט בערוגה בכפר."
            elif page == 3:
                dic[(page, 1)] = "שם תזרח השמש גם מחר"
                dic[(page, 2)] = "תנו לגדול בשקט בלי לקפוא מקור"
                dic[(page, 3)] = "רק קצת זבל, מים וגם אור."
                dic[(page, 4)] = "אפונה וגזר, ישבו בתוך מחבט."
                dic[(page, 5)] = "ויחד עם בטטה רצו להיות לבד"
                dic[(page, 6)] = "אך שוד ושבר, מישהו גפרור מדליק"
                dic[(page, 7)] = "ושמן מכל עבר, זה לא מצחיק!"
                dic[(page, 8)] = "כי חושך מצרים, אז בואו נשיר\"."
                dic[(page, 9)] = "רוץ בן סוסי, רוץ ודהר! רוץ בביקעה, טוס בהר!"
            elif page == 4:
                dic[(page, 1)] = "רוצה, טוסה, יום וליל – פרש אני ובן חיל!"
                dic[(page, 2)] = "אני רץ. אני חייב להספיק כל מה שהעולם מציע"
                dic[(page, 3)] = "כל זמן שהאוויר מגיע וזה לא מפריע ומלטף אותי."
                dic[(page, 4)] = "ויש אצלך אור, למה לי לעצור."
                dic[(page, 5)] = "אני יודע אני זז וזה פוגע, בלב שלי יש חור"
                dic[(page, 6)] = "שאי אפשר לסגור ואני רץ..."
                dic[(page, 7)] = "בים הרוגע השמש שוקע למי מתגעגע"
                dic[(page, 8)] = "לי ולך, לי ולך, לי ולך."
                dic[(page, 9)] = "בהצלחה באימון!"
        return dic

    def FindLabelForLine(self, page, lineNum):
        Label = self.dicPageLineLabel[(page, lineNum)]
        return Label






