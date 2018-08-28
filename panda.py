# -*- coding: utf-8 -*-

import fire
from PIL import Image

from impanda import ImgToTxt, GifToTxt



def entry(img, dir='dest/', max_len=80, text=True, json=True, image=True, html=True, color=False, style='char'):
    try:
        im = Image.open(img)
    except Exception as e:
        print(e)
        return

    print('text: ', text, type(text))
    print('json: ', json, type(json))
    print('image: ', image, type(image))
    print('html: ', html, type(html))
    print('color: ', color, type(color))
    print('style: ', style, type(style))

    format = im.format

    if format == 'JPEG' or format == 'PNG':
        ImgToTxt(image=img, out_dir=dir, max_len=max_len).run(text=text, json=json, image=image, html=html, color=color, style=style)
    elif format == 'GIF':
        GifToTxt(image=img, out_dir=dir, max_len=max_len).run(json=json, image=image, html=html, color=color, style=style)
    else:
        print('仅支持 JPEG/PNG/GIF！')
        return


if __name__ == "__main__":
    fire.Fire(entry)
