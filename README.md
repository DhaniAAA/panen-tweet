# 🐦 Panen Tweet — Twitter/X Scraper

[![PyPI version](https://badge.fury.io/py/panen-tweet.svg)](https://pypi.org/project/panen-tweet/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Changelog](https://img.shields.io/badge/Changelog-v1.1.0-orange)](CHANGELOG.md)

**Panen Tweet** is a Python tool for scraping tweet data from Twitter/X based on keywords, date ranges, language, and tweet types. Suitable for research, data analysis, or thesis purposes.

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Getting Auth Token](#-getting-auth-token)
- [Usage](#-usage)
- [Output Format (CSV)](#-output-format-csv)
- [Complete Parameters](#️-complete-parameters)
- [Tips & Tricks](#-tips--tricks)
- [Troubleshooting](#-troubleshooting)
- [Disclaimer & Legal](#️-disclaimer--legal)

---

## ✅ Prerequisites

Before you start, make sure you have:

- **Python 3.7 or newer** → [Download here](https://www.python.org/downloads/)
- **Google Chrome** installed on your computer
- An active **Twitter/X** account

Check your Python version:

```bash
python --version
```

---

## Installation

### Method 1: From PyPI _(Recommended)_

```bash
pip install panen-tweet
```

### Method 2: From Source Code (GitHub)

```bash
git clone https://github.com/Dhaniaaa/panen-tweet.git
cd panen-tweet
pip install -e .
```

### Special: Google Colab or Linux Server (VPS)

On Google Colab and Linux servers, Google Chrome is not installed by default. Run these commands first:

```bash
# 1. Install the library
!pip install panen-tweet

# 2. Install Google Chrome (only needed once)
!panen-tweet install-chrome
```

---

## Getting Auth Token

> **What is an auth_token?**
> An auth token is a unique code that proves you are logged into Twitter/X. This tool needs this token to access tweet data.

### How to Get the Token (Step-by-Step):

1. **Open your browser** (Chrome or Firefox) and **log in** to [x.com](https://x.com)
2. Press **F12** to open Developer Tools
3. Click the **Application** tab (Chrome) or **Storage** tab (Firefox)
4. In the left panel, click **Cookies** → select **`https://x.com`**
5. Find the row named **`auth_token`**
6. **Click the row**, then **copy the value** in the right column

> 🖼️ The token looks like a long string of characters, example: `1a2b3c4d5e6f7a8b9c0d...`

### TOKEN SECURITY — MUST READ!

This token is the **full access key to your Twitter/X account**.

- ❌ **DO NOT** share the token with anyone
- ❌ **DO NOT** hardcode the token directly in your Python file
- ❌ **DO NOT** commit/push files containing the token to GitHub
- ✅ Store the token in a `.env` file (see the guide in [SECURITY.md](SECURITY.md))
- ✅ If the token is leaked, immediately **change your Twitter/X password**

---

## Usage

There are 3 ways to use Panen Tweet. Choose the one that best suits your needs.

---

### Method 1: Command Line Interface (CLI) — Easiest for Beginners

After installation, simply run:

```bash
panen-tweet
```

The program will guide you interactively. You will be asked to enter:

| No. | Question | Example Input |
| --- | --- | --- |
| 1 | Auth token | _(paste token from browser)_ |
| 2 | Search keyword/topic | `jakarta flood` |
| 3 | Max tweets per session | `100` |
| 4 | Start date | `2024-01-01` |
| 5 | End date | `2024-01-07` |
| 6 | Interval days per session | `1` _(1 = per day)_ |
| 7 | Language code | `id` _(Indonesian)_, `en` _(English)_, or leave blank for all |
| 8 | Tweet type | `1` _(Top)_ or `2` _(Latest)_ |

**Example terminal output:**

```
TWITTER/X SCRAPER - PANEN TWEET
================================
Enter your auth_token: <paste_token_here>

1. Enter search keyword/topic: jakarta flood
2. How many MAXIMUM tweets to scrape PER SESSION? 100
3. Enter overall START DATE (YYYY-MM-DD): 2024-01-01
4. Enter overall END DATE (YYYY-MM-DD): 2024-01-07
5. How many interval days per session? (1 = per day): 1
6. Enter language code (id / en / ja / etc, or leave blank): en
7. Select tweet type (1 for Top, 2 for Latest): 2
```

**The scraped results** will be automatically saved to a CSV file, example:
`tweets_jakartaflood_latest_20240101-20240107.csv`

---

### Method 2: As a Python Library

Suitable if you want to integrate it into your own notebook or script.

```python
from panen_tweet import TwitterScraper
import datetime
import os

# ✅ Safe way: read token from environment variable
# Run this in terminal first: export TWITTER_AUTH_TOKEN="yourtoken"
auth_token = os.getenv('TWITTER_AUTH_TOKEN')

if not auth_token:
    raise ValueError("Token is not set! See SECURITY.md for instructions.")

# Initialize scraper
scraper = TwitterScraper(
    auth_token=auth_token,
    scroll_pause_time=5,  # Pause between scrolls (seconds) - increase if connection is slow
    headless=True         # True = without browser GUI | False = show browser
)

# Run scraping
df = scraper.scrape_with_date_range(
    keyword="jakarta flood",
    target_per_session=100,
    start_date=datetime.datetime(2024, 1, 1),
    end_date=datetime.datetime(2024, 1, 7),
    interval_days=1,
    lang=None,            # Use language code like 'en' or 'id', or None for all languages
    search_type='latest'  # 'top' or 'latest'
)

# Save to CSV
if df is not None:
    scraper.save_to_csv(df, "scraping_results.csv")
    print(f"✅ Successfully scraped {len(df)} tweets!")
    print(df.head())
else:
    print("❌ No data was successfully scraped.")
```

---

### Method 3: Using a `.env` File for Token Security

This method is **the safest** to store the token without the risk of uploading it to GitHub.

**Step 1** — Install `python-dotenv`:

```bash
pip install python-dotenv
```

**Step 2** — Create a `.env` file in your project folder:

```
TWITTER_AUTH_TOKEN=your_token_here
```

**Step 3** — Load it in your Python code:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Read the .env file
auth_token = os.getenv('TWITTER_AUTH_TOKEN')
```

> The `.env` file is automatically included in `.gitignore`, so it **will not be uploaded to GitHub**.

Or if you prefer to use the terminal directly without a `.env` file:

**Windows PowerShell:**

```powershell
$env:TWITTER_AUTH_TOKEN = "your_token_here"
panen-tweet
```

**Linux / Mac:**

```bash
export TWITTER_AUTH_TOKEN="your_token_here"
panen-tweet
```

---

## Output Format (CSV)

Scraping results are automatically saved in CSV format with the following columns:

| Column | Description |
| --- | --- |
| `username` | Display name of the user |
| `handle` | Twitter account name (`@username`) |
| `timestamp` | Time the tweet was posted (ISO 8601 format) |
| `tweet_text` | Text content of the tweet |
| `url` | Direct link to the tweet |
| `reply_count` | Number of replies |
| `retweet_count` | Number of retweets |
| `like_count` | Number of likes |

**Example CSV content:**

```csv
username,handle,timestamp,tweet_text,url,reply_count,retweet_count,like_count
Budi Santoso,@budisant,2024-01-01T10:30:00.000Z,"Severe flood in Jakarta!",https://x.com/budisant/status/123,5,10,25
```

---

## Complete Parameters

### `TwitterScraper()`

```python
TwitterScraper(
    auth_token=None,        # (REQUIRED) Token from browser cookie
    scroll_pause_time=5,    # Pause between scrolls, in seconds (default: 5)
    headless=True           # True = without browser GUI | False = show browser
)
```

### `scrape_with_date_range()`

```python
scraper.scrape_with_date_range(
    keyword="",             # (REQUIRED) Search keyword
    target_per_session=100, # Target number of tweets per session (default: 100)
    start_date=datetime,    # (REQUIRED) Start date, format: datetime(YYYY, M, D)
    end_date=datetime,      # (REQUIRED) End date, format: datetime(YYYY, M, D)
    interval_days=1,        # Interval days per session (1 = scraping per day)
    lang=None,              # Language code: 'en', 'id', 'ja', 'es', etc. None for all.
    search_type='top'       # 'top' = top tweets | 'latest' = latest tweets
)
```

---

## Tips & Tricks

### Collecting Many Tweets

- Use `interval_days=1` to scrape per day for more detailed results
- Do not set `target_per_session` too high (recommended 50–200)
- Increase `scroll_pause_time` to allow more loading time if your connection is slow

### Avoiding Rate Limits

Rate limits mean Twitter/X restricts access because scraping is too fast.

- Use a `scroll_pause_time` of at least 5 seconds
- Do not run more than one scraping process simultaneously
- Add a pause of a few minutes between large sessions

### Available Language Codes

| Code | Language |
| --- | --- |
| `id` | Indonesian |
| `en` | English |
| `ja` | Japanese |
| `es` | Spanish |
| `fr` | French |
| `ko` | Korean |

---

## Troubleshooting

### ❌ Error: `WebDriver not found`

Chrome is not detected or ChromeDriver does not match.

**Solution:**

- Make sure Google Chrome is installed
- The package will automatically download the appropriate ChromeDriver

---

### ❌ Error: `Auth token invalid`

The token you entered is invalid or expired.

**Solution:**

1. Reopen [x.com](https://x.com) in your browser
2. Log in again if necessary
3. Retrieve the `auth_token` value again from the Developer Tools → Cookies tab
4. Make sure there are no trailing spaces when copying and pasting

---

### ❌ Error: `No tweets found`

No tweets were found for the parameters you entered.

**Solution:**

- Check your internet connection
- Try more common/popular keywords
- Check the date range — there might genuinely be no tweets in that period
- Ensure the auth_token is still valid

---

### Browser does not appear

This is **normal** — the default mode is `headless=True` (without browser GUI).

If you want to see the scraping process visually:

```python
scraper = TwitterScraper(auth_token=token, headless=False)
```

---

## Requirements

- **Python** 3.7+
- **Google Chrome** (latest version)
- **Dependencies** (automatically installed with the package):
  - `pandas >= 2.0.0`
  - `selenium >= 4.0.0`
  - `webdriver-manager >= 4.0.0`

---

## Disclaimer & Legal

This tool was created for **educational and scientific research purposes**.

By using this tool, you agree to comply with:

- [Twitter/X Terms of Service](https://twitter.com/tos)
- [Twitter/X Developer Agreement](https://developer.twitter.com/en/developer-terms/agreement-and-policy)
- Platform rate limiting rules and robots.txt
- Privacy rights and copyrights of other users

**The developer is not responsible** for any misuse of this tool.

---

## Contributing

Contributions are very welcome! How to contribute:

1. Fork this repository
2. Create a new branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add a new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Create a Pull Request

---

## License

MIT License — see the [LICENSE](LICENSE) file for full details.

---

## Support & Contact

- **Report Bugs**: [GitHub Issues](https://github.com/Dhaniaaa/panen-tweet/issues)
- **PyPI Package**: [pypi.org/project/panen-tweet](https://pypi.org/project/panen-tweet/)
- **Email**: ramadhanigb19@gmail.com

---

## Special Thanks To

- [Selenium](https://www.selenium.dev/) — Web automation framework
- [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager) — Automatic ChromeDriver management
- [pandas](https://pandas.pydata.org/) — Data processing

---

**Made with ❤️ for the data science & research community**

⭐ If this project is helpful, give it a star on GitHub!
