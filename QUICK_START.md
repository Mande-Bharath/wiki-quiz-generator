# Wiki Quiz Generator - Quick Start Guide

## Setup Status
✅ **Backend dependencies installed**
✅ **Frontend dependencies installed**

## Next Steps

### 1. Create Environment Configuration
Create a `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env
```

Then edit `.env` and add your Google Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./quiz_database.db
```

### 2. Start the Backend Server
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

The backend will be available at: `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### 3. Start the Frontend Development Server
In a new terminal:
```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## Project Structure

```
ai-wiki-quiz-generator/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application entry point
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # SQLAlchemy ORM models
│   │   ├── schemas.py        # Pydantic request/response schemas
│   │   ├── scraper.py        # Wikipedia content scraping
│   │   ├── services.py       # LLM quiz generation service
│   │   ├── prompts.py        # LangChain prompt templates
│   │   └── __init__.py
│   ├── llm_test.py           # LLM integration test
│   ├── scraper_test.py       # Scraper test
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment template
│   └── venv/                 # Virtual environment
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GenerateQuizTab.jsx    # Quiz generation interface
│   │   │   ├── HistoryTab.jsx         # Quiz history viewer
│   │   │   ├── QuizDisplay.jsx        # Interactive quiz taker
│   │   │   ├── GenerateQuizTab.css
│   │   │   ├── HistoryTab.css
│   │   │   └── QuizDisplay.css
│   │   ├── App.jsx           # Main application shell
│   │   ├── App.css
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── node_modules/
├── docs/
│   ├── README.md
│   ├── SETUP.md
│   ├── START_HERE.md
│   └── ...
└── sample-data/
    ├── urls.json
    └── sample-outputs/
```

## API Endpoints

- `POST /api/generate-quiz` - Generate a quiz from a Wikipedia URL
- `GET /api/history` - Get quiz history
- `GET /api/quiz/{id}` - Get quiz details by ID
- `GET /api/stats` - Get statistics
- `GET /health` - Health check

## Features

### Generate Quiz Tab
- Input Wikipedia URL
- Automatic content scraping
- LLM-powered quiz generation
- Real-time loading states
- Cache indicators for repeated URLs

### History Tab
- View all generated quizzes
- Quiz metadata (date, title, difficulty)
- Click to view and take quiz
- Modal-based quiz viewer

### Interactive Quiz Taking
- Multiple choice questions
- Real-time answer tracking
- Score calculation
- Answer explanations
- Difficulty badges

## Technology Stack

**Backend:**
- FastAPI 0.104.1
- SQLAlchemy 2.0.23
- Pydantic 2.12.5
- LangChain 1.2.3 + LangChain Google Genai
- Google Gemini API
- BeautifulSoup4 for web scraping

**Frontend:**
- React 18
- Vite build tool
- CSS3 (custom styling, no external UI library)

**Database:**
- SQLite (default)
- PostgreSQL (configurable via DATABASE_URL)

## Testing

### Test LLM Integration
```bash
cd backend
source venv/bin/activate
python llm_test.py
```

### Test Web Scraper
```bash
cd backend
source venv/bin/activate
python scraper_test.py
```

## Troubleshooting

### Port Already in Use
If port 8000 or 5173 is already in use, you can specify different ports:

**Backend:**
```bash
python -m uvicorn app.main:app --reload --port 8001
```

**Frontend:**
Edit `vite.config.js` and change the port in the server config.

### Missing GEMINI_API_KEY
1. Get an API key from [Google AI Studio](https://aistudio.google.com)
2. Add it to your `.env` file
3. Restart the backend server

### Database Issues
To reset the database:
```bash
cd backend
rm quiz_database.db
# Restart the server - it will recreate the database
```

## Documentation

For detailed documentation, see:
- [README.md](README.md) - Full project documentation
- [SETUP.md](docs/SETUP.md) - Detailed setup instructions
- [START_HERE.md](docs/START_HERE.md) - Getting started guide
- [API_ENDPOINTS.md](docs/API_ENDPOINTS.md) - API documentation
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architecture overview

## Support

For issues or questions, refer to the documentation or check the logs:
- **Backend logs:** Console output from uvicorn
- **Frontend logs:** Browser DevTools console
- **Database logs:** Check `quiz_database.db` file

---

Enjoy building amazing quizzes! 🎉
