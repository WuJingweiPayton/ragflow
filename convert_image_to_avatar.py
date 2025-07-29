#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片转换为 Avatar 字段的 Base64 格式
支持多种图片格式：jpg, jpeg, png, gif, bmp, webp 等
"""

import base64
import os
import sys
from PIL import Image
import io

def convert_image_to_base64(image_path, output_format='JPEG', max_size=(200, 200)):
    """
    将图片转换为 base64 格式
    
    Args:
        image_path (str): 图片文件路径
        output_format (str): 输出格式 (JPEG, PNG, etc.)
        max_size (tuple): 最大尺寸 (width, height)
    
    Returns:
        str: base64 编码的图片数据，包含 data URL 前缀
    """
    try:
        # 打开图片
        with Image.open(image_path) as img:
            # 转换为 RGB 模式（如果是 RGBA，去除透明通道）
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整图片大小（保持宽高比）
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存到内存缓冲区
            buffer = io.BytesIO()
            img.save(buffer, format=output_format, quality=85, optimize=True)
            buffer.seek(0)
            
            # 转换为 base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            # 返回完整的 data URL
            mime_type = f"image/{output_format.lower()}"
            return f"data:{mime_type};base64,{img_base64}"
            
    except Exception as e:
        print(f"转换失败: {e}")
        return None

def convert_image_file(input_path, output_path=None, format='JPEG', max_size=(200, 200)):
    """
    转换图片文件并保存结果
    
    Args:
        input_path (str): 输入图片路径
        output_path (str): 输出文件路径（可选）
        format (str): 输出格式
        max_size (tuple): 最大尺寸
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"错误: 文件不存在 - {input_path}")
        return
    
    # 转换图片
    base64_data = convert_image_to_base64(input_path, format, max_size)
    
    if base64_data:
        print("✅ 转换成功!")
        print(f"📁 输入文件: {input_path}")
        print(f"📏 输出格式: {format}")
        print(f"📐 最大尺寸: {max_size[0]}x{max_size[1]}")
        print(f"📊 Base64 长度: {len(base64_data)} 字符")
        
        # 保存到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(base64_data)
            print(f"💾 已保存到: {output_path}")
        else:
            # 显示前100个字符
            print(f"🔍 Base64 预览: {base64_data[:100]}...")
            print("\n📋 完整的 base64 数据:")
            print(base64_data)
    else:
        print("❌ 转换失败!")

def batch_convert(input_dir, output_dir=None, format='JPEG', max_size=(200, 200)):
    """
    批量转换目录中的图片
    
    Args:
        input_dir (str): 输入目录
        output_dir (str): 输出目录（可选）
        format (str): 输出格式
        max_size (tuple): 最大尺寸
    """
    if not os.path.exists(input_dir):
        print(f"错误: 目录不存在 - {input_dir}")
        return
    
    # 支持的图片格式
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
    
    # 创建输出目录
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历目录
    for filename in os.listdir(input_dir):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            input_path = os.path.join(input_dir, filename)
            base64_data = convert_image_to_base64(input_path, format, max_size)
            
            if base64_data:
                if output_dir:
                    output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(base64_data)
                    print(f"✅ {filename} -> {output_path}")
                else:
                    print(f"✅ {filename} - 转换成功")
            else:
                print(f"❌ {filename} - 转换失败")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 转换单个文件:")
        print("   python convert_image_to_avatar.py <图片路径> [输出文件路径]")
        print("2. 批量转换:")
        print("   python convert_image_to_avatar.py --batch <输入目录> [输出目录]")
        print("3. 交互模式:")
        print("   python convert_image_to_avatar.py --interactive")
        return
    
    if sys.argv[1] == '--batch':
        if len(sys.argv) < 3:
            print("错误: 请指定输入目录")
            return
        input_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        batch_convert(input_dir, output_dir)
    
    elif sys.argv[1] == '--interactive':
        # 交互模式
        input_path = input("请输入图片路径: ").strip()
        output_path = input("请输入输出文件路径 (可选): ").strip() or None
        format = input("请输入输出格式 (JPEG/PNG, 默认JPEG): ").strip() or 'JPEG'
        max_width = input("请输入最大宽度 (默认200): ").strip() or '200'
        max_height = input("请输入最大高度 (默认200): ").strip() or '200'
        
        convert_image_file(input_path, output_path, format, (int(max_width), int(max_height)))
    
    else:
        # 单个文件转换
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        convert_image_file(input_path, output_path)

if __name__ == "__main__":
    main() 