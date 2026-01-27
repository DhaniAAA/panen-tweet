"""
Contoh penggunaan Scrape-X sebagai library Python
"""

from scrape_x import TwitterScraper
import datetime

def example_basic():
    """Contoh penggunaan basic"""
    print("="*60)
    print("CONTOH PENGGUNAAN BASIC")
    print("="*60)

    # GANTI dengan auth_token Anda
    # JANGAN PERNAH commit auth_token asli ke Git!
    # Gunakan environment variable atau file config terpisah
    import os
    AUTH_TOKEN = os.getenv('TWITTER_AUTH_TOKEN', 'your_auth_token_here')

    # Inisialisasi scraper
    scraper = TwitterScraper(
        auth_token=AUTH_TOKEN,
        scroll_pause_time=5,
        headless=True  # Set False jika ingin melihat browser
    )

    # Scraping dengan rentang tanggal
    df = scraper.scrape_with_date_range(
        keyword="python programming",
        target_per_session=50,  # 50 tweets per sesi
        start_date=datetime.datetime(2024, 1, 1),
        end_date=datetime.datetime(2024, 1, 3),
        interval_days=1,  # Scraping per hari
        lang='en',
        search_type='latest'
    )

    # Simpan hasil
    if df is not None:
        scraper.save_to_csv(df, "tweets_python_basic.csv")
        print(f"\n✅ Berhasil mengambil {len(df)} tweets!")
        print("\nContoh data:")
        print(df[['username', 'tweet_text', 'like_count']].head())
    else:
        print("\n❌ Tidak ada data yang berhasil diambil")


# def example_advanced():
#     """Contoh penggunaan advanced dengan kontrol manual"""
#     print("\n" + "="*60)
#     print("CONTOH PENGGUNAAN ADVANCED")
#     print("="*60)

#     import os
    # AUTH_TOKEN = os.getenv('TWITTER_AUTH_TOKEN', 'your_auth_token_here')

    # # Inisialisasi scraper
    # scraper = TwitterScraper(
    #     auth_token=AUTH_TOKEN,
    #     scroll_pause_time=5,
    #     headless=True  # Set False jika ingin melihat browser
    # )

#     # Setup driver manual
#     if scraper.setup_driver():
#         scraper.login()

#         # Scraping manual dengan query custom
#         from urllib.parse import quote
#         query = quote("machine learning lang:en")

#         tweets = scraper.scrape_tweets(
#             query=query,
#             target_count=30,
#             search_type='top'
#         )

#         print(f"\n✅ Ditemukan {len(tweets)} tweets")

#         # Konversi ke DataFrame untuk processing lebih lanjut
#         import pandas as pd
#         df = pd.DataFrame(tweets)

#         if not df.empty:
#             # Analisis sederhana
#             print("\nStatistik:")
#             print(f"- Total tweets: {len(df)}")
#             print(f"- User unik: {df['username'].nunique()}")
#             print(f"- Rata-rata likes: {df['like_count'].apply(lambda x: int(x) if x.isdigit() else 0).mean():.2f}")

#             # Simpan
#             scraper.save_to_csv(df, "tweets_ml_advanced.csv")

#         # Cleanup
#         scraper.quit()


# def example_multiple_keywords():
#     """Contoh scraping multiple keywords"""
#     print("\n" + "="*60)
#     print("CONTOH SCRAPING MULTIPLE KEYWORDS")
#     print("="*60)

#     import os
    # AUTH_TOKEN = os.getenv('TWITTER_AUTH_TOKEN', 'your_auth_token_here')

    # # Inisialisasi scraper
    # scraper = TwitterScraper(
    #     auth_token=AUTH_TOKEN,
    #     scroll_pause_time=5,
    #     headless=True  # Set False jika ingin melihat browser
    # )

#     all_data = []

#     for keyword in keywords:
#         print(f"\n🔍 Scraping keyword: {keyword}")

#         df = scraper.scrape_with_date_range(
#             keyword=keyword,
#             target_per_session=20,
#             start_date=datetime.datetime(2024, 1, 1),
#             end_date=datetime.datetime(2024, 1, 2),
#             interval_days=1,
#             lang='en',
#             search_type='latest'
#         )

#         if df is not None:
#             df['search_keyword'] = keyword  # Tambah kolom untuk tracking
#             all_data.append(df)

#     # Gabungkan semua hasil
#     if all_data:
#         import pandas as pd
#         combined_df = pd.concat(all_data, ignore_index=True)
#         combined_df.drop_duplicates(subset=['url'], inplace=True)

#         scraper.save_to_csv(combined_df, "tweets_multiple_keywords.csv")
#         print(f"\n✅ Total {len(combined_df)} tweets unik dari {len(keywords)} keywords")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║           SCRAPE-X - Contoh Penggunaan                  ║
    ╚══════════════════════════════════════════════════════════╝

    PENTING:
    1. Ganti 'your_auth_token_here' dengan auth_token Anda
    2. Cara mendapatkan auth_token:
       - Login ke x.com
       - Buka Developer Tools (F12)
       - Application > Cookies > x.com
       - Salin nilai 'auth_token'

    Pilih contoh yang ingin dijalankan:
    1. Basic Usage
    2. Advanced Usage
    3. Multiple Keywords

    Atau edit file ini dan uncomment fungsi yang ingin dijalankan.
    """)

    # Uncomment salah satu untuk menjalankan:
    # example_basic()
    # example_advanced()
    # example_multiple_keywords()

    print("\n⚠️  Silakan edit file ini dan uncomment contoh yang ingin dijalankan!")
