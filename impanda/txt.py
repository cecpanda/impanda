# -*- coding: utf-8 -*-

import os
import pathlib
import bisect
import operator
import json
import re

import imageio
from PIL import Image, ImageDraw, ImageFont
from jinja2 import Template


base_dir = os.path.dirname(os.path.abspath(__file__))


class ImgToTxt(object):
    def __init__(self, image, out_dir='dest/', max_len=80):
        self.image = image
        self.out_dir = out_dir
        self.max_len = max_len  # 每行最大长度
        self.init()

    def init(self):
        self.image = Image.open(self.image)
        if self.image.format != 'PNG' and self.image.format != 'JPEG':
            raise Exception('图片格式不符合要求')
        try:
            pathlib.Path(self.out_dir).mkdir()
        except:
            pass

    def set_size(self, image):
        width, height = image.size
        rate = float(self.max_len) / max(width, height)
        w = int(rate * width)
        h = int(rate * height)
        return w, h

    def get_char(self, rgb, color=False, style='char'):
        chars = "MNHQ$OC?7>!:-;. "
        char = chars[int(sum(rgb) / 3.0 / 256.0 * 16)]

        if style == 'block':
            if color:
                return f"<span style='color:rgb{rgb};'>▇</span>"
            return '▇'
        if color:
            return f"<span style='color:rgb{rgb};'>{char}</span>"
        return char

    def transform(self, image, color=False, style='char'):
        width, height = self.set_size(image)
        im = image.resize((width, height))
        # txt = ''
        data = []  # 用数组表示
        for h in range(height):
            strings = ''
            for w in range(width):
                rgb = im.getpixel((w, h))
                strings += self.get_char(rgb, color=color, style=style)
            strings += '\n'
            data.append(strings)
        return data

    def to_console(self, txt):
        raise NotImplemented

    def to_txt(self, data, name='out.txt'):
        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.writelines(data)

    def to_json(self, data, name='out.json', convert=False):
        '''
        data: ['a', 'b', 'c'...]
        :return: ['fsfsf', 'fsdfsf', ..., ]
        '''
        if convert:
            res = []
            for line in data:
                res.append(re.sub(r'\s', '&nbsp;', line))
            data = res
        with open(os.path.join(self.out_dir, name), 'w') as f:
            json.dump(data, f)

    def to_image(self, data, name='out.png', color=False):
        width = len(data[0])
        height = len(data)
        im = Image.new('RGB', (width*6, height*9), (255, 255, 255))
        image = self.image.resize((width*6, height*9))
        fnt = ImageFont.truetype(f'{base_dir}/templates/Courier New.ttf')
        draw = ImageDraw.Draw(im)

        print(image.size)
        print(self.image.size)

        if color:
            for w in range(image.size[0]):
                for h in range(image.size[1]):
                    rgb = image.getpixel((w, h))
                    text = self.get_char(rgb, color=False, style='char')
                    draw.text((w, h), text, font=fnt, fill=rgb, spacing=0)
        else:
            draw.text((0, 0), ''.join(data), font=fnt, fill=0, spacing=0)

        im.save(os.path.join(self.out_dir, name))
        # im.show()
        im.close()

    def to_html(self, data, name='out.html'):
        with open(f'{base_dir}/templates/template.html') as f:
            template = Template(f.read())
            html = template.render(data=data)
        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.write(html)

    def get_name(self, image):
        path = pathlib.Path(image.filename)
        return path.name.split('.')

    def run(self, text=False, json=False, image=False, html=True, color=False, style='char'):
        name, suffix = self.get_name(self.image)

        if style == 'block':
            color = True

        if text:
            txt = self.transform(self.image, color=False, style='char')
            self.to_txt(txt, f'{name}.txt')
        if json:
            txt = self.transform(self.image, color=color, style=style)
            self.to_json(txt, f'{name}.json')
        if image:
            txt = self.transform(self.image, color=False, style=style)
            self.to_image(txt, f'{name}.png', color=color)
        if html:
            txt = self.transform(self.image, color=color, style=style)
            self.to_html(txt, f'{name}.html')


class GifToTxt(ImgToTxt):

    def init(self):
        self.image = Image.open(self.image)
        if self.image.format != 'GIF':
            raise Exception('图片格式不符合要求')
        try:
            pathlib.Path(self.out_dir).mkdir()
        except:
            pass

    def gif_to_png(self, image):
        # im = self.image.copy()
        # im = self.image
        palette = image.getpalette()
        images = []
        try:
            while True:
                image.putpalette(palette)
                new_im = Image.new('RGB', image.size)
                new_im.paste(image)
                images.append(new_im)
                image.seek(image.tell() + 1)
        except EOFError:
            pass
        return images

    def png_to_gif(self):
        pass

    def png_to_gif_save_1(self):
        images = self.gif_to_png()
        im = Image.new('RGB', self.image.size)
        # 0 表示 无限循化
        im.save('test.gif', save_all=True, append_images=images, loop=0, duration=80)

    def png_to_gif_save_2(self):
        images = []
        for i in range(1, 5):
            images.append(imageio.imread(f'{i}.png'))
        imageio.mimsave('_test.gif', images, duration=0.1)

    def to_console(self, txt):
        raise NotImplemented

    def to_txt(self, data, name='out.txt'):
        raise NotImplemented

    def to_json(self, data, name='out.json', convert=False):
        '''
        data: [['a', 'b'...], ['c'...]]
        :return: [['a', 'b'...], ['c'...]]
        '''
        if convert:
            res = []
            for item in data:
                tmp_res = []
                for line in item:
                    tmp_res.append(re.sub(r'\s', '&nbsp;', line))
                res.append(tmp_res)
            data = res
        with open(os.path.join(self.out_dir, name), 'w') as f:
            json.dump(data, f)

    def to_image(self, data, images, name='out.gif', color=False):
        width = len(data[0][0])
        height = len(data[0])

        ims = []
        fnt = ImageFont.truetype(f'{base_dir}/templates/Courier New.ttf')
        for i, image in enumerate(images):
            im = Image.new('RGB', (width*6, height*9), (255, 255, 255))
            image = image.resize((width*6, height*9))

            draw = ImageDraw.Draw(im)

            if color:
                for w in range(image.size[0]):
                    for h in range(image.size[1]):
                        rgb = image.getpixel((w, h))
                        text = self.get_char(rgb, color=False, style='char')
                        draw.text((w, h), text, font=fnt, fill=rgb, spacing=0)
            else:
                draw.text((0, 0), ''.join(data[i]), font=fnt, fill=0, spacing=0)

            ims.append(im)

        im = Image.new('RGB', (width * 6, height * 9), (255, 255, 255))
        im.save(os.path.join(self.out_dir, name), save_all=True, append_images=ims, loop=0, duration=80)
        im.close()

    def to_html(self, data, name='out.html'):
        with open(f'{base_dir}/templates/gif.html') as f:
            template = Template(f.read())
            html = template.render(data=data)

        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.write(html)

    def run(self, json=False, image=False, html=True, color=False, style='char'):
        name, suffix = self.get_name(self.image)

        images = self.gif_to_png(self.image)

        if style == 'block':
            color = True

        if json:
            data = []
            for image in images:
                txt = self.transform(image, color=color, style=style)
                data.append(txt)
            self.to_json(data, f'{name}.json')
        if image:
            data = []
            for image in images:
                txt = self.transform(image, color=False, style=style)
                data.append(txt)
            self.to_image(data, images, f'{name}.gif', color=color)
        if html:
            data = []
            for image in images:
                txt = self.transform(image, color=color, style=style)
                data.append(txt)
            self.to_html(data, f'{name}.html')
