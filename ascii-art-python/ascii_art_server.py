#!/usr/bin/env python3
"""
ASCII Art Generator MCP Server
提供ASCII艺术生成功能的MCP服务器
"""

import os
import tempfile
from pathlib import Path
from uuid import uuid4
from mcp.server.fastmcp import FastMCP
from PIL import Image as PILImage
from PIL import ImageEnhance, ImageDraw
from supabase import create_client, Client

# 导入主程序的ASCIIArtGenerator类
from main import ASCIIArtGenerator

# 初始化FastMCP服务器
mcp = FastMCP("ascii-art-generator")

# 初始化Supabase客户端
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_key = os.getenv("SUPABASE_KEY", "")
supabase_bucket = os.getenv("SUPABASE_BUCKET", "ascii-art-images")
supabase_client: Client | None = None
if supabase_url and supabase_key:
    supabase_client = create_client(supabase_url, supabase_key)


def upload_to_supabase(file_path: str, input_basename: str) -> str:
    """Upload file to Supabase Storage and return public URL.
    
    Args:
        file_path: Path to the file to upload
        input_basename: Base name of the original input file
        
    Returns:
        Public URL of the uploaded file
        
    Raises:
        Exception: If Supabase is not configured or upload fails
    """
    if not supabase_client:
        raise Exception("Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY environment variables.")
    
    file_name = f"{input_basename}_{uuid4().hex}.png"
    
    with open(file_path, 'rb') as f:
        supabase_client.storage.from_(supabase_bucket).upload(
            file=f,
            path=file_name,
            file_options={"content-type": "image/png"}
        )
    
    # Return public URL
    public_url = supabase_client.storage.from_(supabase_bucket).get_public_url(file_name)
    return public_url


@mcp.tool()
async def generate_ascii_image(
    image_path: str,
    width: int = 100,
    charset: str = "simple",
    color_mode: str = "gray",
    brightness: float = 1.0,
    contrast: float = 1.0,
    invert: bool = False,
    font_size: int = 10
) -> str:
    """Generate ASCII art and upload to cloud storage.

    This tool converts an image to ASCII art, renders it as a PNG image with
    VS Code dark theme styling, uploads to Supabase, and returns the public URL.

    Args:
        image_path: ABSOLUTE path to the input image file (relative paths are not allowed)
        width: Width of ASCII art in characters (default: 100, recommended: 80-120 for images)
        charset: Character set to use. Options:
            - 'simple': Basic set ' .:-=+*#%@' (default, best for clarity)
            - 'detailed': Extended set with 70+ characters (best for detail)
            - 'blocks': Unicode blocks ' ░▒▓█' (modern look)
            - 'minimal': Minimal set ' .-+*@' (clean and simple)
            - 'numbers': Digits ' 123456789' (unique style)
            - Or provide custom character string (from dark to bright)
        color_mode: 'gray' for grayscale or 'color' for colored ASCII
        brightness: Brightness adjustment (1.0 = original)
        contrast: Contrast adjustment (1.0 = original)
        invert: Reverse character brightness mapping
        font_size: Font size in pixels (default: 10, affects output image size)

    Returns:
        Success message with public URL and image dimensions, or error message if failed
    """
    temp_file = None
    try:
        # 验证输入路径必须是绝对路径
        input_file = Path(image_path)
        if not input_file.is_absolute():
            return f"❌ Error: Only absolute paths are allowed. Got relative path: {image_path}\n💡 Hint: Use full path like 'D:\\folder\\image.jpg'"
        
        # 验证文件是否存在
        if not input_file.exists():
            return f"❌ Error: Image file not found: {image_path}"
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            temp_file = tmp.name
        
        # 创建生成器
        generator = ASCIIArtGenerator(char_set=charset, invert=invert)
        
        # 生成ASCII艺术图片到内存
        img_original = PILImage.open(str(input_file))
        
        # 应用亮度和对比度调整
        if brightness != 1.0:
            enhancer = ImageEnhance.Brightness(img_original)
            img_original = enhancer.enhance(brightness)
        
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img_original)
            img_original = enhancer.enhance(contrast)
        
        # 保存原始长宽比
        original_aspect_ratio = img_original.height / img_original.width
        
        # 获取字体
        font = generator._get_font(font_size)
        
        # 计算字符尺寸
        bbox = font.getbbox('M')
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        
        # 计算高度以保持纵横比
        new_height = int(original_aspect_ratio * width * (char_width / char_height))
        
        # 调整图片大小
        img_small = img_original.resize((width, new_height))
        gray_img = img_small.convert('L')
        gray_pixels = gray_img.getdata()
        
        # 创建画布
        canvas_width = width * char_width
        canvas_height = new_height * char_height
        bg_color = (40, 44, 52)  # VS Code 深色背景
        text_color = (171, 178, 191)  # VS Code 浅色文字
        
        canvas = PILImage.new('RGB', (canvas_width, canvas_height), bg_color)
        
        draw = ImageDraw.Draw(canvas)
        char_count = len(generator.chars)
        
        # 获取RGB像素（如果需要）
        if color_mode == 'color':
            img_rgb = img_small.convert('RGB')
            rgb_pixels = img_rgb.getdata()
        
        # 绘制字符
        for i in range(new_height):
            for j in range(width):
                idx = i * width + j
                if idx >= len(gray_pixels):
                    break
                
                # 获取字符
                gray_val = gray_pixels[idx]
                char_idx = min(gray_val * char_count // 256, char_count - 1)
                char = generator.chars[char_idx]
                
                # 跳过空格
                if char == ' ':
                    continue
                
                # 计算位置
                x = j * char_width
                y = i * char_height
                
                # 确定颜色
                if color_mode == 'color':
                    r, g, b = rgb_pixels[idx]
                    min_brightness = 80
                    if r + g + b < min_brightness * 3:
                        factor = (min_brightness * 3) / max(r + g + b, 1)
                        r, g, b = min(255, int(r * factor)), min(255, int(g * factor)), min(255, int(b * factor))
                    color = (r, g, b)
                else:
                    brightness_factor = gray_val / 255.0
                    r = int(text_color[0] * (0.3 + 0.7 * brightness_factor))
                    g = int(text_color[1] * (0.3 + 0.7 * brightness_factor))
                    b = int(text_color[2] * (0.3 + 0.7 * brightness_factor))
                    color = (r, g, b)
                
                draw.text((x, y), char, font=font, fill=color)
        
        # 保存图片到临时文件
        canvas.save(temp_file, format="PNG")
        
        # Upload to Supabase
        public_url = upload_to_supabase(temp_file, input_file.stem)
        
        # 获取文件大小
        file_size_kb = Path(temp_file).stat().st_size / 1024
        
        return f"✅ ASCII art image generated and uploaded successfully!\n🌐 Public URL: {public_url}\n📐 Dimensions: {canvas_width}×{canvas_height} pixels\n💾 File size: {file_size_kb:.2f} KB"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"
    
    finally:
        # Clean up temporary file
        if temp_file and Path(temp_file).exists():
            try:
                Path(temp_file).unlink()
            except:
                pass


def main():
    """启动MCP服务器"""
    # 使用stdio传输协议运行服务器
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
