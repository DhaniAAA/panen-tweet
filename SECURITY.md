# 🔒 KEAMANAN - PENTING DIBACA!

## 🚨 Peringatan Utama: Auth Token Twitter/X

> **Auth token adalah kunci akses penuh ke akun Twitter/X kamu.**
> Siapa pun yang memegang token ini bisa membaca, memposting, bahkan menghapus seisi akun kamu — **tanpa perlu password sekalipun.**

---

## ❌ JANGAN LAKUKAN INI!

```python
# ❌ SALAH - BERBAHAYA! Jangan pernah tulis token langsung di kode
auth_token = "1a2b3c4d5e6f..."  # Token asli terekspos!
```

Jika kamu menyimpan token langsung di file Python lalu commit ke Git, **siapa pun yang melihat repository tersebut bisa mengambil alih akun Twitter/X kamu.**

---

## ✅ Cara Aman Menyimpan Auth Token

### Opsi 1: File `.env` _(Paling Direkomendasikan)_

Cara ini paling mudah dan aman untuk pemula.

**Langkah 1** — Buat file `.env` di folder project:

```
TWITTER_AUTH_TOKEN=tokenmu_disini
```

> File ini sudah otomatis masuk ke `.gitignore`, jadi **tidak akan ikut ter-upload ke GitHub**.

**Langkah 2** — Install library `python-dotenv`:

```bash
pip install python-dotenv
```

**Langkah 3** — Muat token di kode Python kamu:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Membaca file .env
auth_token = os.getenv('TWITTER_AUTH_TOKEN')
```

---

### Opsi 2: Environment Variable (Langsung di Terminal)

Token hanya berlaku selama sesi terminal tersebut aktif, **tidak tersimpan ke file apapun**.

**Windows PowerShell:**

```powershell
$env:TWITTER_AUTH_TOKEN = "tokenmu_disini"
python main.py
```

**Windows Command Prompt:**

```cmd
set TWITTER_AUTH_TOKEN=tokenmu_disini
python main.py
```

**Linux / Mac / Google Colab:**

```bash
export TWITTER_AUTH_TOKEN="tokenmu_disini"
python main.py
```

---

### Opsi 3: File `config.ini`

Cocok jika kamu ingin mengelola banyak konfigurasi sekaligus.

**Langkah 1** — Buat file `config.ini`:

```ini
[twitter]
auth_token = tokenmu_disini
```

**Langkah 2** — Baca di kode Python:

```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
auth_token = config['twitter']['auth_token']
```

> File `config.ini` juga sudah masuk ke `.gitignore`, jadi aman.

---
