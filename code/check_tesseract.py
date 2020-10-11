import sys, os
import pytesseract
from difflib import SequenceMatcher as SQ
import jellyfish
from similarity.normalized_levenshtein import NormalizedLevenshtein
import datetime
import ModelTesseract
try:
    from PIL import Image
except ImportError:
    import Image

# set variable:
compare_methods = 'jaro winkler'
lang = "heb5"
folder_output_txtfile = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\models-trained\test_models"
folder_validation = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\validation"
psm=6

tessract = ModelTesseract.ModelTesseract("heb5")
tessract.Check_model_tesseract(folder_validation, folder_output_txtfile, psm=7, compare_methods = "SQ")
# time = datetime.datetime.now()
# file_to_save = open(os.path.join(folder_outpu_txtfile, lang+time.strftime("_%d_%m_%H_%M")+".txt"), "w", encoding="utf-8")
# file_to_save.write("DATE : "+time.strftime("%d_%m %H_%M")+"\n")
# file_to_save.write("Model : "+lang+"\n\n")
# files = os.listdir(folder_path)
# file_to_save.write("Valitation folder: "+folder_path+", length data: "+str(len(files)/2)+"\n\n")
#
# sum = 0
# count = 0
# for file in files:
#     print(file)
#     if file[-4:].lower() == ".tif" or file[-4:].lower() == ".tif":
#         img = Image.open(os.path.join(folder_path, file))
#         raw_text = pytesseract.image_to_string(img, lang=lang, config='--psm '+str(psm))  # make sure to change your `config` if different
#         raw_text.replace("\n", "")
#         raw_text_before = pytesseract.image_to_string(img, lang="heb", config="--psm "+str(psm))  # make sure to change your `config` if different
#
#         txt_file = open(os.path.join(folder_path, file[:-4] + ".gt.txt"), "r", encoding="utf-8")
#         text = txt_file.read()
#         txt_file.close()
#         if compare_methods == "jaro winkler":
#             result_score =  jellyfish.jaro_winkler_similarity(text, raw_text) * 100
#             result_score_befor_train = jellyfish.jaro_winkler_similarity(text, raw_text_before) * 100
#         elif compare_methods == "levenshtein":
#             normalized_levenshtein = NormalizedLevenshtein()
#             result_score = normalized_levenshtein.distance(text, raw_text) * 100
#             result_score_befor_train = normalized_levenshtein.distance(text, raw_text_before) * 100
#
#         elif compare_methods == "SQ":
#             result_score = SQ(None, text, raw_text).ratio() * 100
#             result_score_befor_train = SQ(None, text, raw_text_before).ratio() * 100
#         diff = result_score - result_score_befor_train
#         txt_print = f"text: {text}\nOutput: {raw_text}Befor: {raw_text_before}Percent coincidence after train: {round(result_score,2)}%\ndiff between befor train and after: {round(diff,2)}\n"
#         file_to_save.write(txt_print+"\n\n")
#         sum += result_score
#         count+=1
#         print(txt_print)
# file_to_save.write(f"\nmean present : {(sum / count)}")
# print(sum/count)
# file_to_save.close()