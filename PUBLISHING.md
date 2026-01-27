# 🚀 Panduan Publish ke PyPI dengan Trusted Publishing

Package `panen-tweet` sudah siap untuk dipublish ke PyPI!

## ✅ Setup Sudah Selesai

- ✅ Package name: **`panen-tweet`**
- ✅ GitHub repo: **DhaniAAA/Scrapping-X**
- ✅ Workflow file: **`.github/workflows/workflows.yaml`**
- ✅ Pending publisher sudah terdaftar di PyPI

## 📋 Langkah-Langkah Publish

### 1. Finalisasi Setup di PyPI

Anda sudah ada di halaman "Pending publishers". Sekarang:

1. **Verifikasi informasi**:

   - Publisher: GitHub
   - Repository: `DhaniAAA/Scrapping-X`
   - Workflow: `workflows.yaml`
   - Environment name: Kosongkan atau isi dengan `release`

2. **Klik "Add"** untuk menambahkan publisher

3. PyPI sekarang akan **trust** workflow GitHub Actions Anda untuk publish package

### 2. Verifikasi File Lokal

Pastikan semua file sudah benar:

```bash
# Lihat struktur
tree /F /A

# Pastikan .github/workflows/workflows.yaml ada
ls .github/workflows/
```

### 3. Build dan Test Package Lokal

Sebelum publish, test dulu lokal:

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package quality
twine check dist/*
```

Ini akan membuat:

- `dist/panen-tweet-1.0.0.tar.gz`
- `dist/panen_tweet-1.0.0-py3-none-any.whl`

### 4. Commit dan Push ke GitHub

**PENTING**: Pastikan tidak ada auth_token di file!

```bash
# Check apa yang akan di-commit
git status
git diff

# Pastikan tidak ada token (WAJIB!)
git diff | findstr /i "token"

# Add files
git add .

# Commit
git commit -m "Prepare for PyPI release v1.0.0"

# Push ke GitHub
git push origin main
```

### 5. Create GitHub Release

Ada 2 cara:

#### Cara A: Via GitHub Web Interface (Recommended)

1. Buka https://github.com/DhaniAAA/Scrapping-X
2. Klik **"Releases"** di sidebar kanan
3. Klik **"Create a new release"**
4. Tag version: `v1.0.0`
5. Release title: `panen-tweet v1.0.0`
6. Description (contoh):

   ````markdown
   ## panen-tweet v1.0.0 - Initial Release

   ### Features

   - Twitter/X scraping dengan Selenium
   - CLI command: `scrape-x`
   - Library untuk import di Python
   - Date range scraping
   - Auto CSV export

   ### Installation

   ```bash
   pip install panen-tweet
   ```
   ````

   ### Usage

   ```bash
   scrape-x
   ```

   Or import as library:

   ```python
   from scrape_x import TwitterScraper
   ```

   ```

   ```

7. Klik **"Publish release"**

#### Cara B: Via Git Command Line

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Then create release via GitHub web interface
```

### 6. Automatic Publishing

Setelah Anda create release di GitHub:

1. **GitHub Actions akan otomatis berjalan**
2. Workflow akan:

   - Checkout code
   - Install dependencies
   - Build package
   - Upload ke PyPI

3. **Monitor progress**:

   - Buka https://github.com/DhaniAAA/Scrapping-X/actions
   - Lihat workflow "Publish to PyPI" running
   - Tunggu sampai selesai (biasanya 1-2 menit)

4. **Verifikasi di PyPI**:
   - Package akan muncul di https://pypi.org/project/panen-tweet/
   - Orang lain bisa install dengan: `pip install panen-tweet`

## 🔧 Troubleshooting

### Error: Workflow not found

**Solusi**:

- Pastikan file `.github/workflows/workflows.yaml` sudah di-commit dan di-push
- Pastikan nama file PERSIS: `workflows.yaml` (bukan `workflow.yaml`)

### Error: Publishing failed - Invalid credentials

**Solusi**:

- Pastikan Anda sudah **klik "Add"** di PyPI pending publishers
- Pastikan repository name PERSIS: `DhaniAAA/Scrapping-X`
- Pastikan workflow name PERSIS: `workflows.yaml`

### Error: File already exists

**Solusi**:

- Version `1.0.0` sudah di-upload sebelumnya
- Naikan version number di:
  - `pyproject.toml`
  - `setup.py`
  - `scrape_x/__init__.py`
- Create release baru dengan tag yang sesuai (misal `v1.0.1`)

### Error: Environment 'release' not found

**Solusi 1** - Buat environment di GitHub:

1. Buka https://github.com/DhaniAAA/Scrapping-X/settings/environments
2. Klik "New environment"
3. Name: `release`
4. (Opsional) Add protection rules
5. Save

**Solusi 2** - Hapus environment dari workflow:
Edit `.github/workflows/workflows.yaml`, hapus bagian:

```yaml
environment:
  name: release
  url: https://pypi.org/p/panen-tweet
```

## 📝 Update Version di Masa Depan

Untuk release versi baru (misal 1.0.1):

### 1. Update Version Number

Edit 3 file ini:

**`pyproject.toml`**:

```toml
version = "1.0.1"
```

**`setup.py`**:

```python
version='1.0.1',
```

**`scrape_x/__init__.py`**:

```python
__version__ = '1.0.1'
```

### 2. Commit Changes

```bash
git add .
git commit -m "Bump version to 1.0.1"
git push
```

### 3. Create New Release

```bash
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

Then create release di GitHub web interface dengan tag `v1.0.1`

### 4. GitHub Actions akan Otomatis Publish

## 🎯 Manual Publish (Tanpa GitHub Actions)

Jika Anda ingin publish manual tanpa GitHub Actions:

```bash
# Build
python -m build

# Upload ke PyPI (memerlukan PyPI token)
python -m twine upload dist/*

# Username: __token__
# Password: pypi-...
```

Tapi dengan Trusted Publishing, Anda **TIDAK PERLU** token lagi! 🎉

## ✅ Checklist Sebelum Publish

- [ ] Auth token sudah dihapus dari semua file
- [ ] `.gitignore` sudah mencakup file sensitif
- [ ] `pyproject.toml` dan `setup.py` sudah update dengan info yang benar
- [ ] Package name: `panen-tweet`
- [ ] GitHub repo: `DhaniAAA/Scrapping-X`
- [ ] Workflow file: `.github/workflows/workflows.yaml` sudah ada
- [ ] Build test lokal berhasil: `python -m build`
- [ ] Package check berhasil: `twine check dist/*`
- [ ] Pending publisher sudah di-approve di PyPI
- [ ] README.md sudah lengkap dan jelas

## 🎉 After Publishing

Setelah berhasil publish:

1. **Test instalasi**:

   ```bash
   pip install panen-tweet
   ```

2. **Update README** dengan badge PyPI:

   ```markdown
   [![PyPI version](https://badge.fury.io/py/panen-tweet.svg)](https://badge.fury.io/py/panen-tweet)
   [![Downloads](https://pepy.tech/badge/panen-tweet)](https://pepy.tech/project/panen-tweet)
   ```

3. **Share dengan komunitas**!

---

**Good luck with your PyPI publishing! 🚀**
