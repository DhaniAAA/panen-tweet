# 🐦 Panen Tweet — Twitter/X Scraper

[![PyPI version](https://badge.fury.io/py/panen-tweet.svg)](https://pypi.org/project/panen-tweet/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Changelog](https://img.shields.io/badge/Changelog-v1.1.0-orange)](CHANGELOG.md)

**Panen Tweet** adalah tool Python untuk mengambil (scraping) data tweet dari Twitter/X berdasarkan kata kunci, rentang tanggal, bahasa, dan jenis tweet. Cocok untuk keperluan riset, analisis data, atau skripsi.

---

## 📋 Daftar Isi

- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Mendapatkan Auth Token](#-mendapatkan-auth-token)
- [Cara Penggunaan](#-cara-penggunaan)
- [Format Output (CSV)](#-format-output-csv)
- [Parameter Lengkap](#️-parameter-lengkap)
- [Tips & Tricks](#-tips--tricks)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer](#️-disclaimer--legal)

---

## ✅ Prasyarat

Sebelum mulai, pastikan kamu sudah punya:

- **Python 3.7 atau lebih baru** → [Download di sini](https://www.python.org/downloads/)
- **Google Chrome** terinstall di komputer kamu
- Akun **Twitter/X** yang aktif

Cek versi Python kamu:

```bash
python --version
```

---

## Instalasi

### Cara 1: Dari PyPI _(Direkomendasikan)_

```bash
pip install panen-tweet
```

### Cara 2: Dari Source Code (GitHub)

```bash
git clone https://github.com/Dhaniaaa/panen-tweet.git
cd panen-tweet
pip install -e .
```

### Khusus: Google Colab atau Linux Server (VPS)

Di Google Colab dan Linux server, Google Chrome tidak terinstall secara default. Jalankan perintah ini terlebih dahulu:

```bash
# 1. Install library
!pip install panen-tweet

# 2. Install Google Chrome (cukup sekali)
!panen-tweet install-chrome
```

---

## Mendapatkan Auth Token

> **Apa itu auth_token?**
> Auth token adalah kode unik yang membuktikan kamu sudah login ke Twitter/X. Tool ini membutuhkan token ini untuk bisa mengakses data tweet.

### Cara Mendapatkan Token (Langkah demi Langkah):

1. **Buka browser** (Chrome atau Firefox) dan **login** ke [x.com](https://x.com)
2. Tekan **F12** untuk membuka Developer Tools
3. Klik tab **Application** (Chrome) atau **Storage** (Firefox)
4. Di panel kiri, klik **Cookies** → pilih **`https://x.com`**
5. Cari baris dengan nama **`auth_token`**
6. **Klik baris tersebut**, lalu **salin nilai (value)** di kolom sebelah kanan

> 🖼️ Token terlihat seperti deretan karakter panjang, contoh: `1a2b3c4d5e6f7a8b9c0d...`

### KEAMANAN TOKEN — WAJIB DIBACA!

Token ini adalah **kunci akses penuh ke akun Twitter/X kamu**.

- ❌ **JANGAN** bagikan token ke siapapun
- ❌ **JANGAN** tulis token langsung di file Python
- ❌ **JANGAN** commit/push file yang berisi token ke GitHub
- ✅ Simpan token di file `.env` (lihat panduan di [SECURITY.md](SECURITY.md))
- ✅ Jika token bocor, segera **ganti password Twitter/X kamu**

---

## Cara Penggunaan

Ada 3 cara menggunakan Panen Tweet. Pilih yang paling sesuai dengan kebutuhanmu.

---

### Cara 1: Command Line Interface (CLI) — Termudah untuk Pemula

Setelah instalasi, cukup jalankan:

```bash
panen-tweet
```

Program akan memandu kamu secara interaktif. Kamu akan diminta memasukkan:

| No. | Pertanyaan             | Contoh Input                             |
| --- | ---------------------- | ---------------------------------------- |
| 1   | Auth token             | _(paste token dari browser)_             |
| 2   | Kata kunci pencarian   | `banjir jakarta`                         |
| 3   | Jumlah tweet per sesi  | `100`                                    |
| 4   | Tanggal mulai          | `2024-01-01`                             |
| 5   | Tanggal selesai        | `2024-01-07`                             |
| 6   | Interval hari per sesi | `1` _(1 = per hari)_                     |
| 7   | Kode bahasa            | `id` _(Indonesia)_ atau `en` _(English)_ |
| 8   | Jenis tweet            | `1` _(Top)_ atau `2` _(Terbaru/Latest)_  |

**Contoh tampilan di terminal:**

```
TWITTER/X SCRAPER - PANEN TWEET
================================
Masukkan auth_token Anda: <paste_token_disini>

1. Masukkan kata kunci/topik pencarian: banjir jakarta
2. Berapa jumlah MAKSIMAL tweet yang ingin diambil PER SESI? 100
3. Masukkan TANGGAL MULAI (YYYY-MM-DD): 2024-01-01
4. Masukkan TANGGAL SELESAI (YYYY-MM-DD): 2024-01-07
5. Berapa hari interval per sesi? (1 = per hari): 1
6. Masukkan kode bahasa (id / en / ja / dll): id
7. Pilih jenis tweet (1 untuk Top, 2 untuk Terbaru): 2
```

**Hasil scraping** akan otomatis disimpan ke file CSV, contoh:
`tweets_banjirjakarta_latest_20240101-20240107.csv`

---

### Cara 2: Sebagai Library Python

Cocok jika kamu ingin mengintegrasikan ke dalam notebook atau script sendiri.

```python
from panen_tweet import TwitterScraper
import datetime
import os

# ✅ Cara aman: baca token dari environment variable
# Jalankan dulu di terminal: export TWITTER_AUTH_TOKEN="tokenmu"
auth_token = os.getenv('TWITTER_AUTH_TOKEN')

if not auth_token:
    raise ValueError("Token belum diset! Lihat SECURITY.md untuk panduan.")

# Inisialisasi scraper
scraper = TwitterScraper(
    auth_token=auth_token,
    scroll_pause_time=5,  # Jeda antar scroll (detik) - naikkan jika koneksi lambat
    headless=True         # True = tanpa GUI browser | False = tampilkan browser
)

# Jalankan scraping
df = scraper.scrape_with_date_range(
    keyword="banjir jakarta",
    target_per_session=100,
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 7),
    interval_days=1,
    lang='id',
    search_type='latest'  # 'top' atau 'latest'
)

# Simpan ke CSV
if df is not None:
    scraper.save_to_csv(df, "hasil_scraping.csv")
    print(f"✅ Berhasil mengambil {len(df)} tweets!")
    print(df.head())
else:
    print("❌ Tidak ada data yang berhasil diambil.")
```

---

### Cara 3: Menggunakan File `.env` untuk Keamanan Token

Cara ini **paling aman** untuk menyimpan token tanpa risiko ter-upload ke GitHub.

**Langkah 1** — Install `python-dotenv`:

```bash
pip install python-dotenv
```

**Langkah 2** — Buat file `.env` di folder project:

```
TWITTER_AUTH_TOKEN=tokenmu_disini
```

**Langkah 3** — Muat di kode Python:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Baca file .env
auth_token = os.getenv('TWITTER_AUTH_TOKEN')
```

> File `.env` sudah otomatis masuk ke `.gitignore`, jadi **tidak akan ter-upload ke GitHub**.

Atau jika mau langsung via terminal tanpa file `.env`:

**Windows PowerShell:**

```powershell
$env:TWITTER_AUTH_TOKEN = "tokenmu_disini"
panen-tweet
```

**Linux / Mac:**

```bash
export TWITTER_AUTH_TOKEN="tokenmu_disini"
panen-tweet
```

---

## Format Output CSV

Hasil scraping disimpan otomatis dalam format CSV dengan kolom-kolom berikut:

| Kolom           | Deskripsi                               |
| --------------- | --------------------------------------- |
| `username`      | Nama tampilan pengguna                  |
| `handle`        | Nama akun Twitter (`@username`)         |
| `timestamp`     | Waktu tweet diposting (format ISO 8601) |
| `tweet_text`    | Isi teks tweet                          |
| `url`           | Tautan langsung ke tweet                |
| `reply_count`   | Jumlah reply                            |
| `retweet_count` | Jumlah retweet                          |
| `like_count`    | Jumlah like                             |

**Contoh isi file CSV:**

```csv
username,handle,timestamp,tweet_text,url,reply_count,retweet_count,like_count
Budi Santoso,@budisant,2024-01-01T10:30:00.000Z,"Banjir parah di Jakarta!",https://x.com/budisant/status/123,5,10,25
```

---

## Parameter Lengkap

### `TwitterScraper()`

```python
TwitterScraper(
    auth_token=None,        # (WAJIB) Token dari cookie browser
    scroll_pause_time=5,    # Jeda antar scroll, dalam detik (default: 5)
    headless=True           # True = tanpa browser GUI | False = tampilkan browser
)
```

### `scrape_with_date_range()`

```python
scraper.scrape_with_date_range(
    keyword="",             # (WAJIB) Kata kunci pencarian
    target_per_session=100, # Target jumlah tweet per sesi (default: 100)
    start_date=datetime,    # (WAJIB) Tanggal mulai, format: datetime(YYYY, M, D)
    end_date=datetime,      # (WAJIB) Tanggal selesai, format: datetime(YYYY, M, D)
    interval_days=1,        # Rentang hari per sesi (1 = scraping per hari)
    lang='id',              # Kode bahasa: 'id', 'en', 'ja', 'es', dll.
    search_type='top'       # 'top' = tweet teratas | 'latest' = tweet terbaru
)
```

---

## Tips & Tricks

### Mengumpulkan Banyak Tweet

- Gunakan `interval_days=1` untuk scraping per hari agar lebih detail
- Jangan set `target_per_session` terlalu tinggi (rekomendasinya 50–200)
- Percepat waktu loading dengan menambah `scroll_pause_time` jika koneksi lambat

### Menghindari Rate Limit

Rate limit artinya Twitter/X membatasi akses karena scraping terlalu cepat.

- Gunakan `scroll_pause_time` minimal 5 detik
- Jangan jalankan lebih dari satu proses scraping bersamaan
- Beri jeda beberapa menit antar sesi besar

### Kode Bahasa yang Tersedia

| Kode | Bahasa    |
| ---- | --------- |
| `id` | Indonesia |
| `en` | English   |
| `ja` | Japanese  |
| `es` | Spanish   |
| `fr` | French    |
| `ko` | Korean    |

---

## Troubleshooting

### ❌ Error: `WebDriver not found`

Chrome tidak terdeteksi atau ChromeDriver tidak cocok.

**Solusi:**

- Pastikan Google Chrome sudah terinstall
- Package akan otomatis mendownload ChromeDriver yang sesuai

---

### ❌ Error: `Auth token invalid`

Token yang kamu masukkan tidak valid atau sudah kedaluwarsa.

**Solusi:**

1. Buka kembali [x.com](https://x.com) di browser
2. Login ulang jika perlu
3. Ambil ulang nilai `auth_token` dari tab Developer Tools → Cookies
4. Pastikan tidak ada spasi tersisa saat copy-paste

---

### ❌ Error: `No tweets found`

Tidak ada tweet yang ditemukan untuk parameter yang kamu masukkan.

**Solusi:**

- Periksa koneksi internet
- Coba kata kunci yang lebih umum/populer
- Periksa rentang tanggal — mungkin memang tidak ada tweet di periode tersebut
- Pastikan auth_token masih valid

---

### Browser tidak muncul

Ini **normal** — mode default adalah `headless=True` (tanpa tampilan browser).

Jika ingin melihat proses scraping secara visual:

```python
scraper = TwitterScraper(auth_token=token, headless=False)
```

---

## Requirements

- **Python** 3.7+
- **Google Chrome** (versi terbaru)
- **Dependencies** (otomatis terinstall bersama package):
  - `pandas >= 2.0.0`
  - `selenium >= 4.0.0`
  - `webdriver-manager >= 4.0.0`

---

## Disclaimer & Legal

Tool ini dibuat untuk tujuan **edukasi dan penelitian ilmiah**.

Dengan menggunakan tool ini, kamu setuju untuk mematuhi:

- [Twitter/X Terms of Service](https://twitter.com/tos)
- [Twitter/X Developer Agreement](https://developer.twitter.com/en/developer-terms/agreement-and-policy)
- Aturan rate limiting dan robots.txt platform
- Hak privasi dan hak cipta pengguna lain

**Pengembang tidak bertanggung jawab** atas segala penyalahgunaan tool ini.

---

## Berkontribusi

Kontribusi sangat disambut! Cara berkontribusi:

1. Fork repository ini
2. Buat branch baru: `git checkout -b feature/fitur-baru`
3. Commit perubahan: `git commit -m 'Tambah fitur baru'`
4. Push ke branch: `git push origin feature/fitur-baru`
5. Buat Pull Request

---

## Lisensi

MIT License — lihat file [LICENSE](LICENSE) untuk detail lengkap.

---

## Dukungan & Kontak

- **Laporkan Bug**: [GitHub Issues](https://github.com/Dhaniaaa/panen-tweet/issues)
- **PyPI Package**: [pypi.org/project/panen-tweet](https://pypi.org/project/panen-tweet/)
- **Email**: ramadhanigb19@gmail.com

---

## Terima Kasih Kepada

- [Selenium](https://www.selenium.dev/) — Framework web automation
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) — Manajemen ChromeDriver otomatis
- [pandas](https://pandas.pydata.org/) — Pengolahan data

---

**Dibuat dengan ❤️ untuk komunitas data science & riset Indonesia**

⭐ Jika project ini bermanfaat, berikan bintang di GitHub!
