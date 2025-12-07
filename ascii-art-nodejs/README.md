# ASCII Art MCP Server

[![npm version](https://badge.fury.io/js/@your-username%2Fascii-art-mcp-server.svg)](https://www.npmjs.com/package/@your-username/ascii-art-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MCP server for generating ASCII art from images. Convert any image to beautiful ASCII art in text or PNG format with customizable character sets and color modes.

## Features

- 🎨 **Generate ASCII Text**: Convert images to text-based ASCII art
- 🖼️ **Generate ASCII Image**: Create PNG images of ASCII art with VS Code dark theme styling
- 🔤 **5 Character Sets**: simple, detailed, blocks, minimal, matrix
- 🎭 **Color Modes**: Grayscale or full color
- 🔒 **Path Security**: Strict absolute path validation, output in same directory as input
- ⚡ **Fast & Efficient**: Built with TypeScript and Sharp for high performance

## Quick Start

### Using npx (Recommended for 百宝箱)

```bash
npx -y @your-username/ascii-art-mcp-server
```

### Local Installation

```bash
npm install -g @your-username/ascii-art-mcp-server
ascii-art-mcp-server
```

## Installation for Development

```bash
git clone https://github.com/your-username/ascii-art-mcp-server.git
cd ascii-art-mcp-server
npm install
npm run build
```

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

### Windows

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "node",
      "args": ["C:\\ABSOLUTE\\PATH\\TO\\ascii-art-nodejs\\build\\index.js"]
    }
  }
}
```

### macOS/Linux

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/ascii-art-nodejs/build/index.js"]
    }
  }
}
```

## Tools

### generate_ascii_art

Generate ASCII art text from an image and save to file.

**Parameters:**

- `image_path` (string, required): Absolute path to input image
- `output_path` (string, optional): Output filename (not path)
- `width` (number, optional): Width in characters (default: 80)
- `charset` (string, optional): Character set - simple/detailed/blocks/minimal/matrix

### generate_ascii_image

Generate ASCII art as a PNG image.

**Parameters:**

- `image_path` (string, required): Absolute path to input image
- `output_path` (string, optional): Output filename (not path)
- `width` (number, optional): Width in characters (default: 100)
- `charset` (string, optional): Character set - simple/detailed/blocks/minimal/matrix
- `color_mode` (string, optional): gray or color (default: gray)

## Path Restrictions

- ✅ Input must be absolute path
- ✅ Output must be filename only (no directory separators)
- ✅ Output files saved in same directory as input image

## Dependencies

- `@modelcontextprotocol/sdk`: MCP SDK for Node.js
- `sharp`: High-performance image processing
- `zod`: Schema validation
