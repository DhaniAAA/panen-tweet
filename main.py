import time
import pandas as pd
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import datetime
import tempfile
import shutil

# --- KONFIGURASI ---
# Auth token akan diminta saat program dijalankan
# JANGAN BAGIKAN auth_token ANDA KARENA BERSIFAT RAHASIA!
AUTH_TOKEN_COOKIE = None  # Akan diisi dari input user

# Waktu tunggu (dalam detik) antara setiap scroll agar halaman sempat memuat
SCROLL_PAUSE_TIME = 5 # Direkomendasikan untuk menaikkan jeda untuk scraping jangka panjang
# --------------------


def setup_driver():
    """Menyiapkan instance WebDriver untuk Chrome tanpa user-data-dir (agar kompatibel dengan Colab)."""
    print("Mencoba menyiapkan WebDriver...")
    chrome_options = Options()

    # Gunakan mode headless di Colab
    chrome_options.add_argument("--headless=new")  # Gunakan --headless=new agar lebih stabil
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver berhasil disiapkan.")
        return driver, None
    except (WebDriverException, ValueError) as e:
        print("Error saat menyiapkan WebDriver.")
        print(f"Detail error: {e}")
        return None, None


def scrape_tweets(driver, query, target_count, search_type):
    """
    Mengekstrak data tweet dari halaman pencarian untuk satu sesi.
    """
    # Membuat URL dasar
    search_url = f"https://x.com/search?q={query}&src=typed_query"
    # Menambahkan parameter jika pengguna memilih 'Terbaru' ('live')
    if search_type == 'latest':
        search_url += "&f=live"

    print(f"Mengunjungi halaman pencarian: {search_url}")
    driver.get(search_url)

    try:
        # Menunggu elemen tweet pertama muncul
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
        )
        print("Konten tweet terdeteksi. Memulai proses pengambilan data.")
    except TimeoutException:
        print("Batas waktu menunggu habis. Tidak ada tweet yang ditemukan untuk sesi ini.")
        print("Ini bisa terjadi jika tidak ada tweet pada rentang tanggal ini atau karena masalah jaringan.")
        return []

    # --- Scroll hingga target tercapai ---
    tweets_data = {}
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0

    while len(tweets_data) < target_count:
        print(f"\nTweet terkumpul sesi ini: {len(tweets_data)}/{target_count}. Melakukan scroll...")

        tweet_articles = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

        for tweet in tweet_articles:
            try:
                # Menggunakan URL sebagai ID unik untuk menghindari duplikasi
                tweet_url_elements = tweet.find_elements(By.XPATH, ".//a[contains(@href, '/status/')]")
                tweet_url = tweet_url_elements[0].get_attribute('href') if tweet_url_elements else None

                if tweet_url and tweet_url not in tweets_data:
                    username = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']//span").text
                    handle = tweet.find_element(By.XPATH, ".//span[contains(text(), '@')]").text
                    timestamp = tweet.find_element(By.XPATH, ".//time").get_attribute('datetime')
                    tweet_text = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text.replace('\n', ' ')
                    reply_count = tweet.find_element(By.XPATH, ".//button[@data-testid='reply']").text or "0"
                    retweet_count = tweet.find_element(By.XPATH, ".//button[@data-testid='retweet']").text or "0"
                    like_count = tweet.find_element(By.XPATH, ".//button[@data-testid='like']").text or "0"

                    tweets_data[tweet_url] = {
                        "username": username, "handle": handle, "timestamp": timestamp,
                        "tweet_text": tweet_text, "url": tweet_url, "reply_count": reply_count,
                        "retweet_count": retweet_count, "like_count": like_count
                    }
            except Exception:
                continue

        if len(tweets_data) >= target_count:
            print(f"Target {target_count} tweet untuk sesi ini telah tercapai.")
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
            print("Sudah mencapai akhir halaman untuk sesi ini...")
            if scroll_attempts > 3:
                print("Tidak ada tweet baru yang dimuat. Mengakhiri sesi ini.")
                break
        else:
            scroll_attempts = 0
        last_height = new_height

    return list(tweets_data.values())[:target_count]

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
    """Fungsi utama untuk menjalankan proses scraping secara berulang per interval tanggal."""
    print("="*60)
    print("       TWITTER/X SCRAPER - PANEN TWEET")
    print("="*60)
    print("\nPENTING: Anda memerlukan cookie 'auth_token' dari akun Twitter/X.")
    print("\nCara mendapatkan auth_token:")
    print("1. Login ke x.com di browser")
    print("2. Tekan F12 untuk membuka Developer Tools")
    print("3. Buka tab 'Application' atau 'Storage'")
    print("4. Di sidebar kiri, klik 'Cookies' > 'https://x.com'")
    print("5. Cari cookie dengan nama 'auth_token'")
    print("6. Salin nilai (value) dari cookie tersebut")
    print("\n⚠️  JANGAN BAGIKAN TOKEN INI KEPADA SIAPAPUN!")
    print("="*60)
    print()

    # Minta input auth token dari user
    global AUTH_TOKEN_COOKIE
    if not AUTH_TOKEN_COOKIE:
        AUTH_TOKEN_COOKIE = input("Masukkan auth_token Anda: ").strip()

    if not AUTH_TOKEN_COOKIE:
        print("\n❌ Error: auth_token tidak boleh kosong!")
        print("Silakan jalankan ulang program dan masukkan auth_token yang valid.")
        return

    (keyword, target_per_session, start_date, end_date,
     interval, lang, search_type) = get_user_input()

    driver, user_data_dir = setup_driver()
    if not driver:
        return

    try:
        # --- Login sekali saja di awal ---
        print("Mengunjungi x.com untuk menyuntikkan cookie login...")
        driver.get("https://x.com")
        time.sleep(2)
        if AUTH_TOKEN_COOKIE and AUTH_TOKEN_COOKIE != "Ganti dengan punya kalian":
            cookie = {'name': 'auth_token', 'value': AUTH_TOKEN_COOKIE, 'domain': '.x.com'}
            driver.add_cookie(cookie)
            print("Cookie berhasil disuntikkan.")
        else:
            print("PERINGATAN: Cookie tidak diatur. Script mungkin akan terhadang halaman login.")

        all_scraped_data = []
        current_date = start_date

        # --- Loop utama untuk scraping per interval ---
        while current_date <= end_date:
            chunk_end_date = current_date + datetime.timedelta(days=interval)

            since_str = current_date.strftime('%Y-%m-%d')
            until_str = chunk_end_date.strftime('%Y-%m-%d')

            print("\n" + "="*50)
            print(f"--- MEMULAI SESI UNTUK TANGGAL: {since_str} hingga {until_str} ---")
            print("="*50)

            search_query_raw = f"{keyword} lang:{lang} until:{until_str} since:{since_str}"
            search_query = quote(search_query_raw)

            session_data = scrape_tweets(driver, search_query, target_per_session, search_type)

            if session_data:
                all_scraped_data.extend(session_data)

            print(f"\nSesi untuk {since_str} - {until_str} selesai.")
            print(f"Total tweet terkumpul sejauh ini: {len(all_scraped_data)}")

            current_date = chunk_end_date

            if current_date <= end_date:
                print("Memberi jeda 10 detik sebelum sesi berikutnya...")
                time.sleep(10)

        # --- Proses setelah semua sesi selesai ---
        if not all_scraped_data:
            print("\nTidak ada data yang berhasil diambil dari seluruh sesi.")
            return

        print("\n--- SEMUA SESI SELESAI ---")
        print("Menggabungkan dan membersihkan data duplikat...")

        df = pd.DataFrame(all_scraped_data)
        df.drop_duplicates(subset=['url'], inplace=True, keep='first')

        safe_keyword = "".join(c for c in keyword if c.isalnum())
        output_filename = f"tweets_{safe_keyword}_{search_type}_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv"
        df.to_csv(output_filename, index=False, encoding='utf-8-sig')

        print(f"\n--- PROSES SELESAI ---")
        print(f"Data telah disimpan di file: {output_filename}")
        print(f"Total tweet unik yang berhasil diambil: {len(df)}")
        print("\nContoh data:")
        print(df.head())

    finally:
        if driver:
            print("\nMenutup browser...")
            driver.quit()
        # Membersihkan direktori sementara setelah driver ditutup
        if user_data_dir:
            print(f"Membersihkan direktori sementara: {user_data_dir}")
            shutil.rmtree(user_data_dir, ignore_errors=True)

    print("\nEksekusi skrip telah selesai. Program sekarang akan berhenti.")


if __name__ == "__main__":
    main()
