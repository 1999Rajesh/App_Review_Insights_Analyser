from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class Review(BaseModel):
    """Individual app review model"""
    
    id: str
    source: str = Field(..., description="App Store or Play Store")
    rating: int = Field(..., ge=1, le=5)
    title: str = Field(default='', description="Review title (optional, often empty)")
    text: str
    date: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "rev_001",
                "source": "App Store",
                "rating": 4,
                "title": "",  # Title is optional
                "text": "Love the interface but withdrawals are slow",
                "date": "2026-03-01T10:00:00"
            }
        }


class ThemeAnalysis(BaseModel):
    """Theme analysis result"""
    
    theme_name: str
    review_count: int
    percentage: float
    sentiment: SentimentType
    quotes: list[str] = Field(..., max_length=3)
    action_ideas: list[str] = Field(..., max_length=3)


class WeeklyReport(BaseModel):
    """Weekly pulse report"""
    
    id: str
    week_start: datetime
    week_end: datetime
    total_reviews: int
    top_themes: list[ThemeAnalysis] = Field(..., max_length=3)
    generated_at: datetime = Field(default_factory=datetime.now)
    word_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "report_001",
                "week_start": "2026-02-26T00:00:00",
                "week_end": "2026-03-04T23:59:59",
                "total_reviews": 127,
                "top_themes": [],
                "generated_at": "2026-03-05T10:00:00",
                "word_count": 245
            }
        }
