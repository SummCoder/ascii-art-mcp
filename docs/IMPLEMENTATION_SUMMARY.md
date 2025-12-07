# ASCII Art MCP Server - 实现总结

## ✅ 已完成的工作

### 1. 核心 MCP 服务器实现 (`ascii_art_server.py`)

#### 关键修正：使用标准 MCP 图片类型

**之前的错误实现：**

```python
# ❌ 返回普通字典 - Claude无法识别为图片
return {
    "image_base64": img_base64,
    "mime_type": "image/png",
    "width": canvas_width,
    "height": canvas_height
}
```

**正确的实现：**

```python
# ✅ 使用MCP标准的ImageContent类型
from mcp.types import ImageContent

return ImageContent(
    type="image",
    data=image_base64,        # base64编码的PNG数据
    mimeType="image/png"      # MIME类型
)
```

### 2. 两个 MCP 工具

#### Tool 1: `generate_ascii_art`

- **功能**: 生成纯文本 ASCII 艺术
- **返回类型**: `str`
- **参数**: image_path, width, charset, color_mode, brightness, contrast, invert
- **用途**: 适合在终端显示或保存为文本文件

#### Tool 2: `generate_ascii_image`

- **功能**: 生成 ASCII 艺术 PNG 图片
- **返回类型**: `ImageContent` (MCP 标准类型)
- **参数**: 同上 + font_size
- **特色**:
  - VS Code 深色主题配色
  - 保持原图纵横比
  - 灰度渐变文字颜色
  - Claude 中直接显示

### 3. 图片反馈机制

#### MCP ImageContent 工作流程

```
1. 生成PIL图片 → 2. 保存到BytesIO → 3. Base64编码 → 4. 创建ImageContent → 5. Claude渲染
   (内存)          (PNG格式)           (字符串)        (MCP对象)         (可视化)
```

**代码实现：**

```python
# Step 1-2: 在内存中生成PNG
buffered = io.BytesIO()
canvas.save(buffered, format="PNG")

# Step 3: Base64编码
image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

# Step 4: 创建MCP ImageContent对象
return ImageContent(
    type="image",
    data=image_base64,
    mimeType="image/png"
)

# Step 5: Claude自动识别并显示
```

### 4. 依赖配置

**`pyproject.toml` 更新：**

```toml
requires-python = ">=3.10"  # MCP SDK要求
dependencies = [
    "pillow>=10.0.0",       # 图片处理
    "mcp[cli]>=1.2.0",      # MCP SDK with CLI
]
```

### 5. 测试验证

**`test_mcp_server.py` 测试结果：**

```
✓ 文本ASCII艺术生成成功 (4697字符)
✓ ImageContent对象创建成功
✓ Base64数据长度: 278308字符
✓ PNG解码成功: 208730字节
✓ PNG文件签名验证通过
```

## 📋 配置步骤

### 1. 安装依赖

```powershell
uv sync
```

### 2. 配置 Claude Desktop

编辑 `%AppData%\Claude\claude_desktop_config.json`:

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

### 3. 重启 Claude Desktop

完全退出（系统托盘 → 右键 → 退出），然后重启。

### 4. 验证工具可用

在 Claude 中点击工具图标 🔌，应该看到：

- `generate_ascii_art`
- `generate_ascii_image`

## 💡 关键知识点

### Q1: 为什么之前返回字典不行？

**A:** Claude 只能识别 MCP 协议定义的标准类型。普通字典会被当作文本内容显示，而不会渲染为图片。

### Q2: ImageContent vs 其他方式的区别？

| 方式            | Claude 显示效果   | 实现复杂度       |
| --------------- | ----------------- | ---------------- |
| `ImageContent`  | ✅ 自动渲染图片   | 简单             |
| 字典(含 base64) | ❌ 显示 JSON 文本 | 简单             |
| Resource URI    | ✅ 可以显示       | 复杂(需资源管理) |
| 文件路径        | ❌ 只显示路径     | 简单             |

### Q3: ImageContent 的 data 字段是什么格式？

**A:** Base64 编码的字符串，不是原始字节数据：

```python
# ❌ 错误
return ImageContent(data=buffered.getvalue())  # bytes

# ✅ 正确
return ImageContent(data=base64.b64encode(buffered.getvalue()).decode('utf-8'))  # str
```

### Q4: 支持哪些图片格式？

**A:** `mimeType` 参数支持：

- `image/png` (推荐)
- `image/jpeg`
- `image/gif`
- `image/webp`

本项目使用 PNG 因为支持透明度且质量好。

### Q5: 图片大小限制？

**A:**

- **技术限制**: MCP 协议通过 JSON-RPC 传输，建议 < 10MB
- **实际情况**: ASCII 艺术图片通常 < 1MB
- **本项目**: 100 字符宽度 × 字体 10px ≈ 200KB

## 🎯 使用示例

### 示例 1: 生成文本 ASCII

```
在Claude中提问：
"请用scan.jpg生成ASCII艺术，宽度120字符，使用detailed字符集"

Claude会调用：
generate_ascii_art(
    image_path="d:\\2025_12\\tongyi\\scan.jpg",
    width=120,
    charset="detailed"
)
```

### 示例 2: 生成 ASCII 图片

```
在Claude中提问：
"请把scan.jpg转成彩色ASCII图片，宽度100，提高亮度1.2倍"

Claude会调用：
generate_ascii_image(
    image_path="d:\\2025_12\\tongyi\\scan.jpg",
    width=100,
    color_mode="color",
    brightness=1.2
)

→ Claude会直接显示生成的PNG图片
```

## 📚 参考资料

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Types 规范](https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/types.py)
- [ImageContent 定义](https://github.com/modelcontextprotocol/python-sdk/blob/main/src/mcp/types.py#L140)

## 🔍 调试技巧

### 查看 Claude 日志

```powershell
Get-Content "$env:AppData\Claude\logs\mcp-server-ascii-art.log" -Tail 20 -Wait
```

### 测试服务器

```powershell
# 运行测试脚本
uv run python test_mcp_server.py

# 直接测试导入
uv run python -c "from ascii_art_server import mcp; print(mcp._tool_manager.list_tools())"
```

### 验证 ImageContent

```python
from mcp.types import ImageContent
import base64

# 创建测试对象
img_content = ImageContent(
    type="image",
    data=base64.b64encode(b"fake_png_data").decode('utf-8'),
    mimeType="image/png"
)

print(f"Type: {img_content.type}")
print(f"MIME: {img_content.mimeType}")
print(f"Data length: {len(img_content.data)}")
```

## ✨ 总结

这个 MCP server 成功实现了：

1. ✅ 使用标准 MCP `ImageContent`类型返回图片
2. ✅ Claude 能够自动识别并渲染生成的 ASCII 艺术图片
3. ✅ 无需临时文件，所有操作在内存中完成
4. ✅ 支持丰富的参数调整（字符集、颜色、亮度、对比度等）
5. ✅ 保持原图纵横比，视觉效果优秀
6. ✅ 完整的测试验证和文档说明

**关键改进点：**

- 从返回普通字典 → 改为返回 `ImageContent` 对象
- 这是唯一能让 Claude 正确渲染图片的方式！
