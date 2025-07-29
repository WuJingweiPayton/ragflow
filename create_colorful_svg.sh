#!/bin/bash

# 创建包含彩色图像的SVG文件
# 使用方法: ./create_colorful_svg.sh your_image.png

if [ $# -eq 0 ]; then
    echo "使用方法: $0 <图片文件>"
    echo "例如: $0 my_logo.png"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="colorful_logo.svg"
TEMP_PNG="temp_resized.png"

echo "创建彩色SVG文件: $INPUT_FILE -> $OUTPUT_FILE"

# 1. 调整图片尺寸为32x34
echo "步骤1: 调整图片尺寸..."
convert "$INPUT_FILE" -resize 32x34! "$TEMP_PNG"

# 2. 转换为base64
echo "步骤2: 转换为base64..."
BASE64_DATA=$(base64 -w 0 "$TEMP_PNG")

# 3. 创建SVG文件
echo "步骤3: 创建SVG文件..."
cat > "$OUTPUT_FILE" << EOF
<svg width="32" height="34" viewBox="0 0 32 34" fill="none" xmlns="http://www.w3.org/2000/svg">
  <image href="data:image/png;base64,$BASE64_DATA" width="32" height="34"/>
</svg>
EOF

# 4. 清理临时文件
rm -f "$TEMP_PNG"

echo "完成! 输出文件: $OUTPUT_FILE"
echo ""
echo "下一步操作:"
echo "1. 检查生成的SVG: cat $OUTPUT_FILE"
echo "2. 替换原logo: cp $OUTPUT_FILE web/public/logo.svg"
echo "3. 测试效果: 在浏览器中查看" 