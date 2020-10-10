from PIL import Image
import os
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError


pdf_path = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\handwriteDoc\train_songs\ADI_26_9.pdf"
images = convert_from_path(pdf_path, fmt="jpeg",  poppler_path = r"C:\poppler-20.09.0\bin")
print(images)
outputpath = r"C:\Users\Adi Rosental\Documents\she_code\shecode_final_project\handwriteDoc\train_songs"
def convert_image_format(im, outputpath):

    format = im.format
    print(format)
    # sizeFormat = len(format)
    # if format!="TIF":
    print(outputpath)
    im.save(outputpath, 'TIFF')

i=1
for image in images:
    #image = Image.open(im)
    name_image = "image"+str(i)+".tif"
    i+=1
    convert_image_format(image, os.path.join(outputpath, name_image))