import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock, patch, mock_open
from panen_tweet import TwitterScraper


class TestTwitterScraper:
    """Test suite untuk TwitterScraper class"""

    def test_init_default_values(self):
        """Test inisialisasi dengan nilai default"""
        scraper = TwitterScraper()
        
        assert scraper.auth_token is None
        assert scraper.scroll_pause_time == 5
        assert scraper.headless is True
        assert scraper.chrome_binary_path is None
        assert scraper.driver is None

    def test_init_custom_values(self):
        """Test inisialisasi dengan nilai kustom"""
        scraper = TwitterScraper(
            auth_token="custom_token",
            scroll_pause_time=3,
            headless=False,
            chrome_binary_path="/usr/bin/chrome"
        )
        
        assert scraper.auth_token == "custom_token"
        assert scraper.scroll_pause_time == 3
        assert scraper.headless is False
        assert scraper.chrome_binary_path == "/usr/bin/chrome"

    def test_quit_with_no_driver(self):
        """Test quit() ketika driver belum diinisialisasi"""
        scraper = TwitterScraper()
        scraper.quit()

    def test_quit_with_driver(self, scraper, mock_driver):
        """Test quit() ketika driver ada"""
        scraper.driver = mock_driver
        scraper.quit()
        mock_driver.quit.assert_called_once()

    @patch('panen_tweet.core.webdriver.Chrome')
    @patch('panen_tweet.core.ChromeDriverManager')
    def test_setup_driver_success(self, mock_driver_manager, mock_chrome, scraper):
        """Test setup_driver() berhasil"""
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_chrome_instance = MagicMock()
        mock_chrome.return_value = mock_chrome_instance
        
        result = scraper.setup_driver()
        
        assert result is True
        assert scraper.driver is not None
        mock_chrome.assert_called_once()

    @patch('panen_tweet.core.webdriver.Chrome')
    @patch('panen_tweet.core.ChromeDriverManager')
    def test_setup_driver_failure(self, mock_driver_manager, mock_chrome, scraper):
        """Test setup_driver() gagal"""
        mock_driver_manager.side_effect = Exception("Chrome not found")
        
        result = scraper.setup_driver()
        
        assert result is False

    def test_login_without_token(self, scraper, mock_driver):
        """Test login() tanpa token"""
        scraper.driver = mock_driver
        scraper.auth_token = None
        
        result = scraper.login()
        
        assert result is False

    def test_login_with_token(self, scraper, mock_driver):
        """Test login() dengan token"""
        scraper.driver = mock_driver
        scraper.auth_token = "test_auth_token"
        
        result = scraper.login()
        
        assert result is True
        mock_driver.add_cookie.assert_called_once()

    def test_scrape_tweets_returns_list(self, scraper, mock_driver):
        """Test scrape_tweets() mengembalikan list"""
        scraper.driver = mock_driver
        
        mock_tweet = MagicMock()
        mock_tweet.find_element.return_value.text = "test"
        mock_tweet.find_element.return_value.get_attribute.return_value = "2024-01-01T00:00:00.000Z"
        mock_tweet.find_elements.return_value = [
            MagicMock(get_attribute=MagicMock(return_value="https://x.com/user/status/123"))
        ]
        mock_driver.find_elements.return_value = [mock_tweet]
        
        result = scraper.scrape_tweets("test query", 1, "top")
        
        assert isinstance(result, list)

    def test_save_to_csv(self, scraper, sample_dataframe, tmp_path):
        """Test save_to_csv() menyimpan file dengan benar"""
        output_file = tmp_path / "test_output.csv"
        
        scraper.save_to_csv(sample_dataframe, str(output_file))
        
        assert output_file.exists()
        
        df_read = pd.read_csv(output_file)
        assert len(df_read) == 2
        assert "username" in df_read.columns


class TestScrapeWithDateRange:
    """Test suite untuk scrape_with_date_range"""

    @patch.object(TwitterScraper, 'setup_driver')
    @patch.object(TwitterScraper, 'quit')
    def test_scrape_with_date_range_no_driver(self, mock_quit, mock_setup, scraper):
        """Test scrape_with_date_range() ketika driver gagal di-setup"""
        mock_setup.return_value = False
        
        import datetime
        result = scraper.scrape_with_date_range(
            keyword="test",
            target_per_session=10,
            start_date=datetime.datetime(2024, 1, 1),
            end_date=datetime.datetime(2024, 1, 7),
            interval_days=7
        )
        
        assert result is None

    @patch('panen_tweet.core.webdriver.Chrome')
    @patch('panen_tweet.core.ChromeDriverManager')
    @patch.object(TwitterScraper, 'login')
    @patch.object(TwitterScraper, 'scrape_tweets')
    @patch.object(TwitterScraper, 'quit')
    def test_scrape_with_date_range_success(
        self, mock_quit, mock_scrape, mock_login, mock_chrome_mgr, mock_chrome, scraper
    ):
        """Test scrape_with_date_range() berhasil"""
        import datetime
        
        mock_chrome_mgr.return_value.install.return_value = "/path/to/chromedriver"
        mock_chrome_instance = MagicMock()
        mock_chrome.return_value = mock_chrome_instance
        scraper.driver = mock_chrome_instance
        
        mock_scrape.return_value = [
            {
                "username": "test_user",
                "handle": "@test",
                "timestamp": "2024-01-01",
                "tweet_text": "test",
                "url": "https://x.com/test/status/1",
                "reply_count": "0",
                "retweet_count": "0",
                "like_count": "0"
            }
        ]
        
        result = scraper.scrape_with_date_range(
            keyword="test",
            target_per_session=10,
            start_date=datetime.datetime(2024, 1, 1),
            end_date=datetime.datetime(2024, 1, 2),
            interval_days=1
        )
        
        assert result is not None
        assert isinstance(result, pd.DataFrame)


class TestUtilities:
    """Test untuk utility functions"""

    def test_url_encoding(self):
        """Test URL encoding untuk query"""
        from urllib.parse import quote
        
        query = "test query lang:id"
        encoded = quote(query)
        
        assert "%20" in encoded or " " not in encoded

    def test_date_format(self):
        """Test format tanggal"""
        import datetime
        
        date = datetime.datetime(2024, 1, 15)
        formatted = date.strftime('%Y-%m-%d')
        
        assert formatted == "2024-01-15"
