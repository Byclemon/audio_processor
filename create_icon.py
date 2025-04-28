#!/usr/bin/env python3
"""
创建应用图标 - 生成绿色背景带有合并箭头的图标
"""
from PIL import Image, ImageDraw
import os

def create_icon():
    # 创建assets目录如果不存在
    if not os.path.exists('assets'):
        os.makedirs('assets')
    
    # 创建一个512x512的图像，使用浅绿色背景
    size = 512
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    
    # 创建圆角矩形
    draw = ImageDraw.Draw(img)
    
    # 绘制绿色圆角矩形作为背景
    rect_size = size - 20
    rect_pos = 10
    rect_radius = 100
    green_color = (92, 204, 120, 255)  # 浅绿色
    
    # 绘制圆角矩形
    draw.rounded_rectangle(
        [(rect_pos, rect_pos), (rect_pos + rect_size, rect_pos + rect_size)],
        fill=green_color,
        radius=rect_radius
    )
    
    # 设置白色用于绘制箭头和线条
    white_color = (255, 255, 255, 255)
    
    # 绘制中央垂直线
    line_width = 30
    center_x = size // 2
    v_line_top = size // 5
    v_line_bottom = size - size // 5
    draw.rectangle(
        [(center_x - line_width//2, v_line_top), 
         (center_x + line_width//2, v_line_bottom)],
        fill=white_color
    )
    
    # 绘制左箭头
    arrow_width = 30
    arrow_length = 80
    arrow_y = size // 2
    # 箭头左侧
    draw.rectangle(
        [(center_x - arrow_length - line_width//2, arrow_y - arrow_width//2),
         (center_x - line_width//2, arrow_y + arrow_width//2)],
        fill=white_color
    )
    # 箭头头部
    points_left = [
        (center_x - line_width//2 - 50, arrow_y),
        (center_x - line_width//2, arrow_y - 40),
        (center_x - line_width//2, arrow_y + 40),
    ]
    draw.polygon(points_left, fill=white_color)
    
    # 绘制右箭头
    # 箭头右侧
    draw.rectangle(
        [(center_x + line_width//2, arrow_y - arrow_width//2),
         (center_x + arrow_length + line_width//2, arrow_y + arrow_width//2)],
        fill=white_color
    )
    # 箭头头部
    points_right = [
        (center_x + line_width//2 + 50, arrow_y),
        (center_x + line_width//2, arrow_y - 40),
        (center_x + line_width//2, arrow_y + 40),
    ]
    draw.polygon(points_right, fill=white_color)
    
    # 保存为PNG和ICNS（macOS图标格式）
    png_path = os.path.join('assets', 'app_icon.png')
    img.save(png_path)
    
    print(f"图标已保存到 {png_path}")
    
    # 返回图标路径
    return png_path

if __name__ == '__main__':
    create_icon() 