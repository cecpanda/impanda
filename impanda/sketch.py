# -*- coding: utf-8 -*-

'''
手绘效果的特征：
  黑白灰色
  边界线条较重
  相同或相近色彩趋于白色
'''

import os
import pathlib

import numpy as np
from PIL import Image


class Sketch(object):

    def __init__(self, image, out_dir='dest/', depth=10, duration=80):
        self.image = image
        self.out_dir = out_dir
        self.depth = depth
        self.duration = duration
        self.init()

    def init(self):
        self.image = Image.open(self.image)
        format = self.image.format
        if format != 'PNG' and format != 'JPEG' and format != 'GIF':
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

    def transform(self, image):
        '''
        image: Image 对象
        return: Image 对象
        '''
        depth = self.depth
        a = np.array(image.convert('L')).astype('float')
        grad = np.gradient(a)  # 取图像灰度的梯度值
        grad_x, grad_y = grad  # 分别取横纵图像梯度值
        grad_x = grad_x * depth / 100.
        grad_y = grad_y * depth / 100.
        A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
        uni_x = grad_x / A
        uni_y = grad_y / A
        uni_z = 1. / A

        vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
        vec_az = np.pi / 4.   # 光源的方位角度，弧度值
        dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
        dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
        dz = np.sin(vec_el)   # 光源对z 轴的影响

        b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
        b = b.clip(0, 255)

        im = Image.fromarray(b.astype('uint8'))  # 重构图像
        return im

    def get_name(self, image):
        path = pathlib.Path(image.filename)
        return path.name.split('.')

    def run(self):
        name, suffix = self.get_name(self.image)
        format = self.image.format

        if format == 'GIF':
            images = self.gif_to_png(self.image)
            ims = []
            for image in images:
                im = self.transform(image)
                ims.append(im)
            im = Image.new('RGB', self.image.size)
            im.save(os.path.join(self.out_dir, f'{name}.gif'), save_all=True, append_images=ims, loop=0, duration=self.duration)
            im.close()
        else:
            im = self.transform(self.image)
            im.save(os.path.join(self.out_dir, f'{name}.png'))
