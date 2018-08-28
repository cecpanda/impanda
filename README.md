# image-panda

# Usage

## png/jpeg

```
Usage:

  python panda.py <img> [options]

Options:

  --img  要处理的图片
  --dir  输出目录, 默认 dest/
  --max_len  每行的字符数, 默认 80
  --text
  --json  格式:['abcd', 'sfdfs',...], 每个元素表示图片的每行
  --image
  --html
  --color  是否带有颜色, 每个字符都用 span 包裹起来, 耗时较长。如 "<span style='color:rgb{rgb};'>{char}</span>"
  --style  block/char, 默认为 char, 当指定为 block 时, --color 强制为 True
```

## gif
```
Usage:

  python panda.py <img> [options]

Options:

  --img  要处理的图片
  --dir  输出目录, 默认 dest/
  --max_len  每行的字符数, 默认 80
  --json  格式:[['abcd', 'sfdfs',...],...[...]], 每个元素表示图片
  --image
  --html
  --color  是否带有颜色, 每个字符都用 span 包裹起来, 耗时较长。如 "<span style='color:rgb{rgb};'>{char}</span>"
  --style  block/char, 默认为 char, 当指定为 block 时, --color 强制为 True
```
