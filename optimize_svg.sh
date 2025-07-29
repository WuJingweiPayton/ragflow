#!/bin/bash

# SVG优化脚本
# 使用方法: ./optimize_svg.sh input.svg

if [ $# -eq 0 ]; then
    echo "使用方法: $0 <SVG文件>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="optimized_${INPUT_FILE}"

echo "优化SVG文件: $INPUT_FILE"

# 创建优化的SVG模板
cat > "$OUTPUT_FILE" << 'EOF'
<svg width="32" height="34" viewBox="0 0 32 34" fill="none" xmlns="http://www.w3.org/2000/svg">
EOF

# 提取原SVG的内容并添加到优化版本中
if grep -q "<image" "$INPUT_FILE"; then
    # 如果是image标签，直接复制
    sed -n '/<image/,/\/>/p' "$INPUT_FILE" >> "$OUTPUT_FILE"
else
    # 如果是path标签，复制所有path
    sed -n '/<path/,/\/>/p' "$INPUT_FILE" >> "$OUTPUT_FILE"
fi

echo "</svg>" >> "$OUTPUT_FILE"

echo "优化完成! 输出文件: $OUTPUT_FILE" 