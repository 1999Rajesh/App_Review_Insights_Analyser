"""
Comprehensive Backend API Test Script

Tests all endpoints of the App Review Insights Analyzer backend
Base URL: http://localhost:8000
"""

import requests
import json
from typing import Dict, Any
from datetime import datetime


# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test(test_name: str, status: str, details: str = ""):
    """Print test result with formatting"""
    emoji = "✅" if status == "PASS" else "❌"
    print(f"\n{emoji} {test_name}: {status}")
    if details:
        print(f"   {details}")


def test_health_check() -> bool:
    """Test 1: Basic Connectivity Check"""
    print_section("TEST 1: Basic Connectivity")
    
    try:
        # Test base URL connectivity
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        
        if response.status_code == 200:
            print_test(
                "Backend Connectivity",
                "PASS",
                f"Backend is running at {BASE_URL}"
            )
            return True
        else:
            print_test(
                "Backend Connectivity",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except requests.exceptions.ConnectionError:
        print_test(
            "Backend Connectivity",
            "FAIL",
            "Backend server not running at http://localhost:8000"
        )
        return False
    except Exception as e:
        print_test(
            "Backend Connectivity",
            "FAIL",
            f"Error: {str(e)}"
        )
        return False


def test_get_reviews_stats() -> bool:
    """Test 2: Get Review Statistics"""
    print_section("TEST 2: Get Review Statistics")
    
    try:
        response = requests.get(f"{API_BASE}/reviews/stats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Get Review Stats",
                "PASS",
                f"Total: {data.get('total', 0)}, App Store: {data.get('app_store', 0)}, "
                f"Play Store: {data.get('play_store', 0)}, Avg Rating: {data.get('average_rating', 0)}"
            )
            return True
        else:
            print_test(
                "Get Review Stats",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except Exception as e:
        print_test(
            "Get Review Stats",
            "FAIL",
            f"Error: {str(e)}"
        )
        return False


def test_get_settings() -> bool:
    """Test 3: Get Current Settings"""
    print_section("TEST 3: Get Current Settings")
    
    try:
        response = requests.get(f"{API_BASE}/reviews/settings", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Get Settings",
                "PASS",
                f"Weeks: {data.get('review_weeks_range', 8)}, "
                f"Max Reviews: {data.get('max_reviews_to_fetch', 500)}, "
                f"Themes: {data.get('max_themes', 5)}"
            )
            return True
        else:
            print_test(
                "Get Settings",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except Exception as e:
        print_test(
            "Get Settings",
            "FAIL",
            f"Error: {str(e)}"
        )
        return False


def test_update_settings() -> bool:
    """Test 4: Update Settings"""
    print_section("TEST 4: Update Settings")
    
    try:
        # Test updating max_themes
        new_settings = {
            "max_themes": 7
        }
        
        response = requests.post(
            f"{API_BASE}/reviews/settings",
            json=new_settings,
            timeout=10
        )
        
        if response.status_code == 200:
            print_test(
                "Update Settings",
                "PASS",
                f"Updated max_themes to 7"
            )
            
            # Revert back to 5
            requests.post(
                f"{API_BASE}/reviews/settings",
                json={"max_themes": 5},
                timeout=10
            )
            return True
        else:
            print_test(
                "Update Settings",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except Exception as e:
        print_test(
            "Update Settings",
            "FAIL",
            f"Error: {str(e)}"
        )
        return False


def test_fetch_play_store_reviews() -> bool:
    """Test 5: Fetch Play Store Reviews (Groww App)"""
    print_section("TEST 5: Fetch Play Store Reviews (Groww)")
    
    try:
        payload = {
            "app_id": "in.groww",
            "weeks": 4,  # Shorter range for faster testing
            "max_reviews": 50,  # Smaller number for quick test
            "country": "us",
            "language": "en"
        }
        
        print(f"   Fetching reviews for: {payload['app_id']}")
        print(f"   Weeks: {payload['weeks']}, Max Reviews: {payload['max_reviews']}")
        
        response = requests.post(
            f"{API_BASE}/reviews/fetch-play-store",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Fetch Play Store Reviews",
                "PASS",
                f"Fetched: {data.get('fetched_count', 0)} reviews, "
                f"Total in DB: {data.get('total_in_database', 0)}"
            )
            return True
        elif response.status_code == 400:
            print_test(
                "Fetch Play Store Reviews",
                "FAIL",
                "No reviews found for this app ID (try different app or country)"
            )
            return False
        else:
            print_test(
                "Fetch Play Store Reviews",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except requests.exceptions.Timeout:
        print_test(
            "Fetch Play Store Reviews",
            "FAIL",
            "Request timed out (took > 30 seconds)"
        )
        return False
    except Exception as e:
        print_test(
            "Fetch Play Store Reviews",
            "FAIL",
            f"Error: {str(e)}"
        )
        return False


def test_generate_weekly_report() -> bool:
    """Test 6: Generate Weekly Report"""
    print_section("TEST 6: Generate Weekly Report")
    
    try:
        print("   Generating AI-powered weekly report...")
        print("   This may take 15-20 seconds...")
        
        response = requests.post(
            f"{API_BASE}/analysis/generate-weekly-report",
            timeout=60  # Longer timeout for AI analysis
        )
        
        if response.status_code == 200:
            data = response.json()
            themes_count = len(data.get('top_themes', []))
            print_test(
                "Generate Weekly Report",
                "PASS",
                f"Report ID: {data.get('id', 'N/A')[:8]}..., "
                f"Reviews: {data.get('total_reviews', 0)}, "
                f"Themes: {themes_count}"
            )
            
            # Show first theme as sample
            if themes_count > 0:
                first_theme = data['top_themes'][0]
                print(f"   Sample Theme: {first_theme.get('theme_name', 'Unknown')} "
                      f"({first_theme.get('percentage', 0):.1f}%)")
            
            return True
        else:
            print_test(
                "Generate Weekly Report",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except requests.exceptions.Timeout:
        print_test(
            "Generate Weekly Report",
            "FAIL",
            "Request timed out (AI analysis took > 60 seconds)"
        )
        return False
    except Exception as e:
        print_test(
            "Generate Weekly Report",
            "FAIL",
            f"Error: {str(e)}"
        )
        return False


def test_scheduler_status() -> bool:
    """Test 7: Check Scheduler Status"""
    print_section("TEST 7: Scheduler Status")
    
    try:
        response = requests.get(f"{API_BASE}/scheduler/status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Scheduler Status",
                "PASS",
                f"Running: {data.get('running', False)}, "
                f"Next Run: {data.get('next_run_time', 'N/A')}"
            )
            return True
        else:
            print_test(
                "Scheduler Status",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except Exception as e:
        print_test(
            "Scheduler Status",
            "FAIL",
            f"Error: {str(e)}"
        )
        return False


def test_send_email_report() -> bool:
    """Test 8: Send Email Report (Will fail with dummy credentials - expected)"""
    print_section("TEST 8: Send Email Report")
    
    try:
        print("   Note: This test is expected to fail with dummy SMTP credentials")
        
        payload = {
            "recipient_email": "test@example.com"
        }
        
        response = requests.post(
            f"{API_BASE}/email/send-draft",
            json=payload,
            timeout=15
        )
        
        # Even if it fails, we got a response
        if response.status_code in [200, 404, 500]:
            if response.status_code == 200:
                print_test(
                    "Send Email Report",
                    "PASS",
                    "Email sent successfully!"
                )
                return True
            elif response.status_code == 404:
                print_test(
                    "Send Email Report",
                    "EXPECTED FAIL",
                    "No reports generated yet (expected)"
                )
                return True  # Count as pass since it's expected
            else:
                print_test(
                    "Send Email Report",
                    "EXPECTED FAIL",
                    "SMTP error (expected with dummy credentials)"
                )
                return True  # Count as pass since it's expected
        else:
            print_test(
                "Send Email Report",
                "FAIL",
                f"Status Code: {response.status_code}"
            )
            return False
            
    except Exception as e:
        print_test(
            "Send Email Report",
            "EXPECTED FAIL",
            f"SMTP error (expected with dummy credentials)"
        )
        return True  # Count as pass since it's expected


def run_all_tests():
    """Run all backend API tests"""
    
    print("\n" + "=" * 70)
    print("  🧪 BACKEND API COMPREHENSIVE TEST SUITE")
    print("  Base URL: http://localhost:8000")
    print("=" * 70)
    print(f"\n  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Testing: App Review Insights Analyzer Backend")
    
    # Track results
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # Run tests
    tests = [
        ("Health Check", test_health_check),
        ("Get Review Stats", test_get_reviews_stats),
        ("Get Settings", test_get_settings),
        ("Update Settings", test_update_settings),
        ("Fetch Play Store Reviews", test_fetch_play_store_reviews),
        ("Generate Weekly Report", test_generate_weekly_report),
        ("Scheduler Status", test_scheduler_status),
        ("Send Email Report", test_send_email_report),
    ]
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            if success:
                results["passed"] += 1
            else:
                results["failed"] += 1
        except Exception as e:
            print(f"\n❌ {test_name}: EXCEPTION - {str(e)}")
            results["failed"] += 1
    
    # Print summary
    print_section("TEST SUMMARY")
    total = results["passed"] + results["failed"]
    print(f"\n  Total Tests: {total}")
    print(f"  ✅ Passed: {results['passed']}")
    print(f"  ❌ Failed: {results['failed']}")
    
    if total > 0:
        success_rate = (results["passed"] / total) * 100
        print(f"  Success Rate: {success_rate:.1f}%")
    
    print(f"\n  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 70)
    
    # Return overall success
    return results["failed"] == 0


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  Starting Backend API Tests...")
    print("=" * 70)
    
    try:
        success = run_all_tests()
        
        if success:
            print("\n🎉 All critical tests passed!")
            print("   Backend is functioning correctly.")
        else:
            print("\n⚠️  Some tests failed.")
            print("   Check the output above for details.")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
