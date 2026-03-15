from typing import List, Dict
from app.models.review import Review
from app.config import settings
import google.generativeai as genai
import json


class GeminiAnalyzer:
    """Analyze reviews using Google Gemini LLM"""
    
    def __init__(self):
        """Initialize Gemini client with API key"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    async def analyze_themes(self, reviews: List[Review], max_themes: int = 5) -> Dict:
        """
        Analyze reviews and extract themes using Gemini.
        
        Args:
            reviews: List of sanitized reviews
            max_themes: Maximum number of themes to extract
            
        Returns:
            Dictionary containing themes analysis
        """
        if not reviews:
            return {"themes": [], "error": "No reviews to analyze"}
        
        # Prepare review texts for analysis
        review_texts = [f"- Rating: {r.rating}/5, Review: {r.text}" for r in reviews]
        reviews_text = "\n".join(review_texts)
        
        # Create prompt for Gemini
        prompt = f"""
Analyze these {len(reviews)} app reviews from the last {settings.REVIEW_WEEKS_RANGE} weeks.

REVIEWS:
{reviews_text}

TASK:
Group into MAX {max_themes} themes. For each theme provide:
1. Theme name (short, descriptive title)
2. Number of reviews mentioning this theme
3. Percentage of total reviews
4. Sentiment: positive, negative, or neutral
5. Up to 3 direct user quotes from the reviews
6. Three actionable ideas for improvement

CONSTRAINTS:
- Maximum {max_themes} themes only
- Total response under {settings.MAX_WORDS} words
- NO PII (personally identifiable information) in output
- Use exact user quotes when possible
- Focus on actionable insights

Respond in valid JSON format with this structure:
{{
  "themes": [
    {{
      "theme_name": "string",
      "review_count": number,
      "percentage": number,
      "sentiment": "positive|negative|neutral",
      "quotes": ["quote1", "quote2", "quote3"],
      "action_ideas": ["idea1", "idea2", "idea3"]
    }}
  ]
}}
"""
        
        try:
            # Call Gemini API
            response = await self._generate_with_retry(prompt)
            
            if not response or not response.text:
                return {"themes": [], "error": "Empty response from Gemini"}
            
            # Parse JSON response
            result = self._parse_gemini_response(response.text)
            
            # Validate and convert to ThemeAnalysis objects
            validated_themes = self._validate_themes(result.get('themes', []))
            
            return {
                'themes': validated_themes,
                'total_reviews': len(reviews),
                'model_used': settings.GEMINI_MODEL
            }
            
        except Exception as e:
            error_msg = str(e)
            if "API_KEY_INVALID" in error_msg or "403" in error_msg:
                raise Exception(f"Gemini API authentication failed. Check your API key. Error: {error_msg}")
            elif "quota" in error_msg.lower():
                raise Exception(f"Gemini API quota exceeded. Error: {error_msg}")
            else:
                raise Exception(f"Error during Gemini analysis: {error_msg}")
    
    async def _generate_with_retry(self, prompt: str, max_retries: int = 3):
        """Generate response with retry logic for rate limits"""
        import asyncio
        
        for attempt in range(max_retries):
            try:
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: self.model.generate_content(prompt)
                )
                return response
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                # Wait before retrying (exponential backoff)
                await asyncio.sleep(2 ** attempt)
    
    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini's text response to extract JSON"""
        import re
        
        # Try to find JSON in response (Gemini sometimes wraps it in markdown)
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', response_text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try parsing the entire response as JSON
            json_str = response_text.strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, try to extract what we can
            print(f"Warning: Could not parse full JSON from Gemini response: {e}")
            print(f"Raw response: {response_text[:500]}...")
            
            # Return empty themes if parsing fails
            return {"themes": []}
    
    def _validate_themes(self, themes_data: List[Dict]) -> List[Dict]:
        """Validate and clean themes data"""
        validated = []
        
        for theme in themes_data:
            try:
                # Ensure required fields exist with defaults
                validated_theme = {
                    'theme_name': str(theme.get('theme_name', 'Unknown Theme')),
                    'review_count': int(theme.get('review_count', 0)),
                    'percentage': float(theme.get('percentage', 0)),
                    'sentiment': str(theme.get('sentiment', 'neutral')).lower(),
                    'quotes': list(theme.get('quotes', []))[:3],  # Max 3 quotes
                    'action_ideas': list(theme.get('action_ideas', []))[:3]  # Max 3 ideas
                }
                
                # Validate sentiment values
                if validated_theme['sentiment'] not in ['positive', 'negative', 'neutral']:
                    validated_theme['sentiment'] = 'neutral'
                
                validated.append(validated_theme)
                
            except (ValueError, TypeError) as e:
                print(f"Warning: Skipping invalid theme data: {e}")
                continue
        
        # Sort by review count (descending) and limit to max_themes
        validated.sort(key=lambda x: x['review_count'], reverse=True)
        
        return validated[:settings.MAX_THEMES]
    
    async def generate_weekly_report(self, reviews: List[Review]) -> Dict:
        """
        Generate a weekly pulse report from analyzed themes.
        
        Args:
            reviews: List of sanitized reviews
            
        Returns:
            Weekly report dictionary
        """
        # First get theme analysis
        analysis = await self.analyze_themes(reviews)
        
        if 'error' in analysis or not analysis.get('themes'):
            return {"error": "Could not generate report: No themes identified"}
        
        themes = analysis['themes']
        
        # Select top 3 themes for the report
        top_themes = themes[:3]
        
        # Calculate word count
        word_count = sum(
            len(theme['theme_name'].split()) +
            len(theme['action_ideas']) * 5  # Estimate 5 words per action idea
            for theme in top_themes
        )
        
        return {
            'top_themes': top_themes,
            'total_reviews': len(reviews),
            'generated_at': datetime.now().isoformat(),
            'word_count': min(word_count, settings.MAX_WORDS),
            'model_used': settings.GEMINI_MODEL
        }


# Import datetime
from datetime import datetime
