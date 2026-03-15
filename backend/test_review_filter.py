"""
Test script to verify review filtering functionality.
Run this to ensure reviews with < 5 words are filtered out.
"""

import sys
sys.path.append('backend')

from app.services.review_importer import ReviewImporter
import pandas as pd
import tempfile
import os


def test_word_count_filter():
    """Test that reviews with less than 5 words are filtered out."""
    
    print("=" * 60)
    print("Testing Review Word Count Filter")
    print("=" * 60)
    
    # Create test CSV data
    test_data = """Date,Rating,Title,Review
2026-03-10,5,Great,"Amazing"
2026-03-09,4,Good,"Really good app"
2026-03-08,3,OK,"It works fine for me"
2026-03-07,1,Bad,"Terrible"
2026-03-06,5,Wow,"Best app I have ever used"
2026-03-05,2,Hmm,"This is okay I guess"
2026-03-04,4,Nice,"Very nice and helpful"
2026-03-03,1,Awful,"Worst experience ever had"
2026-03-02,5,Perfect,"Absolutely perfect in every way"
2026-03-01,3,Meh,"Its fine nothing special"
"""

    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_data)
        temp_file = f.name
    
    try:
        # Import reviews
        importer = ReviewImporter()
        reviews = importer.parse_app_store_csv(temp_file)
        
        print(f"\n📊 Results:")
        print(f"   Original rows in CSV: 10")
        print(f"   Reviews after filtering: {len(reviews)}")
        print(f"   Reviews filtered out: {10 - len(reviews)}")
        
        print(f"\n✅ KEPT Reviews ({len(reviews)}):")
        for i, review in enumerate(reviews, 1):
            word_count = len(review.text.split())
            print(f"   {i}. \"{review.text}\" ({word_count} words)")
        
        # Verify all kept reviews have >= 5 words
        print(f"\n🔍 Validation:")
        all_valid = True
        for review in reviews:
            word_count = len(review.text.split())
            if word_count < 5:
                print(f"   ❌ ERROR: Review with {word_count} words was not filtered!")
                all_valid = False
        
        if all_valid:
            print(f"   ✅ All kept reviews have >= 5 words")
        
        # Check title field is empty
        print(f"\n📝 Title Field Check:")
        titles_empty = all(review.title == '' for review in reviews)
        if titles_empty:
            print(f"   ✅ All titles are empty (as expected)")
        else:
            print(f"   ❌ Some titles are not empty!")
        
        print(f"\n{'=' * 60}")
        if all_valid and titles_empty:
            print("✅ TEST PASSED: Filtering working correctly!")
        else:
            print("❌ TEST FAILED: Issues detected!")
        print(f"{'=' * 60}\n")
        
        return all_valid and titles_empty
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.unlink(temp_file)


def test_edge_cases():
    """Test edge cases for word count filtering."""
    
    print("=" * 60)
    print("Testing Edge Cases")
    print("=" * 60)
    
    test_cases = [
        ("", 0, "Empty string"),
        ("   ", 0, "Whitespace only"),
        ("Word", 1, "Single word"),
        ("Two words", 2, "Two words"),
        ("Three words here", 3, "Three words"),
        ("Four words in this", 4, "Four words"),
        ("Five words in this one", 5, "Exactly 5 words"),
        ("Six words in this example", 6, "Six words"),
    ]
    
    print("\n🧪 Word Count Logic Test:\n")
    
    for text, expected_count, description in test_cases:
        actual_count = len(text.split())
        status = "✅" if actual_count == expected_count else "❌"
        should_keep = "KEEP" if actual_count >= 5 else "FILTER"
        print(f"   {status} {description}: '{text}'")
        print(f"      Expected: {expected_count}, Actual: {actual_count} → {should_keep}")
    
    print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    """Run all tests."""
    
    print("\n🚀 Starting Review Filter Tests\n")
    
    # Run edge case tests first
    test_edge_cases()
    
    # Run main filter test
    passed = test_word_count_filter()
    
    # Summary
    print("\n📋 Test Summary:")
    print(f"   Overall Status: {'✅ PASSED' if passed else '❌ FAILED'}")
    print(f"   Filter Threshold: 5 words minimum")
    print(f"   Title Field: Empty (removed)\n")
    
    exit(0 if passed else 1)
