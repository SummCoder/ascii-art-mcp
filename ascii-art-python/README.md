# ASCII Art MCP Server (Python)

MCP server for generating ASCII art from images using Python and FastMCP.

## Features

- **Generate ASCII Text**: Convert images to text-based ASCII art
- **Generate ASCII Image**: Create PNG images of ASCII art
- **5 Character Sets**: simple, detailed, blocks, minimal, matrix
- **Path Security**: Strict absolute path validation, output in same directory as input

## Installation

```bash
cd ascii-art-python
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv add "mcp[cli]" Pillow
```

## Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

### Windows

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\ABSOLUTE\\PATH\\TO\\ascii-art-python",
        "run",
        "ascii_art_server.py"
      ]
    }
  }
}
```

### macOS/Linux

```json
{
  "mcpServers": {
    "ascii-art": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/ascii-art-python",
        "run",
        "ascii_art_server.py"
      ]
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
- `width` (int, optional): Width in characters (default: 80)
- `charset` (string, optional): Character set - simple/detailed/blocks/minimal/matrix

### generate_ascii_image

Generate ASCII art as a PNG image.

**Parameters:**

- `image_path` (string, required): Absolute path to input image
- `output_path` (string, optional): Output filename (not path)
- `width` (int, optional): Width in characters (default: 100)
- `charset` (string, optional): Character set - simple/detailed/blocks/minimal/matrix
- `color_mode` (string, optional): gray or color (default: gray)

## Path Restrictions

- ✅ Input must be absolute path
- ✅ Output must be filename only (no directory separators)
- ✅ Output files saved in same directory as input image

## Testing

```bash
uv run python test_mcp_server.py
```

## Dependencies

- `mcp[cli]`: FastMCP framework
- `Pillow`: Image processing library
