# Deployment Guide - ASCII Art MCP Server with Supabase

## Overview

This guide covers deploying the updated ASCII Art MCP server to the 百宝箱 platform with Supabase cloud storage integration.

## Prerequisites

- Node.js 18+ (for TypeScript version) OR Python 3.10+ (for Python version)
- Supabase account and project
- npm or uv package manager
- Git (optional, for version control)

## Step-by-Step Deployment

### Phase 1: Supabase Setup (5 minutes)

#### 1.1 Create Supabase Project

1. Visit https://supabase.com
2. Sign in or create account
3. Click "New Project"
4. Fill in:
   - Project name: `ascii-art`
   - Database password: (save securely)
   - Region: Choose closest to your users
5. Wait for project to be ready (~2 minutes)

#### 1.2 Get API Credentials

1. Go to **Settings → API**
2. Copy and save:
   ```
   Project URL:    https://xxxxxx.supabase.co
   Anon Public Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

#### 1.3 Create Storage Bucket

1. Go to **Storage** (left sidebar)
2. Click **New bucket**
3. Name: `ascii-art-images`
4. **CHECK** "Make it public"
5. Click **Create bucket**

#### 1.4 Set CORS Policy (if needed)

1. Go to **Storage → Settings**
2. If buckets show CORS issues, set:
   - Allowed Origins: `*` or your domain
   - Allowed Methods: `GET, POST, PUT, DELETE`

### Phase 2: Application Deployment

Choose ONE of the following (TypeScript OR Python):

---

## Option A: Deploy TypeScript/Node.js Version

### A.1 Build Application

```bash
# Navigate to project
cd ascii-art-nodejs

# Install dependencies
npm install

# Build
npm run build

# Verify build succeeded
ls -la dist/
# Should show: dist/index.js (the compiled MCP server)
```

### A.2 Prepare for 百宝箱

```bash
# Create deployment package
npm pack

# This creates: ascii-art-mcp-server-1.0.0.tgz
```

### A.3 Deploy to 百宝箱

1. Go to 百宝箱 platform
2. Navigate to "Upload Tool" or "New Tool"
3. Select "Node.js" environment
4. Upload `ascii-art-mcp-server-1.0.0.tgz`
5. Or use command:
   ```bash
   npm publish --registry https://registry.baobaoboxes.com
   ```

### A.4 Configure Environment Variables

In 百宝箱 deployment settings, add:

```
SUPABASE_URL=https://xxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Option B: Deploy Python Version

### B.1 Build Application

```bash
# Navigate to project
cd ascii-art-python

# Install in editable mode
uv pip install -e .

# Verify installation
uv pip list | grep supabase
# Should show: supabase 2.25.0
```

### B.2 Create Distribution Package

```bash
# Build source distribution
python -m build

# Or with setuptools
python setup.py sdist

# Creates: dist/ascii-art-generator-1.0.0.tar.gz
```

### B.3 Deploy to 百宝箱

1. Go to 百宝箱 platform
2. Navigate to "Upload Tool" or "New Tool"
3. Select "Python 3.10+" environment
4. Upload distribution package
5. Or via command:
   ```bash
   # If 百宝箱 supports PyPI publishing
   twine upload dist/ascii-art-generator-1.0.0.tar.gz
   ```

### B.4 Configure Environment Variables

In 百宝箱 deployment settings, add:

```
SUPABASE_URL=https://xxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Phase 3: Testing

### Manual Testing (Before Deployment)

#### Test 1: Check Tool Registration

**Node.js:**

```bash
cd ascii-art-nodejs
npm run build
node dist/index.js
# Should start MCP server and show "Server running..."
```

**Python:**

```bash
cd ascii-art-python
export SUPABASE_URL="https://..."
export SUPABASE_KEY="..."
python -c "import ascii_art_server; print('Module loads successfully')"
```

#### Test 2: Environment Variables

```bash
# Verify variables are accessible
echo $SUPABASE_URL
echo $SUPABASE_KEY

# Should output your Supabase credentials
```

#### Test 3: Supabase Connectivity

**Node.js Test Script:**

```javascript
// test-supabase.js
const { createClient } = require("@supabase/supabase-js");

const client = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

client.storage
  .from("ascii-art-images")
  .list()
  .then(() => console.log("✅ Supabase connection OK"))
  .catch((err) => console.log("❌ Error:", err.message));
```

**Python Test Script:**

```python
# test-supabase.py
from supabase import create_client
import os

client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

try:
    client.storage.from_("ascii-art-images").list()
    print("✅ Supabase connection OK")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Deployment Testing

After deploying to 百宝箱:

1. **Check Tool Registration**

   - Verify tool `generate_ascii_image` appears in tool list
   - Check parameter documentation loads correctly

2. **Test Tool Call**

   ```json
   {
     "tool": "generate_ascii_image",
     "params": {
       "image_path": "C:\\path\\to\\test.jpg",
       "width": 80,
       "charset": "detailed",
       "color_mode": "gray"
     }
   }
   ```

3. **Verify Response**

   - Should return public URL from Supabase
   - URL format: `https://xxxxxx.supabase.co/storage/v1/object/public/ascii-art-images/...`
   - Should start with "✅ ASCII art image..."

4. **Test URL Accessibility**
   ```bash
   curl "https://xxxxxx.supabase.co/storage/v1/object/public/ascii-art-images/..."
   # Should download PNG image
   ```

---

## Troubleshooting Deployment

### Issue: "Cannot find module '@supabase/supabase-js'"

**Solution:**

```bash
cd ascii-art-nodejs
npm install --save @supabase/supabase-js
npm run build
```

### Issue: "supabase module not found (Python)"

**Solution:**

```bash
cd ascii-art-python
uv pip install supabase>=2.4.0
uv pip install -e .
```

### Issue: "Supabase is not configured" error

**Solution:**

- Verify environment variables are set in 百宝箱
- Check variable names: `SUPABASE_URL` and `SUPABASE_KEY` (exact case)
- Confirm values don't have quotes: `https://...` not `"https://..."`

### Issue: "Bucket 'ascii-art-images' not found"

**Solution:**

1. Log into Supabase dashboard
2. Go to **Storage**
3. Create bucket: `ascii-art-images`
4. Enable **Public** access
5. Verify in code bucket name matches exactly

### Issue: "Permission denied" uploading to Supabase

**Solution:**

- Check `SUPABASE_KEY` is the **Public Anon Key**, not Secret Key
- Verify bucket is set to **Public** (not private)
- Check Supabase RLS policies allow uploads

### Issue: "401 Unauthorized" error

**Solution:**

- Regenerate API keys:
  1. Go to **Settings → API**
  2. Click "Regenerate" under Anon Key
  3. Update `SUPABASE_KEY` in 百宝箱
  4. Redeploy application

---

## Monitoring & Maintenance

### Log Monitoring

**百宝箱 Logs:**

- Check application logs for errors
- Look for "Supabase is not configured" messages
- Monitor upload success rates

**Supabase Usage:**

1. Go to **Settings → Usage**
2. Monitor storage usage
3. Check API request rates

### Cleanup Old Files

**Manual cleanup (if needed):**

```javascript
// Node.js cleanup script
const { createClient } = require("@supabase/supabase-js");
const client = createClient(SUPABASE_URL, SUPABASE_KEY);

const { data, error } = await client.storage.from("ascii-art-images").list();

// Delete files older than 30 days (optional)
data?.forEach((file) => {
  const fileDate = new Date(file.created_at);
  const ageMs = Date.now() - fileDate.getTime();
  const ageDays = ageMs / (1000 * 60 * 60 * 24);

  if (ageDays > 30) {
    client.storage.from("ascii-art-images").remove([file.name]);
  }
});
```

---

## Performance Optimization

### For High Volume

1. **Enable Caching**

   - Configure CDN in Supabase Storage settings
   - Cache generated URLs on client side

2. **Optimize Images**

   - Reduce default width (100 → 80-120 range)
   - Use grayscale mode by default
   - Consider compression settings

3. **Monitor Performance**
   - Track average generation time
   - Monitor Supabase latency
   - Set up alerts for errors

### Scalability Considerations

- Supabase handles unlimited storage
- Each upload creates new file (no overwrites)
- Files are immutable once uploaded
- Consider implementing cleanup policy for old files

---

## Security Checklist

- [ ] Supabase credentials only in environment variables
- [ ] Never commit `SUPABASE_KEY` to version control
- [ ] Use `.gitignore` for `.env` files
- [ ] Bucket set to Public (for URL sharing)
- [ ] Review Supabase RLS policies
- [ ] Monitor for unusual upload patterns
- [ ] Keep dependencies updated

---

## Post-Deployment Verification

After deployment, run this checklist:

- [ ] Tool appears in 百宝箱 tool list
- [ ] Tool description shows correctly
- [ ] Parameters display with descriptions
- [ ] Test generate_ascii_image with sample image
- [ ] Verify returned URL is valid
- [ ] Test URL in browser - should show ASCII art PNG
- [ ] Check Supabase usage stats increased
- [ ] Verify no errors in application logs
- [ ] Test with different parameters (charsets, colors)
- [ ] Confirm temporary files are cleaned up

---

## Rollback Instructions

If deployment has issues:

### Option 1: Revert to Previous Version

```bash
# If using git
git revert <commit-hash>
npm run build
# Redeploy

# Or reinstall from backup
npm install --no-save ascii-art-mcp-server@0.9.0
```

### Option 2: Disable Supabase Integration

Comment out in code:

```typescript
// const supabaseClient = createClient(supabaseUrl, supabaseKey);
// Keep only local file generation
```

### Option 3: Contact Supabase Support

If Supabase is misconfigured, reach out to their support team with:

- Project URL
- Error messages
- Steps to reproduce

---

## Version Information

- **Application Version**: 2.0.0 (with cloud storage)
- **Node.js Minimum**: 18.0.0
- **Python Minimum**: 3.10.0
- **Supabase SDK Version**: 2.25.0+ (Node.js), 2.4.0+ (Python)
- **MCP Protocol**: 1.0.0

## Support & Documentation

- **MCP Protocol**: https://modelcontextprotocol.io
- **Supabase Docs**: https://supabase.com/docs
- **Storage Guide**: https://supabase.com/docs/guides/storage
- **API Reference**: https://supabase.com/docs/reference

---

**Deployment Status**: ✅ Ready for 百宝箱
**Last Updated**: 2025-01-17
**Maintainer**: Your Team
