import cv2
import pytesseract
import datetime
import jellyfish, os
try:
    from PIL import Image
except ImportError:
    import Image
from difflib import SequenceMatcher as SQ

#def calcMatch(realtext, resultText, compare_methods = "SQ"):
#    # if compare_methods == "jaro winkler":
#    #     result_score = jellyfish.jaro_winkler_similarity(realtext, resultText) * 100
#   elif compare_methods == "SQ":
#    result_score = calcMatchLine(realtext, resultText)

#    return result_score


def calcMatch(textTrue, textResult):
    textTrue_lines = textTrue.split("\n")
    print(textTrue_lines)
    textResult_lines = textResult.split("\n")
    print(textResult_lines)
    num_lineTrue = 0
    num_lineResult = 0
    sum_score = 0
    count = 1
    while num_lineTrue != len(textTrue_lines) and num_lineResult != len(textResult_lines):
        while textResult_lines[num_lineResult] == "" or textResult_lines[num_lineResult] == " " and num_lineResult != len(textResult_lines) - 1:
            num_lineResult += 1
        print(textResult_lines[num_lineResult])
        print(textTrue_lines[num_lineTrue])
        print(num_lineTrue)
        print(num_lineResult)
        print(SQ(None, textResult_lines[num_lineResult], textTrue_lines[num_lineTrue]).ratio() * 100)
        sum_score += SQ(None, textResult_lines[num_lineResult], textTrue_lines[num_lineTrue]).ratio() * 100
        count += 1
        num_lineTrue+=1
        num_lineResult+=1
    return sum_score / (count-1)

class ModelTesseract:
    def __init__(self, modelName = "heb7"):
        self.acuracy = 0
        self.lang = modelName

    def TrainModelTesseract(self):
        pass

    def ExportTextTesseract(self, image):
        print(self.lang)
        str = pytesseract.image_to_string(image, lang=self.lang)
        return str

    def BoxesAroundText(self, img):
        h, w, c = img.shape
        boxes = pytesseract.image_to_boxes(img)
        for b in boxes.splitlines():
            b = b.split(' ')
            img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

        cv2.imshow('img', img)
        cv2.waitKey(0)


    def Check_model_tesseract(self, folder_validation, folder_output_txtfile, psm=7, compare_methods = "SQ"):
        time = datetime.datetime.now()
        lang_trained = self.lang
        file_to_save = open(os.path.join(folder_output_txtfile, lang_trained + time.strftime("_%d_%m_%H_%M") + ".txt"), "w",
                            encoding="utf-8")
        file_to_save.write("DATE : " + time.strftime("%d_%m %H_%M") + "\n")
        file_to_save.write("Model : " + lang_trained + "\n\n")
        files = os.listdir(folder_validation)
        file_to_save.write("Validation folder: " + folder_output_txtfile + ", length data: " + str(len(files) / 2) + "\n\n")
        file_to_save.write("Algorithem of compare strings : " + compare_methods + "\n\n")
        sum = 0
        sum_dif = 0
        count = 0
        for file in files:
            if file[-4:].lower() == ".tif" or file[-4:].lower() == ".tif":
                img = Image.open(os.path.join(folder_validation, file))
                resultText = pytesseract.image_to_string(img, lang=lang_trained, config='--psm ' + str(
                    psm))  # make sure to change your `config` if different
                resultText.replace("\n", "")
                resultText_before = pytesseract.image_to_string(img, lang="heb", config="--psm " + str(
                    psm))  # make sure to change your `config` if different

                txt_file = open(os.path.join(folder_validation, file[:-4] + ".gt.txt"), "r", encoding="utf-8")
                realText = txt_file.read()
                txt_file.close()
                result_score = calcMatch(realText, resultText)
                result_score_befor_train = calcMatch(realText, resultText_before)

                diff = result_score - result_score_befor_train
                sum_dif+=diff
                txt_print = f"text: {realText}\nOutput: {resultText}Befor: {resultText_before}Percent coincidence after train: {round(result_score,2)}%\ndiff between befor train and after: {round(diff,2)}%\n"
                file_to_save.write(txt_print + "\n\n")
                sum += result_score
                count += 1
                print(txt_print)
        file_to_save.write(f"\nmean present : {(sum / count)}")
        file_to_save.write(f"\nmean present : {(sum_dif / count)}")
        print("mean:"+str(sum / count))
        print("mean improve fron 'heb': "+str(sum_dif / count))
        file_to_save.close()
        self.acuracy = sum / count