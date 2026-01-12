"""
Vercel serverless function entry point for FastAPI app
Uses Mangum to wrap FastAPI as an ASGI application
"""
import sys
import os

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from mangum import Mangum
from app.main import app

# Wrap FastAPI app with Mangum for serverless deployment
handler = Mangum(app, lifespan="off")

# Export handler for Vercel
__all__ = ["handler"]
