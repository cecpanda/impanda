from PIL import Image, ImageDraw, ImageFont


ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_char(r, g, b, alpha=256):
    '''将256灰度映射到70个字符上  '''
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    # 计算灰度
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


def start():
    width = 80
    height = 60
    im = Image.open('ycy.jpg')
    # im = im.resize((width, height), Image.NEAREST)  # 更改图片的显示比例
    txt = ""
    for i in range(height):
        for j in range(width):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'

    with open("output.txt", 'w') as f:
        f.write(txt)

    im1 = Image.new('L', im.size, 255)
    draw = ImageDraw.Draw(im1)
    draw.text((0, 0), txt, fill=0)
    im1.save('output.jpg')
    im1.close()