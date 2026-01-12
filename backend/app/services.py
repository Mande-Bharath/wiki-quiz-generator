"""
Services for quiz generation using LangChain and LLM
"""
import json
import logging
from typing import Dict, List, Tuple
from langchain_google_genai import ChatGoogleGenerativeAI
from app.prompts import QUIZ_GENERATION_PROMPT, RELATED_TOPICS_PROMPT, SUMMARY_PROMPT
from app.config import settings

logger = logging.getLogger(__name__)


class QuizGenerationService:
    """Service for generating quizzes using LLM"""
    
    def __init__(self):
        """Initialize the LLM"""
        # Allow model to be configured via environment (useful if quota prevents a model)
        model = getattr(settings, "LLM_MODEL", "gemini-2.0-flash")
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
            max_tokens=2000
        )
    
    def generate_quiz(self, title: str, content: str) -> Dict:
        """
        Generate a quiz from article content using LLM
        
        Args:
            title: Article title
            content: Article content text
            
        Returns:
            Dictionary with quiz questions
        """
        try:
            # Generate quiz questions
            prompt_value = QUIZ_GENERATION_PROMPT.invoke(
                {"title": title, "content": content[:8000]}  # Limit content to avoid token limits
            )
            
            response = self.llm.invoke(prompt_value)
            response_text = response.content.strip()
            
            # Parse JSON response
            # Try to extract JSON from response
            quiz_data = self._parse_json_response(response_text)
            
            if not quiz_data or "questions" not in quiz_data:
                logger.error(f"Invalid quiz response format. Response length: {len(response_text)}")
                logger.error(f"Response preview (first 500 chars): {response_text[:500]}")
                logger.error(f"Parsed quiz_data: {quiz_data}")
                raise ValueError("Failed to generate valid quiz format")
            
            return quiz_data
            
        except Exception as e:
            # Detect quota / ResourceExhausted style errors and propagate a clear message
            msg = str(e)
            low = msg.lower()
            if "quota" in low or "resourceexhausted" in low or "exceeded" in low:
                logger.error(f"LLM quota error: {e}")
                raise RuntimeError("LLM_QUOTA_EXCEEDED: Gemini quota exhausted or model unavailable. Check GEMINI_API_KEY, billing, or switch LLM_MODEL in config.")
            logger.error(f"Error generating quiz: {e}")
            raise
    
    def generate_related_topics(self, title: str, content: str) -> List[str]:
        """
        Extract related topics from article content
        
        Args:
            title: Article title
            content: Article content text
            
        Returns:
            List of related topics
        """
        try:
            prompt_value = RELATED_TOPICS_PROMPT.invoke(
                {"title": title, "content": content[:8000]}
            )
            
            response = self.llm.invoke(prompt_value)
            response_text = response.content.strip()
            
            # Parse JSON response
            topics_data = self._parse_json_response(response_text)
            
            if topics_data and "related_topics" in topics_data:
                return topics_data["related_topics"]
            
            return []
            
        except Exception as e:
            msg = str(e).lower()
            if "quota" in msg or "resourceexhausted" in msg or "exceeded" in msg:
                logger.error(f"LLM quota error while generating topics: {e}")
                # propagate to caller to surface a 503
                raise RuntimeError("LLM_QUOTA_EXCEEDED: Gemini quota exhausted or model unavailable.")
            logger.error(f"Error generating related topics: {e}")
            return []
    
    def generate_summary(self, title: str, content: str) -> str:
        """
        Generate a brief summary of the article
        
        Args:
            title: Article title
            content: Article content text
            
        Returns:
            Summary text
        """
        try:
            prompt_value = SUMMARY_PROMPT.invoke(
                {"title": title, "content": content[:4000]}
            )
            
            response = self.llm.invoke(prompt_value)
            return response.content.strip()
            
        except Exception as e:
            msg = str(e).lower()
            if "quota" in msg or "resourceexhausted" in msg or "exceeded" in msg:
                logger.error(f"LLM quota error while generating summary: {e}")
                raise RuntimeError("LLM_QUOTA_EXCEEDED: Gemini quota exhausted or model unavailable.")
            logger.error(f"Error generating summary: {e}")
            return f"Article about {title}"
    
    @staticmethod
    def _parse_json_response(response_text: str) -> Dict:
        """
        Parse JSON from LLM response
        
        Tries to extract JSON from various formats that LLM might return
        """
        try:
            # Try direct JSON parsing
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Try to extract JSON from code blocks
        if "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Last resort: try to find JSON object in response
        import re
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        logger.error(f"Could not parse JSON from response. Length: {len(response_text)}")
        logger.error(f"Response preview (first 500 chars): {response_text[:500]}")
        return {}
