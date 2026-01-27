# 🚀 Quick Start - Publishing panen-tweet to PyPI

## ⚡ Super Quick Guide

### 1️⃣ Security Check (MANDATORY!)

```bash
# Check for exposed tokens
findstr /s /i "e5c192" *.py
# Should return NOTHING!

# Change your Twitter/X password NOW if token was exposed
```

### 2️⃣ Final Checks

```bash
# Build package
python -m build

# Check dist folder
ls dist/
# Should see: panen_tweet-1.0.0-py3-none-any.whl
```

### 3️⃣ Git Push

```bash
# Review changes
git status
git diff

# NO TOKENS!!! Then commit:
git add .
git commit -m "Ready for PyPI v1.0.0"
git push origin main
```

### 4️⃣ PyPI Setup

1. Go to https://pypi.org/manage/account/publishing/
2. Find **panen-tweet** (pending)
3. Verify settings:
   - Repo: `DhaniAAA/Scrapping-X` ✓
   - Workflow: `workflows.yaml` ✓
4. Click **"Add"** ✓

### 5️⃣ GitHub Release

1. https://github.com/DhaniAAA/Scrapping-X/releases
2. Click **"Create a new release"**
3. Tag: **`v1.0.0`** (must start with 'v')
4. Title: **`panen-tweet v1.0.0`**
5. Click **"Publish release"**

### 6️⃣ Wait for Automation

- GitHub Actions runs automatically
- Monitor: https://github.com/DhaniAAA/Scrapping-X/actions
- Wait ~2 minutes

### 7️⃣ Verify

```bash
pip install panen-tweet
scrape-x  # Should work!
```

---

## 🔗 Important Links

| What              | Link                                                 |
| ----------------- | ---------------------------------------------------- |
| PyPI Publishers   | https://pypi.org/manage/account/publishing/          |
| Your Repo         | https://github.com/DhaniAAA/Scrapping-X              |
| Create Release    | https://github.com/DhaniAAA/Scrapping-X/releases/new |
| Actions Status    | https://github.com/DhaniAAA/Scrapping-X/actions      |
| PyPI Page (after) | https://pypi.org/project/panen-tweet/                |

---

## ⚠️ Common Issues

### "Token not found"

→ You didn't approve pending publisher at PyPI

### "Workflow not found"

→ Make sure `.github/workflows/workflows.yaml` is pushed

### "Version already exists"

→ Bump version number, can't re-upload same version

---

## 📖 Full Guides

- **Complete Guide**: `PUBLISHING.md`
- **Security Guide**: `SECURITY.md`
- **Ready Status**: `READY_TO_PUBLISH.md`

---

**Good luck! 🍀**
