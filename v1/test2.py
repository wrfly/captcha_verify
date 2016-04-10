# coding=utf-8
import Image
import ImageEnhance
import ImageFilter
import sys
from pytesseract import *

# 二值化
threshold = 140
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

# 由于都是数字
# 对于识别成字母的 采用该表进行修正
rep = {'O': '0',
       'I': '1', 'L': '1',
       'Z': '2', 'S': '8',
       ' ': '', ',': '',
       '\'': '', '.': '',
       'E' : '6', '‘': ''
       }
def getsumdot(x, y, img):
    x = x - 1
    y = y - 1
    l1 = (x , y)
    l2 = (x + 1, y)
    l3 = (x + 2, y)
    m1 = (x , y + 1)
    m2 = (x + 1, y + 1)
    m3 = (x + 2, y + 1)
    b1 = (x , y + 2)
    b2 = (x + 1, y + 2)
    b3 = (x + 2, y + 2)
    sumdot = img.getpixel(l1) + img.getpixel(l2) + img.getpixel(l3) + \
        img.getpixel(m1) + img.getpixel(m2) + img.getpixel(m3) + \
        img.getpixel(b1) + img.getpixel(b2) + img.getpixel(b3)
    return sumdot

def rmdot(x, y, img):
    x = x - 1
    y = y - 1
    l1 = (x , y)
    l2 = (x + 1, y)
    l3 = (x + 2, y)
    m1 = (x , y + 1)
    m2 = (x + 1, y + 1)
    m3 = (x + 2, y + 1)
    b1 = (x , y + 2)
    b2 = (x + 1, y + 2)
    b3 = (x + 2, y + 2)
    sumdot = img.putpixel(l1, 1) + img.putpixel(l2, 1) + img.putpixel(l3, 1) + \
        img.putpixel(m1, 1) + img.putpixel(m2, 1) + img.putpixel(m3, 1) + \
        img.putpixel(b1, 1) + img.putpixel(b2, 1) + img.putpixel(b3, 1)

def removedot(img):
    x, y = img.size
    for ix in xrange(1, x-1):
        for iy in xrange(1, y-1):
            if img.getpixel((ix, iy)) == 0: # 0-black 1-white
                try:
                    sumdot = getsumdot(ix, iy, img)
                    if sumdot == 8:
                        # rmdot(ix,iy, img)
                        img.putpixel((ix, iy), 1)
                except Exception, e:
                    pass
    return img

def getverify(name):
    # 打开图片
    img = Image.open(name)
    # 转化到灰度图
    imgry = img.convert('L')

    # 二值化，采用阈值分割法，threshold为分割点
    out = imgry.point(table, '1')
    # out.save('b'+name)

    out = removedot(out)
    
    # 保存图像
    out.save('o'+name)
    # 识别
    text = image_to_string(out)
    # 识别对吗
    text = text.strip()
    text = text.upper()
    for r in rep:
        text = text.replace(r, rep[r])
    # out.save(text+'.jpg')
    # print text
    return text


pics = ["1317.png", "3764.png", "3952.png", "5322.png", "6135.png",
        "7336.png", "7339.png", "7384.png", "7572.png", "7932.png"]

# pic = "6135.png"
# print pic, getverify(pic)

for pic in pics:
    if pic.replace('.png','') != getverify(pic):
        print pic, getverify(pic)
        print "###"
