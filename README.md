# Scrape-X 🐦

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Scrape-X** adalah tool powerful untuk scraping Twitter/X menggunakan Selenium. Tool ini memungkinkan Anda mengekstrak tweet berdasarkan kata kunci, rentang tanggal, bahasa, dan jenis tweet (teratas/terbaru).

## ✨ Fitur

- 🔍 **Pencarian Fleksibel**: Cari tweet berdasarkan kata kunci
- 📅 **Filter Tanggal**: Tentukan rentang tanggal yang spesifik
- 🌍 **Multi-bahasa**: Support untuk filter bahasa
- 🔝 **Jenis Tweet**: Pilih antara tweet teratas atau terbaru
- 📊 **Export CSV**: Simpan hasil dalam format CSV
- 🔄 **Scraping Bertahap**: Scraping otomatis dengan interval untuk menghindari rate limit
- 🤖 **Headless Mode**: Jalankan browser tanpa GUI

## 📦 Instalasi

### Instalasi dari Source (Development)

```bash
# Clone repository
git clone https://github.com/yourusername/Scrapping-X.git
cd Scrapping-X

# Install dalam mode development
pip install -e .
```

### Instalasi dari PyPI (Setelah publish)

```bash
pip install scrape-x
```

### Instalasi Manual dari ZIP

```bash
# Download dan extract ZIP, lalu:
cd Scrapping-X
pip install .
```

## 🚀 Cara Penggunaan

### 1. Dapatkan Auth Token

Sebelum menggunakan, Anda perlu mendapatkan cookie `auth_token` dari akun Twitter/X Anda:

1. Login ke [x.com](https://x.com)
2. Buka Developer Tools (tekan `F12`)
3. Pergi ke tab **Application** > **Storage** > **Cookies** > `https://x.com`
4. Cari cookie dengan nama `auth_token`
5. Salin nilai (value) dari cookie tersebut

⚠️ **PENTING**: Jangan bagikan `auth_token` Anda kepada siapapun!

### 2. Menggunakan Command Line Interface (CLI)

Setelah instalasi, Anda bisa langsung menggunakan command `scrape-x`:

```bash
scrape-x
```

Anda akan diminta memasukkan:

- Auth token
- Kata kunci pencarian
- Jumlah tweet per sesi
- Tanggal mulai dan selesai
- Interval scraping
- Kode bahasa
- Jenis tweet (Top/Latest)

### 3. Menggunakan sebagai Library Python

#### Contoh Basic:

```python
from scrape_x import TwitterScraper
import datetime

# Inisialisasi scraper
scraper = TwitterScraper(
    auth_token="your_auth_token_here",
    scroll_pause_time=5,
    headless=True
)

# Scraping dengan rentang tanggal
df = scraper.scrape_with_date_range(
    keyword="python programming",
    target_per_session=100,
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 7),
    interval_days=1,
    lang='en',
    search_type='latest'
)

# Simpan hasil
if df is not None:
    scraper.save_to_csv(df, "tweets_python.csv")
    print(f"Berhasil mengambil {len(df)} tweets!")
```

#### Contoh Advanced dengan Custom Configuration:

```python
from scrape_x import TwitterScraper
import datetime

# Inisialisasi dengan konfigurasi custom
scraper = TwitterScraper(
    auth_token="your_auth_token",
    scroll_pause_time=3,  # Pause lebih cepat
    headless=False  # Tampilkan browser
)

# Setup driver manual
if scraper.setup_driver():
    scraper.login()

    # Scraping manual
    tweets = scraper.scrape_tweets(
        query="machine%20learning%20lang%3Aen",
        target_count=50,
        search_type='top'
    )

    print(f"Ditemukan {len(tweets)} tweets")

    # Cleanup
    scraper.quit()
```

## 📊 Format Output

Data yang dihasilkan dalam format CSV dengan kolom:

| Kolom           | Deskripsi                          |
| --------------- | ---------------------------------- |
| `username`      | Nama user yang mem-posting tweet   |
| `handle`        | Handle Twitter (@username)         |
| `timestamp`     | Waktu tweet diposting (ISO format) |
| `tweet_text`    | Isi konten tweet                   |
| `url`           | URL lengkap tweet                  |
| `reply_count`   | Jumlah replies                     |
| `retweet_count` | Jumlah retweets                    |
| `like_count`    | Jumlah likes                       |

## ⚙️ Konfigurasi

### Parameter TwitterScraper

```python
TwitterScraper(
    auth_token=None,        # Cookie auth_token dari X.com
    scroll_pause_time=5,    # Waktu jeda antara scroll (detik)
    headless=True          # Mode headless browser
)
```

### Parameter scrape_with_date_range

```python
scraper.scrape_with_date_range(
    keyword="",             # Kata kunci pencarian
    target_per_session=100, # Target tweet per sesi
    start_date=datetime,    # Tanggal mulai
    end_date=datetime,      # Tanggal selesai
    interval_days=1,        # Interval hari per sesi
    lang='id',             # Kode bahasa (id/en/dll)
    search_type='top'      # 'top' atau 'latest'
)
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/Scrapping-X.git
cd Scrapping-X

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Di Windows: venv\Scripts\activate

# Install dependencies development
pip install -e .
```

### Build Package

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload ke PyPI (memerlukan akun PyPI)
python -m twine upload dist/*
```

## 📋 Requirements

- Python 3.7+
- Chrome/Chromium browser
- Dependencies:
  - pandas >= 2.0.0
  - selenium >= 4.0.0
  - webdriver-manager >= 4.0.0

## ⚠️ Disclaimer

Tool ini dibuat untuk tujuan edukasi dan penelitian. Pastikan Anda mematuhi:

- [Twitter/X Terms of Service](https://twitter.com/tos)
- [Twitter/X Developer Agreement](https://developer.twitter.com/en/developer-terms/agreement-and-policy)
- Kebijakan scraping dan rate limiting
- Privasi dan hak cipta pengguna lain

Penulis tidak bertanggung jawab atas penyalahgunaan tool ini.

## 📝 License

MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 💬 Support

Jika Anda menemukan bug atau memiliki saran, silakan buat [issue](https://github.com/yourusername/Scrapping-X/issues).

## 🙏 Acknowledgments

- Menggunakan [Selenium](https://www.selenium.dev/) untuk web scraping
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) untuk manajemen ChromeDriver otomatis
- [pandas](https://pandas.pydata.org/) untuk data processing

---

**Made with ❤️ for the data science community**
