# coding=utf-8
import Image
import ImageEnhance
import ImageFilter
import sys
import os
from pytesseract import *

pics = os.walk('test').next()[2]

class captcha:

    """docstring for captcha"""

    def __init__(self, image):
        self.imgname = image
        self.img = Image.open(image)
        self.size = self.img.size
        maxn = self.size[0] * self.size[1]
        self.dotMap = []
        self.rmMap = []
        self.root = [i for i in range(maxn)]
        self.count = [1 for i in range(maxn)]
        self.dx = [1, -1, 0,  0, 1, -1, 1, -1]
        self.dy = [0,  0, 1, -1, 1, -1, -1, 1]
        self.vis = [False for i in range(maxn)]
        self.tmp = []

    def find(self, x):
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
            return self.root[x]
        else:
            return self.root[x]

    def merge(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if (x == y):
            return
        else:
            self.root[x] = y
            self.count[y] += self.count[x]

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
        rep = {'O': '0', 'A' : '8'
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
            for x in xrange(1, 10):
                pass
        except Exception, e:
            raise e

    def scan(self):
        self.w, self.h = self.size
        for x in range(self.w):
            for y in range(self.h):
                if self.img.getpixel((x, y)) == 0:  # 1 = blank; 0 = dot
                    self.dotMap.append((x, y))

    def scanPixel(self):
        for x in range(self.w):
            for y in range(self.h):
                if self.img.getpixel((x, y)) == 0:
                    for i in range(8):
                        sx = self.dx[i] + x
                        sy = self.dy[i] + y
                        if sx < 0 or sy < 0 or sx >= self.w or sy >= self.h:
                            continue
                        if self.img.getpixel((sx, sy)) == 0:
                            self.merge(x*self.h+y, sx*self.h+sy)

    def calarea(self, x, y):
        # if self.vis[self.find(x*self.h + y)] == True:
            # self.count[self.find(x*self.h + y)] = 0
        self.vis[self.find(x*self.h + y)] = True
        return self.count[self.find(x*self.h + y)]

    def traverse(self):
        pass

    def captcha(self):
        self.gray()
        self.threshold()
        self.scan()
        self.clear()
        self.text2String()

    def saveImg(self):
        self.img.save(self.imgname+".out.png")

    def clear(self):
        self.scanPixel()
        for dot in self.dotMap:
            self.tmp.append(self.calarea(dot[0], dot[1]))
            self.tmp.sort()
            if self.calarea(dot[0], dot[1]) < 15:
                self.img.putpixel(dot, 1)
                # print self.calarea(dot[0], dot[1])
        # print set(self.tmp).difference()

total = len(pics)
wrong = 0.0

for pic in pics:
    i = captcha('test/'+pic)
    i.captcha()
    if i.imgname.replace(".png","").replace("test/", "") != i.text:
        print i.imgname.replace(".png","").replace("test/", ""), i.text
        # print i.imgname, i.text
        print "###"
        wrong += 1
    # i.saveImg()
    i.closeImg()

print '%f' % int(wrong/total*100) + ' %'