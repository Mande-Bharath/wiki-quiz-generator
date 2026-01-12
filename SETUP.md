# Wiki Quiz Generator - Detailed Setup Guide

This document provides step-by-step instructions for setting up and running the Wiki Quiz Generator application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16 or higher**: [Download Node.js](https://nodejs.org/)
- **Git**: [Download Git](https://git-scm.com/)
- **Google Gemini API Key**: Get it free from [ai.google.dev](https://ai.google.dev)

### Verify Installations

```bash
# Check Python version
python3 --version

# Check Node.js version
node --version

# Check npm version
npm --version
```

---

## Step 1: Prepare the Environment

### 1.1 Navigate to Project Directory

```bash
cd /Users/mandebharath/Documents/project7890/ai-wiki-quiz-generator
```

### 1.2 Get Your Google Gemini API Key

1. Visit [https://ai.google.dev](https://ai.google.dev)
2. Click "Get API Key"
3. Create a new project or use existing
4. Copy your API key
5. Keep it safe - you'll need it in the next steps

---

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# On Windows, use:
# venv\Scripts\activate
```

You should see `(venv)` at the beginning of your terminal prompt.

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (web framework)
- SQLAlchemy (database ORM)
- Pydantic (data validation)
- LangChain and Gemini libraries (LLM integration)
- BeautifulSoup4 (web scraping)
- All other required packages

### 2.4 Create Environment Configuration

```bash
# Copy the example environment file
cp ../.env.example .env
```

### 2.5 Add Your API Key

Edit the `.env` file:

```bash
# Using nano or your preferred editor
nano .env
```

Replace `your_api_key_here` with your actual Google Gemini API key:

```
GEMINI_API_KEY=sk-api-key-from-ai-google-dev
```

Save the file (Ctrl+O, Enter, Ctrl+X if using nano).

### 2.6 Test the Backend Setup

```bash
# Test the scraper
python scraper_test.py

# You should see output like:
# TITLE:
# China
# 
# CONTENT PREVIEW (first 500 chars):
# China is a country in East Asia...
```

### 2.7 Start the Backend Server

```bash
# From the backend directory with venv activated
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

**Leave this terminal running** and open a new terminal for the frontend.

---

## Step 3: Frontend Setup

### 3.1 Open New Terminal and Navigate to Frontend

```bash
# In a new terminal window
cd /Users/mandebharath/Documents/project7890/ai-wiki-quiz-generator/frontend
```

### 3.2 Install Dependencies

```bash
npm install
```

This will create a `node_modules` directory with all React and Vite dependencies.

### 3.3 Start the Frontend Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

---

## Step 4: Access the Application

1. Open your web browser
2. Go to `http://localhost:5173`
3. You should see the Wiki Quiz Generator interface

### Tab 1: Generate Quiz

1. Copy a Wikipedia URL: `https://en.wikipedia.org/wiki/Alan_Turing`
2. Paste it in the input field
3. Click "🚀 Generate Quiz"
4. Wait for processing (30-60 seconds for first request)
5. View the generated quiz with 5-10 questions
6. See related topics
7. Try taking the quiz

### Tab 2: Past Quizzes

1. Click the "📖 Past Quizzes" tab
2. View all previously generated quizzes
3. Click "👁️ View" to see full quiz details
4. Take the quiz again if desired

---

## Verification Checklist

- [ ] Backend server running on http://localhost:8000
- [ ] Frontend server running on http://localhost:5173
- [ ] API health check: visit http://localhost:8000/health
- [ ] Generated first quiz successfully
- [ ] Quiz appears in history
- [ ] Can take quiz and see score

---

## Testing the API Directly

### Test 1: Health Check

```bash
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy"}
```

### Test 2: Generate Quiz

```bash
curl -X POST http://localhost:8000/api/generate-quiz \
  -H "Content-Type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Alan_Turing"}'

# Expected: Full quiz JSON response
```

### Test 3: Get History

```bash
curl http://localhost:8000/api/history

# Expected: List of generated quizzes
```

### Test 4: Get Quiz Details

```bash
curl http://localhost:8000/api/quiz/1

# Expected: Full details of quiz ID 1
```

---

## Testing with Sample URLs

Use these Wikipedia URLs to test the application:

1. **Alan Turing** (Cryptography, WWII)
   - https://en.wikipedia.org/wiki/Alan_Turing

2. **Machine Learning** (AI, Data Science)
   - https://en.wikipedia.org/wiki/Machine_learning

3. **Albert Einstein** (Physics, History)
   - https://en.wikipedia.org/wiki/Albert_Einstein

4. **Python** (Programming, Technology)
   - https://en.wikipedia.org/wiki/Python_(programming_language)

5. **Artificial Intelligence** (AI, Technology)
   - https://en.wikipedia.org/wiki/Artificial_intelligence

---

## Project Structure After Setup

```
ai-wiki-quiz-generator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           ← FastAPI app
│   │   ├── config.py         ← Settings
│   │   ├── database.py       ← Database models
│   │   ├── schemas.py        ← API schemas
│   │   ├── scraper.py        ← Web scraping
│   │   ├── services.py       ← LLM service
│   │   └── prompts.py        ← LangChain prompts
│   ├── venv/                 ← Virtual environment
│   ├── .env                  ← API key (created)
│   ├── requirements.txt
│   ├── llm_test.py
│   └── scraper_test.py
├── frontend/
│   ├── src/
│   │   ├── components/       ← React components
│   │   ├── styles/          ← CSS files
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── node_modules/        ← Dependencies (created)
│   ├── package.json
│   └── vite.config.js
├── sample_data/             ← Example outputs
├── README.md
└── .env.example
```

---

## Troubleshooting

### Port Already in Use

If you get "Address already in use":

```bash
# Find process using port 8000 (backend)
lsof -i :8000

# Find process using port 5173 (frontend)
lsof -i :5173

# Kill the process (replace PID)
kill -9 <PID>
```

Or use different ports:
```bash
# Backend
python -m uvicorn app.main:app --reload --port 8001

# Frontend (update package.json dev script)
npm run dev -- --port 5174
```

### Virtual Environment Issues

```bash
# If venv won't activate, recreate it
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dependencies Installation Fails

```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Try installing again
pip install -r requirements.txt
```

### API Key Issues

```
# Error: "Invalid API key"
# Solution: Check your .env file has correct key
# Run: cat backend/.env | grep GEMINI_API_KEY
```

### Database Issues

```bash
# Reset database (SQLite)
rm quiz_app.db

# The database will be recreated on next run
python -m uvicorn app.main:app --reload
```

### Frontend Not Connecting to Backend

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check browser console for CORS errors
# Make sure API_URL in frontend matches backend

# Try restarting both servers
# 1. Stop backend (Ctrl+C)
# 2. Stop frontend (Ctrl+C)
# 3. Start backend first
# 4. Start frontend
```

---

## Development Workflow

### Making Backend Changes

1. Edit files in `backend/app/`
2. Backend will auto-reload (--reload flag)
3. Test via API or frontend
4. Check terminal for errors

### Making Frontend Changes

1. Edit files in `frontend/src/`
2. Frontend will hot-reload automatically
3. Check browser for changes
4. Check console for errors

### Adding New Dependencies

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install new-package
pip freeze > requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install new-package
npm install --save-dev new-dev-package
```

---

## Building for Production

### Build Frontend

```bash
cd frontend
npm run build

# Output in frontend/dist/
# Can be served by any static file server
```

### Build Backend

FastAPI apps are typically deployed as-is. For production:

1. Remove `--reload` flag
2. Use production ASGI server (e.g., Gunicorn)
3. Set up reverse proxy (nginx)
4. Configure CORS for your domain
5. Use environment-based database

---

## Common Commands Reference

### Backend Commands

```bash
# Activate virtual environment
source backend/venv/bin/activate

# Start development server
python -m uvicorn app.main:app --reload

# Run tests
python llm_test.py
python scraper_test.py

# Deactivate virtual environment
deactivate
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## Getting Help

### Check Logs

**Backend:**
- Look at terminal where `uvicorn` is running
- Check for error messages and tracebacks

**Frontend:**
- Open browser DevTools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API calls

### Common Issues with Solutions

See the Troubleshooting section above for:
- Port conflicts
- Environment variable issues
- Dependency problems
- API connection issues

### Manual Testing

```bash
# Test scraper independently
python scraper_test.py

# Test LLM independently
python llm_test.py

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/stats
```

---

## Performance Tips

1. **First Load**: LLM API calls take 30-60 seconds - this is normal
2. **Caching**: Same URL won't be processed twice - instant results
3. **Network**: Requires internet for Wikipedia and Gemini API
4. **Storage**: Database grows ~1KB per quiz generated

---

## Next Steps

1. ✅ Complete the setup above
2. ✅ Test with sample URLs
3. ✅ Explore the UI
4. ✅ Check the sample data in `sample_data/`
5. ✅ Read the main README.md for API details

---

## Support & Resources

- **FastAPI Docs**: http://localhost:8000/docs (when backend is running)
- **React Docs**: https://react.dev
- **LangChain Docs**: https://python.langchain.com
- **Gemini API Docs**: https://ai.google.dev/docs
- **BeautifulSoup Docs**: https://www.crummy.com/software/BeautifulSoup

---

**Version**: 1.0  
**Last Updated**: January 9, 2026  
**Created for**: Wiki Quiz Generator Application
