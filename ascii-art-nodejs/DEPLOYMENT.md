# 部署到百宝箱平台指南

## 方式一：发布到 npm 后使用 npx 部署（推荐）

### 1. 准备发布到 npm

**修改 package.json**：

- 将 `@your-username/ascii-art-mcp-server` 改为你的 npm 用户名
- 修改 `author` 为你的名字
- 修改 `repository` URL 为你的 GitHub 仓库

**发布到 npm**：

```bash
# 登录npm（如果还没登录）
npm login

# 发布包
npm publish --access public
```

### 2. 在百宝箱部署

发布成功后，在百宝箱使用以下命令部署：

```
npx -y @your-username/ascii-art-mcp-server
```

**注意事项**：

- ✅ 百宝箱 Node.js 版本：22.21.0
- ✅ npm 源：https://npmmirror.com/（发布后等待同步）
- ✅ 确保 package.json 中的 bin 字段正确配置

## 方式二：自部署后使用 SSE 连接

如果你想自己部署 MCP 服务，需要添加 SSE 传输支持。

### 1. 安装依赖

```bash
npm install express cors
npm install --save-dev @types/express @types/cors
```

### 2. 创建 SSE 服务器

创建 `src/sse-server.ts`：

```typescript
import express from "express";
import cors from "cors";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

const app = express();
app.use(cors());
app.use(express.json());

// 从你的主文件导入server配置
import { createServer } from "./index.js";

app.post("/sse", async (req, res) => {
  const server = createServer();
  const transport = new SSEServerTransport("/message", res);
  await server.connect(transport);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`MCP SSE Server running on http://localhost:${PORT}`);
});
```

### 3. 修改 index.ts

将服务器创建逻辑提取为函数，以便 SSE 服务器使用。

### 4. 部署

部署到任何支持 Node.js 的云服务（Vercel、Railway、Render 等），然后在百宝箱填入：

- 协议类型：SSE
- URL：`https://your-domain.com/sse`

## 推荐方案

对于百宝箱平台，**推荐使用方式一（npm + npx）**：

1. ✅ 简单：用户无需关心部署细节
2. ✅ 免费：百宝箱提供免费托管
3. ✅ 快速：2 分钟完成部署

## 当前状态

你的 MCP Server 已经准备好发布到 npm：

- ✅ package.json 已配置 bin 字段
- ✅ 构建脚本已配置
- ✅ 依赖已明确定义
- ✅ TypeScript 已编译到 build/

下一步：

1. 注册 npm 账号（如果还没有）：https://www.npmjs.com/signup
2. 修改 package.json 中的用户名和仓库信息
3. 运行 `npm publish --access public`
4. 等待 npmmirror.com 同步（通常几分钟）
5. 在百宝箱使用 `npx -y @your-username/ascii-art-mcp-server` 部署
