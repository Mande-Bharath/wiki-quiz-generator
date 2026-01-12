# Vercel Deployment Guide

This guide will help you deploy the Wiki Quiz Generator to Vercel.

## Important Considerations

**Note**: Deploying FastAPI to Vercel as serverless functions has some limitations:
- SQLite database won't work (filesystem is read-only). You'll need PostgreSQL (Vercel Postgres recommended).
- Cold starts may occur with serverless functions.
- Large dependencies may increase function size.

**Recommended Approach**: Deploy the frontend to Vercel and the backend separately to Railway, Render, or Fly.io for better performance and simplicity.

However, if you want both on Vercel, follow this guide.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed: `npm i -g vercel`
3. A Google Gemini API key
4. A PostgreSQL database (Vercel Postgres recommended)

## Setup Steps

### 1. Install Vercel CLI (if not already installed)

```bash
npm install -g vercel
```

### 2. Set Up PostgreSQL Database

Since SQLite won't work on Vercel's serverless functions, you need PostgreSQL:

**Option A: Vercel Postgres (Recommended)**
1. Go to your Vercel dashboard
2. Create a new project or select existing one
3. Go to Storage tab
4. Create a new Postgres database
5. Copy the connection string (DATABASE_URL)

**Option B: External PostgreSQL**
- Use services like Supabase, Neon, or Railway
- Get the PostgreSQL connection string

### 3. Configure Environment Variables

Create a `.env` file in the root directory (or set in Vercel dashboard):

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://user:password@host:port/database
LLM_MODEL=gemini-2.0-flash
```

### 4. Update Database Configuration

The database configuration already supports PostgreSQL via the `DATABASE_URL` environment variable, so no code changes are needed.

### 5. Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Login to Vercel
vercel login

# Deploy (from project root)
vercel

# Follow the prompts
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? wiki-quiz-generator (or your choice)
# - Directory? ./
# - Override settings? No

# For production deployment
vercel --prod
```

#### Option B: Using GitHub Integration

1. Push your code to GitHub
2. Go to https://vercel.com/new
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
5. Add environment variables in the Vercel dashboard
6. Deploy

### 6. Configure Environment Variables in Vercel Dashboard

1. Go to your project on Vercel
2. Go to Settings → Environment Variables
3. Add the following variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `LLM_MODEL`: `gemini-2.0-flash` (optional)

### 7. Initialize Database Tables

After deployment, you need to initialize the database tables. You can do this by:

**Option A: Create an initialization script**

Create `backend/init_db.py`:
```python
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app.database import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
```

Run it locally with your DATABASE_URL:
```bash
cd backend
DATABASE_URL=your_postgres_url python init_db.py
```

**Option B: The tables will be created automatically on first API call**

The FastAPI app creates tables on startup, but this might not work reliably with serverless functions. It's better to initialize manually.

## Project Structure for Vercel

```
ai-wiki-quiz-generator/
├── api/
│   └── index.py              # Serverless function entry point
├── backend/
│   ├── app/                  # FastAPI application
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/                  # React app
│   ├── dist/                 # Build output (created during build)
│   └── package.json
├── vercel.json               # Vercel configuration
└── .env                      # Environment variables (not committed)
```

## Troubleshooting

### Database Connection Issues

- Ensure `DATABASE_URL` is set correctly in Vercel environment variables
- Check that PostgreSQL database is accessible from Vercel
- Verify connection string format: `postgresql://user:password@host:port/database`

### API Routes Not Working

- Check that `/api/*` routes are properly configured in `vercel.json`
- Verify the serverless function is deployed (check Vercel dashboard → Functions)
- Check function logs in Vercel dashboard for errors

### Build Failures

- Ensure all dependencies are in `requirements.txt`
- Check that Python version is compatible (3.9+)
- Review build logs in Vercel dashboard

### Cold Starts

- Serverless functions may have cold starts (first request is slower)
- This is normal for serverless functions
- Consider using Vercel Pro plan for better performance

## Alternative: Separate Deployment (Recommended)

For better performance and simpler setup, consider:

1. **Frontend on Vercel**: Deploy only the frontend to Vercel
2. **Backend on Railway/Render/Fly.io**: Deploy the FastAPI backend separately
3. **Update API URL**: Set `VITE_API_URL` environment variable in Vercel to point to your backend

This approach:
- ✅ Allows SQLite (if using a persistent filesystem)
- ✅ Better performance (no cold starts)
- ✅ Simpler deployment
- ✅ Easier debugging

## Post-Deployment

After deployment:

1. Visit your Vercel URL
2. Test quiz generation
3. Check Vercel dashboard for function logs
4. Monitor database connections
5. Test all API endpoints

## Support

For issues:
- Check Vercel function logs in the dashboard
- Review environment variables
- Verify database connectivity
- Check API endpoints at `/api/docs` (if deployed)
