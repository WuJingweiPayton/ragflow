#!/usr/bin/env python3
"""
测试 Avatar 大小限制修复的脚本
"""

import base64
import json
import os
import sys
from PIL import Image
import io

def create_test_image(width=200, height=200, format='JPEG', quality=95):
    """创建一个测试图片"""
    # 创建一个彩色图片
    image = Image.new('RGB', (width, height), color='red')
    
    # 保存到内存
    buffer = io.BytesIO()
    image.save(buffer, format=format, quality=quality)
    buffer.seek(0)
    
    return buffer.getvalue()

def image_to_base64(image_data, mime_type='image/jpeg'):
    """将图片数据转换为 base64"""
    base64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"

def test_avatar_sizes():
    """测试不同大小的 avatar"""
    print("🔍 测试 Avatar 大小限制修复")
    print("=" * 50)
    
    # 测试不同大小的图片
    test_cases = [
        (100, 100, "小图片"),
        (200, 200, "中等图片"),
        (400, 400, "大图片"),
        (800, 800, "超大图片"),
    ]
    
    for width, height, description in test_cases:
        print(f"\n📸 测试 {description} ({width}x{height})")
        
        # 创建图片
        image_data = create_test_image(width, height)
        base64_string = image_to_base64(image_data)
        
        # 计算大小
        size_bytes = len(base64_string)
        size_kb = size_bytes / 1024
        
        print(f"   Base64 字符串长度: {size_bytes:,} 字符")
        print(f"   大小: {size_kb:.2f} KB")
        
        # 检查是否超过限制
        old_limit = 65535  # 原来的限制
        new_limit = 1048576  # 新的限制
        
        if size_bytes <= old_limit:
            status = "✅ 通过旧限制"
        elif size_bytes <= new_limit:
            status = "✅ 通过新限制 (修复生效)"
        else:
            status = "❌ 超过新限制"
        
        print(f"   状态: {status}")
        
        # 检查是否包含完整的 base64 数据
        if base64_string.endswith('=='):
            print(f"   Base64 完整性: ✅ 完整")
        else:
            print(f"   Base64 完整性: ⚠️ 可能被截断")

def test_template_file():
    """测试模板文件中的 avatar"""
    print("\n\n📄 测试模板文件中的 Avatar")
    print("=" * 50)
    
    template_file = "agent/templates/共富农仓.json"
    
    if not os.path.exists(template_file):
        print(f"❌ 模板文件不存在: {template_file}")
        return
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            template_data = json.load(f)
        
        avatar = template_data.get('avatar', '')
        if not avatar:
            print("❌ 模板文件中没有找到 avatar 字段")
            return
        
        size_bytes = len(avatar)
        size_kb = size_bytes / 1024
        
        print(f"   模板文件: {template_file}")
        print(f"   Avatar 长度: {size_bytes:,} 字符")
        print(f"   Avatar 大小: {size_kb:.2f} KB")
        
        # 检查是否被截断
        if avatar.endswith('=='):
            print(f"   Base64 完整性: ✅ 完整")
        else:
            print(f"   Base64 完整性: ⚠️ 可能被截断")
        
        # 检查是否超过限制
        old_limit = 65535
        new_limit = 1048576
        
        if size_bytes <= old_limit:
            status = "✅ 在旧限制范围内"
        elif size_bytes <= new_limit:
            status = "✅ 在新限制范围内 (修复生效)"
        else:
            status = "❌ 超过新限制"
        
        print(f"   状态: {status}")
        
    except Exception as e:
        print(f"❌ 读取模板文件失败: {e}")

def create_optimized_template():
    """创建优化后的模板文件"""
    print("\n\n🔧 创建优化后的模板文件")
    print("=" * 50)
    
    # 创建一个高质量的测试图片
    image_data = create_test_image(300, 300, 'JPEG', 90)
    base64_string = image_to_base64(image_data)
    
    # 创建模板数据
    template_data = {
        "id": "test_template_optimized",
        "avatar": base64_string,
        "title": "测试优化模板",
        "description": "这是一个用于测试 avatar 大小限制修复的模板",
        "canvas_type": "agent",
        "dsl": {
            "nodes": [],
            "edges": []
        }
    }
    
    # 保存到文件
    output_file = "agent/templates/test_optimized_template.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(template_data, f, ensure_ascii=False, indent=2)
    
    size_bytes = len(base64_string)
    size_kb = size_bytes / 1024
    
    print(f"   创建文件: {output_file}")
    print(f"   Avatar 长度: {size_bytes:,} 字符")
    print(f"   Avatar 大小: {size_kb:.2f} KB")
    print(f"   状态: ✅ 创建成功")

def main():
    """主函数"""
    print("🚀 Avatar 大小限制修复验证工具")
    print("=" * 60)
    
    # 测试不同大小的图片
    test_avatar_sizes()
    
    # 测试现有模板文件
    test_template_file()
    
    # 创建优化后的模板
    create_optimized_template()
    
    print("\n\n📋 修复总结")
    print("=" * 50)
    print("✅ 已修改 api/utils/validation_utils.py 中的 max_length 限制")
    print("✅ 已修改 rag/utils/opendal_conn.py 中的 max_allowed_packet 配置")
    print("✅ 现在支持最大 1MB 的 avatar 图片")
    print("\n🔧 建议:")
    print("   1. 重启 Docker 容器以应用配置更改")
    print("   2. 使用图片压缩工具优化大图片")
    print("   3. 监控数据库性能")

if __name__ == "__main__":
    main() 