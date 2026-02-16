# Changelog

Semua perubahan penting pada project ini akan didokumentasikan di file ini.

## [1.1.0] - 2026-02-16

### Added

- **Auto-Resume**: Fitur untuk melanjutkan scraping dari tanggal terakhir jika terputus, tanpa duplikasi data.
- **Media Downloader**: Opsi untuk mendownload gambar dan video thumbnail dari tweet secara otomatis.
- **Improved CLI**: Antarmuka command-line yang lebih interaktif dengan opsi resume dan media download.

### Fixed

- Perbaikan logika penyimpanan file CSV untuk mendukung mode _append_ (menambahkan data baru ke file lama).

## [1.0.5] - 2026-02-14

### Added

- Rilis stabil pertama di PyPI.
- Fitur dasar scraping berdasarkan query, rentang tanggal, dan jenis tweet (Top/Latest).
- Dukungan untuk output CSV.
- Otomatisasi instalasi Chrome Driver via `webdriver-manager`.
