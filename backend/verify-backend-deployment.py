"""
Backend Deployment Verification Script

Tests all critical endpoints to ensure backend is working correctly.

Usage:
    python verify-backend-deployment.py YOUR_RAILWAY_URL

Example:
    python verify-backend-deployment.py https://your-app-production.up.railway.app
"""

import requests
import sys
from datetime import datetime


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test(test_name, status, details=""):
    """Print test result"""
    emoji = "✅" if status == "PASS" else "❌"
    print(f"\n{emoji} {test_name}: {status}")
    if details:
        print(f"   {details}")


def verify_deployment(base_url):
    """Verify backend deployment with comprehensive tests"""
    
    print_section("BACKEND DEPLOYMENT VERIFICATION")
    print(f"\n  Railway URL: {base_url}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 70)
    
    results = {
        "passed": 0,
        "failed": 0,
        "warnings": 0
    }
    
    # Test 1: API Documentation Accessible
    print("\n[TEST 1] Checking API Documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print_test("API Documentation", "PASS", f"Swagger UI accessible at {base_url}/docs")
            results["passed"] += 1
        else:
            print_test("API Documentation", "FAIL", f"Status code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print_test("API Documentation", "FAIL", f"Error: {str(e)}")
        results["failed"] += 1
    
    # Test 2: Reviews Stats Endpoint
    print("\n[TEST 2] Testing Reviews Statistics...")
    try:
        response = requests.get(f"{base_url}/api/reviews/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Reviews Stats",
                "PASS",
                f"Total: {data.get('total', 0)}, Avg Rating: {data.get('average_rating', 0)}"
            )
            results["passed"] += 1
        else:
            print_test("Reviews Stats", "FAIL", f"Status code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print_test("Reviews Stats", "FAIL", f"Error: {str(e)}")
        results["failed"] += 1
    
    # Test 3: Settings Endpoint
    print("\n[TEST 3] Testing Settings Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/reviews/settings", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_test(
                "Settings",
                "PASS",
                f"Weeks: {data.get('review_weeks_range', 8)}, Max Reviews: {data.get('max_reviews_to_fetch', 500)}"
            )
            results["passed"] += 1
        else:
            print_test("Settings", "FAIL", f"Status code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print_test("Settings", "FAIL", f"Error: {str(e)}")
        results["failed"] += 1
    
    # Test 4: Scheduler Status
    print("\n[TEST 4] Testing Scheduler Status...")
    try:
        response = requests.get(f"{base_url}/api/scheduler/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            is_running = data.get('is_running', False)
            status = "RUNNING" if is_running else "STOPPED"
            next_run = data.get('next_run_formatted', 'N/A')
            print_test(
                "Scheduler Status",
                "PASS" if is_running else "WARNING",
                f"Status: {status}, Next Run: {next_run}"
            )
            if is_running:
                results["passed"] += 1
            else:
                results["warnings"] += 1
        else:
            print_test("Scheduler Status", "FAIL", f"Status code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print_test("Scheduler Status", "FAIL", f"Error: {str(e)}")
        results["failed"] += 1
    
    # Test 5: Play Store Fetch (Optional - may fail if app not available)
    print("\n[TEST 5] Testing Play Store Auto-Fetch...")
    try:
        payload = {
            "app_id": "com.whatsapp",
            "weeks": 4,
            "max_reviews": 50,
            "country": "us",
            "language": "en"
        }
        response = requests.post(
            f"{base_url}/api/reviews/fetch-play-store",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            fetched_count = data.get('fetched_count', 0)
            print_test(
                "Play Store Fetch",
                "PASS",
                f"Fetched {fetched_count} reviews for com.whatsapp"
            )
            results["passed"] += 1
        elif response.status_code == 400:
            print_test(
                "Play Store Fetch",
                "WARNING",
                "No reviews found for this app (try different app or country)"
            )
            results["warnings"] += 1
        else:
            print_test("Play Store Fetch", "FAIL", f"Status code: {response.status_code}")
            results["failed"] += 1
    except Exception as e:
        print_test("Play Store Fetch", "FAIL", f"Error: {str(e)}")
        results["failed"] += 1
    
    # Test 6: Generate Report (May fail if no data)
    print("\n[TEST 6] Testing Report Generation...")
    try:
        print("   ⏳ This may take 15-20 seconds...")
        response = requests.post(
            f"{base_url}/api/analysis/generate-weekly-report",
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            themes_count = len(data.get('top_themes', []))
            print_test(
                "Report Generation",
                "PASS",
                f"Generated report with {themes_count} themes"
            )
            results["passed"] += 1
        elif response.status_code == 400:
            print_test(
                "Report Generation",
                "WARNING",
                "No reviews in database (fetch some reviews first)"
            )
            results["warnings"] += 1
        else:
            print_test("Report Generation", "FAIL", f"Status code: {response.status_code}")
            results["failed"] += 1
    except requests.exceptions.Timeout:
        print_test("Report Generation", "FAIL", "Timeout (>60 seconds)")
        results["failed"] += 1
    except Exception as e:
        print_test("Report Generation", "FAIL", f"Error: {str(e)}")
        results["failed"] += 1
    
    # Print Summary
    print_section("VERIFICATION SUMMARY")
    total = results["passed"] + results["failed"] + results["warnings"]
    
    print(f"\n  Total Tests: {total}")
    print(f"  ✅ Passed: {results['passed']}")
    print(f"  ⚠️  Warnings: {results['warnings']}")
    print(f"  ❌ Failed: {results['failed']}")
    
    if total > 0:
        success_rate = (results["passed"] / total) * 100
        print(f"  Success Rate: {success_rate:.1f}%")
    
    print("\n" + "=" * 70)
    
    # Overall Assessment
    if results["failed"] == 0 and results["passed"] >= 4:
        print("\n  🎉 EXCELLENT! Backend is fully operational!")
        print("\n  Next Steps:")
        print("  1. Deploy frontend to Vercel")
        print("  2. Update CORS with Vercel URL")
        print("  3. Test end-to-end integration")
    elif results["failed"] <= 1:
        print("\n  ✅ GOOD! Backend is mostly working.")
        print("  Check warnings above for minor issues.")
    else:
        print("\n  ⚠️  ISSUES FOUND! Please review errors above.")
        print("  Check Railway logs: railway logs")
    
    print("\n" + "=" * 70)
    
    return results["failed"] == 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage: python verify-backend-deployment.py YOUR_RAILWAY_URL")
        print("\nExample:")
        print("  python verify-backend-deployment.py https://your-app-production.up.railway.app")
        sys.exit(1)
    
    railway_url = sys.argv[1]
    
    # Remove trailing slash if present
    railway_url = railway_url.rstrip('/')
    
    # Validate URL format
    if not railway_url.startswith('http'):
        railway_url = 'https://' + railway_url
    
    print(f"\nVerifying backend at: {railway_url}")
    
    success = verify_deployment(railway_url)
    
    if success:
        print("\n✅ Backend verification PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Backend verification FAILED!")
        sys.exit(1)
