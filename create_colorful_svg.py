#!/usr/bin/env python3
"""
创建包含彩色图像的SVG文件
使用方法: python3 create_colorful_svg.py your_image.png
"""

import sys
import base64
import os
from PIL import Image

def create_colorful_svg(image_path, output_path="colorful_logo.svg"):
    """将图片转换为包含彩色图像的SVG"""
    
    # 检查输入文件
    if not os.path.exists(image_path):
        print(f"错误: 文件 {image_path} 不存在")
        return False
    
    # 调整图片尺寸为32x34
    try:
        with Image.open(image_path) as img:
            # 转换为RGBA模式以保持透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # 调整尺寸
            img_resized = img.resize((32, 34), Image.Resampling.LANCZOS)
            
            # 保存为临时PNG文件
            temp_png = "temp_resized.png"
            img_resized.save(temp_png, "PNG")
            
            # 读取PNG文件并转换为base64
            with open(temp_png, "rb") as f:
                png_data = f.read()
                base64_data = base64.b64encode(png_data).decode('utf-8')
            
            # 删除临时文件
            os.remove(temp_png)
            
    except Exception as e:
        print(f"处理图片时出错: {e}")
        return False
    
    # 创建SVG文件
    svg_content = f'''<svg width="32" height="34" viewBox="0 0 32 34" fill="none" xmlns="http://www.w3.org/2000/svg">
  <image href="data:image/png;base64,{base64_data}" width="32" height="34"/>
</svg>'''
    
    # 写入SVG文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"成功创建彩色SVG文件: {output_path}")
        return True
    except Exception as e:
        print(f"写入SVG文件时出错: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("使用方法: python3 create_colorful_svg.py <图片文件>")
        print("例如: python3 create_colorful_svg.py my_logo.png")
        return
    
    image_path = sys.argv[1]
    output_path = "colorful_logo.svg"
    
    if create_colorful_svg(image_path, output_path):
        print(f"\n下一步操作:")
        print(f"1. 检查生成的SVG: cat {output_path}")
        print(f"2. 替换原logo: cp {output_path} web/public/logo.svg")
        print(f"3. 测试效果: 在浏览器中查看")

if __name__ == "__main__":
    main() 