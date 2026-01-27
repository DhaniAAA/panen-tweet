"""
Command Line Interface untuk Scrape-X
"""
import datetime
from scrape_x.core import TwitterScraper


def get_user_input():
    """Meminta input dari pengguna untuk parameter pencarian."""
    keyword = input("1. Masukkan kata kunci/topik pencarian: ")

    while True:
        try:
            target_count = int(input("2. Berapa jumlah MAKSIMAL tweet yang ingin diambil PER SESI? "))
            if target_count > 0:
                break
            else:
                print("Jumlah harus lebih dari 0.")
        except ValueError:
            print("Input tidak valid, masukkan angka.")

    while True:
        start_date_str = input("3. Masukkan TANGGAL MULAI KESELURUHAN (YYYY-MM-DD): ")
        try:
            start_date_obj = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
            break
        except ValueError:
            print("Format tanggal salah. Gunakan format YYYY-MM-DD.")

    while True:
        end_date_str = input("4. Masukkan TANGGAL SELESAI KESELURUHAN (YYYY-MM-DD): ")
        try:
            end_date_obj = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
            if end_date_obj >= start_date_obj:
                break
            else:
                print("Tanggal selesai harus sama atau setelah tanggal mulai.")
        except ValueError:
            print("Format tanggal salah. Gunakan format YYYY-MM-DD.")

    while True:
        try:
            interval_days = int(input("5. Berapa hari interval per sesi scraping? (misal: 1 untuk per hari): "))
            if interval_days > 0:
                break
            else:
                print("Interval harus lebih dari 0.")
        except ValueError:
            print("Input tidak valid, masukkan angka.")

    lang = input("6. Masukkan kode bahasa (misal: 'id' untuk Indonesia, 'en' untuk Inggris): ")

    while True:
        choice = input("7. Pilih jenis tweet (1 untuk Top, 2 untuk Terbaru): ")
        if choice == '1':
            search_type = 'top'
            break
        elif choice == '2':
            search_type = 'latest'
            break
        else:
            print("Input tidak valid. Masukkan 1 atau 2.")

    return keyword, target_count, start_date_obj, end_date_obj, interval_days, lang, search_type


def main():
    """Fungsi utama untuk CLI"""
    print("="*60)
    print("       SCRAPE-X - Twitter/X Scraping Tool")
    print("="*60)
    print()

    # Minta auth token
    print("PENTING: Anda memerlukan cookie 'auth_token' dari akun Twitter/X Anda.")
    print("Cara mendapatkan:")
    print("1. Login ke x.com")
    print("2. Buka Developer Tools (F12)")
    print("3. Pergi ke tab Application/Storage > Cookies")
    print("4. Salin nilai dari cookie 'auth_token'")
    print()

    auth_token = input("Masukkan auth_token Anda: ").strip()

    if not auth_token or auth_token == "cookie kalian":
        print("Error: auth_token tidak valid!")
        return

    print("\n" + "="*60)
    print("       KONFIGURASI SCRAPING")
    print("="*60 + "\n")

    (keyword, target_per_session, start_date, end_date,
     interval, lang, search_type) = get_user_input()

    # Inisialisasi scraper
    scraper = TwitterScraper(auth_token=auth_token, scroll_pause_time=5, headless=True)

    # Jalankan scraping
    df = scraper.scrape_with_date_range(
        keyword=keyword,
        target_per_session=target_per_session,
        start_date=start_date,
        end_date=end_date,
        interval_days=interval,
        lang=lang,
        search_type=search_type
    )

    if df is not None:
        # Generate filename
        safe_keyword = "".join(c for c in keyword if c.isalnum())
        output_filename = f"tweets_{safe_keyword}_{search_type}_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv"

        # Simpan ke CSV
        scraper.save_to_csv(df, output_filename)

        print("\n--- PROSES SELESAI ---")
        print(f"Total tweet unik yang berhasil diambil: {len(df)}")
        print("\nContoh data:")
        print(df.head())

    print("\nEksekusi skrip telah selesai. Program sekarang akan berhenti.")


if __name__ == "__main__":
    main()
