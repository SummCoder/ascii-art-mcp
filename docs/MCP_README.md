# ASCII Art Generator - MCP Server

将图片转换为 ASCII 艺术的 Model Context Protocol (MCP) 服务器。

## 功能特点

这个 MCP 服务器提供两个工具：

1. **generate_ascii_art** - 生成纯文本 ASCII 艺术
2. **generate_ascii_image** - 生成 ASCII 艺术并返回为 PNG 图片（base64 编码）

## 快速开始

### 1. 安装依赖

```powershell
# 确保已经安装了 uv
uv sync
```

### 2. 配置 Claude for Desktop

编辑配置文件 `%AppData%\Claude\claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\2025_12\\tongyi",
        "run",
        "ascii_art_server.py"
      ]
    }
  }
}
```

**注意：**

- 将路径 `D:\\2025_12\\tongyi` 替换为你的实际项目路径
- Windows 路径使用双反斜杠 `\\` 或正斜杠 `/`
- 使用绝对路径

### 3. 重启 Claude for Desktop

完全退出 Claude（在系统托盘中右键点击图标 → 退出），然后重新启动。

### 4. 验证安装

在 Claude 中，点击"Search and tools"图标（🔌），你应该能看到两个工具：

- `generate_ascii_art`
- `generate_ascii_image`

## 工具说明

### generate_ascii_art

生成纯文本格式的 ASCII 艺术。

**参数：**

| 参数         | 类型   | 默认值   | 说明                                  |
| ------------ | ------ | -------- | ------------------------------------- |
| `image_path` | string | **必需** | 输入图片路径（支持 JPG、PNG、BMP 等） |
| `width`      | int    | 100      | ASCII 艺术的字符宽度（推荐 50-200）   |
| `charset`    | string | "simple" | 字符集选项，见下表                    |
| `color_mode` | string | "gray"   | 'gray'（灰度）或 'color'（彩色 ANSI） |
| `brightness` | float  | 1.0      | 亮度调整（<1 变暗，>1 变亮）          |
| `contrast`   | float  | 1.0      | 对比度调整（<1 降低，>1 增加）        |
| `invert`     | bool   | false    | 反转字符亮度映射                      |

**字符集选项：**

| 字符集   | 字符         | 适用场景                  |
| -------- | ------------ | ------------------------- |
| simple   | ` .:-=+*#%@` | 默认，清晰简洁            |
| detailed | 70+字符      | 最佳细节表现              |
| blocks   | ` ░▒▓█`      | 现代风格，使用 Unicode 块 |
| minimal  | ` .-+*@`     | 极简风格                  |
| numbers  | ` 123456789` | 独特数字风格              |

**返回：** 纯文本 ASCII 艺术字符串

### generate_ascii_image

生成 ASCII 艺术并渲染为 PNG 图片（使用 VS Code 深色主题样式）。

**参数：**

除了 `generate_ascii_art` 的所有参数外，还包括：

| 参数        | 类型 | 默认值 | 说明                               |
| ----------- | ---- | ------ | ---------------------------------- |
| `font_size` | int  | 10     | 字体大小（像素），影响输出图片尺寸 |

**返回：** `ImageContent` 对象（MCP 标准图片类型）

- Claude 会自动识别并渲染这个图片对象
- 图片使用 base64 编码的 PNG 格式
- 采用 VS Code 深色主题配色（背景深色，文字浅色渐变）

**关于图片反馈机制：**

本工具使用 MCP 协议的 `ImageContent` 类型来返回图片：

```python
from mcp.types import ImageContent

return ImageContent(
    type="image",
    data=base64_encoded_png,  # base64编码的PNG数据
    mimeType="image/png"
)
```

这是 MCP 的标准图片返回方式：

- ✅ Claude 会自动识别 `ImageContent` 类型并渲染图片
- ✅ 用户在对话中直接看到可视化的 ASCII 艺术图片
- ✅ 无需保存临时文件，数据在内存中处理
- ✅ 适合中小型图片（ASCII 艺术图片通常 < 1MB）
- 图片使用 VS Code 深色主题配色，视觉效果更好

## 使用示例

在 Claude 中，你可以这样提问：

### 示例 1：生成基础 ASCII 艺术

```
请用scan.jpg生成ASCII艺术，宽度120字符
```

Claude 会调用：

```python
generate_ascii_art(
    image_path="d:\\2025_12\\tongyi\\scan.jpg",
    width=120
)
```

### 示例 2：生成详细的彩色 ASCII 图片

```
请用scan.jpg生成彩色ASCII艺术图片，使用detailed字符集，宽度100
```

Claude 会调用：

```python
generate_ascii_image(
    image_path="d:\\2025_12\\tongyi\\scan.jpg",
    width=100,
    charset="detailed",
    color_mode="color"
)
```

### 示例 3：调整亮度和对比度

```
请把scan.jpg转成ASCII图片，提高亮度1.2倍，增强对比度1.3倍
```

Claude 会调用：

```python
generate_ascii_image(
    image_path="d:\\2025_12\\tongyi\\scan.jpg",
    brightness=1.2,
    contrast=1.3
)
```

## 图片如何反馈给用户？

### MCP ImageContent - 标准图片返回方式

本项目使用 **MCP 协议的 `ImageContent` 类型**来返回图片，这是官方推荐的标准方式。

**实现代码：**

```python
from mcp.types import ImageContent
import base64

# 生成PNG图片到内存
buffered = io.BytesIO()
canvas.save(buffered, format="PNG")

# 转换为base64编码
image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

# 返回MCP ImageContent对象
return ImageContent(
    type="image",           # 固定值
    data=image_base64,      # base64编码的图片数据
    mimeType="image/png"    # MIME类型
)
```

**为什么这样做有效？**

1. **MCP 协议标准** - `ImageContent` 是 MCP 规范定义的标准内容类型
2. **Claude 原生支持** - Claude for Desktop 会自动识别并渲染 `ImageContent`
3. **无需文件系统** - 所有数据在内存中处理，不产生临时文件
4. **即时显示** - 用户立即在对话中看到图片，无需额外操作

**MCP 支持的其他图片返回方式（供参考）：**

| 方式                      | 适用场景        | 优缺点                                                                  |
| ------------------------- | --------------- | ----------------------------------------------------------------------- |
| `ImageContent` (当前使用) | 中小型图片      | ✅ 标准方式，即时显示 <br> ✅ 无需文件系统 <br> ⚠️ 大图片会增加传输负担 |
| Resource URI              | 大文件/缓存场景 | ✅ 适合大文件 <br> ✅ 支持缓存 <br> ⚠️ 需要实现资源管理                 |
| 文件路径                  | 本地工具        | ✅ 简单直接 <br> ⚠️ 用户需手动打开 <br> ⚠️ 产生临时文件                 |

**本项目选择 `ImageContent` 的原因：**

- ASCII 艺术图片通常不大（几百 KB）
- Base64 直接嵌入响应，用户体验最佳
- Claude 能立即显示图片，无需额外步骤

## 技术细节

### 图片生成流程

1. 读取输入图片
2. 应用亮度/对比度调整
3. 调整图片尺寸到字符网格（保持原始纵横比）
4. 转换为灰度图选择字符
5. 在画布上绘制字符（使用等宽字体）
6. 应用 VS Code 深色主题配色
7. 转换为 PNG 并 base64 编码

### 纵横比保持

计算公式：

```python
original_aspect_ratio = img.height / img.width
new_height = int(original_aspect_ratio * width * (char_width / char_height))
```

确保生成的 ASCII 艺术图片与原图比例一致（误差<0.1%）。

### 字体选择

自动检测系统等宽字体：

- **Windows**: Consolas, Lucida Console
- **macOS**: Menlo, Monaco
- **Linux**: DejaVu Sans Mono, Liberation Mono

## 故障排查

### Claude 中看不到工具

1. 检查 `claude_desktop_config.json` 语法是否正确
2. 确认路径是否为绝对路径
3. 完全退出并重启 Claude（系统托盘 → 右键 → 退出）

### 工具调用失败

查看日志：

```powershell
# Windows
Get-Content "$env:AppData\Claude\logs\mcp-server-ascii-art.log" -Tail 20 -Wait
```

常见问题：

- 图片路径不存在 → 确认文件路径正确
- 导入错误 → 运行 `uv sync` 重新安装依赖
- 字体加载失败 → 会自动降级到默认字体

### 图片不显示

- 确认 `generate_ascii_image` 返回了 `image_base64` 字段
- 检查 base64 数据是否完整
- 尝试减小图片尺寸（降低 `width` 或 `font_size` 参数）

## 开发测试

### 直接运行服务器（调试）

```powershell
# 安装依赖
uv sync

# 运行服务器（stdio模式）
uv run ascii_art_server.py
```

### 使用 MCP Inspector 测试

```powershell
# 安装MCP Inspector
npm install -g @modelcontextprotocol/inspector

# 启动测试
mcp dev ascii_art_server.py
```

## 许可证

本项目使用 MIT 许可证。

## 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Python SDK 文档](https://github.com/modelcontextprotocol/python-sdk)
- [Claude for Desktop](https://claude.ai/download)
