"""
Test script for Phase 1: Play Store Review Fetcher

Tests the complete scraping pipeline with various configurations.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.play_store_scraper import PlayStoreScraper


async def test_basic_fetch():
    """Test 1: Basic fetch with default settings"""
    print("\n" + "="*70)
    print("TEST 1: Basic Fetch (Default Settings)")
    print("="*70)
    
    try:
        scraper = PlayStoreScraper()
        result = await scraper.fetch_and_store(weeks=8, max_reviews=100)
        
        if result['success']:
            print(f"✅ SUCCESS: Fetched {result['reviews_fetched']} reviews")
            print(f"📁 File: {result.get('file_path', 'N/A')}")
            
            if result['metadata']:
                meta = result['metadata']
                print(f"\n📊 Statistics:")
                print(f"   - Total fetched: {meta.get('totalFetched', 0)}")
                print(f"   - After date filter: {meta.get('afterDateFilter', 0)}")
                print(f"   - After quality filters: {meta.get('totalAfterFilters', 0)}")
                
                if 'filterStats' in meta:
                    stats = meta['filterStats']
                    print(f"\n🔍 Filter breakdown:")
                    print(f"   - Too short: {stats.get('too_short', 0)}")
                    print(f"   - Has emoji: {stats.get('has_emoji', 0)}")
                    print(f"   - Wrong language: {stats.get('wrong_language', 0)}")
                    print(f"   - PII removed: {stats.get('pii_removed', 0)}")
            
            return True
        else:
            print(f"❌ FAILED: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


async def test_custom_weeks():
    """Test 2: Custom week range (4 weeks)"""
    print("\n" + "="*70)
    print("TEST 2: Custom Week Range (4 weeks)")
    print("="*70)
    
    try:
        scraper = PlayStoreScraper()
        result = await scraper.fetch_and_store(weeks=4, max_reviews=50)
        
        if result['success']:
            print(f"✅ SUCCESS: Fetched {result['reviews_fetched']} reviews from last 4 weeks")
            return True
        else:
            print(f"❌ FAILED: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


async def test_large_fetch():
    """Test 3: Large fetch (500 reviews)"""
    print("\n" + "="*70)
    print("TEST 3: Large Fetch (500 reviews, 12 weeks)")
    print("="*70)
    
    try:
        scraper = PlayStoreScraper()
        result = await scraper.fetch_and_store(weeks=12, max_reviews=500)
        
        if result['success']:
            print(f"✅ SUCCESS: Fetched {result['reviews_fetched']} reviews from last 12 weeks")
            return True
        else:
            print(f"❌ FAILED: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False


def test_quality_filters():
    """Test 4: Quality filter functions"""
    print("\n" + "="*70)
    print("TEST 4: Quality Filter Functions")
    print("="*70)
    
    scraper = PlayStoreScraper()
    
    # Test word count
    test_cases = [
        ("Good app", False, "Too short"),
        ("This is a great application for investing", True, "Good length"),
        ("Love it! 😍😍", False, "Has emoji"),
        ("बहुत अच्छा है", False, "Not English"),
        ("Excellent service and support", True, "English, good length"),
    ]
    
    all_passed = True
    
    for text, expected_keep, description in test_cases:
        keep, reason = scraper.should_keep_review(text)
        passed = (keep == expected_keep)
        
        status = "✅" if passed else "❌"
        print(f"{status} {description}: '{text[:30]}...' -> Keep={keep} ({reason})")
        
        if not passed:
            all_passed = False
    
    return all_passed


def test_pii_removal():
    """Test 5: PII removal patterns"""
    print("\n" + "="*70)
    print("TEST 5: PII Removal Patterns")
    print("="*70)
    
    scraper = PlayStoreScraper()
    
    test_cases = [
        ("Contact me at test@email.com", "[EMAIL_REDACTED]"),
        ("Call 9876543210", "[PHONE_REDACTED]"),
        ("Card: 1234-5678-9012-3456", "[CARD_REDACTED]"),
        ("Visit https://example.com", "[URL_REDACTED]"),
        ("My PAN is ABCDE1234F", "[PAN_REDACTED]"),
    ]
    
    all_passed = True
    
    for input_text, expected_marker in test_cases:
        output = scraper.remove_pii(input_text)
        passed = expected_marker in output
        
        status = "✅" if passed else "❌"
        print(f"{status} {input_text} -> {output}")
        
        if not passed:
            all_passed = False
    
    return all_passed


async def run_all_tests():
    """Run all tests sequentially"""
    print("\n" + "="*70)
    print("🧪 PHASE 1: PLAY STORE FETCHER - TEST SUITE")
    print("="*70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 App ID: {os.getenv('PLAY_STORE_DEFAULT_APP_ID', 'com.nextbillion.groww')}")
    print(f"⚙️  Config: Weeks=8, Max Reviews=500")
    print("="*70)
    
    results = []
    
    # Run async tests
    results.append(("Basic Fetch", await test_basic_fetch()))
    results.append(("Custom Weeks", await test_custom_weeks()))
    results.append(("Large Fetch", await test_large_fetch()))
    
    # Run sync tests
    results.append(("Quality Filters", test_quality_filters()))
    results.append(("PII Removal", test_pii_removal()))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n📈 Results: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    print("="*70)
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Phase 1 implementation is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
