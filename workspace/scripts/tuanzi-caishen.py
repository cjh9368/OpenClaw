#!/usr/bin/env python3
"""
团子财神图生成器
给团子的照片添加财神元素
"""

from PIL import Image, ImageDraw, ImageFont
import sys

# 输入输出路径
input_path = "/home/admin/.openclaw/media/inbound/file_0---df275c24-a72b-499e-ac2f-a34d6aa8a6bf.jpg"
output_path = "/home/admin/.openclaw/workspace/tuanzi-caishen.jpg"

# 打开图片
img = Image.open(input_path)
width, height = img.size

# 创建绘图对象
draw = ImageDraw.Draw(img)

# 1. 添加红色边框 (财神风格)
border_width = 20
draw.rectangle([0, 0, width-1, height-1], outline="#DC143C", width=border_width)

# 2. 添加金色文字 "财神到"
# 尝试使用系统字体
font_paths = [
    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "C:\\Windows\\Fonts\\simhei.ttf",
]

font = None
for fp in font_paths:
    try:
        font = ImageFont.truetype(fp, 60)
        print(f"使用字体：{fp}")
        break
    except:
        continue

if font is None:
    font = ImageFont.load_default()
    print("使用默认字体")

# 文字内容
text_top = " 财神到 "
text_bottom = "团子送福"

# 获取文字边界框
bbox_top = draw.textbbox((0, 0), text_top, font=font)
bbox_bottom = draw.textbbox((0, 0), text_bottom, font=font)

text_width_top = bbox_top[2] - bbox_top[0]
text_width_bottom = bbox_bottom[2] - bbox_bottom[0]
text_height = bbox_top[3] - bbox_top[1]

# 3. 添加文字背景（半透明黑色）
padding = 20
draw.rectangle(
    [10, 10, text_width_top + padding*2, text_height + padding*2],
    fill=(0, 0, 0, 180)
)

draw.rectangle(
    [10, height - text_height - padding*2 - 10, text_width_bottom + padding*2, height - 10],
    fill=(0, 0, 0, 180)
)

# 4. 绘制金色文字
gold_color = "#FFD700"
draw.text((padding, 15), text_top, fill=gold_color, font=font)
draw.text((padding, height - text_height - padding - 15), text_bottom, fill=gold_color, font=font)

# 5. 添加一些元宝装饰（简单的椭圆形）
def draw_yuanbao(draw, x, y, size=30):
    # 元宝主体
    draw.ellipse([x, y, x+size, y+size//2], fill="#FFD700", outline="#FFA500", width=2)
    draw.rectangle([x+5, y+size//4, x+size-5, y+size//2+5], fill="#FFD700", outline="#FFA500", width=2)

# 在四个角添加元宝装饰
draw_yuanbao(draw, width - 60, 20, 40)
draw_yuanbao(draw, width - 60, height - 60, 40)

# 保存图片
img.save(output_path, "JPEG", quality=95)

print(f"✅ 团子财神图已生成：{output_path}")
print(f"图片尺寸：{width}x{height}")
