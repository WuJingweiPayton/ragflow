#!/bin/bash

# 简单的图片转SVG脚本
# 使用方法: ./simple_convert.sh your_image.png

if [ $# -eq 0 ]; then
    echo "使用方法: $0 <图片文件>"
    echo "例如: $0 my_logo.png"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="converted_logo.svg"

echo "转换图片: $INPUT_FILE -> $OUTPUT_FILE"

# 使用ImageMagick直接转换
convert "$INPUT_FILE" -resize 32x34! "$OUTPUT_FILE"

echo "转换完成! 输出文件: $OUTPUT_FILE"
echo ""
echo "下一步:"
echo "cp $OUTPUT_FILE web/public/logo.svg" 