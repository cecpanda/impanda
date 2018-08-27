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

    def __init__(self, image, out_dir='dest/'):
        self.image = image
        self.out_dir = out_dir
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
        max_len = 80
        width, height = image.size
        rate = float(max_len) / max(width, height)
        w = int(rate * width)
        h = int(rate * height)
        return w, h

    def get_char(self, rgb, color=False, style='char'):
        chars = "MNHQ$OC?7>!:-;. "
        char = chars[int(sum(rgb) / 3.0 / 256.0 * 16)]

        if style == 'block':
            '''直接忽略 color, 必带 color'''
            return f"<span style='color:rgb{rgb};'>▇</span>"
        if color:
            return f"<span style='color:rgb{rgb};'>{char}</span>"
        return char

    def transform(self, image, color=False, style='char'):
        width, height = self.set_size(image)
        im = image.resize((width, height))
        txt = ''
        for h in range(height):
            for w in range(width):
                rgb = im.getpixel((w, h))
                txt += self.get_char(rgb, color=color, style=style)
            txt += '\r\n'
        return txt

    def to_console(self, txt):
        return NotImplemented

    def to_txt(self, txt, name='out.txt'):
        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.write(txt)

    def to_json(self, txt, name='out.json', convert=False):
        '''
        convert space to & nbsp;
        :return: ['fsfsf', 'fsdfsf', ..., ]
        '''
        data = []
        lines = txt.split('\r\n')
        if convert:
            for line in lines:
                data.append(re.sub(r'\s', '&nbsp;', line))
        else:
            data = lines
        with open(os.path.join(self.out_dir, name), 'w') as f:
            json.dump(data, f)

    def to_image(self, txt, name='out.png'):
        im = Image.new('L', self.image.size, 255)
        fnt = ImageFont.truetype(f'{base_dir}/templates/Courier New.ttf')
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), txt, font=fnt, fill=0)
        im.save(os.path.join(self.out_dir, name))
        # im.show()
        im.close()

    def to_html(self, txt, name='out.html'):
        with open(f'{base_dir}/templates/template.html') as f:
            template = Template(f.read())
            html = template.render(txt=txt)
        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.write(html)

    def get_name(self, image):
        path = pathlib.Path(image.filename)
        return path.name.split('.')

    def run(self, text=False, json=False, image=True, html=False, color=False, style='char'):
        name, suffix = self.get_name(self.image)

        if style == 'block':
            txt = self.transform(self.image, style=style)
            if json:
                self.to_json(txt, f'{name}.json')
            if html:
                self.to_html(txt, f'{name}.html')
        else:
            if color:
                txt = self.transform(self.image, color=True)
                if json:
                    self.to_json(txt, f'{name}.json')
                if html:
                    self.to_html(txt, f'{name}.html')
            else:
                txt = self.transform(self.image)
                if json:
                    self.to_json(txt, f'{name}.json')
                if html:
                    self.to_html(txt, f'{name}.html')

        txt = self.transform(self.image)
        if text:
            self.to_txt(txt, f'{name}.txt')
        if image:
            self.to_image(txt, f'{name}.png')




class Img2Txt(object):
    '''
    image to txt
    '''
    def __init__(self, image='', out_dir='dest/', resolution=0.3):
        self.image = Image.open(image)
        self.out_dir = out_dir
        self.resolution = resolution  # 必须大于0，可以大于1，越大越精细
        self.sizes = [resolution * i for i in (0.665, 0.3122, 4)]
        self.fnt = ImageFont.truetype(f'{base_dir}/templates/Courier New.ttf', 10)
        self.init()

        try:
            pathlib.Path(self.out_dir).mkdir()
        except:
            pass

    def init(self):
        chrx, chry = self.fnt.getsize(chr(32))
        normalization = chrx * chry * 255

        weights = {}
        # get gray density for characters in range [32, 126]
        for i in range(32, 127):
            chr_image = self.fnt.getmask(chr(i))
            sizex, sizey = chr_image.size
            ctr = sum(chr_image.getpixel((x, y)) for y in range(sizey) for x in range(sizex))
            weights[chr(i)] = ctr / normalization

        weights[chr(32)] = 0.01  # increase it to make blank space ' ' more available
        weights.pop('_', None)  # remove '_' since it is too directional
        weights.pop('-', None)  # remove '-' since it is too directional

        self.sorted_weights = sorted(weights.items(), key=operator.itemgetter(1))
        self.scores = [y for (x, y) in self.sorted_weights]

        return self.sorted_weights

    def get_char(self, val):
        '''
        根据灰度值返回相应的字符串
        '''
        # find index of val in scores
        index = bisect.bisect_left(self.scores, val)

        # check and choose the nearer one between current index and former index
        if index > 0 and self.sorted_weights[index][1] + self.sorted_weights[index - 1][1] > 2 * val:
            index -= 1

        return self.sorted_weights[index][0]

    def transform(self, image):
        """
        return a string containing characters representing each pixel
        """
        # find index of val in scores
        maximum = self.scores[-1]
        im = image.resize((int(image.size[0] * self.sizes[0]), int(image.size[1] * self.sizes[1])))
        im = im.convert("L")  # transform image to black-white
        txt = ''
        for h in range(im.size[1]):
            item = ''
            for w in range(im.size[0]):
                gray = im.getpixel((w, h))
                txt += self.get_char(maximum * (1 - gray / 255))  # append characters
            txt += '\r\n'
        im.close()
        return txt

    def get_name(self):
        path = pathlib.Path(self.image.filename)
        return path.name.split('.')

    def to_console(self, txt):
        print(txt)

    def to_txt(self, txt, name='out.txt'):
        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.write(txt)

    def to_json(self, txt, name='out.json', convert=True):
        '''
        convert space to &nbsp;
        :return: ['fsfsf', 'fsdfsf', ...,]
        '''
        data = []
        lines = txt.split('\r\n')
        if convert:
            for line in lines:
                data.append(re.sub(r'\s', '&nbsp;', line))
        else:
            data = lines
        with open(os.path.join(self.out_dir, name), 'w') as f:
            json.dump(data, f)

    def to_image(self, txt, name='out.png'):
        im = Image.new('L', (int(self.image.size[0] * self.sizes[2]), int(self.image.size[1] * self.sizes[2])), 255)
        draw = ImageDraw.Draw(im)
        draw.text((0, 0), txt, font=self.fnt, fill=0)
        im.save(os.path.join(self.out_dir, name))
        # im.show()
        im.close()

    def to_html(self, txt, name='out.html'):
        # lines = txt.split('\r\n')
        with open(f'{base_dir}/templates/template.html') as f:
            template = Template(f.read())
            html = template.render(txt=txt)

        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.write(html)

    def run(self, txt=False, json=False, image=True, html=False, *args, **kwargs):
        name, suffix = self.get_name()
        txt = self.transform(self.image)
        self.image.close()

        if txt:
            self.to_txt(txt, f'{name}.txt')
        if json:
            self.to_json(txt, f'{name}.json')
        if image:
            self.to_image(txt, f'{name}.png')
        if html:
            self.to_html(txt, f'{name}.html')


class Gif2Txt(object):
    '''
    image to txt
    '''
    def __init__(self, image='', out_dir='dest/', resolution=0.3, duration=100):
        self.image = Image.open(image)
        self.out_dir = out_dir
        self.resolution = resolution  # 必须大于0，可以大于1，越大越精细
        self.sizes = [resolution * i for i in (0.665, 0.3122, 4)]
        self.duration = duration
        self.fnt = ImageFont.truetype(f'{base_dir}/templates/Courier New.ttf', 10)
        self.init()

        try:
            pathlib.Path(self.out_dir).mkdir()
        except:
            pass

    def init(self):
        chrx, chry = self.fnt.getsize(chr(32))
        normalization = chrx * chry * 255

        weights = {}
        # get gray density for characters in range [32, 126]
        for i in range(32, 127):
            chr_image = self.fnt.getmask(chr(i))
            sizex, sizey = chr_image.size
            ctr = sum(chr_image.getpixel((x, y)) for y in range(sizey) for x in range(sizex))
            weights[chr(i)] = ctr / normalization

        weights[chr(32)] = 0.01  # increase it to make blank space ' ' more available
        weights.pop('_', None)  # remove '_' since it is too directional
        weights.pop('-', None)  # remove '-' since it is too directional

        self.sorted_weights = sorted(weights.items(), key=operator.itemgetter(1))
        self.scores = [y for (x, y) in self.sorted_weights]

        return self.sorted_weights

    def get_char(self, val):
        '''
        根据灰度值返回相应的字符串
        '''
        # find index of val in scores
        index = bisect.bisect_left(self.scores, val)

        # check and choose the nearer one between current index and former index
        if index > 0 and self.sorted_weights[index][1] + self.sorted_weights[index - 1][1] > 2 * val:
            index -= 1

        return self.sorted_weights[index][0]

    def transform(self, image):
        """
        return a string containing characters representing each pixel
        """
        # find index of val in scores
        maximum = self.scores[-1]
        im = image.resize((int(image.size[0] * self.sizes[0]), int(image.size[1] * self.sizes[1])))
        im = im.convert("L")  # transform image to black-white
        txt = ''
        for h in range(im.size[1]):
            for w in range(im.size[0]):
                gray = im.getpixel((w, h))
                txt += self.get_char(maximum * (1 - gray / 255))  # append characters
            txt += '\r\n'
        im.close()
        return txt

    def transform2(self, image):
        chs = "MNHQ$OC?7>!:-;. "
        max_len = 80
        width, height = image.size
        rate = float(max_len) / max(width, height)
        width = int(rate * width)
        height = int(rate * height)
        txt = ''
        for h in range(height):
            for w in range(width):
                rgb = image.getpixel((w, h))
                txt += chs[int(sum(rgb) / 3.0 / 256.0 * 16)]
            txt += '\r\n'
        return txt


    def gif2png(self):
        # im = self.image.copy()
        im = self.image
        palette = im.getpalette()
        images = []
        try:
            while True:
                im.putpalette(palette)
                new_im = Image.new('RGB', im.size)
                new_im.paste(im)
                images.append(new_im)
                im.seek(im.tell() + 1)
        except EOFError:
            pass
        return images

    def png2gif(self):
        pass

    def png2gif_save_1(self):
        images = self.gif2png()
        im = Image.new('RGB', self.image.size)
        # 0 表示 无限循化
        im.save('test.gif', save_all=True, append_images=images, loop=0, duration=80)

    def png2gif_save_2(self):
        images = []
        for i in range(1, 5):
            images.append(imageio.imread(f'{i}.png'))
        imageio.mimsave('_test.gif', images, duration=0.1)

    def to_txt(self, txt, name='out.txt'):
        return NotImplemented

    def to_json(self, txts, name='out.json', convert=True):
        pass

        '''
        convert space to &nbsp;
        :return: [['fsfsf', 'fsdfsf'], ..., []]
        '''
        data = []
        for txt in txts:
            item = []
            lines = txt.split('\r\n')
            if convert:
                for line in lines:
                    item.append(re.sub(r'\s', '&nbsp;', line))
            else:
                item = lines
            data.append(item)
        with open(os.path.join(self.out_dir, name), 'w') as f:
            json.dump(data, f)

    def to_image(self, txts, name='out.gif'):
        images = []
        for txt in txts:
            im = Image.new('L', (int(self.image.size[0] * self.sizes[2]), int(self.image.size[1] * self.sizes[2])), 255)
            # im = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(im)
            draw.text((0, 0), txt, font=self.fnt, fill=0)
            images.append(im)
        im = Image.new('RGB', (int(self.image.size[0] * self.sizes[2]), int(self.image.size[1] * self.sizes[2])))
        # im = Image.new('RGB', (width, height))
        im.save(os.path.join(self.out_dir, name), save_all=True, append_images=images, loop=0, duration=self.duration)
        im.close()

    def to_html(self, txts, name='out.html'):
        with open(f'{base_dir}/templates/gif.html') as f:
            template = Template(f.read())
            html = template.render(txts=txts)

        with open(os.path.join(self.out_dir, name), 'w') as f:
            f.write(html)

    def get_name(self):
        path = pathlib.Path(self.image.filename)
        return path.name.split('.')

    def run(self, json=False, image=True, html=False, *args, **kwargs):
        name, suffix = self.get_name()
        images = self.gif2png()
        txts = []
        for image in images:
            txt = self.transform2(image)
            txts.append(txt)

        self.image.close()
        if json:
            self.to_json(txts, f'{name}.json')
        if image:
            self.to_image(txts, f'{name}.gif')
        if html:
            self.to_html(txts, f'{name}.html')
