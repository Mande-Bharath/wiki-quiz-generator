"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime


class QuestionOption(BaseModel):
    """Single quiz question"""
    question: str
    options: List[str]
    answer: str
    difficulty: str  # easy, medium, hard
    explanation: str


class QuizResponse(BaseModel):
    """Full quiz response"""
    questions: List[QuestionOption]
    related_topics: Optional[List[str]] = []
    summary: Optional[str] = None


class QuizGenerateRequest(BaseModel):
    """Request to generate a quiz from a Wikipedia URL"""
    url: HttpUrl


class QuizHistoryItem(BaseModel):
    """Single quiz item in history"""
    id: int
    url: str
    title: str
    article_preview: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuizHistoryResponse(BaseModel):
    """Response for history list endpoint"""
    quizzes: List[QuizHistoryItem]
    total_count: int


class QuizDetailResponse(BaseModel):
    """Full quiz detail response"""
    id: int
    url: str
    title: str
    article_preview: str
    quiz_data: dict
    related_topics: List[str]
    created_at: datetime

    class Config:
        from_attributes = True
