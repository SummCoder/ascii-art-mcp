# ASCII Art MCP Server - Supabase Integration Quick Start

## 🚀 Quick Setup

### 1. Supabase Configuration (2 minutes)

1. Go to https://supabase.com
2. Create a new project (or use existing)
3. Get your credentials from **Project Settings → API**:

   - Copy `Project URL` → `SUPABASE_URL`
   - Copy `Public Anon Key` → `SUPABASE_KEY`

4. Create storage bucket:
   - Go to **Storage** tab
   - Click **New bucket** → name it `ascii-art-images`
   - Enable **Public** access

### 2. Environment Setup

```bash
# Create .env file or set environment variables:
export SUPABASE_URL="https://yourproject.supabase.co"
export SUPABASE_KEY="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### 3. Build & Run

**TypeScript/Node.js:**

```bash
cd ascii-art-nodejs
npm install              # Dependencies already include @supabase/supabase-js
npm run build
```

**Python:**

```bash
cd ascii-art-python
uv pip install -e .      # Installs supabase dependency
python -m ascii_art_server.py
```

## 📝 API Usage

Both versions now have a **single tool**: `generate_ascii_image`

### Parameters

- `image_path` (string, required): Absolute path to image file
  - Example: `D:\images\photo.jpg` or `/home/user/photo.jpg`
- `width` (number, optional): ASCII art width in characters (default: 100)
- `charset` (string, optional): Character set - `simple|detailed|blocks|minimal|matrix` (default: `detailed`)
- `color_mode` (string, optional): `gray|color` (default: `gray`)
- `brightness` (float, optional): Brightness adjustment 0.0-2.0 (default: 1.0)
- `contrast` (float, optional): Contrast adjustment 0.0-2.0 (default: 1.0)
- `invert` (boolean, optional): Reverse character mapping (default: false)
- `font_size` (integer, optional, Python only): Font size in pixels (default: 10)

### Example Call

```json
{
  "image_path": "D:\\Pictures\\portrait.jpg",
  "width": 120,
  "charset": "detailed",
  "color_mode": "color"
}
```

### Response Format

**Success:**

```
✅ ASCII art image generated and uploaded successfully!
🌐 Public URL: https://yourproject.supabase.co/storage/v1/object/public/ascii-art-images/portrait_abc123.png
📐 Dimensions: 720×960 pixels
💾 File size: 125.45 KB
```

**Error (Supabase not configured):**

```
❌ Error: Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY environment variables.
```

## 🔄 Implementation Details

### What Happens When You Call `generate_ascii_image`:

1. **Validate** absolute path to input image
2. **Load** image and apply brightness/contrast adjustments
3. **Generate** ASCII art with selected charset
4. **Render** as PNG with VS Code dark theme colors
5. **Save** to temporary file
6. **Upload** to Supabase Storage `ascii-art-images` bucket
7. **Delete** temporary file
8. **Return** public URL to user

### Removed Features

- ❌ `generate_ascii_art` tool (text file generation)
- ❌ `output_path` parameter (files now auto-uploaded)
- ❌ Local file output (always cloud storage now)

## 💡 Key Differences from Original

| Feature      | Before           | After                  |
| ------------ | ---------------- | ---------------------- |
| Tools        | 2 (text + image) | 1 (image only)         |
| Output       | Local files      | Cloud URLs             |
| Storage      | Local disk       | Supabase Storage       |
| Parameter    | `output_path`    | None (auto-generated)  |
| Return Value | File path        | Public URL             |
| Cleanup      | Manual           | Automatic temp cleanup |

## 🐛 Troubleshooting

### "Cannot find module '@supabase/supabase-js'"

```bash
# TypeScript/Node.js
cd ascii-art-nodejs
npm install
npm run build
```

### "Supabase is not configured"

```bash
# Set environment variables
export SUPABASE_URL="https://..."
export SUPABASE_KEY="..."

# Verify they're set
echo $SUPABASE_URL    # Should show your Supabase URL
```

### "Bucket 'ascii-art-images' not found"

1. Go to Supabase Dashboard → Storage
2. Create new bucket named `ascii-art-images`
3. Enable Public access
4. Click on bucket → Policies
5. Allow public read access

### "Upload failed - Permission denied"

1. Check bucket is set to Public
2. Verify `SUPABASE_KEY` is the public Anon Key (not secret key!)
3. Check Supabase project settings → Auth policies

## 📊 File Locations

```
TypeScript Version:
  Main: ascii-art-nodejs/src/index.ts
  Build: ascii-art-nodejs/dist/
  Config: ascii-art-nodejs/package.json

Python Version:
  Main: ascii-art-python/ascii_art_server.py
  Generator: ascii-art-python/main.py
  Config: ascii-art-python/pyproject.toml
```

## ✅ Verification Checklist

- [ ] Supabase project created
- [ ] `SUPABASE_URL` environment variable set
- [ ] `SUPABASE_KEY` environment variable set
- [ ] `ascii-art-images` bucket created and set to Public
- [ ] TypeScript version builds without errors (`npm run build`)
- [ ] Python version installs successfully (`uv pip install -e .`)
- [ ] Can generate ASCII art and receive public URL

## 🌐 Using the Generated URLs

Generated URLs are publicly accessible:

```
https://yourproject.supabase.co/storage/v1/object/public/ascii-art-images/imagename_uuid.png
```

You can:

- ✅ Share the link with others
- ✅ Embed in websites
- ✅ Download and save
- ✅ View in browser directly
- ✅ Use in documents

## 📚 Additional Resources

- Supabase Docs: https://supabase.com/docs
- Storage Guide: https://supabase.com/docs/guides/storage
- MCP Protocol: https://modelcontextprotocol.io
- Sharp (Node.js image processing): https://sharp.pixelplumbing.com
- Pillow (Python image processing): https://python-pillow.org

---

**Version**: 1.0.0  
**Status**: ✅ Ready for Production  
**Last Updated**: 2025-01-17
