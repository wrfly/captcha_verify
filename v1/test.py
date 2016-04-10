#coding=utf-8
from PIL import Image
 
img = Image.open('1.png') # 读入图片
img = img.convert("RGBA")

def step_1(img):
    pixdata = img.load()
    #二值化
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)
     
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)
     
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)

step_1(img)
img.save("input-black.png", "PNG")
 
# #放大图像 方便识别
# im_orig = Image.open('input-black.png')
# big = im_orig.resize((1000, 500), Image.NEAREST)