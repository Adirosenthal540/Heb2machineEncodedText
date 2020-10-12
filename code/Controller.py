import ImageProcessing
from HandwrittenDoc import Check_image_page, ExportHandriteLinesFromScannedDoc
import DataManager
import ModelTesseract
import Main


class Controller():

    def __init__(self, isTrain, images, root = None, isScanned = False, modelName=None, labels = None):
        self.isTrain = isTrain
        self.isScanned = isScanned
        self.image_processing_list = images
        self.root = root
        self.modelName = modelName
        self.labels = labels

    def processLabeledImages(self):
        image = self.image_processing_list[0]
        boundries = ImageProcessing.GetLineBounds(image.imageArray)
        line_images_array = []
        for i in range(len(boundries)):
            x, y, w, h = boundries[i]
            cutImage = image.cutImage(image.imageArray, x, y, x + w, y + h)
            line_images_array.append(cutImage)
        Main.userSetLabel(line_images_array, self)

    def setLabels(self, labels):
        self.labels = labels

    def processScannedImages(self):
        newImagesForTrain =[]
        for image in self.image_processing_list:
            pageNum = Check_image_page(image.imagePath)
            newImagesForTrain= newImagesForTrain + ExportHandriteLinesFromScannedDoc(image, pageNum)
        numS, numE = DataManager.Insert_to_database(newImagesForTrain)
        return (numS, numE)


    def processExportFromImage(self):
        if self.modelName != None:
            print(self.modelName)
            tesseract = ModelTesseract.ModelTesseract(self.modelName)
        else:
            tesseract = ModelTesseract.ModelTesseract()
        text = tesseract.ExportTextTesseract(self.image_processing_list[0].imageArray)
        return text

    def insert_data_to_dataBase(self, newImagesForTrain):
        numS, numE = DataManager.Insert_to_database(newImagesForTrain)
        return (numS, numE)

    def main(self):
        for image in self.image_processing_list:
            print(image.imagePath)
            print(image.Label)
            print(image.handwrite_ID)

        if self.isTrain:
            if self.isScanned:
                numS, numE = self.processScannedImages()
                return ("Sucsses - insert " +str(numE - numS)+ " lines for training, images - " + str(numS) + " to "+str(numE))
            else:
                self.processLabeledImages()
        else:
            text = self.processExportFromImage()
            return text