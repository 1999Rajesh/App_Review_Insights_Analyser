"""
Test Script for Weekly Review Pipeline

Tests the complete pipeline:
1. Fetch reviews from Play Store
2. Save in hybrid format (JSON + CSV)
3. Generate weekly pulse note
4. Verify PII protection

Usage:
    python test_weekly_pipeline.py          # Test without email
    python test_weekly_pipeline.py --email  # Test with email enabled
"""

import os
import sys
import argparse
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_hybrid_collector():
    """Test the hybrid review collector"""
    print("\n" + "=" * 70)
    print("🧪 TEST 1: HYBRID REVIEW COLLECTOR")
    print("=" * 70)
    
    try:
        from services.hybrid_review_collector import HybridReviewCollector
        
        collector = HybridReviewCollector()
        
        print(f"Configuration:")
        print(f"   App ID: {collector.app_id}")
        print(f"   Weeks: {collector.weeks_range}")
        print(f"   Max Reviews: {collector.max_reviews}")
        print(f"   Min Word Count: {collector.min_word_count}")
        print(f"   Allow Emojis: {collector.allow_emojis}")
        
        result = collector.collect()
        
        if result.get('success'):
            print(f"\n✅ Collector test PASSED")
            print(f"   Reviews collected: {result.get('reviews_collected', 0)}")
            print(f"   JSON file: {result.get('json_file')}")
            print(f"   CSV file: {result.get('csv_file')}")
            return True
        else:
            print(f"\n❌ Collector test FAILED")
            print(f"   Message: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ Collector test ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pulse_generator():
    """Test the weekly pulse note generator"""
    print("\n" + "=" * 70)
    print("🧪 TEST 2: WEEKLY PULSE GENERATOR")
    print("=" * 70)
    
    try:
        from services.weekly_pulse_generator import WeeklyPulseNoteGenerator
        
        generator = WeeklyPulseNoteGenerator()
        
        # Find latest JSON file
        data_dir = os.getenv('REVIEWS_DATA_DIR', 'data/reviews')
        json_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.json')])
        
        if not json_files:
            print("⚠️ No JSON files found. Run collector test first.")
            return False
        
        latest_json = os.path.join(data_dir, json_files[-1])
        print(f"Using JSON file: {latest_json}")
        
        result = generator.generate(latest_json)
        
        if result.get('success'):
            print(f"\n✅ Pulse generator test PASSED")
            print(f"   Note file: {result.get('note_file')}")
            print(f"   Themes identified: {result.get('themes_identified', 0)}")
            print(f"   Reviews analyzed: {result.get('total_reviews', 0)}")
            
            # Show preview of note
            note_content = result.get('note_content', '')
            if note_content:
                preview = note_content[:500]
                print(f"\n📝 Note Preview:\n{preview}...\n")
            
            return True
        else:
            print(f"\n❌ Pulse generator test FAILED")
            print(f"   Message: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"\n❌ Pulse generator test ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_pii_protection():
    """Test PII redaction functionality"""
    print("\n" + "=" * 70)
    print("🧪 TEST 3: PII PROTECTION")
    print("=" * 70)
    
    try:
        from services.hybrid_review_collector import HybridReviewCollector
        
        collector = HybridReviewCollector()
        
        # Test cases with PII
        test_cases = [
            ("Contact me at test@example.com", "[EMAIL_REDACTED]"),
            ("Call 9876543210 for support", "[PHONE_REDACTED]"),
            ("My card is 1234-5678-9012-3456", "[CARD_REDACTED]"),
            ("PAN: ABCDE1234F", "[PAN_REDACTED]"),
            ("Visit https://example.com/page", "[URL_REDACTED]"),
        ]
        
        all_passed = True
        
        for original, expected_marker in test_cases:
            cleaned = collector.remove_pii(original)
            
            if expected_marker in cleaned:
                print(f"✅ {original[:30]}... → {cleaned}")
            else:
                print(f"❌ {original[:30]}... → {cleaned} (expected {expected_marker})")
                all_passed = False
        
        if all_passed:
            print(f"\n✅ PII protection test PASSED")
            return True
        else:
            print(f"\n❌ PII protection test FAILED")
            return False
            
    except Exception as e:
        print(f"\n❌ PII protection test ERROR: {str(e)}")
        return False


def test_complete_pipeline(send_email: bool = False):
    """Test the complete pipeline"""
    print("\n" + "=" * 70)
    print("🧪 TEST 4: COMPLETE PIPELINE")
    print("=" * 70)
    
    try:
        from services.weekly_review_pipeline import WeeklyReviewPipeline
        
        pipeline = WeeklyReviewPipeline()
        
        print(f"Pipeline Configuration:")
        print(f"   Send Email: {send_email}")
        print(f"   Recipient: {pipeline.recipient_email}")
        print(f"   Weeks Range: {pipeline.collector.weeks_range}")
        
        result = pipeline.run(send_email=send_email)
        
        if result.get('success'):
            print(f"\n✅ Complete pipeline test PASSED")
            print(f"   Steps completed: {len(result.get('steps_completed', []))}")
            print(f"   Reviews: {result.get('reviews_collected', 0)}")
            print(f"   Themes: {result.get('themes_identified', 0)}")
            print(f"   Email sent: {result.get('email_sent', False)}")
            
            # List steps completed
            for step in result.get('steps_completed', []):
                print(f"   ✅ {step}")
            
            return True
        else:
            print(f"\n❌ Complete pipeline test FAILED")
            errors = result.get('errors', [])
            for error in errors:
                print(f"   Error: {error}")
            return False
            
    except Exception as e:
        print(f"\n❌ Complete pipeline test ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    parser = argparse.ArgumentParser(description='Test Weekly Review Pipeline')
    parser.add_argument(
        '--email',
        action='store_true',
        help='Enable email sending in tests'
    )
    parser.add_argument(
        '--skip-collector',
        action='store_true',
        help='Skip collector test (use existing data)'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🧪 WEEKLY REVIEW PIPELINE - TEST SUITE")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = {
        'hybrid_collector': False,
        'pii_protection': False,
        'pulse_generator': False,
        'complete_pipeline': False
    }
    
    # Test 1: PII Protection (independent)
    results['pii_protection'] = test_pii_protection()
    
    # Test 2: Hybrid Collector (fetches live data)
    if not args.skip_collector:
        results['hybrid_collector'] = test_hybrid_collector()
    else:
        print("\n⏭️  Skipping collector test (using existing data)")
        results['hybrid_collector'] = True
    
    # Test 3: Pulse Generator (requires collector to pass)
    if results['hybrid_collector'] or args.skip_collector:
        results['pulse_generator'] = test_pulse_generator()
    
    # Test 4: Complete Pipeline (optional email)
    if results['pulse_generator']:
        results['complete_pipeline'] = test_complete_pipeline(send_email=args.email)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    print("=" * 70)
    
    # Exit with appropriate code
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
