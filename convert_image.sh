#!/bin/bash

# 图片转换为 Base64 的 Bash 脚本
# 需要安装: imagemagick, base64

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo -e "${BLUE}图片转换为 Base64 工具${NC}"
    echo ""
    echo "使用方法:"
    echo "  $0 <输入图片> [输出文件] [格式] [最大尺寸]"
    echo ""
    echo "参数:"
    echo "  输入图片    要转换的图片文件路径"
    echo "  输出文件    输出的base64文件路径 (可选)"
    echo "  格式        jpg, png, gif (默认: jpg)"
    echo "  最大尺寸    格式: 宽x高 (默认: 200x200)"
    echo ""
    echo "示例:"
    echo "  $0 image.jpg"
    echo "  $0 image.png output.txt png"
    echo "  $0 image.jpg output.txt jpg 300x300"
    echo ""
}

# 检查依赖
check_dependencies() {
    if ! command -v convert &> /dev/null; then
        echo -e "${RED}错误: 未找到 ImageMagick (convert 命令)${NC}"
        echo "请安装 ImageMagick:"
        echo "  Ubuntu/Debian: sudo apt-get install imagemagick"
        echo "  CentOS/RHEL: sudo yum install ImageMagick"
        echo "  macOS: brew install imagemagick"
        exit 1
    fi
    
    if ! command -v base64 &> /dev/null; then
        echo -e "${RED}错误: 未找到 base64 命令${NC}"
        exit 1
    fi
}

# 转换图片
convert_image() {
    local input_file="$1"
    local output_file="$2"
    local format="${3:-jpg}"
    local max_size="${4:-200x200}"
    
    # 检查输入文件
    if [[ ! -f "$input_file" ]]; then
        echo -e "${RED}错误: 文件不存在 - $input_file${NC}"
        exit 1
    fi
    
    # 创建临时文件
    local temp_file=$(mktemp)
    
    echo -e "${BLUE}开始转换图片...${NC}"
    echo "📁 输入文件: $input_file"
    echo "📏 输出格式: $format"
    echo "📐 最大尺寸: $max_size"
    
    # 使用 ImageMagick 转换图片
    if convert "$input_file" -resize "$max_size" -quality 85 "$temp_file"; then
        # 转换为 base64
        local mime_type="image/$format"
        local base64_data="data:$mime_type;base64,$(base64 -w 0 "$temp_file")"
        
        echo -e "${GREEN}✅ 转换成功!${NC}"
        echo "📊 Base64 长度: ${#base64_data} 字符"
        
        # 保存或显示结果
        if [[ -n "$output_file" ]]; then
            echo "$base64_data" > "$output_file"
            echo -e "${GREEN}💾 已保存到: $output_file${NC}"
        else
            echo ""
            echo -e "${YELLOW}📋 Base64 数据:${NC}"
            echo "$base64_data"
        fi
        
        # 清理临时文件
        rm -f "$temp_file"
    else
        echo -e "${RED}❌ 转换失败!${NC}"
        rm -f "$temp_file"
        exit 1
    fi
}

# 批量转换
batch_convert() {
    local input_dir="$1"
    local output_dir="$2"
    local format="${3:-jpg}"
    local max_size="${4:-200x200}"
    
    if [[ ! -d "$input_dir" ]]; then
        echo -e "${RED}错误: 目录不存在 - $input_dir${NC}"
        exit 1
    fi
    
    # 创建输出目录
    if [[ -n "$output_dir" ]] && [[ ! -d "$output_dir" ]]; then
        mkdir -p "$output_dir"
    fi
    
    echo -e "${BLUE}开始批量转换...${NC}"
    echo "📁 输入目录: $input_dir"
    echo "📏 输出格式: $format"
    echo "📐 最大尺寸: $max_size"
    
    # 支持的图片格式
    local count=0
    local success=0
    
    for file in "$input_dir"/*.{jpg,jpeg,png,gif,bmp,webp,tiff,tif}; do
        if [[ -f "$file" ]]; then
            count=$((count + 1))
            local filename=$(basename "$file")
            local name_without_ext="${filename%.*}"
            
            echo -n "处理: $filename ... "
            
            if [[ -n "$output_dir" ]]; then
                local output_file="$output_dir/${name_without_ext}.txt"
                if convert_image "$file" "$output_file" "$format" "$max_size" > /dev/null 2>&1; then
                    echo -e "${GREEN}✅${NC}"
                    success=$((success + 1))
                else
                    echo -e "${RED}❌${NC}"
                fi
            else
                if convert_image "$file" "" "$format" "$max_size" > /dev/null 2>&1; then
                    echo -e "${GREEN}✅${NC}"
                    success=$((success + 1))
                else
                    echo -e "${RED}❌${NC}"
                fi
            fi
        fi
    done
    
    echo ""
    echo -e "${GREEN}批量转换完成!${NC}"
    echo "📊 总计: $count 个文件"
    echo "✅ 成功: $success 个文件"
    echo "❌ 失败: $((count - success)) 个文件"
}

# 主函数
main() {
    # 检查参数
    if [[ $# -eq 0 ]] || [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        show_help
        exit 0
    fi
    
    # 检查依赖
    check_dependencies
    
    # 处理批量转换
    if [[ "$1" == "--batch" ]]; then
        if [[ $# -lt 2 ]]; then
            echo -e "${RED}错误: 请指定输入目录${NC}"
            exit 1
        fi
        batch_convert "$2" "$3" "$4" "$5"
    else
        # 单个文件转换
        convert_image "$1" "$2" "$3" "$4"
    fi
}

# 运行主函数
main "$@" 