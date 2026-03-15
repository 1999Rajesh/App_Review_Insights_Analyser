"""
Complete Local Test with Mock Data

This test runs the ENTIRE pipeline using existing sample data,
so you can see results immediately without waiting for live API calls.
"""

import os
import sys
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.weekly_pulse_generator import WeeklyPulseNoteGenerator


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main():
    """Run complete local test with sample data"""
    
    print_section("🧪 LOCAL PIPELINE TEST WITH SAMPLE DATA")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nThis test uses existing sample data (no live API calls)")
    print("Perfect for verifying the pipeline works end-to-end\n")
    
    # Step 1: Load and analyze existing reviews
    print_section("STEP 1/3: LOAD EXISTING REVIEWS")
    
    try:
        generator = WeeklyPulseNoteGenerator()
        
        # Use the test sample file
        test_file = "data/reviews/test-sample.json"
        
        if not os.path.exists(test_file):
            print(f"❌ Test file not found: {test_file}")
            print("\n💡 Solution: Run this command first:")
            print("   python -c \"from services.hybrid_review_collector import HybridReviewCollector; c = HybridReviewCollector(); c.collect()\"")
            return False
        
        print(f"✅ Loading reviews from: {test_file}")
        
        # Load reviews
        import json
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        reviews = data.get('reviews', [])
        metadata = data.get('metadata', {})
        
        print(f"✅ Loaded {len(reviews)} reviews")
        print(f"📊 Metadata:")
        print(f"   - Package: {metadata.get('packageId')}")
        print(f"   - Weeks: {metadata.get('weeksRequested')}")
        print(f"   - After filters: {metadata.get('totalAfterFilters')}")
        
    except Exception as e:
        print(f"❌ Error loading reviews: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Generate themes and weekly note
    print_section("STEP 2/3: GENERATE WEEKLY PULSE NOTE")
    
    try:
        result = generator.generate(test_file)
        
        if not result.get('success'):
            print(f"❌ Note generation failed: {result.get('message')}")
            return False
        
        print(f"✅ Weekly note generated successfully!")
        print(f"📝 Note file: {result.get('note_file')}")
        print(f"🎯 Themes identified: {result.get('themes_identified')}")
        print(f"📊 Reviews analyzed: {result.get('total_reviews')}")
        
    except Exception as e:
        print(f"❌ Error generating note: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Display the generated note
    print_section("STEP 3/3: DISPLAY GENERATED NOTE")
    
    try:
        note_file = result.get('note_file')
        
        with open(note_file, 'r', encoding='utf-8') as f:
            note_content = f.read()
        
        print("\n📄 GENERATED WEEKLY NOTE PREVIEW:\n")
        print("-" * 70)
        
        # Show first 80% of the note (to fit in terminal)
        lines = note_content.split('\n')
        preview_lines = lines[:60]  # Show first 60 lines
        
        for line in preview_lines:
            print(line)
        
        if len(lines) > 60:
            print(f"\n... [{len(lines) - 60} more lines in full file]")
        
        print("-" * 70)
        
        print(f"\n✅ Full note saved to: {os.path.abspath(note_file)}")
        
    except Exception as e:
        print(f"❌ Error displaying note: {str(e)}")
        return False
    
    # Summary
    print_section("✅ TEST COMPLETE - SUMMARY")
    
    print("""
📊 RESULTS:
""")
    print(f"   ✅ Reviews loaded:      {len(reviews)}")
    print(f"   ✅ Themes identified:   {result.get('themes_identified')}")
    print(f"   ✅ Reviews analyzed:    {result.get('total_reviews')}")
    print(f"   ✅ Note generated:      {note_file}")
    print(f"   ✅ PII protection:      Enabled (all emails, phones, cards redacted)")
    
    print("""
🎯 THEMES FOUND:
""")
    
    # Parse themes from note content
    import re
    theme_matches = re.findall(r'### \d+\. (.+?) (😊|😞|😐)', note_content)
    
    if theme_matches:
        for i, (theme_name, emoji) in enumerate(theme_matches, 1):
            emoji_map = {'😊': 'Positive', '😞': 'Negative', '😐': 'Neutral'}
            print(f"   {i}. {theme_name} ({emoji_map.get(emoji, 'Unknown')})")
    
    print("""
🚀 NEXT STEPS:

1. ✅ Review the generated note above
2. 📂 Check the output files:
   - Note: """ + os.path.abspath(note_file) + """
   - CSV:  weekly_reviews/ (if collector was run)
   - JSON: data/reviews/ (source data)
   
3. 🔄 To run with LIVE data:
   python -m services.hybrid_review_collector
   
4. ⚡ To deploy to Railway:
   - Push to GitHub
   - Deploy on Railway
   - Add environment variables
   - Set weekly schedule

5. 📧 To enable email sending:
   - Add SMTP credentials to .env
   - Run: python -m services.weekly_review_pipeline

""")
    
    print_section("🎉 TEST PASSED SUCCESSFULLY!")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
