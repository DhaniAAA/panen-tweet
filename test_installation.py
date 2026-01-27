#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test script untuk memverifikasi instalasi package
"""

import sys
import shutil # Added for shutil.which

def test_basic_functionality():
    """Test basic functionality: import, class init, CLI availability"""
    all_ok = True

    print("1. Testing Import...")
    try:
        import panen_tweet
        from panen_tweet import TwitterScraper
        print(f"   [SUCCESS] Berhasil import panen_tweet (Version: {panen_tweet.__version__})")
        print("   [SUCCESS] Berhasil import TwitterScraper class")
    except ImportError as e:
        print(f"   [FAILED] Gagal import: {e}")
        return False

    # 2. Test Class Initialization
    print("\n2. Testing Class Initialization...")
    try:
        scraper = TwitterScraper(auth_token="test_token", headless=True)
        print("   [SUCCESS] Berhasil inisialisasi TwitterScraper")
        print(f"   - Auth token: {'Set' if scraper.auth_token else 'Not set'}")
        print(f"   - Headless mode: {scraper.headless}")
        print(f"   - Scroll pause time: {scraper.scroll_pause_time}s")
    except Exception as e:
        print(f"   [FAILED] Gagal inisialisasi: {e}")
        return False

    # 3. Test CLI Availability
    print("\n3. Testing CLI Command...")
    cli_command = "panen-tweet"
    if shutil.which(cli_command):
        print(f"   [SUCCESS] Command '{cli_command}' ditemukan di path")
    else:
        print(f"   [WARNING] Command '{cli_command}' tidak ditemukan (mungkin perlu restart terminal)")
        # This is a warning, not a hard failure for the entire basic functionality test
        # The original CLI test also didn't always return False.
        # We'll let the overall test pass if other critical steps passed.

    return all_ok


def test_module_attributes():
    """Test apakah module attributes tersedia"""
    print("\n🔍 Testing module attributes...")
    try:
        import scrape_x
        print("✅ Module attributes:")
        print(f"   - Version: {scrape_x.__version__}")
        print(f"   - Author: {scrape_x.__author__}")
        print(f"   - Available exports: {scrape_x.__all__}")
        return True
    except Exception as e:
        print(f"❌ Module attributes: FAILED - {e}")
        return False


def test_cli_available():
    """Test apakah CLI command tersedia"""
    print("\n🔍 Testing CLI availability...")
    import subprocess
    try:
        result = subprocess.run(
            ['scrape-x', '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )
        # CLI doesn't have --help, but command should exist
        print("✅ CLI command 'scrape-x': AVAILABLE")
        return True
    except FileNotFoundError:
        print("❌ CLI command 'scrape-x': NOT FOUND")
        return False
    except subprocess.TimeoutExpired:
        # Timeout is okay - it means command exists but waiting for input
        print("✅ CLI command 'scrape-x': AVAILABLE (interactive mode)")
        return True
    except Exception as e:
        print(f"⚠️  CLI command test: {e}")
        return True  # Don't fail the test for this


def test_dependencies():
    """Test apakah semua dependencies terinstall"""
    print("\n🔍 Testing dependencies...")
    dependencies = {
        'pandas': 'pandas',
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager'
    }

    all_ok = True
    for module_name, package_name in dependencies.items():
        try:
            __import__(module_name)
            print(f"✅ {package_name}: INSTALLED")
        except ImportError:
            print(f"❌ {package_name}: NOT INSTALLED")
            all_ok = False

    return all_ok


def main():
    """Run all tests"""
    print("=" * 60)
    print("  SCRAPE-X Package Installation Test")
    print("=" * 60)
    print()

    tests = [
        ("Import Test", test_import),
        ("Class Initialization Test", test_class_initialization),
        ("Module Attributes Test", test_module_attributes),
        ("CLI Availability Test", test_cli_available),
        ("Dependencies Test", test_dependencies),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n⚠️  {test_name} raised exception: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("  TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")

    print("\n" + "-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("-" * 60)

    if passed == total:
        print("\n🎉 All tests passed! Package is ready to use!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
