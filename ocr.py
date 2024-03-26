import pytesseract
from PIL import Image
import re

def getPicContent(image_path):
    # image_path = 'test.jpeg'  # 替换为你自己的图像文件路径
    img = Image.open(image_path)
    # 使用 pytesseract 进行文字识别
    text = pytesseract.image_to_string(img, lang='eng+chi_sim')  # 英文和中文识别，根据需要更改语言参数
    # 输出识别结果
    text = str(text)
    text = text.replace(" ", "")
    begin = text.find("复习")
    end = text.find("时长")
    text = text[begin:end]
    text = text.replace("\n", "")
    print(text)
    result = re.findall(r"\d+", text)
    if len(result) >= 2:
        print(result)
        return result
