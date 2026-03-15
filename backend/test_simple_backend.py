"""
Simple Backend Test - Quick connectivity check
"""

import requests
from datetime import datetime

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

print("=" * 60)
print("  🧪 SIMPLE BACKEND API TEST")
print("=" * 60)
print(f"\n  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  Base URL: {BASE_URL}")
print("\n" + "=" * 60)

# Test 1: Basic connectivity
print("\n[TEST 1] Backend Connectivity...")
try:
    response = requests.get(f"{BASE_URL}/docs", timeout=5)
    if response.status_code == 200:
        print(f"  ✅ PASS - Backend is running")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - Error: {str(e)}")

# Test 2: Get review stats
print("\n[TEST 2] Get Review Statistics...")
try:
    response = requests.get(f"{API_BASE}/reviews/stats", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ PASS - Total: {data['total']}, Avg Rating: {data['average_rating']}")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - Error: {str(e)}")

# Test 3: Get settings
print("\n[TEST 3] Get Current Settings...")
try:
    response = requests.get(f"{API_BASE}/reviews/settings", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ PASS - Weeks: {data['review_weeks_range']}, Max Reviews: {data['max_reviews_to_fetch']}")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - Error: {str(e)}")

# Test 4: Scheduler status
print("\n[TEST 4] Scheduler Status...")
try:
    response = requests.get(f"{API_BASE}/scheduler/status", timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ PASS - Running: {data.get('is_running', False)}, Next: {data.get('next_run_formatted', 'N/A')}")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"  ❌ FAIL - Error: {str(e)}")

# Test 5: Try to generate report (with detailed error)
print("\n[TEST 5] Generate Weekly Report (AI Analysis)...")
try:
    print("  ⏳ This may take 15-20 seconds...")
    response = requests.post(f"{API_BASE}/analysis/generate-weekly-report", timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ PASS - Generated report with {len(data['top_themes'])} themes")
    else:
        print(f"  ❌ FAIL - Status: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
except requests.exceptions.Timeout:
    print(f"  ❌ FAIL - Timeout (>60 seconds)")
except Exception as e:
    print(f"  ❌ FAIL - Error: {str(e)}")

print("\n" + "=" * 60)
print("  Test completed!")
print("=" * 60)
