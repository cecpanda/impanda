# -*- coding: utf-8 -*-

import fire

from impanda import panda



def entry(img, dir='dest/', max_len=80, duration=80,
          text=False, json=False, image=False, html=True, color=False, style='char',
          sketch=False, depth=10):

    panda(img=img, dir=dir, max_len=max_len, duration=duration,
          text=text, json=json, image=image, html=html, color=color, style=style,
          sketch=sketch, depth=depth)

if __name__ == "__main__":
    fire.Fire(entry)
