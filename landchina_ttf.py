# -*- coding: utf-8 -*-#

# Name:         直接解析font
# Author:       air
# Date:         2020/9/18

#!/user/bin/env python3
# -*- coding: utf-8 -*-
import base64
import re

import requests
import pytesseract
from fontTools.ttLib import TTFont
from PIL import Image,ImageDraw,ImageFont
import time
import textwrap

def get_woff():
    '''
    获取字体加密后对应的映射
    :param woff_css: woff文件的url
    :return:
    '''
    # woff_css = re.findall("url\('(.*?\.woff)'\) format\('woff'\);",source,re.S)[0]
    font = TTFont('landchina.ttf')
    font.saveXML('landchina.xml')
    code_list = font.getGlyphOrder()[5:]
    # print("code_list:",code_list)
    new_list = [code.replace('uni','\\u') for code in code_list]
    text = ''.join(new_list)
    text = text.encode('utf-8').decode('unicode_escape')
    # 新建一张长宽1800像素，背景色255,255,255的画布对象
    im = Image.new("RGB", (1800, 1800), (255, 255, 255))  # 长宽1800像素，背景色255,255,255


    # 新建画布绘画对象
    image_draw = ImageDraw.Draw(im)
    # 使用truetype定义字体
    font = ImageFont.truetype('landchina.ttf', 40)
    # 在新建的对象上坐标（0,100）处开始画出文本
    lines = textwrap.wrap(text, width=40)
    y_text = 36
    for line in lines:
        width, height = font.getsize(line)
        image_draw.text(((1800-width)/2, y_text), line, font=font, fill='#000000')
        y_text += height*2
    im.save('sss.jpg')
    im = Image.open('sss.jpg')
    res = pytesseract.image_to_string(im,lang='chi_sim')    #type--->str类型
    res_str = [i for i in res if i != ' ']
    # 进行替换
    html_code_list = [i.lower().replace("uni","&#x") + ";" for i in code_list]
    result = dict(zip(html_code_list,res_str))
    print(result)
    # return result


if __name__ == '__main__':
    get_woff()
