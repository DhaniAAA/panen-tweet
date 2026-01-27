# 🔒 SECURITY WARNING - IMPORTANT!

## ⚠️ Auth Token Security

**JANGAN PERNAH** commit auth_token asli Anda ke Git!

### Cara Aman Menggunakan Auth Token:

#### Opsi 1: Environment Variable (Recommended)

**Windows PowerShell:**

```powershell
$env:TWITTER_AUTH_TOKEN = "your_auth_token_here"
python examples_usage.py
```

**Windows Command Prompt:**

```cmd
set TWITTER_AUTH_TOKEN=your_auth_token_here
python examples_usage.py
```

**Linux/Mac:**

```bash
export TWITTER_AUTH_TOKEN="your_auth_token_here"
python examples_usage.py
```

#### Opsi 2: File .env (Recommended)

1. Install python-dotenv:

```bash
pip install python-dotenv
```

2. Buat file `.env` di root project (sudah di .gitignore):

```
TWITTER_AUTH_TOKEN=your_auth_token_here
```

3. Di script Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()
auth_token = os.getenv('TWITTER_AUTH_TOKEN')
```

#### Opsi 3: File Config Terpisah

1. Buat file `config.ini` (sudah di .gitignore):

```ini
[twitter]
auth_token = your_auth_token_here
```

2. Di script Python:

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
auth_token = config['twitter']['auth_token']
```

### ⚠️ Jika Token Sudah Ter-expose:

1. **SEGERA logout dari semua device Twitter/X**
2. **Ganti password Twitter/X Anda** untuk invalidate semua token
3. **Periksa git history**:
   ```bash
   git log -p -- examples_usage.py
   ```
4. **Jika sudah di-push ke GitHub**, token TIDAK BISA dihapus dari history
   - Solusi: Ganti password Twitter/X
   - Atau: Hapus repository dan buat ulang

### 🔐 Best Practices:

✅ **DO:**

- Gunakan environment variables
- Gunakan file .env (pastikan di .gitignore)
- Review code sebelum commit
- Gunakan `git diff` sebelum commit

❌ **DON'T:**

- Hard-code token di file Python
- Commit token ke Git
- Share token dengan orang lain
- Screenshot code yang ada token

### 🛡️ Periksa Before Commit:

```bash
# Lihat apa yang akan di-commit
git diff

# Pastikan tidak ada token
git diff | grep -i "token"
git diff | grep -i "auth"

# Hanya commit jika aman
git add .
git commit -m "Your message"
git push
```

### 📋 File yang Sudah Ditambahkan ke .gitignore:

- `.env`
- `.env.local`
- `config.ini`
- `auth_token.txt`
- `*auth_token*` (semua file yang mengandung kata "auth_token")

Pastikan file-file ini **TIDAK PERNAH** di-commit ke Git!
