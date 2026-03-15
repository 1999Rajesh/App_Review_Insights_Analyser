from typing import List, Dict
from app.models.review import Review


def select_best_quotes(
    reviews: List[Review], 
    count: int = 3,
    max_words: int = 50
) -> List[str]:
    """
    Select the best user quotes from reviews based on quality criteria.
    
    Selection criteria:
    - Clarity and specificity
    - Emotional impact
    - Recent reviews prioritized
    - Extreme ratings (1-star or 5-star) weighted higher
    - Avoid duplicates and overly long quotes
    
    Args:
        reviews: List of reviews to select from
        count: Number of quotes to select (default: 3)
        max_words: Maximum words per quote (default: 50)
        
    Returns:
        List of selected quote strings
    """
    from datetime import datetime
    
    if not reviews:
        return []
    
    # Score each review
    scored_reviews = []
    now = datetime.now()
    
    for review in reviews:
        score = 0
        
        # Recency score (newer is better)
        days_old = (now - review.date).days
        recency_score = max(0, 100 - days_old)
        score += recency_score * 0.4
        
        # Rating extremity score (1-star and 5-star are more impactful)
        if review.rating == 1:
            score += 30  # Very negative reviews often highlight issues
        elif review.rating == 5:
            score += 25  # Positive reviews show what works
        elif review.rating == 2:
            score += 20
        elif review.rating == 4:
            score += 15
        else:  # 3 stars
            score += 5
        
        # Content quality score
        combined_text = f"{review.title} {review.text}".strip()
        word_count = len(combined_text.split())
        
        # Prefer substantive but concise reviews
        if 10 <= word_count <= max_words:
            score += 20
        elif word_count < 10:
            score += 5
        else:
            score += 10
        
        # Specificity bonus (reviews with specific details)
        specific_keywords = [
            'slow', 'fast', 'easy', 'difficult', 'broken', 'fixed',
            'issue', 'problem', 'love', 'hate', 'best', 'worst',
            'feature', 'update', 'change', 'improve'
        ]
        text_lower = combined_text.lower()
        if any(keyword in text_lower for keyword in specific_keywords):
            score += 15
        
        scored_reviews.append({
            'review': review,
            'score': score,
            'text': combined_text
        })
    
    # Sort by score (highest first)
    scored_reviews.sort(key=lambda x: x['score'], reverse=True)
    
    # Select top quotes, avoiding duplicates
    selected_quotes = []
    seen_texts = set()
    
    for item in scored_reviews:
        if len(selected_quotes) >= count:
            break
        
        # Clean and truncate quote
        quote = item['text'].strip()
        
        # Skip if too similar to already selected quote
        if quote in seen_texts:
            continue
        
        # Truncate to max words if needed
        words = quote.split()
        if len(words) > max_words:
            quote = ' '.join(words[:max_words]) + '...'
        
        selected_quotes.append(quote)
        seen_texts.add(quote)
    
    return selected_quotes
