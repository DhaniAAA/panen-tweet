import pytest
import os
import pandas as pd
from unittest.mock import MagicMock, patch, mock_open
from panen_tweet import TwitterScraper
import datetime

class TestNewFeatures:

    @patch('panen_tweet.core.requests.get')
    def test_download_media_success(self, mock_get, tmp_path):
        scraper = TwitterScraper()
        output_folder = tmp_path / "media"

        # Mock requests response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"chunk1", b"chunk2"]
        mock_get.return_value = mock_response

        url = "http://example.com/image.jpg"
        result = scraper.download_media(url, str(output_folder))

        assert result is not None
        assert os.path.exists(result)
        with open(result, 'rb') as f:
            assert f.read() == b"chunk1chunk2"

    def test_auto_resume(self, tmp_path):
        scraper = TwitterScraper()

        # Create existing CSV
        csv_file = tmp_path / "scraped.csv"
        df = pd.DataFrame({
            'timestamp': ['2024-01-01', '2024-01-02'],
            'url': ['url1', 'url2']
        })
        df.to_csv(csv_file, index=False)

        # Mock setup_driver and login and scrape_tweets
        with patch.object(scraper, 'setup_driver', return_value=True), \
             patch.object(scraper, 'login', return_value=True), \
             patch.object(scraper, 'scrape_tweets', return_value=[]) as mock_scrape, \
             patch.object(scraper, 'quit'):

             start_date = datetime.datetime(2024, 1, 1)
             end_date = datetime.datetime(2024, 1, 4)

             scraper.scrape_with_date_range(
                 keyword="test",
                 target_per_session=10,
                 start_date=start_date,
                 end_date=end_date,
                 interval_days=1,
                 resume=True,
                 output_filename=str(csv_file)
             )

             # Expected:
             # Last date in CSV is 2024-01-02.
             # Resume should start from 2024-01-03.

             args_list = mock_scrape.call_args_list
             # Check if scrape_tweets was NOT called for 2024-01-01
             found_jan_01 = any("since%3A2024-01-01" in str(call) for call in args_list)
             found_jan_03 = any("since%3A2024-01-03" in str(call) for call in args_list)

             assert found_jan_01 is False, "Should have skipped 2024-01-01"
             assert found_jan_03 is True, "Should have resumed at 2024-01-03"

    @patch('panen_tweet.core.requests.get')
    def test_scrape_with_media_download(self, mock_get, tmp_path):
        scraper = TwitterScraper()
        media_dir = tmp_path / "media_test"

        # Mock data return with media_urls
        mock_data = [{
            "url": "tweet1",
            "media_urls": ["http://example.com/img1.jpg"]
        }]

         # Mock requests response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b"img"]
        mock_get.return_value = mock_response

        with patch.object(scraper, 'setup_driver', return_value=True), \
             patch.object(scraper, 'login', return_value=True), \
             patch.object(scraper, 'scrape_tweets', return_value=mock_data), \
             patch.object(scraper, 'quit'):

            scraper.scrape_with_date_range(
                keyword="test",
                target_per_session=1,
                start_date=datetime.datetime(2024, 1, 1),
                end_date=datetime.datetime(2024, 1, 1),
                interval_days=1,
                download_media=True,
                media_dir=str(media_dir)
            )

            # Check if file downloaded
            assert os.path.exists(media_dir)
            files = os.listdir(media_dir)
            assert len(files) > 0
            assert "img1.jpg" in files[0]
