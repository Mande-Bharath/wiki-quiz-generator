"""
Main FastAPI application
"""
import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db, engine, Base, QuizRecord
from app.schemas import QuizGenerateRequest, QuizDetailResponse, QuizHistoryResponse, QuizHistoryItem
from app.scraper import scrape_wikipedia
from app.services import QuizGenerationService
from app.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Wiki Quiz Generator",
    description="Generate quizzes from Wikipedia articles using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
quiz_service = QuizGenerationService()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/generate-quiz")
async def generate_quiz(
    request: QuizGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a quiz from a Wikipedia article URL
    
    Steps:
    1. Scrape the Wikipedia article
    2. Generate quiz using LLM
    3. Generate related topics
    4. Store in database
    5. Return quiz data
    """
    try:
        url_str = str(request.url)
        
        # Check if URL already exists in database (caching)
        existing = db.query(QuizRecord).filter(QuizRecord.url == url_str).first()
        if existing:
            logger.info(f"Found cached quiz for {url_str}")
            return {
                "id": existing.id,
                "url": existing.url,
                "title": existing.title,
                "article_preview": existing.article_preview,
                "quiz_data": existing.quiz_data,
                "related_topics": existing.related_topics,
                "created_at": existing.created_at,
                "cached": True
            }
        
        # Step 1: Scrape Wikipedia
        logger.info(f"Scraping Wikipedia article: {url_str}")
        scraped_data = scrape_wikipedia(url_str)
        
        # Extract title and content
        title = scraped_data["title"]
        content = scraped_data["content"]
        raw_html = scraped_data.get("raw_html")
        
        # Create preview (first 500 chars)
        preview = content[:500] if len(content) > 500 else content
        
        # Step 2: Generate quiz
        logger.info(f"Generating quiz for {title}")
        quiz_data = quiz_service.generate_quiz(title, content)
        
        # Step 3: Generate related topics
        logger.info(f"Generating related topics for {title}")
        related_topics = quiz_service.generate_related_topics(title, content)
        
        # Step 4: Store in database
        logger.info(f"Storing quiz in database")
        db_record = QuizRecord(
            url=url_str,
            title=title,
            article_preview=preview,
            quiz_data=quiz_data,
            related_topics=related_topics,
            raw_html=raw_html
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        logger.info(f"Quiz generated and stored successfully")
        
        # Return response
        return {
            "id": db_record.id,
            "url": db_record.url,
            "title": db_record.title,
            "article_preview": db_record.article_preview,
            "quiz_data": db_record.quiz_data,
            "related_topics": db_record.related_topics,
            "created_at": db_record.created_at,
            "cached": False
        }
        
    except Exception as e:
        logger.error(f"Error generating quiz: {e}", exc_info=True)
        # Surface LLM quota errors as 503 Service Unavailable with guidance
        if isinstance(e, RuntimeError) and str(e).startswith("LLM_QUOTA_EXCEEDED"):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=("LLM quota exhausted or model unavailable. Check GEMINI_API_KEY, enable billing for your Google Cloud project, "
                        "or set a different LLM_MODEL in backend/.env (e.g. gemini-1.5-mini)."))

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing Wikipedia article: {str(e)}"
        )


@app.get("/api/history")
async def get_quiz_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get list of previously generated quizzes
    """
    try:
        total = db.query(QuizRecord).count()
        quizzes = db.query(QuizRecord).order_by(
            QuizRecord.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        items = [
            QuizHistoryItem(
                id=q.id,
                url=q.url,
                title=q.title,
                article_preview=q.article_preview,
                created_at=q.created_at
            )
            for q in quizzes
        ]
        
        return QuizHistoryResponse(quizzes=items, total_count=total)
        
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error fetching quiz history"
        )


@app.get("/api/quiz/{quiz_id}")
async def get_quiz_detail(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    """
    Get full details of a specific quiz
    """
    try:
        quiz = db.query(QuizRecord).filter(QuizRecord.id == quiz_id).first()
        
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz not found"
            )
        
        return QuizDetailResponse(
            id=quiz.id,
            url=quiz.url,
            title=quiz.title,
            article_preview=quiz.article_preview,
            quiz_data=quiz.quiz_data,
            related_topics=quiz.related_topics or [],
            created_at=quiz.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching quiz detail: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error fetching quiz details"
        )


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """
    Get statistics about generated quizzes
    """
    try:
        total_quizzes = db.query(QuizRecord).count()
        
        return {
            "total_quizzes": total_quizzes,
            "database_status": "operational"
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error fetching statistics"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
