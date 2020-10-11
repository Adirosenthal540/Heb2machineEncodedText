import ModelTesseract
try:
    from PIL import Image
except ImportError:
    import Image

# set variable:
compare_methods = 'jaro winkler'
lang = "heb3"
folder_output_txtfile = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\models-trained\test_models"
folder_validation = r"C:\Users\Adi Rosental\Documents\shecodes_finalProject\data\validation"
psm=6

tessract = ModelTesseract.ModelTesseract(lang)
tessract.Check_model_tesseract(folder_validation, folder_output_txtfile, psm=7, compare_methods = "SQ")
