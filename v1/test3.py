# coding=utf-8
import Image
import ImageEnhance
import ImageFilter
import sys
from pytesseract import *

pics = ["1317.png", "3764.png", "3952.png", "5322.png", "6135.png",
        "7336.png", "7339.png", "7384.png", "7572.png", "7932.png"]

class captcha:
    """docstring for captcha"""
    def __init__(self):
        self.dotMap = []
        self.rmMap = []
        root = [i for i in range()]
        count = [1 for i in range()]



    def closeImg(self):
        self.img.close()

    def gray(self):
        """ convert the image to gray """
        self.img = self.img.convert('L')

    def threshold(self):
        """ 二值化 - 采用阈值分割法，threshold为分割点 """
        threshold = 140
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        self.img = self.img.point(table, '1')
    
    def text2String(self):
        """ 由于都是数字 对于识别成字母的 采用该表进行修正"""
        rep = {'O': '0',
               'I': '1', 'L': '1',
               'Z': '2', 'S': '8',
               ' ': '', ',': '',
               '\'': '', '.': '',
               'E': '6', '‘': ''
               }
        self.text = image_to_string(self.img)
        self.text = self.text.strip()
        self.text = self.text.upper()
        for r in rep:
            self.text = self.text.replace(r, rep[r])

    def removal(self):
        try:
            for x in xrange(1,10):
                pass
        except Exception, e:
            raise e

    def scan(self):
        w, h = self.size
        for x in range(w):
            for y in range(h):
                if self.img.getpixel((x, y)) == 0: # 1 = blank; 0 = dot 
                    self.dotMap.append((x, y))
    def 
    def calarea(self, x, y):
        
        pass

    def traverse(self):
        pass

    def captcha(self, image):
        self.imgname = image
        self.img = Image.open(image)
        self.size = self.img.size
        self.gray()
        self.threshold()
        self.text2String()  

    def saveImg(self):
        self.img.save('out-'+self.imgname)

i = captcha()
i.captcha('7384.png')
i.scan()
print i.dotMap
i.saveImg()
i.closeImg()
print i.text
