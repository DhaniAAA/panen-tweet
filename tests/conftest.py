import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock, patch
from panen_tweet import TwitterScraper


@pytest.fixture
def scraper():
    """Fixture untuk TwitterScraper instance"""
    return TwitterScraper(
        auth_token="test_token",
        scroll_pause_time=1,
        headless=True
    )


@pytest.fixture
def mock_driver():
    """Fixture untuk mock Selenium driver"""
    driver = MagicMock()
    
    mock_element = MagicMock()
    mock_element.text = "test_user"
    mock_element.get_attribute.return_value = "2024-01-01T00:00:00.000Z"
    
    mock_tweet = MagicMock()
    mock_tweet.find_element.return_value = mock_element
    mock_tweet.find_elements.return_value = []
    
    driver.find_elements.return_value = [mock_tweet]
    driver.execute_script.return_value = 1000
    
    return driver


@pytest.fixture
def sample_tweets_data():
    """Fixture untuk sample tweet data"""
    return [
        {
            "username": "user1",
            "handle": "@user1",
            "timestamp": "2024-01-01T00:00:00.000Z",
            "tweet_text": "Test tweet 1",
            "url": "https://x.com/user1/status/123",
            "reply_count": "5",
            "retweet_count": "10",
            "like_count": "50"
        },
        {
            "username": "user2",
            "handle": "@user2",
            "timestamp": "2024-01-02T00:00:00.000Z",
            "tweet_text": "Test tweet 2",
            "url": "https://x.com/user2/status/456",
            "reply_count": "3",
            "retweet_count": "7",
            "like_count": "25"
        }
    ]


@pytest.fixture
def sample_dataframe(sample_tweets_data):
    """Fixture untuk sample DataFrame"""
    return pd.DataFrame(sample_tweets_data)
