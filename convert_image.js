#!/usr/bin/env node

/**
 * 图片转换为 Base64 的 Node.js 脚本
 * 需要安装: npm install sharp fs path
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// 颜色输出
const colors = {
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    reset: '\x1b[0m'
};

function log(message, color = 'reset') {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * 将图片转换为 base64 格式
 * @param {string} imagePath - 图片文件路径
 * @param {Object} options - 转换选项
 * @returns {Promise<string>} base64 数据
 */
async function convertImageToBase64(imagePath, options = {}) {
    const {
        format = 'jpeg',
        maxWidth = 200,
        maxHeight = 200,
        quality = 85
    } = options;

    try {
        // 读取图片并处理
        const imageBuffer = await sharp(imagePath)
            .resize(maxWidth, maxHeight, {
                fit: 'inside',
                withoutEnlargement: true
            })
            .toFormat(format, { quality })
            .toBuffer();

        // 转换为 base64
        const base64Data = imageBuffer.toString('base64');
        const mimeType = `image/${format}`;
        
        return `data:${mimeType};base64,${base64Data}`;
    } catch (error) {
        throw new Error(`转换失败: ${error.message}`);
    }
}

/**
 * 转换单个文件
 * @param {string} inputPath - 输入文件路径
 * @param {string} outputPath - 输出文件路径（可选）
 * @param {Object} options - 转换选项
 */
async function convertFile(inputPath, outputPath = null, options = {}) {
    try {
        // 检查输入文件
        if (!fs.existsSync(inputPath)) {
            log(`错误: 文件不存在 - ${inputPath}`, 'red');
            return;
        }

        log('开始转换图片...', 'blue');
        log(`📁 输入文件: ${inputPath}`);
        log(`📏 输出格式: ${options.format || 'jpeg'}`);
        log(`📐 最大尺寸: ${options.maxWidth || 200}x${options.maxHeight || 200}`);

        // 转换图片
        const base64Data = await convertImageToBase64(inputPath, options);

        log('✅ 转换成功!', 'green');
        log(`📊 Base64 长度: ${base64Data.length} 字符`);

        // 保存或显示结果
        if (outputPath) {
            fs.writeFileSync(outputPath, base64Data, 'utf8');
            log(`💾 已保存到: ${outputPath}`, 'green');
        } else {
            log('📋 Base64 数据:', 'yellow');
            console.log(base64Data);
        }
    } catch (error) {
        log(`❌ 转换失败: ${error.message}`, 'red');
    }
}

/**
 * 批量转换目录中的图片
 * @param {string} inputDir - 输入目录
 * @param {string} outputDir - 输出目录（可选）
 * @param {Object} options - 转换选项
 */
async function batchConvert(inputDir, outputDir = null, options = {}) {
    try {
        // 检查输入目录
        if (!fs.existsSync(inputDir)) {
            log(`错误: 目录不存在 - ${inputDir}`, 'red');
            return;
        }

        // 创建输出目录
        if (outputDir && !fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }

        log('开始批量转换...', 'blue');
        log(`📁 输入目录: ${inputDir}`);
        log(`📏 输出格式: ${options.format || 'jpeg'}`);
        log(`📐 最大尺寸: ${options.maxWidth || 200}x${options.maxHeight || 200}`);

        // 支持的图片格式
        const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'];
        
        const files = fs.readdirSync(inputDir);
        let count = 0;
        let success = 0;

        for (const file of files) {
            const ext = path.extname(file).toLowerCase();
            if (imageExtensions.includes(ext)) {
                count++;
                const inputPath = path.join(inputDir, file);
                const nameWithoutExt = path.parse(file).name;
                
                process.stdout.write(`处理: ${file} ... `);

                try {
                    if (outputDir) {
                        const outputPath = path.join(outputDir, `${nameWithoutExt}.txt`);
                        await convertFile(inputPath, outputPath, options);
                        log('✅', 'green');
                        success++;
                    } else {
                        await convertFile(inputPath, null, options);
                        log('✅', 'green');
                        success++;
                    }
                } catch (error) {
                    log('❌', 'red');
                }
            }
        }

        log('', 'reset');
        log('批量转换完成!', 'green');
        log(`📊 总计: ${count} 个文件`);
        log(`✅ 成功: ${success} 个文件`);
        log(`❌ 失败: ${count - success} 个文件`);
    } catch (error) {
        log(`批量转换失败: ${error.message}`, 'red');
    }
}

/**
 * 显示帮助信息
 */
function showHelp() {
    log('图片转换为 Base64 工具', 'blue');
    console.log('');
    console.log('使用方法:');
    console.log('  node convert_image.js <输入图片> [输出文件] [格式] [最大尺寸]');
    console.log('');
    console.log('参数:');
    console.log('  输入图片    要转换的图片文件路径');
    console.log('  输出文件    输出的base64文件路径 (可选)');
    console.log('  格式        jpeg, png, gif, webp (默认: jpeg)');
    console.log('  最大尺寸    格式: 宽x高 (默认: 200x200)');
    console.log('');
    console.log('示例:');
    console.log('  node convert_image.js image.jpg');
    console.log('  node convert_image.js image.png output.txt png');
    console.log('  node convert_image.js image.jpg output.txt jpeg 300x300');
    console.log('');
    console.log('批量转换:');
    console.log('  node convert_image.js --batch <输入目录> [输出目录] [格式] [最大尺寸]');
    console.log('');
}

/**
 * 主函数
 */
async function main() {
    const args = process.argv.slice(2);

    // 检查参数
    if (args.length === 0 || args[0] === '-h' || args[0] === '--help') {
        showHelp();
        return;
    }

    // 检查依赖
    try {
        require('sharp');
    } catch (error) {
        log('错误: 未找到 sharp 模块', 'red');
        log('请安装依赖: npm install sharp', 'yellow');
        return;
    }

    // 处理批量转换
    if (args[0] === '--batch') {
        if (args.length < 2) {
            log('错误: 请指定输入目录', 'red');
            return;
        }

        const inputDir = args[1];
        const outputDir = args[2] || null;
        const format = args[3] || 'jpeg';
        const maxSize = args[4] || '200x200';

        const [maxWidth, maxHeight] = maxSize.split('x').map(Number);

        await batchConvert(inputDir, outputDir, {
            format,
            maxWidth,
            maxHeight
        });
    } else {
        // 单个文件转换
        const inputPath = args[0];
        const outputPath = args[1] || null;
        const format = args[2] || 'jpeg';
        const maxSize = args[3] || '200x200';

        const [maxWidth, maxHeight] = maxSize.split('x').map(Number);

        await convertFile(inputPath, outputPath, {
            format,
            maxWidth,
            maxHeight
        });
    }
}

// 运行主函数
if (require.main === module) {
    main().catch(error => {
        log(`程序执行失败: ${error.message}`, 'red');
        process.exit(1);
    });
}

module.exports = {
    convertImageToBase64,
    convertFile,
    batchConvert
}; 