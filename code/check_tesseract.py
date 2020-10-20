import ModelTesseract
import config
import os
try:
    from PIL import Image
except ImportError:
    import Image
import cv2

# set variable:
lang = "heb28"
compare_model = "heb"
compare_methods = "SQ"

HOME_DIRECTORY = config.get_home_directory()
folder_output_txtfile = os.path.join(HOME_DIRECTORY, "models-trained\\test_models")
folder_validation = os.path.join(HOME_DIRECTORY, "data\\validation")


results =[]

tessract = ModelTesseract.ModelTesseract(lang)
tessract.Check_model_tesseract(folder_validation, folder_output_txtfile, psm=7, compare_methods = compare_methods, compare_model= compare_model)

#langs = ['heb320.018_398', 'heb320.022_397', 'heb320.027_353', 'heb320.03_352', 'heb320.044_352', 'heb320.048_352', 'heb320.051_349', 'heb320.056_348', 'heb320.068_348', 'heb320.107_348', 'heb320.135_319', 'heb320.13_347', 'heb320.199_317', 'heb320.226_316', 'heb320.266_312', 'heb320.296_310', 'heb320.357_307', 'heb320.418_306', 'heb320.449_305', 'heb320.521_304', 'heb320.624_304', 'heb320.739_300', 'heb320.794_295', 'heb320.959_286', 'heb321.252_280', 'heb322.044_272', 'heb322.183_261', 'heb322.372_253', 'heb322.647_246', 'heb322.949_226', 'heb323.333_210', 'heb323.809_186', 'heb324.626_164', 'heb325.938_133', 'heb328.334_80']
#for lang in  langs:

# results.append((lang, tessract.acuracy))

#print (results)
