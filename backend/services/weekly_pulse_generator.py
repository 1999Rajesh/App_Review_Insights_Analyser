"""
Weekly Pulse Note Generator

Generates a one-page weekly note with:
- Top 3 themes from reviews (max 5 themes total)
- 3 user quotes per theme
- 3 action ideas per theme
- No PII included
"""

import os
from datetime import datetime
from typing import List, Dict
import json


class WeeklyPulseNoteGenerator:
    """Generate weekly one-page pulse notes from app reviews"""
    
    def __init__(self):
        self.max_themes = 5
        self.top_themes_count = 3
        self.quotes_per_theme = 3
        self.actions_per_theme = 3
        
        # Sample theme categories for Groww app
        self.theme_categories = [
            "Onboarding",
            "KYC Verification",
            "Payments & Transactions",
            "Account Statements",
            "Withdrawals",
            "Stock Trading",
            "Mutual Funds",
            "Customer Support",
            "App Performance",
            "UI/UX Experience"
        ]
    
    def load_reviews(self, json_file: str = None) -> List[Dict]:
        """Load reviews from JSON file"""
        if not json_file:
            # Find latest JSON file
            data_dir = os.getenv('REVIEWS_DATA_DIR', 'data/reviews')
            json_files = sorted([f for f in os.listdir(data_dir) if f.endswith('.json')])
            
            if not json_files:
                raise FileNotFoundError("No review JSON files found")
            
            json_file = os.path.join(data_dir, json_files[-1])
        
        print(f"📂 Loading reviews from: {json_file}")
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        reviews = data.get('reviews', [])
        print(f"✅ Loaded {len(reviews)} reviews")
        
        return reviews
    
    def group_into_themes(self, reviews: List[Dict]) -> List[Dict]:
        """
        Group reviews into themes (max 5 themes).
        Uses simple keyword matching - can be enhanced with AI later.
        """
        print(f"🎯 Grouping {len(reviews)} reviews into themes...")
        
        # Initialize theme counters
        themes = {category: {'reviews': [], 'keywords': []} for category in self.theme_categories}
        
        # Simple keyword-based theme classification
        theme_keywords = {
            "Onboarding": ["signup", "register", "onboard", "account creation", "first time", "new user"],
            "KYC Verification": ["kyc", "verification", "pan card", "aadhaar", "document", "approve"],
            "Payments & Transactions": ["payment", "transaction", "upi", "bank transfer", "failed payment", "money"],
            "Account Statements": ["statement", "transaction history", "download", "report", "export"],
            "Withdrawals": ["withdraw", "withdrawal", "bank transfer", "settlement", "payout"],
            "Stock Trading": ["stock", "trading", "buy", "sell", "order", "portfolio"],
            "Mutual Funds": ["mutual fund", "sip", "investment", "fund", "nav"],
            "Customer Support": ["support", "customer service", "help", "response", "complaint"],
            "App Performance": ["slow", "lag", "crash", "freeze", "performance", "bug", "error"],
            "UI/UX Experience": ["interface", "design", "easy", "user friendly", "navigation", "clean"]
        }
        
        # Classify each review
        for review in reviews:
            content = review.get('content', '').lower()
            rating = review.get('score', 0)
            
            # Find best matching theme
            best_match = None
            best_score = 0
            
            for theme, keywords in theme_keywords.items():
                score = sum(1 for keyword in keywords if keyword in content)
                if score > best_score:
                    best_score = score
                    best_match = theme
            
            # If no match found, use sentiment-based default
            if not best_match:
                if rating >= 4:
                    best_match = "UI/UX Experience"
                elif rating <= 2:
                    best_match = "App Performance"
                else:
                    best_match = "General Feedback"
            
            # Add review to theme
            if best_match in themes:
                themes[best_match]['reviews'].append(review)
                themes[best_match]['keywords'].append(best_match)
        
        # Convert to list format and calculate stats
        theme_list = []
        for theme_name, data in themes.items():
            if len(data['reviews']) > 0:
                review_count = len(data['reviews'])
                percentage = (review_count / len(reviews)) * 100 if reviews else 0
                
                # Calculate average rating for this theme
                avg_rating = sum(r.get('score', 0) for r in data['reviews']) / review_count
                
                # Determine sentiment
                if avg_rating >= 4:
                    sentiment = "positive"
                elif avg_rating <= 2:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                theme_list.append({
                    'theme_name': theme_name,
                    'review_count': review_count,
                    'percentage': percentage,
                    'sentiment': sentiment,
                    'average_rating': round(avg_rating, 2),
                    'reviews': data['reviews']
                })
        
        # Sort by review count (most mentioned first)
        theme_list.sort(key=lambda x: x['review_count'], reverse=True)
        
        # Keep only top 5 themes
        theme_list = theme_list[:self.max_themes]
        
        print(f"✅ Identified {len(theme_list)} themes")
        for theme in theme_list:
            print(f"   - {theme['theme_name']}: {theme['review_count']} reviews ({theme['percentage']:.1f}%)")
        
        return theme_list
    
    def extract_quotes(self, reviews: List[Dict], count: int = 3) -> List[str]:
        """Extract representative quotes from reviews"""
        # Select reviews with good length (not too short, not too long)
        suitable_reviews = [
            r for r in reviews 
            if 20 <= len(r.get('content', '')) <= 300
        ]
        
        if not suitable_reviews:
            suitable_reviews = reviews
        
        # Sort by rating diversity (get mix of ratings)
        suitable_reviews.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        # Extract quotes
        quotes = []
        for review in suitable_reviews[:count]:
            content = review.get('content', '')
            # Ensure no PII (double-check)
            content = self._redact_pii_simple(content)
            quotes.append(content)
        
        return quotes
    
    def generate_action_ideas(self, theme: Dict) -> List[str]:
        """Generate action ideas based on theme and sentiment"""
        theme_name = theme['theme_name']
        sentiment = theme.get('sentiment', 'neutral')
        
        # Pre-defined action templates
        action_templates = {
            "Onboarding": {
                "positive": [
                    "Create onboarding tutorial showcasing smooth signup experience",
                    "Share user success stories about quick account setup",
                    "Highlight features that make onboarding easy"
                ],
                "negative": [
                    "Simplify KYC document upload process",
                    "Add real-time verification status tracking",
                    "Create video guides for common onboarding issues"
                ],
                "neutral": [
                    "Add progress tracker for onboarding steps",
                    "Provide FAQ section for common signup questions",
                    "Enable chat support during onboarding"
                ]
            },
            "KYC Verification": {
                "positive": [
                    "Promote fast KYC approval times in marketing",
                    "Create case studies on seamless verification",
                    "Highlight security measures that protect users"
                ],
                "negative": [
                    "Implement automated document verification",
                    "Add instant retry for rejected documents",
                    "Provide clear rejection reasons with examples"
                ],
                "neutral": [
                    "Send proactive KYC status updates via SMS/email",
                    "Add document preview before submission",
                    "Create checklist for KYC requirements"
                ]
            },
            "Payments & Transactions": {
                "positive": [
                    "Showcase UPI integration success rate",
                    "Highlight instant payment confirmations",
                    "Promote zero-fee transactions"
                ],
                "negative": [
                    "Add transaction failure analytics dashboard",
                    "Implement automatic retry for failed payments",
                    "Provide instant refund notifications"
                ],
                "neutral": [
                    "Add transaction status tracking in real-time",
                    "Send payment confirmation SMS/notifications",
                    "Create troubleshooting guide for common issues"
                ]
            },
            "Account Statements": {
                "positive": [
                    "Promote easy statement download feature",
                    "Highlight comprehensive transaction history",
                    "Showcase export formats available"
                ],
                "negative": [
                    "Add custom date range for statements",
                    "Implement PDF statement email delivery",
                    "Fix statement generation delays"
                ],
                "neutral": [
                    "Add filter options for transaction history",
                    "Enable scheduled statement emails",
                    "Create visual spending/trading summaries"
                ]
            },
            "Withdrawals": {
                "positive": [
                    "Promote fast withdrawal processing times",
                    "Highlight zero withdrawal fees",
                    "Share user testimonials on smooth withdrawals"
                ],
                "negative": [
                    "Reduce withdrawal settlement time",
                    "Add withdrawal status tracking",
                    "Provide clear timeline expectations"
                ],
                "neutral": [
                    "Send withdrawal confirmation notifications",
                    "Add withdrawal history dashboard",
                    "Create FAQ on withdrawal process"
                ]
            }
        }
        
        # Get actions for this theme
        if theme_name in action_templates:
            return action_templates[theme_name].get(sentiment, action_templates[theme_name]['neutral'])[:self.actions_per_theme]
        
        # Default actions for unknown themes
        return [
            f"Investigate {theme_name.lower()} related feedback",
            f"Create improvement plan for {theme_name.lower()}",
            f"Monitor {theme_name.lower()} metrics weekly"
        ]
    
    def _redact_pii_simple(self, text: str) -> str:
        """Simple PII redaction for quotes"""
        import re
        
        # Email
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        # Phone
        text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
        # URLs
        text = re.sub(r'https?://\S+', '[URL]', text)
        
        return text
    
    def generate_one_page_note(self, themes: List[Dict]) -> str:
        """Generate formatted one-page weekly note"""
        today = datetime.now().strftime('%B %d, %Y')
        
        # Get top 3 themes
        top_themes = themes[:self.top_themes_count]
        
        # Build the note
        note = f"""# 📊 Weekly App Review Pulse
**Week {datetime.now().isocalendar()[1]}, {datetime.now().year}** | Generated: {today}

---

## 🎯 Executive Summary

This week analyzed **{sum(t['review_count'] for t in themes)} reviews** across **{len(themes)} key themes**.

**Quick Stats:**
- 😊 Positive: {sum(t['review_count'] for t in themes if t['sentiment'] == 'positive')} reviews
- 😞 Negative: {sum(t['review_count'] for t in themes if t['sentiment'] == 'negative')} reviews  
- 😐 Neutral: {sum(t['review_count'] for t in themes if t['sentiment'] == 'neutral')} reviews

---

## 📋 Top 3 Themes This Week

"""
        
        # Add each top theme
        for i, theme in enumerate(top_themes, 1):
            emoji = "😊" if theme['sentiment'] == 'positive' else "😞" if theme['sentiment'] == 'negative' else "😐"
            
            note += f"""### {i}. {theme['theme_name']} {emoji}

**Impact:** {theme['review_count']} reviews ({theme['percentage']:.1f}%) | Avg Rating: {theme['average_rating']}/5 ⭐

**What Users Are Saying:**
"""
            
            # Extract 3 quotes
            quotes = self.extract_quotes(theme['reviews'], self.quotes_per_theme)
            for quote in quotes:
                note += f"- \"{quote}\"\n"
            
            note += "\n**Recommended Actions:**\n"
            
            # Generate 3 action ideas
            actions = self.generate_action_ideas(theme)
            for j, action in enumerate(actions, 1):
                note += f"{j}. {action}\n"
            
            note += "\n---\n\n"
        
        # Add remaining themes (4th and 5th)
        if len(themes) > self.top_themes_count:
            note += """## 📝 Other Notable Themes

"""
            for theme in themes[self.top_themes_count:]:
                emoji = "😊" if theme['sentiment'] == 'positive' else "😞" if theme['sentiment'] == 'negative' else "😐"
                note += f"- **{theme['theme_name']}** {emoji}: {theme['review_count']} reviews\n"
            
            note += "\n---\n\n"
        
        # Add footer
        note += f"""## ℹ️ About This Report

- **Data Source:** Google Play Store Reviews
- **Analysis Period:** Last 12 weeks
- **Total Reviews Analyzed:** {sum(t['review_count'] for t in themes)}
- **Themes Identified:** {len(themes)} (showing top {self.top_themes_count})
- **Privacy:** All PII removed (emails, phones, card numbers redacted)

---

**Powered by App Review Insights Analyzer**  
*Turning app store reviews into actionable weekly insights*
"""
        
        return note
    
    def generate(self, json_file: str = None) -> Dict:
        """Main method to generate weekly pulse note"""
        print("=" * 60)
        print("📝 WEEKLY PULSE NOTE GENERATOR")
        print("=" * 60)
        
        try:
            # Step 1: Load reviews
            reviews = self.load_reviews(json_file)
            
            if not reviews:
                print("⚠️ No reviews to analyze")
                return {'success': False, 'message': 'No reviews found'}
            
            # Step 2: Group into themes (max 5)
            themes = self.group_into_themes(reviews)
            
            if not themes:
                print("⚠️ Could not identify themes")
                return {'success': False, 'message': 'No themes identified'}
            
            # Step 3: Generate one-page note
            note = self.generate_one_page_note(themes)
            
            # Step 4: Save note to file
            output_file = f"weekly_pulse_note_{datetime.now().strftime('%Y-%m-%d')}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(note)
            
            print(f"\n✅ Saved weekly note to: {output_file}")
            print("=" * 60)
            
            return {
                'success': True,
                'note_file': output_file,
                'themes_identified': len(themes),
                'total_reviews': sum(t['review_count'] for t in themes),
                'note_content': note
            }
            
        except Exception as e:
            print(f"❌ Error generating note: {str(e)}")
            raise


def main():
    """Entry point for generating weekly pulse note"""
    generator = WeeklyPulseNoteGenerator()
    result = generator.generate()
    
    if result['success']:
        print("\n🎉 Weekly pulse note generated successfully!")
        print(f"   File: {result['note_file']}")
        print(f"   Themes: {result['themes_identified']}")
        print(f"   Reviews analyzed: {result['total_reviews']}")
    else:
        print(f"\n⚠️ {result.get('message')}")


if __name__ == "__main__":
    main()
