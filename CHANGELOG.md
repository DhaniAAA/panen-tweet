# Changelog

All notable changes to this project will be documented in this file.

## [1.1.1] - 2026-06-15

### Changed

- **Language Parameter**: Made the `lang` parameter optional in searches. Users can now search across all languages without being restricted to a default language.

## [1.1.0] - 2026-02-16

### Added

- **Auto-Resume**: Feature to resume scraping from the last scraped date if interrupted, preventing data duplication.
- **Media Downloader**: Option to automatically download images and video thumbnails from tweets.
- **Improved CLI**: A more interactive command-line interface with options for resume and media download.

### Fixed

- Fixed CSV saving logic to support _append_ mode (adding new data to an existing file).

## [1.0.5] - 2026-02-14

### Added

- First stable release on PyPI.
- Basic features for scraping based on query, date range, and tweet type (Top/Latest).
- Support for CSV output.
- Automated installation of Chrome Driver via `webdriver-manager`.
