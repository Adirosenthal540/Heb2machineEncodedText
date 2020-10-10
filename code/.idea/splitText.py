import sys, os

try:
    from PIL import Image
except ImportError:
    import Image
    
folder_path = r"C:\Users\Adi Rosental\Documents\she_code\validation"

files = os.listdir(folder_path)

for file in files:
    if file[-4:].lower() == ".txt":
        txt_file = open(os.path.join(folder_path, file), "r", encoding="utf-8")
        line = txt_file.readline()
        txt_file = open(os.path.join(folder_path, file), "w", encoding="utf-8")
        txt_file.writelines(line[::-1])
        txt_file.close()

        print(line)

