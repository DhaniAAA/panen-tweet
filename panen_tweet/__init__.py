"""
Scrape-X: Powerful Twitter/X Scraping Tool
===========================================

Package untuk scraping Twitter/X menggunakan Selenium dengan fitur:
- Scraping berdasarkan kata kunci
- Filter berdasarkan tanggal dan bahasa
- Support untuk tweet teratas atau terbaru
- Export ke CSV

Contoh penggunaan:
    from panen_tweet import TwitterScraper

    scraper = TwitterScraper(auth_token="your_auth_token_here")
    df = scraper.scrape_with_date_range(
        keyword="python",
        target_per_session=100,
        start_date=datetime.datetime(2024, 1, 1),
        end_date=datetime.datetime(2024, 1, 7),
        interval_days=1,
        lang='en',
        search_type='latest'
    )

    if df is not None:
        scraper.save_to_csv(df, "tweets.csv")
"""

__version__ = '1.0.5'
__author__ = 'Ramadhani'
__all__ = ['TwitterScraper']

from panen_tweet.core import TwitterScraper
