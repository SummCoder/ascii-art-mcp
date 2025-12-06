# ASCII Art Generator

一个功能强大的 ASCII 艺术生成器，可以将图片转换为由字符组成的艺术作品。

## 功能特点

- 🎨 **多种字符集**：simple、detailed、blocks、minimal、numbers
- 🖼️ **图片导出**：保存为 PNG 图片，完美还原编辑器显示效果，保持原图长宽比
- 🔆 **图像增强**：支持调整亮度和对比度
- 🌈 **彩色支持**：支持彩色 ASCII 艺术
- 💾 **文本输出**：可输出到文本文件或控制台

## 安装

```bash
# 安装 uv
pip install uv

# 同步依赖
uv sync
```

## 快速开始

```bash
# 基础转换
uv run main.py scan.jpg

# 保存为图片（推荐）
uv run main.py scan.jpg --save-img output.png

# 使用详细字符集
uv run main.py scan.jpg -c detailed -w 120 --save-img output.png

# 调整亮度和对比度
uv run main.py scan.jpg -b 1.2 --contrast 1.5 --save-img output.png
```

## 命令行参数

| 参数               | 说明                                             | 默认值   |
| ------------------ | ------------------------------------------------ | -------- |
| `image`            | 输入图片路径（必需）                             | -        |
| `-w, --width`      | 输出宽度（字符数）                               | 100      |
| `--height`         | 输出高度（字符数）                               | 自动计算 |
| `-c, --charset`    | 字符集（simple/detailed/blocks/minimal/numbers） | simple   |
| `-b, --brightness` | 亮度调整（>1 变亮，<1 变暗）                     | 1.0      |
| `--contrast`       | 对比度调整（>1 增强，<1 降低）                   | 1.0      |
| `--invert`         | 反转明暗                                         | False    |
| `--color`          | 启用彩色输出                                     | False    |
| `-o, --output`     | 保存为文本文件                                   | -        |
| `--save-img`       | 保存为图片文件（PNG/JPG）                        | -        |

## 字符集说明

- **simple**: ` .:-=+*#%@` - 10 个字符，适合快速预览
- **detailed**: 70+个字符，提供最详细的层次
- **blocks**: ` ░▒▓█` - Unicode 块字符
- **minimal**: ` .-+*@` - 5 个字符
- **numbers**: ` 123456789` - 数字风格

## 为什么推荐保存为图片？

### 文本文件的问题

- ❌ 字符间距可能失真（取决于字体和编辑器）
- ❌ 不同设备显示效果不一致
- ❌ 长宽比可能变形

### 图片文件的优势

- ✅ **完美还原**：使用等宽字体精确渲染
- ✅ **长宽比准确**：自动计算字符尺寸，保持原图比例
- ✅ **统一显示**：任何设备查看效果一致
- ✅ **美观主题**：VS Code 深色主题配色
- ✅ **易于分享**：直接发送图片，无需解释如何设置字体

## Python 代码使用

```python
from main import ASCIIArtGenerator

# 创建生成器
generator = ASCIIArtGenerator(char_set='detailed')

# 转换为文本
ascii_art = generator.image_to_ascii('scan.jpg', width=100)
print(ascii_art)

# 保存为图片（推荐）
generator.save_as_image('scan.jpg', 'output.png', width=120)

# 调整参数
generator.save_as_image(
    'scan.jpg',
    'output.png',
    width=150,
    brightness=1.2,
    contrast=1.3
)
```

## 技术说明

### 图片生成原理

1. **字体选择**：自动检测系统等宽字体（Windows: Consolas, macOS: Menlo, Linux: DejaVu Sans Mono）
2. **尺寸计算**：精确测量字符像素尺寸，计算正确的行数
3. **长宽比保持**：`高度 = 原图长宽比 × 宽度 × (字符宽度 / 字符高度)`
4. **主题配色**：深色背景 `(40, 44, 52)` + 渐变文字颜色
5. **智能渲染**：根据像素亮度调整字符颜色

### 文本 vs 图片对比

| 特性       | 文本文件   | 图片文件    |
| ---------- | ---------- | ----------- |
| 文件大小   | 几 KB      | 几百 KB     |
| 长宽比     | 可能失真   | ✅ 完全准确 |
| 显示一致性 | 依赖字体   | ✅ 完全一致 |
| 编辑性     | 可编辑     | 不可编辑    |
| 分享便利性 | 需说明字体 | ✅ 直接分享 |

**建议**：快速测试用文本，最终输出用图片。

## 示例

```bash
# 示例 1: 基础转换
uv run main.py scan.jpg
# 输出到控制台

# 示例 2: 保存为高质量图片
uv run main.py scan.jpg -c detailed -w 150 --save-img hd_output.png

# 示例 3: 调整效果
uv run main.py scan.jpg -b 1.3 --contrast 1.5 -w 120 --save-img enhanced.png

# 示例 4: 同时保存文本和图片
uv run main.py scan.jpg -o ascii.txt --save-img ascii.png

# 示例 5: 彩色版本
uv run main.py scan.jpg --color --save-img color.png
```

## 依赖项

- Python >= 3.8
- Pillow >= 10.0.0

## 许可证

MIT License
