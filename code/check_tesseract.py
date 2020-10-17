import ModelTesseract
import config
import os
try:
    from PIL import Image
except ImportError:
    import Image

# set variable:
lang = "heb29"
compare_model = "heb28"
compare_methods = "SQ"

HOME_DIRECTORY = config.get_home_directory()
folder_output_txtfile = os.path.join(HOME_DIRECTORY, "models-trained\\test_models")
folder_validation = os.path.join(HOME_DIRECTORY, "data\\validation")
psm=6

tessract = ModelTesseract.ModelTesseract(lang)
tessract.Check_model_tesseract(folder_validation, folder_output_txtfile, psm=7, compare_methods = compare_methods, compare_model= compare_model)
