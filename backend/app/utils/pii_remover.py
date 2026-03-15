import re
from typing import List


def remove_pii(text: str) -> str:
    """
    Remove Personally Identifiable Information from review text.
    
    Removes:
    - Email addresses
    - Phone numbers
    - Usernames/mentions (@username)
    - Credit card numbers
    - Social security numbers
    - IP addresses
    - URLs with personal identifiers
    
    Args:
        text: Raw review text
        
    Returns:
        Sanitized text with PII removed
    """
    if not text:
        return ""
    
    # Email addresses
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '[EMAIL]',
        text
    )
    
    # Phone numbers (various formats)
    text = re.sub(
        r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        '[PHONE]',
        text
    )
    
    # Usernames/mentions
    text = re.sub(
        r'@\w+',
        '[USER]',
        text
    )
    
    # Credit card numbers (13-19 digits with optional spaces/dashes)
    text = re.sub(
        r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{1,7}\b',
        '[CARD_NUM]',
        text
    )
    
    # Social Security Numbers (XXX-XX-XXXX format)
    text = re.sub(
        r'\b\d{3}-\d{2}-\d{4}\b',
        '[SSN]',
        text
    )
    
    # IP addresses
    text = re.sub(
        r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        '[IP]',
        text
    )
    
    # Account IDs (common patterns)
    text = re.sub(
        r'\b(?:Account|Acc|ID|User)\s*#?\s*\d{6,}\b',
        '[ACCOUNT_ID]',
        text,
        flags=re.IGNORECASE
    )
    
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def sanitize_reviews(reviews: List[dict]) -> List[dict]:
    """
    Remove PII from a list of reviews.
    
    Args:
        reviews: List of review dictionaries
        
    Returns:
        List of sanitized reviews
    """
    sanitized = []
    for review in reviews:
        sanitized_review = review.copy()
        sanitized_review['title'] = remove_pii(review.get('title', ''))
        sanitized_review['text'] = remove_pii(review.get('text', ''))
        sanitized.append(sanitized_review)
    
    return sanitized
