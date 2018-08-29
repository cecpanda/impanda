# -*- coding: utf-8 -*-

'''
灰度值 0-255，黑：0， 白：255

RGB 转灰度值：R，G，B 的比一般为 3：6：1

1.浮点算法：Gray=R*0.3+G*0.59+B*0.11
2.整数方法：Gray=(R*30+G*59+B*11)/100
3.移位方法：Gray =(R*77+G*151+B*28)>>8;
4.平均值法：Gray=（R+G+B）/3;
5.仅取绿色：Gray=G；

有一个很著名的心理学公式：

Gray = R*0.299 + G*0.587 + B*0.114
而实际应用时，希望避免低速的浮点运算，所以需要整数算法

Gray = (R*299 + G*587 + B*114 + 500) / 1000
RGB一般是8位精度，现在缩放1000倍，所以上面的运算是32位整型的运算。注意后面那个除法是整数除法，所以需要加上500来实现四舍五入。就是由于该算法需要32位运算，所以该公式的另一个变种很流行：

Gray = (R*30 + G*59 + B*11 + 50) / 100
'''

from PIL import Image

from .txt import ImgToTxt, GifToTxt
from .sketch import Sketch


def panda(img, dir='dest/', max_len=80, duration=80,
          text=False, json=False, image=False, html=True, color=False, style='char',
          sketch=False, depth=10):
    try:
        im = Image.open(img)
    except Exception as e:
        print(e)
        return

    format = im.format

    if sketch:
        Sketch(image=img, out_dir=dir, depth=depth, duration=duration).run()
    else:
        if format == 'JPEG' or format == 'PNG':
            ImgToTxt(image=img, out_dir=dir, max_len=max_len).run(text=text, json=json, image=image, html=html, color=color, style=style)
        elif format == 'GIF':
            GifToTxt(image=img, out_dir=dir, max_len=max_len, duration=duration).run(json=json, image=image, html=html, color=color, style=style)
        else:
            print('仅支持 JPEG/PNG/GIF！')
            return