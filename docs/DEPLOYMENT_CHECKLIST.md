# ✅ Deployment Checklist - ASCII Art MCP Server v2.0

Print this out and use it during deployment!

---

## Phase 1: Supabase Setup (15 minutes)

### Supabase Account

- [ ] Create Supabase account at https://supabase.com
- [ ] Create new project
- [ ] Wait for project to be ready (~2 minutes)

### Get Credentials

- [ ] Go to Settings → API
- [ ] Copy **Project URL** → `SUPABASE_URL`
- [ ] Copy **Public Anon Key** → `SUPABASE_KEY`
- [ ] Save credentials securely (will use later)

### Create Storage Bucket

- [ ] Go to **Storage** in left sidebar
- [ ] Click **New bucket**
- [ ] Name: `ascii-art-images` (exactly!)
- [ ] **CHECK "Make it public"** (important!)
- [ ] Click **Create bucket**

### Verify Setup

- [ ] Credentials saved
- [ ] Bucket created and public
- [ ] Ready for next phase ✓

---

## Phase 2: Choose Your Deployment Method

### Option A: TypeScript/Node.js (Check if using)

#### Build

- [ ] Navigate: `cd ascii-art-nodejs`
- [ ] Install: `npm install`
- [ ] Build: `npm run build`
- [ ] Verify: Check `dist/` directory exists

#### Prepare Package

- [ ] Create package: `npm pack`
- [ ] File created: `ascii-art-mcp-server-1.0.0.tgz`
- [ ] Ready for upload ✓

#### Deploy to 百宝箱

- [ ] Log into 百宝箱 platform
- [ ] Navigate to Upload/New Tool section
- [ ] Select **Node.js** environment
- [ ] Upload `ascii-art-mcp-server-1.0.0.tgz`
- [ ] Set environment variables (see below)
- [ ] Deploy ✓

### Option B: Python (Check if using)

#### Build

- [ ] Navigate: `cd ascii-art-python`
- [ ] Install: `uv pip install -e .`
- [ ] Verify: Installation successful

#### Prepare Package

- [ ] Build distribution: `python -m build`
- [ ] File created: `dist/ascii-art-generator-1.0.0.tar.gz`
- [ ] Ready for upload ✓

#### Deploy to 百宝箱

- [ ] Log into 百宝箱 platform
- [ ] Navigate to Upload/New Tool section
- [ ] Select **Python 3.10+** environment
- [ ] Upload distribution package
- [ ] Set environment variables (see below)
- [ ] Deploy ✓

---

## Phase 3: Configure Environment Variables

### In 百宝箱 Deployment Settings

Add these environment variables:

```
Variable Name:  SUPABASE_URL
Value:          https://xxxxxx.supabase.co
                (from credentials saved earlier)

Variable Name:  SUPABASE_KEY
Value:          eyJhbGciOiJIUzI1NiIsInR5c...
                (from credentials saved earlier)
```

- [ ] SUPABASE_URL set correctly
- [ ] SUPABASE_KEY set correctly
- [ ] Values don't have quotes
- [ ] No extra spaces
- [ ] Ready to deploy ✓

---

## Phase 4: Testing

### Verify Tool Registration

- [ ] Log into 百宝箱
- [ ] Check tool `generate_ascii_image` appears
- [ ] Check parameters display correctly
- [ ] Tool description shows

### Test Tool Call

- [ ] Call tool with test image
- [ ] Expected: Public URL returned
- [ ] Verify URL format: `https://...supabase.co/storage/...`
- [ ] URL starts with "✅ ASCII art image..."

### Test URL Access

- [ ] Copy returned URL
- [ ] Open in browser
- [ ] Should download PNG image
- [ ] Image shows ASCII art

### Verify Supabase Storage

- [ ] Go to Supabase dashboard
- [ ] Check Storage → ascii-art-images bucket
- [ ] Should contain uploaded PNG files
- [ ] Files public and accessible

### Success Indicators ✓

- [ ] Tool visible in 百宝箱
- [ ] Public URLs returned
- [ ] URLs are valid and accessible
- [ ] Files appear in Supabase
- [ ] Images display correctly

---

## Phase 5: Final Verification

### Code Quality

- [ ] TypeScript builds with 0 errors (if using)
- [ ] Python installs without errors (if using)
- [ ] No runtime errors in logs
- [ ] No security warnings

### Functionality

- [ ] `generate_ascii_image` tool works
- [ ] Accepts absolute image paths
- [ ] Returns public URLs
- [ ] Supports all character sets
- [ ] Supports color modes

### Performance

- [ ] Generation completes in reasonable time
- [ ] Files upload successfully
- [ ] URLs are permanent
- [ ] No file size limits hit

### Documentation

- [ ] Users can follow QUICK_START.md
- [ ] Error messages are clear
- [ ] Troubleshooting guides work
- [ ] Configuration is documented

---

## Phase 6: Production Sign-Off

### Before Going Live

- [ ] All tests pass
- [ ] Documentation reviewed
- [ ] Team trained
- [ ] Backup plan ready
- [ ] Monitoring set up

### Monitoring Setup

- [ ] Check 百宝箱 error logs
- [ ] Monitor Supabase usage
- [ ] Track upload success rate
- [ ] Alert on failures

### Post-Deployment

- [ ] Monitor for 24 hours
- [ ] Check user feedback
- [ ] Verify no errors
- [ ] Update status page

---

## Troubleshooting

### If Tool Doesn't Appear

- [ ] Check environment variables set
- [ ] Verify deployment completed
- [ ] Check error logs in 百宝箱
- [ ] Redeploy if needed

### If Upload Fails

- [ ] Verify bucket exists: `ascii-art-images`
- [ ] Check bucket is Public
- [ ] Verify SUPABASE_KEY is correct
- [ ] Check Supabase API key permissions

### If URLs Don't Work

- [ ] Verify bucket is Public
- [ ] Check CORS settings in Supabase
- [ ] Verify files actually uploaded
- [ ] Check URL format from response

### If Generation Fails

- [ ] Verify image path is absolute
- [ ] Check image file exists
- [ ] Check file format supported
- [ ] Review error message

---

## Quick Reference

### Important Credentials

```
SUPABASE_URL = ___________________________
SUPABASE_KEY = ___________________________
Bucket Name  = ascii-art-images
```

### Critical Files

```
TypeScript:  ascii-art-nodejs/dist/index.js
Python:      ascii-art-python/ascii_art_server.py
```

### Key URLs

```
Supabase:     https://app.supabase.com
百宝箱:        [Your platform URL]
Documentation: QUICK_START.md
Deployment:   DEPLOYMENT_GUIDE.md
```

---

## Estimated Timeline

| Phase          | Estimated Time |
| -------------- | -------------- |
| Supabase Setup | 15 min         |
| Build/Prepare  | 10 min         |
| Deploy         | 10-20 min      |
| Test           | 10 min         |
| Verify         | 10 min         |
| **Total**      | **~1 hour**    |

---

## Success Criteria

✓ All checks passed when you can answer YES to:

1. Supabase account created and bucket set up?
2. Environment variables configured in 百宝箱?
3. Tool deployment completed successfully?
4. Tool appears in 百宝箱 tool list?
5. Sample image generates successfully?
6. Returned URL is valid and accessible?
7. Image downloads and displays correctly?
8. Team trained on usage?

---

## Post-Deployment Tasks

After successful deployment:

- [ ] Notify team of availability
- [ ] Update documentation with live URL
- [ ] Train users on 5-minute setup
- [ ] Set up monitoring
- [ ] Schedule review in 1 week
- [ ] Collect initial feedback
- [ ] Plan optimization phase 2

---

## Contact & Support

**Deployment Issues?**
→ Check DEPLOYMENT_GUIDE.md

**Tool Issues?**
→ Check QUICK_START.md troubleshooting

**General Questions?**
→ Check INDEX.md for all documentation

---

## Approval Sign-Off

```
Project:     ASCII Art MCP Server v2.0
Checklist:   Complete ✓
Status:      Ready for Production
Date:        _______________
Approved By: _______________
Deployed By: _______________
```

---

**Good luck with your deployment!** 🚀

Remember:

1. Follow the checklist in order
2. Don't skip steps
3. Save credentials securely
4. Test thoroughly
5. Monitor after deployment

**Questions?** Check the documentation first - answers are there!
