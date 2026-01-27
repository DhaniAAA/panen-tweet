"""
Core functionality untuk scraping Twitter/X
"""
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


class TwitterScraper:
    """Kelas utama untuk scraping Twitter/X"""

    def __init__(self, auth_token=None, scroll_pause_time=5, headless=True):
        """
        Inisialisasi TwitterScraper

        Args:
            auth_token (str): Cookie auth_token untuk login
            scroll_pause_time (int): Waktu jeda antara scroll (dalam detik)
            headless (bool): Jalankan browser dalam mode headless
        """
        self.auth_token = auth_token
        self.scroll_pause_time = scroll_pause_time
        self.headless = headless
        self.driver = None
        self.user_data_dir = None

    def setup_driver(self):
        """Menyiapkan instance WebDriver untuk Chrome"""
        print("Mencoba menyiapkan WebDriver...")
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("WebDriver berhasil disiapkan.")
            return True
        except (WebDriverException, ValueError) as e:
            print("Error saat menyiapkan WebDriver.")
            print(f"Detail error: {e}")
            return False

    def login(self):
        """Login menggunakan cookie auth_token"""
        if not self.auth_token or self.auth_token == "cookie kalian":
            print("PERINGATAN: Cookie tidak diatur. Script mungkin akan terhadang halaman login.")
            return False

        print("Mengunjungi x.com untuk menyuntikkan cookie login...")
        self.driver.get("https://x.com")
        time.sleep(2)

        cookie = {'name': 'auth_token', 'value': self.auth_token, 'domain': '.x.com'}
        self.driver.add_cookie(cookie)
        print("Cookie berhasil disuntikkan.")
        return True

    def scrape_tweets(self, query, target_count, search_type='top'):
        """
        Mengekstrak data tweet dari halaman pencarian

        Args:
            query (str): Query pencarian yang sudah di-encode
            target_count (int): Jumlah target tweet yang ingin diambil
            search_type (str): 'top' untuk tweet teratas, 'latest' untuk terbaru

        Returns:
            list: List dictionary berisi data tweet
        """
        # Membuat URL dasar
        search_url = f"https://x.com/search?q={query}&src=typed_query"
        if search_type == 'latest':
            search_url += "&f=live"

        print(f"Mengunjungi halaman pencarian: {search_url}")
        self.driver.get(search_url)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//article[@data-testid='tweet']"))
            )
            print("Konten tweet terdeteksi. Memulai proses pengambilan data.")
        except TimeoutException:
            print("Batas waktu menunggu habis. Tidak ada tweet yang ditemukan untuk sesi ini.")
            print("Ini bisa terjadi jika tidak ada tweet pada rentang tanggal ini atau karena masalah jaringan.")
            return []

        # Scroll hingga target tercapai
        tweets_data = {}
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0

        while len(tweets_data) < target_count:
            print(f"\nTweet terkumpul sesi ini: {len(tweets_data)}/{target_count}. Melakukan scroll...")

            tweet_articles = self.driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")

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
                            "username": username,
                            "handle": handle,
                            "timestamp": timestamp,
                            "tweet_text": tweet_text,
                            "url": tweet_url,
                            "reply_count": reply_count,
                            "retweet_count": retweet_count,
                            "like_count": like_count
                        }
                except Exception:
                    continue

            if len(tweets_data) >= target_count:
                print(f"Target {target_count} tweet untuk sesi ini telah tercapai.")
                break

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.scroll_pause_time)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
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

    def scrape_with_date_range(self, keyword, target_per_session, start_date, end_date,
                                interval_days, lang='id', search_type='top'):
        """
        Scraping tweet dengan rentang tanggal dan interval

        Args:
            keyword (str): Kata kunci pencarian
            target_per_session (int): Jumlah target tweet per sesi
            start_date (datetime): Tanggal mulai
            end_date (datetime): Tanggal selesai
            interval_days (int): Interval hari per sesi
            lang (str): Kode bahasa (misal: 'id', 'en')
            search_type (str): 'top' atau 'latest'

        Returns:
            pd.DataFrame: DataFrame berisi semua tweet yang berhasil diambil
        """
        if not self.setup_driver():
            return None

        try:
            self.login()

            all_scraped_data = []
            current_date = start_date

            # Loop utama untuk scraping per interval
            while current_date <= end_date:
                chunk_end_date = current_date + datetime.timedelta(days=interval_days)

                since_str = current_date.strftime('%Y-%m-%d')
                until_str = chunk_end_date.strftime('%Y-%m-%d')

                print("\n" + "="*50)
                print(f"--- MEMULAI SESI UNTUK TANGGAL: {since_str} hingga {until_str} ---")
                print("="*50)

                search_query_raw = f"{keyword} lang:{lang} until:{until_str} since:{since_str}"
                search_query = quote(search_query_raw)

                session_data = self.scrape_tweets(search_query, target_per_session, search_type)

                if session_data:
                    all_scraped_data.extend(session_data)

                print(f"\nSesi untuk {since_str} - {until_str} selesai.")
                print(f"Total tweet terkumpul sejauh ini: {len(all_scraped_data)}")

                current_date = chunk_end_date

                if current_date <= end_date:
                    print("Memberi jeda 10 detik sebelum sesi berikutnya...")
                    time.sleep(10)

            # Proses setelah semua sesi selesai
            if not all_scraped_data:
                print("\nTidak ada data yang berhasil diambil dari seluruh sesi.")
                return None

            print("\n--- SEMUA SESI SELESAI ---")
            print("Menggabungkan dan membersihkan data duplikat...")

            df = pd.DataFrame(all_scraped_data)
            df.drop_duplicates(subset=['url'], inplace=True, keep='first')

            print(f"Total tweet unik yang berhasil diambil: {len(df)}")
            return df

        finally:
            self.quit()

    def quit(self):
        """Tutup browser dan bersihkan resource"""
        if self.driver:
            print("\nMenutup browser...")
            self.driver.quit()
        if self.user_data_dir:
            print(f"Membersihkan direktori sementara: {self.user_data_dir}")
            shutil.rmtree(self.user_data_dir, ignore_errors=True)

    def save_to_csv(self, df, filename):
        """
        Simpan DataFrame ke file CSV

        Args:
            df (pd.DataFrame): DataFrame yang akan disimpan
            filename (str): Nama file output
        """
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nData telah disimpan di file: {filename}")
