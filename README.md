# image-panda

熊猫画图, 支持 png、jpeg、gif 格式。 

# Usage

## 字符画

```
Usage:

  python panda.py <ycy.jpg> [options]

Options:

  --img          要处理的图片
  --dir          输出目录, 默认 dest/
  --max_len      每行的字符数, 默认 80
  --duration     gif 图片每帧的持续时间, 默认 80, 单位 ms
  --text         默认 False, gif图片无此选项
  --json         默认 False, 每个元素表示图片的每行
                 png/jpeg: ['abcd', 'sfdfs',...]
                 gif: [['abcd', 'sfdfs',...],...[...]]
  --image        默认 False, 生成 png/gif 图片
  --html         默认 True
  --color        默认 False, 是否带有颜色。 每个字符都用 span 包裹起来
                 如 "<span style='color:rgb{rgb};'>{char}</span>"
                 此选项耗时较长!
  --style        默认为 char, 可选 block 或 char, 当指定为 block 时, --color 强制为 True
```

## 手绘图

```
Usage:

  python panda.py <ycy.jpg> --sketch [options]

Options:

  --img          要处理的图片
  --dir          输出目录, 默认 dest/
  --sketch       必须指定此参数, 才能生成图手绘图
  --depth        深度值, 可选 0-100, 默认 10
  --duration     处理 gif 图片时的每帧的持续时间, 默认 80, 单位 ms
           
```
