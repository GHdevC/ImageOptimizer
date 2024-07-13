import os
from PIL import Image
from os import listdir
from os.path import isfile, join


input_images = [f for f in listdir(os.path.dirname(os.path.abspath(__file__)) + "\\imgs") if isfile(join(os.path.dirname(os.path.abspath(__file__)) + "\\imgs", f))]


def getSize(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compressor(image_name, new_size_ratio, quality, to_jpg, width=None, height=None, ):
    img = Image.open(image_name)
    print("[*] Размер изображения:", img.size)
    image_size = os.path.getsize(image_name)
    print("[*] Размер до сжатия:", getSize(image_size))
    if new_size_ratio < 1.0:
        if int(img.size[0] * new_size_ratio) <= 0:
            x = 1
        else:
            x = int(img.size[0] * new_size_ratio)
        if int(img.size[1] * new_size_ratio) <= 0:
            y = 1
        else:
            y = int(img.size[1] * new_size_ratio)
        img = img.resize((x, y), Image.Resampling.LANCZOS)
        print("[+] Новый размер изображения:", img.size)
    elif width and height:
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        print("[+] Новый размер изображения:", img.size)
    filename, ext = os.path.splitext(image_name)
    if to_jpg:
        new_filename = f"{filename}.jpg"
    else:
        new_filename = f"{filename}{ext}"
    try:
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        img = img.convert("RGB")
        img.save(new_filename, quality=quality, optimize=True)
    print("[+] Новый файл сохранен как:", new_filename)
    new_image_size = os.path.getsize(new_filename)
    print("[+] Размер после сжатия:", getSize(new_image_size))
    saving_diff = new_image_size - image_size
    print(f"[+] Размер изменился на: {saving_diff/image_size*100:.2f}%.")

for i in input_images:
    compressor(os.path.dirname(os.path.abspath(__file__)) + "\\imgs\\" +i, 0.9, 90, True)
