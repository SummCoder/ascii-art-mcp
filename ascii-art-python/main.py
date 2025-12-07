#!/usr/bin/env python3
"""
ASCII Art Generator
将图片转换为ASCII艺术的生成器
"""

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import argparse
import sys
import platform
from pathlib import Path


class ASCIIArtGenerator:
    """ASCII艺术生成器类"""
    
    # 不同的ASCII字符集
    CHAR_SETS = {
        'simple': ' .:-=+*#%@',
        'detailed': ' .\'"`,^:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$',
        'blocks': ' ░▒▓█',
        'minimal': ' .-+*@',
        'numbers': ' 123456789',
    }
    
    def __init__(self, char_set='simple', invert=False):
        """
        初始化生成器
        
        Args:
            char_set: 字符集名称或自定义字符集字符串
            invert: 是否反转字符顺序（亮度映射）
        """
        if char_set in self.CHAR_SETS:
            self.chars = self.CHAR_SETS[char_set]
        else:
            self.chars = char_set
        
        if invert:
            self.chars = self.chars[::-1]
            
    def _get_font(self, size=12):
        """
        获取等宽字体
        尝试加载系统常见的等宽字体
        """
        system = platform.system()
        fonts = []
        
        if system == 'Windows':
            fonts = ['consola.ttf', 'lucon.ttf', 'arial.ttf']
        elif system == 'Darwin':  # macOS
            fonts = ['Menlo.ttc', 'Monaco.ttf', 'Courier New.ttf']
        else:  # Linux
            fonts = ['DejaVuSansMono.ttf', 'LiberationMono-Regular.ttf', 'FreeMono.ttf']
            
        # 尝试加载字体
        for font_name in fonts:
            try:
                return ImageFont.truetype(font_name, size)
            except IOError:
                continue
                
        # 如果都失败了，尝试加载默认字体（可能不是等宽的，效果会差）
        print("警告: 未找到系统等宽字体，使用默认字体，效果可能不佳。", file=sys.stderr)
        return ImageFont.load_default()
    
    def image_to_ascii(self, image_path, width=100, height=None, color_mode='gray', brightness=1.0, contrast=1.0):
        """
        将图片转换为ASCII艺术
        
        Args:
            image_path: 图片文件路径
            width: 输出宽度（字符数）
            height: 输出高度（字符数），如果为None则自动计算保持比例
            color_mode: 颜色模式 ('gray', 'color')
            brightness: 亮度调整系数 (1.0为原图)
            contrast: 对比度调整系数 (1.0为原图)
        
        Returns:
            ASCII艺术字符串
        """
        try:
            img = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"无法打开图片文件 {image_path}: {e}")
        
        # 调整亮度和对比度
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
        
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
        
        # 计算新的尺寸，保持纵横比
        aspect_ratio = img.height / img.width
        if height is None:
            # 0.55 调整字符高宽比（因为字符通常比宽度高）
            new_height = int(aspect_ratio * width * 0.55)
        else:
            new_height = height
        
        # 调整图片大小
        img = img.resize((width, new_height))
        
        if color_mode == 'color':
            return self._create_colored_ascii(img, width)
        else:
            return self._create_grayscale_ascii(img, width)
    
    def _create_grayscale_ascii(self, img, width):
        """创建灰度ASCII艺术"""
        # 转换为灰度图
        img = img.convert('L')
        pixels = img.getdata()
        
        # 将像素值映射到字符
        char_count = len(self.chars)
        ascii_str = ''.join(
            self.chars[min(pixel * char_count // 256, char_count - 1)]
            for pixel in pixels
        )
        
        # 格式化为多行
        ascii_img = '\n'.join(
            ascii_str[i:i+width] for i in range(0, len(ascii_str), width)
        )
        return ascii_img
    
    def _create_colored_ascii(self, img, width):
        """创建彩色ASCII艺术（使用ANSI颜色代码）"""
        # 转换为RGB模式
        img = img.convert('RGB')
        pixels = img.getdata()
        
        # 创建灰度版本用于字符选择
        gray_img = img.convert('L')
        gray_pixels = gray_img.getdata()
        
        ascii_lines = []
        char_count = len(self.chars)
        
        for i in range(0, len(pixels), width):
            line = ''
            for j in range(width):
                if i + j < len(pixels):
                    # 获取RGB值
                    r, g, b = pixels[i + j]
                    # 获取对应的ASCII字符
                    gray_val = gray_pixels[i + j]
                    char = self.chars[min(gray_val * char_count // 256, char_count - 1)]
                    # 添加ANSI颜色代码
                    line += f'\033[38;2;{r};{g};{b}m{char}\033[0m'
            ascii_lines.append(line)
        
        return '\n'.join(ascii_lines)
    
    def save_to_file(self, ascii_art, output_path):
        """
        将ASCII艺术保存到文件
        
        Args:
            ascii_art: ASCII艺术字符串
            output_path: 输出文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(ascii_art)
            print(f"ASCII艺术已保存到: {output_path}")
        except Exception as e:
            raise ValueError(f"无法保存文件 {output_path}: {e}")

    def save_as_image(self, image_path, output_path, width=100, color_mode='gray', brightness=1.0, contrast=1.0, font_size=10, bg_color=None, text_color=None):
        """
        将ASCII艺术保存为图片（模拟文本编辑器显示效果）
        
        Args:
            image_path: 输入图片路径
            output_path: 输出图片路径
            width: 字符宽度
            color_mode: 'gray' 或 'color'
            brightness: 亮度调整
            contrast: 对比度调整
            font_size: 字体大小
            bg_color: 背景色，默认深色主题 (40, 44, 52)
            text_color: 文字颜色，默认浅色 (171, 178, 191)
        """
        try:
            img = Image.open(image_path)
        except Exception as e:
            raise ValueError(f"无法打开图片文件 {image_path}: {e}")

        # 保存原始长宽比
        original_aspect_ratio = img.height / img.width

        # 调整亮度和对比度
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
        
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)

        # 加载字体
        font = self._get_font(font_size)
        
        # 获取字符尺寸
        bbox = font.getbbox('M')
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        
        # 计算字符行数，保持原图长宽比
        # 我们希望：(height * char_height) / (width * char_width) = original_aspect_ratio
        # 所以：height = original_aspect_ratio * width * (char_width / char_height)
        new_height = int(original_aspect_ratio * width * (char_width / char_height))
        
        # 调整图片大小到字符网格
        img_small = img.resize((width, new_height))
        
        # 转换为灰度图用于字符选择
        gray_img = img_small.convert('L')
        gray_pixels = gray_img.getdata()
        
        # 准备绘制
        canvas_width = width * char_width
        canvas_height = new_height * char_height
        
        # 设置默认颜色（模拟 VS Code 深色主题）
        if bg_color is None:
            bg_color = (40, 44, 52)  # VS Code 深色背景
        if text_color is None:
            text_color = (171, 178, 191)  # VS Code 浅色文字
        
        # 创建画布
        if color_mode == 'color':
            canvas = Image.new('RGB', (canvas_width, canvas_height), bg_color)
            img_rgb = img_small.convert('RGB')
            rgb_pixels = img_rgb.getdata()
        else:
            # 灰度模式也使用彩色画布，以便设置背景色
            canvas = Image.new('RGB', (canvas_width, canvas_height), bg_color)

        draw = ImageDraw.Draw(canvas)
        char_count = len(self.chars)
        
        # 绘制字符
        for i in range(new_height):
            for j in range(width):
                idx = i * width + j
                if idx >= len(gray_pixels):
                    break
                
                # 获取字符
                gray_val = gray_pixels[idx]
                char_idx = min(gray_val * char_count // 256, char_count - 1)
                char = self.chars[char_idx]
                
                # 跳过空格（不绘制，保持背景色）
                if char == ' ':
                    continue
                
                # 计算位置
                x = j * char_width
                y = i * char_height
                
                # 绘制字符
                if color_mode == 'color':
                    # 彩色模式：使用原图颜色，但调整亮度使其更明显
                    r, g, b = rgb_pixels[idx]
                    # 确保颜色足够亮，能在深色背景上显示
                    min_brightness = 80
                    if r + g + b < min_brightness * 3:
                        factor = (min_brightness * 3) / max(r + g + b, 1)
                        r, g, b = min(255, int(r * factor)), min(255, int(g * factor)), min(255, int(b * factor))
                    color = (r, g, b)
                else:
                    # 灰度模式：根据灰度值调整文字颜色
                    # 灰度值越高（越亮），字符颜色越亮
                    brightness_factor = gray_val / 255.0
                    r = int(text_color[0] * (0.3 + 0.7 * brightness_factor))
                    g = int(text_color[1] * (0.3 + 0.7 * brightness_factor))
                    b = int(text_color[2] * (0.3 + 0.7 * brightness_factor))
                    color = (r, g, b)
                
                draw.text((x, y), char, font=font, fill=color)
        
        # 保存
        canvas.save(output_path)
        print(f"ASCII图片已保存到: {output_path}")


def main():
    """主函数 - 命令行界面"""
    parser = argparse.ArgumentParser(
        description='ASCII艺术生成器 - 将图片转换为ASCII艺术',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  python main.py image.jpg                          # 基础转换
  python main.py image.jpg -w 150                   # 指定宽度
  python main.py image.jpg -c detailed              # 使用详细字符集
  python main.py image.jpg --color                  # 彩色输出
  python main.py image.jpg -o output.txt            # 保存到文件
  python main.py image.jpg -c blocks --invert       # 使用块字符并反转
  
可用字符集: simple, detailed, blocks, minimal, numbers
        '''
    )
    
    parser.add_argument('image', help='输入图片文件路径')
    parser.add_argument('-w', '--width', type=int, default=100,
                        help='输出宽度（字符数，默认100）')
    parser.add_argument('--height', type=int, default=None,
                        help='输出高度（字符数，默认自动计算）')
    parser.add_argument('-c', '--charset', default='simple',
                        help='字符集（simple/detailed/blocks/minimal/numbers或自定义字符串）')
    parser.add_argument('--invert', action='store_true',
                        help='反转字符顺序（明暗反转）')
    parser.add_argument('--color', action='store_true',
                        help='启用彩色输出（使用ANSI颜色代码）')
    parser.add_argument('-b', '--brightness', type=float, default=1.0,
                        help='亮度调整系数 (默认1.0, <1变暗, >1变亮)')
    parser.add_argument('--contrast', type=float, default=1.0,
                        help='对比度调整系数 (默认1.0, <1降低对比度, >1增加对比度)')
    parser.add_argument('-o', '--output', help='输出文件路径（不指定则打印到控制台）')
    parser.add_argument('--save-img', help='保存为图片文件的路径 (例如 output.png)')
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not Path(args.image).exists():
        print(f"错误: 找不到图片文件 '{args.image}'", file=sys.stderr)
        sys.exit(1)
    
    # 创建生成器
    generator = ASCIIArtGenerator(char_set=args.charset, invert=args.invert)
    
    try:
        # 转换图片
        color_mode = 'color' if args.color else 'gray'
        
        # 如果指定了保存图片
        if args.save_img:
            generator.save_as_image(
                args.image,
                args.save_img,
                width=args.width,
                color_mode=color_mode,
                brightness=args.brightness,
                contrast=args.contrast
            )
        
        # 正常的文本输出逻辑
        ascii_art = generator.image_to_ascii(
            args.image,
            width=args.width,
            height=args.height,
            color_mode=color_mode,
            brightness=args.brightness,
            contrast=args.contrast
        )
        
        # 输出结果
        if args.output:
            generator.save_to_file(ascii_art, args.output)
        elif not args.save_img: # 如果只保存图片，就不打印到控制台了，除非没指定输出文件
            print(ascii_art)
        elif args.save_img and not args.output:
             # 如果保存了图片但没指定文本输出，还是打印一下文本预览
             print(ascii_art)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()