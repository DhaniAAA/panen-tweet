# 🐦 Panen Tweet - Twitter/X Scraper

[![PyPI version](https://badge.fury.io/py/panen-tweet.svg)](https://pypi.org/project/panen-tweet/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Panen Tweet** adalah tool powerful untuk scraping Twitter/X menggunakan Selenium. Dengan tool ini, Anda dapat mengekstrak tweet berdasarkan kata kunci, rentang tanggal, bahasa, dan jenis tweet (teratas/terbaru) dengan mudah.

## 📦 Instalasi

### Instalasi dari PyPI (Recommended)

```bash
pip install panen-tweet
```

### Instalasi dari Source

```bash
git clone https://github.com/Dhaniaaa/panen-tweet.git
cd panen-tweet
pip install -e .
```

### 🐧 Running on Google Colab / Linux Server

Jika Anda menjalankan di Google Colab atau Linux Server (VPS), Anda **WAJIB** menginstall Google Chrome.

Kami sudah menyertakan perintah otomatis untuk ini:

```bash
# 1. Install library
!pip install panen-tweet

# 2. Install Google Chrome (Sekali jalan)
!panen-tweet install-chrome
```

## 🔑 Mendapatkan Auth Token

Sebelum menggunakan, Anda perlu mendapatkan **auth_token** dari akun Twitter/X Anda:

### Langkah-langkah:

1. **Login** ke [x.com](https://x.com) menggunakan browser Anda
2. Tekan **F12** untuk membuka Developer Tools
3. Buka tab **Application** (Chrome) atau **Storage** (Firefox)
4. Di sidebar kiri, expand **Cookies** → klik **`https://x.com`**
5. Cari cookie dengan nama **`auth_token`**
6. **Klik** pada cookie tersebut dan **salin nilai (value)** nya
7. Nilai ini yang akan Anda gunakan

### ⚠️ PENTING - Keamanan Token:

- **JANGAN** bagikan auth_token Anda kepada siapapun
- **JANGAN** commit auth_token ke Git/GitHub
- Token ini memberikan akses penuh ke akun Twitter/X Anda
- Jika token ter-expose, segera ganti password Twitter/X Anda

## 🚀 Cara Penggunaan

### Opsi 1: Command Line Interface (Termudah)

Setelah instalasi, jalankan command berikut di terminal:

```bash
panen-tweet
```

Program akan meminta Anda untuk:

1. **Memasukkan auth_token**
2. **Kata kunci** yang ingin dicari
3. **Jumlah tweet** maksimal per sesi
4. **Tanggal mulai** (format: YYYY-MM-DD)
5. **Tanggal selesai** (format: YYYY-MM-DD)
6. **Interval hari** per sesi scraping
7. **Kode bahasa** (contoh: `id` untuk Indonesia, `en` untuk English)
8. **Jenis tweet** (1 untuk Top, 2 untuk Terbaru/Latest)

**Contoh interaksi:**

```
TWITTER/X SCRAPER - PANEN TWEET
...
Masukkan auth_token Anda: <paste_token_anda_disini>

1. Masukkan kata kunci/topik pencarian: python programming
2. Berapa jumlah MAKSIMAL tweet yang ingin diambil PER SESI? 100
3. Masukkan TANGGAL MULAI KESELURUHAN (YYYY-MM-DD): 2024-01-01
4. Masukkan TANGGAL SELESAI KESELURUHAN (YYYY-MM-DD): 2024-01-07
5. Berapa hari interval per sesi scraping? (misal: 1 untuk per hari): 1
6. Masukkan kode bahasa (misal: 'id' untuk Indonesia, 'en' untuk Inggris): en
7. Pilih jenis tweet (1 untuk Top, 2 untuk Terbaru): 2
```

Program akan otomatis:

- Scraping tweet sesuai parameter
- Menyimpan hasil ke file CSV
- Menghapus duplikat otomatis

**Output:** File CSV dengan nama seperti `tweets_pythonprogramming_latest_20240101-20240107.csv`

### Opsi 2: Menggunakan sebagai Library Python

Jika Anda ingin mengintegrasikan ke dalam kode Python Anda:

```python
from panen_tweet import TwitterScraper
import datetime
import os

# Setup auth token (gunakan environment variable untuk keamanan)
# Windows: $env:TWITTER_AUTH_TOKEN = "your_token_here"
# Linux/Mac: export TWITTER_AUTH_TOKEN="your_token_here"
auth_token = os.getenv('TWITTER_AUTH_TOKEN', 'your_auth_token_here')

# Inisialisasi scraper
scraper = TwitterScraper(
    auth_token=auth_token,
    scroll_pause_time=5,  # Waktu jeda antar scroll (detik)
    headless=True         # Set False untuk melihat browser
)

# Scraping dengan rentang tanggal
df = scraper.scrape_with_date_range(
    keyword="python programming",
    target_per_session=100,      # 100 tweets per sesi
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 7),
    interval_days=1,             # Scraping per hari
    lang='en',                   # Bahasa English
    search_type='latest'         # 'top' atau 'latest'
)

# Simpan hasil ke CSV
if df is not None:
    scraper.save_to_csv(df, "hasil_scraping.csv")
    print(f"✅ Berhasil mengambil {len(df)} tweets!")
    print(df.head())
else:
    print("❌ Tidak ada data yang berhasil diambil")
```

### Opsi 3: Menggunakan Environment Variable (Recommended untuk Security)

**Windows PowerShell:**

```powershell
# Set environment variable
$env:TWITTER_AUTH_TOKEN = "your_auth_token_here"

# Jalankan program
panen-tweet
```

**Windows CMD:**

```cmd
set TWITTER_AUTH_TOKEN=your_auth_token_here
panen-tweet
```

**Linux/Mac:**

```bash
export TWITTER_AUTH_TOKEN="your_auth_token_here"
panen-tweet
```

Atau buat file `.env`:

```bash
# Install python-dotenv
pip install python-dotenv

# Buat file .env
echo "TWITTER_AUTH_TOKEN=your_token_here" > .env

# Di kode Python Anda:
from dotenv import load_dotenv
load_dotenv()
```

## 📊 Format Output

Data yang dihasilkan dalam format CSV dengan kolom-kolom berikut:

| Kolom           | Deskripsi                          |
| --------------- | ---------------------------------- |
| `username`      | Nama user yang memposting tweet    |
| `handle`        | Handle Twitter (@username)         |
| `timestamp`     | Waktu tweet diposting (format ISO) |
| `tweet_text`    | Isi konten tweet                   |
| `url`           | URL lengkap ke tweet               |
| `reply_count`   | Jumlah replies                     |
| `retweet_count` | Jumlah retweets                    |
| `like_count`    | Jumlah likes                       |

**Contoh output CSV:**

```csv
username,handle,timestamp,tweet_text,url,reply_count,retweet_count,like_count
John Doe,@johndoe,2024-01-01T10:30:00.000Z,Python is awesome!,https://x.com/johndoe/status/...,5,10,25
...
```

## ⚙️ Parameter & Konfigurasi

### TwitterScraper Parameters

```python
TwitterScraper(
    auth_token=None,        # Cookie auth_token (WAJIB)
    scroll_pause_time=5,    # Waktu jeda antar scroll dalam detik
    headless=True          # True = tanpa GUI, False = tampilkan browser
)
```

### scrape_with_date_range Parameters

```python
scraper.scrape_with_date_range(
    keyword="",             # Kata kunci pencarian (WAJIB)
    target_per_session=100, # Jumlah target tweet per sesi
    start_date=datetime,    # Tanggal mulai (WAJIB)
    end_date=datetime,      # Tanggal selesai (WAJIB)
    interval_days=1,        # Interval hari per sesi (1 = per hari)
    lang='id',             # Kode bahasa: 'id', 'en', 'ja', dll
    search_type='top'      # 'top' = tweet teratas, 'latest' = terbaru
)
```

## 💡 Tips & Tricks

### 1. Scraping Banyak Tweet

Untuk hasil maksimal:

- Gunakan interval kecil (1 hari) untuk dataset besar
- Set `target_per_session` tidak terlalu tinggi (50-200)
- Gunakan `scroll_pause_time` lebih besar (7-10 detik) untuk koneksi lambat

### 2. Menghindari Rate Limit

- Jangan scraping terlalu cepat
- Gunakan `scroll_pause_time` minimal 5 detik
- Beri jeda antar sesi scraping
- Jangan jalankan multiple instance bersamaan

### 3. Filter Bahasa Spesifik

Gunakan parameter `lang` dengan kode ISO 639-1:

- `id` - Bahasa Indonesia
- `en` - English
- `ja` - Japanese
- `es` - Spanish
- `fr` - French
- Dan lainnya...

### 4. Troubleshooting "No tweets found"

Jika tidak menemukan tweet:

- Periksa koneksi internet
- Pastikan auth_token masih valid
- Coba dengan keyword yang lebih umum
- Periksa rentang tanggal (mungkin tidak ada tweet di periode tersebut)

## 📋 Requirements

- **Python 3.7+**
- **Chrome/Chromium browser**
- **Dependencies** (otomatis terinstall):
  - pandas >= 2.0.0
  - selenium >= 4.0.0
  - webdriver-manager >= 4.0.0

## ⚠️ Disclaimer & Legal

Tool ini dibuat untuk tujuan **edukasi dan penelitian**.

Pastikan Anda mematuhi:

- [Twitter/X Terms of Service](https://twitter.com/tos)
- [Twitter/X Developer Agreement](https://developer.twitter.com/en/developer-terms/agreement-and-policy)
- Kebijakan scraping dan rate limiting
- Privasi dan hak cipta pengguna lain

**Penulis tidak bertanggung jawab** atas penyalahgunaan tool ini.

## 🐛 Troubleshooting

### Error: "WebDriver not found"

**Solusi:** Package otomatis download ChromeDriver, pastikan Chrome terinstall.

### Error: "Auth token invalid"

**Solusi:**

1. Login ulang ke x.com
2. Dapatkan auth_token baru
3. Pastikan tidak ada spasi saat copy-paste

### Error: "No tweets found"

**Solusi:**

- Periksa koneksi internet
- Verifikasi auth_token masih valid
- Coba keyword lain atau rentang tanggal berbeda

### Browser tidak muncul (headless mode)

Ini normal! Set `headless=False` jika ingin melihat browser:

```python
scraper = TwitterScraper(auth_token=token, headless=False)
```

## 🤝 Contributing

Kontribusi sangat diterima!

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 License

MIT License - lihat file [LICENSE](LICENSE) untuk detail lengkap.

## 💬 Support & Contact

- **GitHub Issues**: [https://github.com/Dhaniaaa/panen-tweet/issues](https://github.com/Dhaniaaa/panen-tweet/issues)
- **PyPI Package**: [https://pypi.org/project/panen-tweet/](https://pypi.org/project/panen-tweet/)
- **Email**: rhamadhanigb19@gmail.com

## 🙏 Acknowledgments

- [Selenium](https://www.selenium.dev/) - Web automation framework
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) - Automatic ChromeDriver management
- [pandas](https://pandas.pydata.org/) - Data processing

---

**Made with ❤️ for the data science & research community**

⭐ Jika project ini membantu, berikan star di GitHub!
