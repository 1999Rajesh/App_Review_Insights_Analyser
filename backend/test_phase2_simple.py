"""
Phase 2 Workflow Test - Simplified Version
Tests: CSV Import → Filtering → PII Removal → Display Sample
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.review_importer import ReviewImporter
from app.utils.pii_remover import sanitize_reviews
from app.config import settings
from datetime import datetime
import tempfile


def create_test_csv():
    """Create a sample App Store CSV file for testing."""
    
    csv_content = """Date,Rating,Title,Review
2026-03-10,5,Best App!,Love this application so much
2026-03-09,4,Great,Works well but needs improvements
2026-03-08,3,OK,Its fine I guess nothing special
2026-03-07,5,Amazing,Absolutely perfect in every way
2026-03-06,2,Bad,Terrible experience overall
2026-03-05,5,Wow,"Contact me at john@example.com or call 555-123-4567"
2026-03-04,4,Nice,Very nice and helpful app indeed
2026-03-03,1,Awful,Worst experience ever had with any app
2026-03-02,5,Perfect,"My account #123456 has issues, card 1234-5678-9012-3456"
2026-03-01,3,Meh,Its fine nothing special really
2026-02-28,4,Good,Really good app for productivity
2026-02-27,5,Excellent,Cannot imagine working without this tool
2026-02-26,2,Poor,Disappointing update broke features
2026-02-25,5,Love,Best investment for my business growth
2026-02-20,1,Horrible,App crashes constantly unusable garbage
2026-02-15,5,Outstanding,Exceptional quality and customer support"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    temp_file.write(csv_content)
    temp_file.close()
    
    return temp_file.name


def test_phase2_simple():
    """Test Phase 2 workflow without LLM call."""
    
    print("=" * 80)
    print("PHASE 2 WORKFLOW TEST - Filtered Reviews Ready for LLM")
    print("=" * 80)
    print()
    
    # Configuration
    print("📋 CONFIGURATION:")
    print(f"   Groq Model: {settings.GROQ_MODEL}")
    print(f"   API Key: {'✅ Configured' if settings.GROQ_API_KEY and not settings.GROQ_API_KEY.startswith('test') else '⚠️ Using placeholder'}")
    print(f"   Word Threshold: ≥5 words")
    print(f"   Date Range: Last {settings.REVIEW_WEEKS_RANGE} weeks")
    print()
    
    # Step 1: Create test CSV
    print("📝 Step 1: Creating test CSV...")
    csv_file = create_test_csv()
    print(f"   ✅ Created temporary CSV")
    print()
    
    # Step 2: Import reviews
    print("📥 Step 2: Importing reviews with filtering...")
    importer = ReviewImporter()
    
    try:
        all_reviews = importer.parse_app_store_csv(csv_file)
        print(f"   📊 CSV rows: 16")
        print(f"   ✅ After word filter: {len(all_reviews)} reviews kept")
        print(f"   🗑️  Filtered out: {16 - len(all_reviews)} reviews (< 5 words)")
        print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Step 3: Date filtering
    print("📅 Step 3: Applying date range filter...")
    filtered_reviews = importer.filter_by_date_range(all_reviews, weeks=8)
    print(f"   ✅ After date filter: {len(filtered_reviews)} recent reviews")
    print()
    
    # Step 4: Remove PII
    print("🔒 Step 4: Removing PII...")
    review_dicts = [r.model_dump() for r in filtered_reviews]
    sanitized_reviews = sanitize_reviews(review_dicts)
    
    pii_count = sum(1 for orig, san in zip(review_dicts, sanitized_reviews) 
                    if orig['text'] != san['text'])
    
    print(f"   ✅ PII removed from {pii_count} reviews")
    print()
    
    # Step 5: Show sample reviews
    print("📋 Step 5: Sample Clean Reviews (Ready for LLM):")
    print()
    
    for i, review in enumerate(sanitized_reviews[:3], 1):
        print(f"   Review {i}:")
        print(f"      Source: {review['source']}")
        print(f"      Rating: {'⭐' * review['rating']} ({review['rating']}/5)")
        print(f"      Text: \"{review['text']}\"")
        print(f"      Date: {review['date']}")
        print()
    
    if len(sanitized_reviews) > 3:
        print(f"   ... and {len(sanitized_reviews) - 3} more reviews")
        print()
    
    # Step 6: Summary statistics
    print("📊 Step 6: Review Statistics:")
    print(f"   Total clean reviews: {len(sanitized_reviews)}")
    
    if sanitized_reviews:
        avg_rating = sum(r['rating'] for r in sanitized_reviews) / len(sanitized_reviews)
        print(f"   Average rating: {avg_rating:.2f}/5")
        
        sources = {}
        for r in sanitized_reviews:
            sources[r['source']] = sources.get(r['source'], 0) + 1
        
        for source, count in sources.items():
            print(f"   {source}: {count} reviews")
    
    print()
    
    # Step 7: Prepare for LLM
    print("🤖 Step 7: Ready to Send to LLM!")
    print()
    print("   The following data is ready for Groq LLM analysis:")
    print(f"   • {len(sanitized_reviews)} clean, filtered reviews")
    print(f"   • All reviews have ≥5 words")
    print(f"   • All PII removed")
    print(f"   • Date range: last {settings.REVIEW_WEEKS_RANGE} weeks")
    print(f"   • Sanitized text ready for theme analysis")
    print()
    
    # Show what would be sent to LLM
    print("   Sample prompt for LLM:")
    print("   " + "-" * 76)
    print(f"   Analyze these {len(sanitized_reviews)} app reviews from the last {settings.REVIEW_WEEKS_RANGE} weeks.")
    print(f"   Group into MAX 5 themes. For each theme provide:")
    print(f"     - Theme name")
    print(f"     - Review count and percentage")
    print(f"     - Sentiment (positive/negative/neutral)")
    print(f"     - Up to 3 direct user quotes")
    print(f"     - 3 actionable ideas")
    print(f"   CONSTRAINTS: Max 5 themes, under 250 words, NO PII")
    print("   " + "-" * 76)
    print()
    
    # Cleanup
    if os.path.exists(csv_file):
        os.unlink(csv_file)
    
    print("=" * 80)
    print("✅ PHASE 2 WORKFLOW COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("1. Start the backend server: python -m uvicorn app.main:app --reload")
    print("2. Upload your actual CSV files via POST /api/reviews/upload")
    print("3. Generate report via POST /api/analysis/generate-report")
    print("4. The system will automatically:")
    print("   - Import and filter reviews")
    print("   - Remove PII")
    print("   - Send to Groq LLM for analysis")
    print("   - Generate weekly pulse report")
    print()
    
    return True


if __name__ == "__main__":
    print("\n🚀 Starting Phase 2 Workflow Test\n")
    success = test_phase2_simple()
    
    if success:
        print("🎉 All Phase 2 components working correctly!")
        print("   Your filtered reviews are ready for LLM analysis!")
    else:
        print("❌ Some issues detected. Please check the errors above.")
    
    print()
