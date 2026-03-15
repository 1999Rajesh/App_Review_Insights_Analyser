from typing import List, Dict, Optional
import json
from groq import Groq
from app.models.review import Review, ThemeAnalysis, SentimentType
from app.config import settings


class GroqAnalyzer:
    """Analyze app reviews using Groq LLM"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key (defaults to settings.GROQ_API_KEY)
        """
        self.api_key = api_key or settings.GROQ_API_KEY
        self.client = Groq(api_key=self.api_key)
        self.model = settings.GROQ_MODEL
    
    def _format_reviews_for_prompt(self, reviews: List[Review]) -> str:
        """
        Format reviews into a concise string for the LLM prompt.
        
        Args:
            reviews: List of reviews
            
        Returns:
            Formatted string of reviews
        """
        formatted = []
        for i, review in enumerate(reviews[:100], 1):  # Limit to 100 reviews
            formatted.append(
                f"{i}. [{review.rating}★] {review.title} - {review.text[:200]}"
            )
        return "\n".join(formatted)
    
    async def analyze_themes(
        self, 
        reviews: List[Review],
        max_themes: int = 5
    ) -> Dict:
        """
        Analyze reviews and group into themes using LLM.
        
        Args:
            reviews: List of reviews to analyze
            max_themes: Maximum number of themes to identify
            
        Returns:
            Dictionary containing theme analysis results
        """
        if not reviews:
            raise ValueError("No reviews provided for analysis")
        
        # Prepare the prompt
        formatted_reviews = self._format_reviews_for_prompt(reviews)
        
        system_prompt = """You are an expert product analyst analyzing app reviews.
Your task is to identify key themes and provide actionable insights.
Be concise, specific, and avoid generic statements.
Always follow the exact output format provided."""

        user_prompt = f"""
Analyze these {len(reviews)} app reviews from the last {settings.REVIEW_WEEKS_RANGE} weeks.

IDENTIFIED THEMES (group into MAX {max_themes} themes):
Common theme examples:
- Onboarding/Sign-up: Account creation, registration flow, verification
- KYC Verification: Document upload, identity checks, approval delays
- Payments/Transactions: Failed payments, processing issues, fees
- Account Statements: Transaction history, export features, clarity
- Withdrawals/Cash-out: Transfer delays, limits, failures
- Customer Support: Response time, helpfulness, availability
- App Performance/Bugs: Crashes, slowness, technical issues
- UI/UX Issues: Navigation, design confusion, feature discoverability

For EACH theme, provide:
1. Theme name (choose from list above or create specific name)
2. Count of reviews mentioning this theme
3. Overall sentiment (positive/negative/neutral)
4. Top 3 user quotes (exact text from reviews, ≤50 words each)
5. 3 action ideas (specific, actionable improvements)

CONSTRAINTS:
- MAX {max_themes} themes total
- Total output under 250 words
- NO PII (no usernames, emails, phone numbers, account IDs)
- Quotes must be exact text from reviews
- Action items must be specific and implementable

OUTPUT FORMAT (JSON):
{{
  "themes": [
    {{
      "theme_name": "Theme Name",
      "review_count": 25,
      "sentiment": "negative",
      "quotes": ["quote 1", "quote 2", "quote 3"],
      "action_ideas": ["action 1", "action 2", "action 3"]
    }}
  ],
  "total_analyzed": {len(reviews)}
}}

REVIEWS TO ANALYZE:
{formatted_reviews}

Provide your analysis in JSON format:
"""

        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result_text = response.choices[0].message.content.strip()
            result = json.loads(result_text)
            
            # Validate and transform themes
            themes = []
            for theme_data in result.get('themes', [])[:max_themes]:
                theme = ThemeAnalysis(
                    theme_name=theme_data.get('theme_name', 'Unknown'),
                    review_count=theme_data.get('review_count', 0),
                    percentage=0.0,  # Will calculate later
                    sentiment=SentimentType(theme_data.get('sentiment', 'neutral')),
                    quotes=theme_data.get('quotes', [])[:3],
                    action_ideas=theme_data.get('action_ideas', [])[:3]
                )
                themes.append(theme)
            
            # Calculate percentages
            total = sum(t.review_count for t in themes)
            if total > 0:
                for theme in themes:
                    theme.percentage = round(
                        (theme.review_count / total) * 100, 1
                    )
            
            return {
                'themes': themes,
                'total_analyzed': result.get('total_analyzed', len(reviews))
            }
            
        except Exception as e:
            raise Exception(f"Error during LLM analysis: {str(e)}")
    
    def generate_summary(
        self, 
        themes: List[ThemeAnalysis],
        total_reviews: int,
        week_start: str,
        week_end: str
    ) -> str:
        """
        Generate a human-readable weekly summary from theme analysis.
        
        Args:
            themes: List of analyzed themes
            total_reviews: Total number of reviews analyzed
            week_start: Start date of the week
            week_end: End date of the week
            
        Returns:
            Formatted markdown summary (≤250 words)
        """
        # Sort themes by review count (top 3)
        sorted_themes = sorted(
            themes, 
            key=lambda x: x.review_count, 
            reverse=True
        )[:3]
        
        # Build the report
        lines = [
            "# Weekly App Review Pulse",
            f"**Period:** {week_start} to {week_end}",
            f"**Total Reviews Analyzed:** {total_reviews}",
            "",
            "## Top 3 Themes This Week",
            ""
        ]
        
        word_count = len(" ".join(lines).split())
        
        for i, theme in enumerate(sorted_themes, 1):
            theme_header = (
                f"### {i}. {theme.theme_name} - {theme.percentage}% of reviews\n"
            )
            lines.append(theme_header)
            word_count += len(theme_header.split())
            
            sentiment_line = f"**Sentiment:** {theme.sentiment.value.capitalize()}\n"
            lines.append(sentiment_line)
            word_count += len(sentiment_line.split())
            
            # Add quotes
            lines.append("**User Quotes:**")
            word_count += 2
            
            for quote in theme.quotes[:3]:
                quote_line = f"- \"{quote}\""
                lines.append(quote_line)
                word_count += len(quote_line.split())
            
            lines.append("")
            
            # Add action ideas
            lines.append("**Action Ideas:**")
            word_count += 2
            
            for j, action in enumerate(theme.action_ideas[:3], 1):
                action_line = f"{j}. {action}"
                lines.append(action_line)
                word_count += len(action_line.split())
            
            lines.append("")
            
            # Check word count limit
            if word_count >= 230:  # Leave room for footer
                break
        
        # Add footer
        lines.append("---")
        lines.append("*Generated by App Review Insights Analyzer*")
        
        return "\n".join(lines)
