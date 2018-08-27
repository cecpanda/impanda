# -*- coding: utf-8 -*-

import fire
from PIL import Image

from impanda import Img2Txt, Gif2Txt, ImgToTxt


def entry(img, dir='dest/', txt=True, json=True, image=True, html=True, resolution=0.3):
    try:
        im = Image.open(img)
    except Exception as e:
        print(e)
        return

    format = im.format

    if format == 'JPEG' or format == 'PNG':
        Img2Txt(image=img, out_dir=dir, resolution=resolution).run(txt=txt, json=json, image=image, html=html)
    elif format == 'GIF':
        Gif2Txt(image=img, out_dir=dir, resolution=resolution).run(json=json, image=image, html=html)
    else:
        print('仅支持 JPEG/PNG/GIF！')
        return

def entry1(img, dir='dest/', text=True, json=True, image=True, html=True, color=False, style='char'):
    try:
        im = Image.open(img)
    except Exception as e:
        print(e)
        return

    format = im.format

    if format == 'JPEG' or format == 'PNG':
        ImgToTxt(image=img, out_dir=dir).run(text=text, json=json, image=image, html=html, color=color, style=style)
    elif format == 'GIF':
        pass
    else:
        print('仅支持 JPEG/PNG/GIF！')
        return


if __name__ == "__main__":
    fire.Fire(entry1)
