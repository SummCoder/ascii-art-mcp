# Claude Desktop MCP 配置示例

本文档展示如何在 Claude Desktop 中配置 ASCII Art MCP Server。

## 配置文件位置

**Windows:**

```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**

```
~/.config/Claude/claude_desktop_config.json
```

---

## 配置方法

### 方法 1: 使用 npx（推荐 - TypeScript 版本）

打开 `claude_desktop_config.json` 文件，添加以下配置：

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "npx",
      "args": ["-y", "@your-username/ascii-art-mcp-server"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_KEY": "your-public-anon-key-here",
        "SUPABASE_BUCKET": "ascii-art-images"
      }
    }
  }
}
```

### 方法 2: 使用本地 Node.js 路径（TypeScript 版本）

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "node",
      "args": ["d:\\2025_12\\tongyi\\ascii-art-nodejs\\dist\\index.js"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_KEY": "your-public-anon-key-here",
        "SUPABASE_BUCKET": "ascii-art-images"
      }
    }
  }
}
```

### 方法 3: 使用 Python uv（Python 版本）

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "uv",
      "args": [
        "--directory",
        "d:\\2025_12\\tongyi\\ascii-art-python",
        "run",
        "ascii_art_server.py"
      ],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_KEY": "your-public-anon-key-here",
        "SUPABASE_BUCKET": "ascii-art-images"
      }
    }
  }
}
```

### 方法 4: 使用 Python 直接运行（Python 版本）

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "python",
      "args": ["-m", "ascii_art_server"],
      "cwd": "d:\\2025_12\\tongyi\\ascii-art-python",
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_KEY": "your-public-anon-key-here",
        "SUPABASE_BUCKET": "ascii-art-images"
      }
    }
  }
}
```

---

## 如何获取 Supabase 密钥

### 步骤 1: 创建 Supabase 项目

1. 访问 https://supabase.com
2. 使用 GitHub/Google 账户登录
3. 点击 "New Project"
4. 填写项目信息并等待创建完成

### 步骤 2: 获取 API 密钥

1. 进入你的项目
2. 左侧菜单 → **Settings** (⚙️) → **API**
3. 复制以下信息：
   - **Project URL** → 替换配置中的 `SUPABASE_URL`
   - **anon public** → 替换配置中的 `SUPABASE_KEY`

### 步骤 3: 创建存储桶

1. 左侧菜单 → **Storage**
2. 点击 **New bucket**
3. Bucket name: `ascii-art-images` (或者使用你自定义的名字，需与配置中的 `SUPABASE_BUCKET` 保持一致)
4. ✅ 勾选 **Public bucket**
5. 点击 **Create bucket**

---

## 完整配置示例

如果你有多个 MCP Server，配置文件应该像这样：

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "npx",
      "args": ["-y", "@your-username/ascii-art-mcp-server"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "SUPABASE_BUCKET": "ascii-art-images"
      }
    },
    "amap-maps": {
      "command": "npx",
      "args": ["-y", "@amap/amap-maps-mcp-server"],
      "env": {
        "AMAP_MAPS_API_KEY": "your-amap-key"
      }
    },
    "other-server": {
      "command": "node",
      "args": ["/path/to/server.js"]
    }
  }
}
```

---

## 配置说明

### 环境变量说明

| 变量名            | 说明                  | 示例                                      | 必需                                |
| ----------------- | --------------------- | ----------------------------------------- | ----------------------------------- |
| `SUPABASE_URL`    | Supabase 项目 URL     | `https://xxxxx.supabase.co`               | ✅ 是                               |
| `SUPABASE_KEY`    | Supabase 公开匿名密钥 | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | ✅ 是                               |
| `SUPABASE_BUCKET` | Supabase 存储桶名称   | `ascii-art-images`                        | ⭕ 可选（默认: `ascii-art-images`） |

### 配置字段说明

- **`command`**: 执行命令（`npx`, `node`, `python`, `uv` 等）
- **`args`**: 命令参数数组
- **`env`**: 环境变量对象（所有配置都在这里）
- **`cwd`**: 工作目录（可选）

---

## 验证配置

配置完成后：

1. **重启 Claude Desktop**
2. 在对话中输入：`列出可用的工具`
3. 应该能看到 `generate_ascii_image` 工具
4. 测试生成：`用这张图片生成 ASCII 艺术：D:\Pictures\photo.jpg`

---

## 常见问题

### Q: 配置后 Claude 没有识别到工具？

**A:** 检查以下几点：

- ✅ JSON 格式是否正确（没有多余的逗号）
- ✅ 路径是否使用双反斜杠 `\\`（Windows）
- ✅ 重启了 Claude Desktop
- ✅ 环境变量值没有引号嵌套

### Q: 报错 "Supabase is not configured"？

**A:** 检查：

- ✅ `SUPABASE_URL` 和 `SUPABASE_KEY` 都已设置
- ✅ 密钥值正确（从 Supabase 复制的完整字符串）
- ✅ 没有多余的空格或换行

### Q: 报错 "Bucket not found"？

**A:** 确保：

- ✅ 在 Supabase 中创建了 `ascii-art-images` 桶
- ✅ 桶设置为 **Public**
- ✅ 桶名字完全匹配（区分大小写）

### Q: Windows 路径怎么写？

**A:** 使用双反斜杠：

```json
"args": ["d:\\2025_12\\tongyi\\ascii-art-nodejs\\dist\\index.js"]
```

或使用正斜杠：

```json
"args": ["d:/2025_12/tongyi/ascii-art-nodejs/dist/index.js"]
```

---

## 安全建议

⚠️ **重要提示：**

1. **不要将配置文件提交到 Git** - 包含敏感密钥
2. **使用 Public Anon Key** - 不要使用 Service Role Key
3. **定期更换密钥** - 如果怀疑泄露
4. **配置文件权限** - 确保只有你能读取

---

## 高级配置

### 使用环境变量文件

如果不想在配置文件中硬编码密钥，可以使用系统环境变量：

**Windows PowerShell:**

```powershell
$env:SUPABASE_URL = "https://your-project.supabase.co"
$env:SUPABASE_KEY = "your-key"
```

**macOS/Linux:**

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_KEY="your-key"
```

然后在配置中引用：

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "npx",
      "args": ["-y", "@your-username/ascii-art-mcp-server"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_KEY": "${SUPABASE_KEY}"
      }
    }
  }
}
```

**注意：** 这种方式取决于 Claude Desktop 是否支持环境变量展开。

---

## 完整示例（推荐）

### TypeScript 版本（使用 npx）

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "npx",
      "args": ["-y", "@your-username/ascii-art-mcp-server"],
      "env": {
        "SUPABASE_URL": "https://abcdefgh.supabase.co",
        "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk5OTk5OTksImV4cCI6MjAxNTU3NTk5OX0.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

### Python 版本（使用 uv）

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "uv",
      "args": [
        "--directory",
        "d:\\2025_12\\tongyi\\ascii-art-python",
        "run",
        "ascii_art_server.py"
      ],
      "env": {
        "SUPABASE_URL": "https://abcdefgh.supabase.co",
        "SUPABASE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTk5OTk5OTksImV4cCI6MjAxNTU3NTk5OX0.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

---

## 下一步

配置完成后：

1. 重启 Claude Desktop
2. 测试工具是否可用
3. 开始生成 ASCII 艺术！

更多信息请参考：

- [QUICK_START.md](../QUICK_START.md) - 快速上手指南
- [DEPLOYMENT_GUIDE.md](../DEPLOYMENT_GUIDE.md) - 部署指南
- [SUPABASE_INTEGRATION_SUMMARY.md](../SUPABASE_INTEGRATION_SUMMARY.md) - 技术细节

---

**祝你使用愉快！** 🎨
