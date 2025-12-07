# Code Changes Summary - Before & After

## TypeScript/Node.js Changes

### BEFORE: Two Separate Tools

```typescript
// Tool 1: Generate text ASCII art
@mcp.tool()
async function generate_ascii_art(
  image_path: string,
  output_path: string,
  width: number = 100,
  ...
) {
  // Generate ASCII text
  // Write to local file
  return "✅ File saved to: C:\\output\\image_ascii.txt"
}

// Tool 2: Generate PNG image
@mcp.tool()
async function generate_ascii_image(
  image_path: string,
  output_path: string,
  width: number = 100,
  ...
) {
  // Generate ASCII art image
  // Save PNG to local file
  return "✅ File saved to: C:\\output\\image_ascii.png"
}
```

### AFTER: Single Tool with Cloud Upload

```typescript
// Upload helper function
async function uploadToSupabase(
  file_path: string,
  input_basename: string
): Promise<string> {
  if (!supabaseClient) {
    throw new Error("Supabase is not configured...");
  }

  const file_name = `${input_basename}_${randomUUID()}.png`;

  const fileBuffer = await readFile(file_path);
  await supabaseClient
    .storage
    .from("ascii-art-images")
    .upload(file_name, fileBuffer, {
      contentType: "image/png"
    });

  return supabaseClient
    .storage
    .from("ascii-art-images")
    .getPublicUrl(file_name).data.publicUrl;
}

// Single consolidated tool
@mcp.tool()
async function generate_ascii_image(
  image_path: string,
  width: number = 100,
  charset: string = "detailed",
  color_mode: "gray" | "color" = "gray"
) {
  let tempFile = null;

  try {
    // Create temp file
    tempFile = join(tmpdir(), `ascii_${randomUUID()}_${basename(image_path)}.png`);

    // Generate ASCII image
    const result = await createAsciiImage(
      image_path,
      tempFile,
      width,
      charset,
      color_mode
    );

    // Upload to Supabase
    const publicUrl = await uploadToSupabase(tempFile, basename(image_path));

    return `✅ ASCII art image generated and uploaded successfully!
🌐 Public URL: ${publicUrl}
📐 Dimensions: ${result.width}×${result.height} pixels
💾 File size: ${(result.size / 1024).toFixed(2)} KB`;
  } finally {
    // Cleanup
    if (tempFile) await unlink(tempFile);
  }
}
```

### Key Changes:

- ❌ Removed: `generate_ascii_art` tool
- ❌ Removed: `output_path` parameter
- ✅ Added: `uploadToSupabase()` function
- ✅ Added: Supabase client initialization
- ✅ Changed: Return public URL instead of local path
- ✅ Added: Automatic temp file cleanup
- ✅ Import: Added `tmpdir`, `randomUUID`, `unlink`

---

## Python Changes

### BEFORE: Two Separate Tools

```python
@mcp.tool()
async def generate_ascii_art(
    image_path: str,
    output_path: str = None,
    width: int = 100,
    ...
) -> str:
    """Generate ASCII art text file"""
    # Generate ASCII text
    # Write to local file
    return f"✅ File saved to: {output_path}"

@mcp.tool()
async def generate_ascii_image(
    image_path: str,
    output_path: str = None,
    width: int = 100,
    ...
) -> str:
    """Generate PNG image locally"""
    # Generate ASCII image
    # Save to local file
    return f"✅ File saved to: {output_path}"
```

### AFTER: Single Tool with Cloud Upload

```python
def upload_to_supabase(file_path: str, input_basename: str) -> str:
    """Upload file to Supabase Storage and return public URL"""
    if not supabase_client:
        raise Exception(
            "Supabase is not configured. "
            "Set SUPABASE_URL and SUPABASE_KEY environment variables."
        )

    file_name = f"{input_basename}_{uuid4().hex}.png"

    with open(file_path, 'rb') as f:
        supabase_client.storage.from_("ascii-art-images").upload(
            file=f,
            path=file_name,
            file_options={"content-type": "image/png"}
        )

    public_url = supabase_client.storage.from_(
        "ascii-art-images"
    ).get_public_url(file_name)

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
    """Generate ASCII art and upload to cloud storage"""
    temp_file = None

    try:
        # Validate absolute path
        input_file = Path(image_path)
        if not input_file.is_absolute():
            return f"❌ Error: Only absolute paths allowed"

        # Create temp file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            temp_file = tmp.name

        # Generate ASCII image
        generator = ASCIIArtGenerator(char_set=charset, invert=invert)

        # ... (image generation code remains same)

        # Save to temporary file
        canvas.save(temp_file, format="PNG")

        # Upload to Supabase
        public_url = upload_to_supabase(temp_file, input_file.stem)

        file_size_kb = Path(temp_file).stat().st_size / 1024

        return f"""✅ ASCII art image generated and uploaded successfully!
🌐 Public URL: {public_url}
📐 Dimensions: {canvas_width}×{canvas_height} pixels
💾 File size: {file_size_kb:.2f} KB"""

    except Exception as e:
        return f"❌ Error: {str(e)}"

    finally:
        # Cleanup temp file
        if temp_file and Path(temp_file).exists():
            try:
                Path(temp_file).unlink()
            except:
                pass
```

### Key Changes:

- ❌ Removed: `generate_ascii_art` tool
- ❌ Removed: `output_path` parameter
- ✅ Added: `upload_to_supabase()` function
- ✅ Added: Supabase client initialization
- ✅ Changed: Return public URL instead of local path
- ✅ Added: Automatic temp file cleanup using finally block
- ✅ Import: Added `tempfile`, `uuid4`, `supabase`
- ✅ Dependency: Added `supabase>=2.4.0` to `pyproject.toml`

---

## Configuration Changes

### Dependencies Added

**TypeScript/Node.js (package.json):**

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0",
    "sharp": "^0.33.0",
    "@supabase/supabase-js": "^2.45.0" // ← NEW
  }
}
```

**Python (pyproject.toml):**

```toml
dependencies = [
    "pillow>=10.0.0",
    "mcp[cli]>=1.2.0",
    "supabase>=2.4.0",  # ← NEW
]
```

### Environment Variables Required

```bash
# Supabase Configuration (NEW)
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your-public-anon-key"
```

---

## API Endpoint Changes

### Tool Parameter Changes

**Removed Parameters:**

- `output_path` (string) - No longer needed, files auto-uploaded

**New Expected Output:**

```
Before:
  "✅ File saved to: C:\Users\...\image_ascii.png"

After:
  "✅ ASCII art image generated and uploaded successfully!
   🌐 Public URL: https://yourproject.supabase.co/storage/v1/object/public/ascii-art-images/image_abc123.png
   📐 Dimensions: 600×800 pixels
   💾 File size: 45.32 KB"
```

---

## File System Impact

### Before (Local Storage)

```
User's Disk:
  D:\Pictures\
    ├── photo.jpg
    ├── photo_ascii.txt       ← Generated text file
    └── photo_ascii.png       ← Generated PNG file
```

### After (Cloud Storage + Temp Cleanup)

```
User's Disk:
  D:\Pictures\
    └── photo.jpg            ← Only original file remains

Supabase Storage (Public Bucket):
  ascii-art-images/
    ├── photo_a1b2c3d4.png
    ├── photo_e5f6g7h8.png
    └── ...                  ← All generated images (public URLs)
```

---

## Summary of Changes

| Aspect               | Before                  | After               |
| -------------------- | ----------------------- | ------------------- |
| **Number of Tools**  | 2                       | 1                   |
| **Output Format**    | Local files             | Cloud URLs          |
| **Storage Backend**  | Local disk              | Supabase Storage    |
| **Temp Files**       | None                    | Auto-cleaned        |
| **Parameters**       | `output_path`           | None                |
| **Return Values**    | File paths              | Public URLs         |
| **Disk Usage**       | Accumulates over time   | Minimal (temp only) |
| **File Sharing**     | Manual copy/paste paths | Share public URL    |
| **Scalability**      | Limited by disk         | Unlimited cloud     |
| **Data Persistence** | User manages            | Supabase manages    |

---

## Migration Checklist for 百宝箱 Deployment

- [ ] Update MCP configuration to include new tool
- [ ] Remove references to `generate_ascii_art` tool
- [ ] Remove references to `output_path` parameter
- [ ] Add Supabase environment variables to deployment
- [ ] Test cloud upload functionality
- [ ] Update user documentation
- [ ] Update API documentation
- [ ] Test error handling (Supabase not configured)
- [ ] Verify URL sharing works
- [ ] Set up monitoring for Supabase uploads

---

**Version**: 1.0.0 → 2.0.0 (with cloud storage)  
**Status**: ✅ Migration Complete
