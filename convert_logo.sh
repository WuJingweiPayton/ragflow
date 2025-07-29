#!/bin/bash

# 图片转换为SVG的脚本
# 使用方法: ./convert_logo.sh your_image.png

if [ $# -eq 0 ]; then
    echo "使用方法: $0 <图片文件>"
    echo "例如: $0 my_logo.png"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="converted_logo.svg"
TEMP_PNG="temp_32x34.png"

echo "开始转换图片: $INPUT_FILE"

# 检查输入文件是否存在
if [ ! -f "$INPUT_FILE" ]; then
    echo "错误: 文件 $INPUT_FILE 不存在"
    exit 1
fi

# 1. 调整图片尺寸为32x34
echo "步骤1: 调整图片尺寸为32x34..."
convert "$INPUT_FILE" -resize 32x34! "$TEMP_PNG"

# 2. 转换为SVG（使用ImageMagick的SVG输出）
echo "步骤2: 转换为SVG..."
convert "$TEMP_PNG" "$OUTPUT_FILE"

# 3. 优化SVG文件
echo "步骤3: 优化SVG文件..."

# 创建优化的SVG模板
cat > "$OUTPUT_FILE" << 'EOF'
<svg width="32" height="34" viewBox="0 0 32 34" fill="none" xmlns="http://www.w3.org/2000/svg">
  <image href="data:image/png;base64,'$(base64 -w 0 "$TEMP_PNG")'" width="32" height="34"/>
</svg>
EOF

# 4. 清理临时文件
rm -f "$TEMP_PNG"

echo "转换完成!"
echo "输出文件: $OUTPUT_FILE"
echo ""
echo "下一步操作:"
echo "1. 检查生成的SVG文件: cat $OUTPUT_FILE"
echo "2. 替换原logo: cp $OUTPUT_FILE web/public/logo.svg"
echo "3. 测试效果: 在浏览器中查看" 