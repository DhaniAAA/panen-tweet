# 🚀 Quick Usage Guide - Panen Tweet

## 🎯 Cara Cepat Menggunakan Panen Tweet

### Method 1: Menggunakan pip install (Recommended)

#### Step 1: Install Package

```bash
pip install panen-tweet
```

#### Step 2: Jalankan CLI

```bash
panen-tweet
```

#### Step 3: Ikuti Instruksi

Program akan meminta Anda input:

1. **Auth token** (copy dari x.com cookies)
2. **Kata kunci** (misal: "python programming")
3. **Jumlah tweet** per sesi (misal: 100)
4. **Tanggal mulai** (misal: 2024-01-01)
5. **Tanggal selesai** (misal: 2024-01-07)
6. **Interval hari** (misal: 1)
7. **Bahasa** (misal: en atau id)
8. **Jenis tweet** (1=Top, 2=Latest)

#### Step 4: Tunggu Proses Selesai

Program akan:

- Otomatis scraping tweet
- Simpan ke file CSV
- Hapus duplikat

**Output:** File CSV di folder yang sama dengan format `tweets_[keyword]_[type]_[date].csv`

---

### Method 2: Menggunakan Script main.py

Jika Anda belum install package atau ingin development:

```bash
# Install dependencies
pip install pandas selenium webdriver-manager

# Jalankan script
python main.py
```

Lalu ikuti instruksi yang sama seperti Method 1.

---

### Method 3: Import sebagai Library

Untuk integrasi ke code Python Anda:

```python
from scrape_x import TwitterScraper
import datetime

# Setup (ganti dengan token Anda)
scraper = TwitterScraper(
    auth_token="your_auth_token_here",
    headless=True  # False untuk lihat browser
)

# Scraping
df = scraper.scrape_with_date_range(
    keyword="python",
    target_per_session=50,
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 3),
    interval_days=1,
    lang='en',
    search_type='latest'
)

# Simpan
if df is not None:
    scraper.save_to_csv(df, "hasil.csv")
```

---

## 🔑 Cara Mendapatkan Auth Token

### Visual Guide:

1. **Buka x.com** dan login
2. **Tekan F12** → Developer Tools terbuka
3. **Klik tab "Application"** (Chrome) atau "Storage" (Firefox)
4. Di sidebar kiri:
   - Expand **Cookies**
   - Klik **`https://x.com`**
5. Di tabel cookies, cari **`auth_token`**
6. **Klik** pada row tersebut
7. **Copy value** di bagian bawah atau klik kanan → Copy value
8. **Paste** token saat diminta program

### 🎥 Screenshot Location:

```
Developer Tools (F12)
└── Application tab
    └── Storage
        └── Cookies
            └── https://x.com
                └── auth_token  ← Copy value ini
```

---

## 💡 Contoh Penggunaan Nyata

### Contoh 1: Scraping Tweet Bahasa Indonesia tentang "AI"

```bash
panen-tweet
```

Input:

- Auth token: `[paste token Anda]`
- Kata kunci: `AI kecerdasan buatan`
- Jumlah: `100`
- Tanggal mulai: `2024-01-01`
- Tanggal selesai: `2024-01-07`
- Interval: `1`
- Bahasa: `id`
- Jenis: `2` (Latest)

Output: `tweets_AIkecerdasanbuatan_latest_20240101-20240107.csv`

### Contoh 2: Scraping Top Tweets tentang "Python"

Input:

- Kata kunci: `python programming`
- Jumlah: `50`
- Tanggal: Dec 2024
- Bahasa: `en`
- Jenis: `1` (Top)

### Contoh 3: Research tentang Brand/Product

Input:

- Kata kunci: `iPhone 15`
- Jumlah: `200`
- Periode: 1 minggu
- Bahasa: `en`
- Jenis: `2` (Latest - untuk sentiment analysis)

---

## ⚙️ Tips Penggunaan

### 1. Untuk Dataset Besar

- Gunakan interval kecil (1 hari)
- Target per sesi: 50-100 tweets
- Jangan terburu-buru

### 2. Menghindari Rate Limit

- Pause time: 5-10 detik
- Jeda antar sesi: otomatis 10 detik
- Jangan jalankan multiple instance

### 3. Filter yang Efektif

- Gunakan keyword spesifik
- Kombinasikan dengan bahasa
- Pilih Top untuk kualitas, Latest untuk kuantitas

### 4. Keamanan Token

```bash
# Gunakan environment variable (lebih aman)
$env:TWITTER_AUTH_TOKEN = "your_token"
panen-tweet
```

---

## 🐛 Quick Troubleshooting

| Problem              | Solution                                 |
| -------------------- | ---------------------------------------- |
| "Command not found"  | Install ulang: `pip install panen-tweet` |
| "No tweets found"    | Cek keyword, tanggal, atau token         |
| "WebDriver error"    | Install Chrome browser                   |
| "Auth invalid"       | Dapatkan token baru dari x.com           |
| Browser tidak muncul | Normal (headless mode)                   |

---

## 📊 Output CSV Format

File CSV akan berisi kolom:

- `username` - Nama user
- `handle` - @username
- `timestamp` - Waktu post
- `tweet_text` - Isi tweet
- `url` - Link ke tweet
- `reply_count` - Jumlah reply
- `retweet_count` - Jumlah RT
- `like_count` - Jumlah like

Import ke Excel/Google Sheets untuk analisis lebih lanjut!

---

## 🆘 Butuh Bantuan?

- **README lengkap**: [README.md](README.md)
- **GitHub Issues**: [Issues](https://github.com/Dhaniaaa/panen-tweet/issues)
- **Email**: rhamadhanigb19@gmail.com

---

**Happy scraping! 🐦📊**
