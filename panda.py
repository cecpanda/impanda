# -*- coding: utf-8 -*-

import fire
from PIL import Image

from impanda import Img2Txt


def entry(img, dir='dest/', txt=True, json=True, image=True, html=True):
    try:
        im = Image.open(img)
    except Exception as e:
        print(e)
        return

    format = im.format

    if format == 'JPEG' or format == 'PNG':
        Img2Txt(img, out_dir=dir).start(txt=txt, json=json, image=image, html=html)
    elif format == 'GIF':
        pass
    else:
        print('仅支持 JPEG/PNG/GIF！')
        return


if __name__ == "__main__":
    fire.Fire(entry)
