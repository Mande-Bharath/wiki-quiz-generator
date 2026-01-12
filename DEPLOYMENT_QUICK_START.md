# Quick Start: Deploy to Vercel

## What's Been Set Up

✅ **Vercel configuration** (`vercel.json`)
✅ **Serverless function wrapper** (`api/index.py`)
✅ **Frontend API configuration** (uses environment variables)
✅ **Requirements file** for Python dependencies
✅ **Deployment documentation** (`VERCEL_DEPLOY.md`)

## Quick Deployment Steps

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Set Up PostgreSQL Database

**Important**: SQLite won't work on Vercel serverless functions. You need PostgreSQL.

**Option A: Vercel Postgres (Easiest)**
1. Go to https://vercel.com/dashboard
2. Create/select your project
3. Go to Storage → Create Postgres Database
4. Copy the `POSTGRES_URL` or `DATABASE_URL`

**Option B: External PostgreSQL**
- Use Supabase, Neon, Railway, or any PostgreSQL provider
- Get the connection string

### 3. Deploy to Vercel

```bash
# Login
vercel login

# Deploy (from project root directory)
vercel

# For production
vercel --prod
```

### 4. Set Environment Variables in Vercel Dashboard

Go to your project → Settings → Environment Variables and add:

```
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@host:port/database
LLM_MODEL=gemini-2.0-flash
```

### 5. Initialize Database Tables

The database tables will be created automatically on the first API call, but you can also initialize them manually by calling any API endpoint after deployment.

## Files Created/Modified

- `vercel.json` - Vercel configuration
- `api/index.py` - Serverless function entry point
- `requirements.txt` - Python dependencies for Vercel
- `frontend/src/config.js` - API URL configuration
- `frontend/src/components/GenerateQuizTab.jsx` - Updated to use config
- `frontend/src/components/HistoryTab.jsx` - Updated to use config
- `VERCEL_DEPLOY.md` - Detailed deployment guide

## Alternative: Simpler Deployment

If you encounter issues with serverless functions, consider:

1. **Deploy frontend to Vercel** (works great!)
2. **Deploy backend to Railway/Render/Fly.io** (simpler, better performance)
3. **Set `VITE_API_URL` in Vercel** to point to your backend URL

This approach avoids serverless function complexity and works better with databases.

## Next Steps

1. ✅ Set up PostgreSQL database
2. ✅ Deploy to Vercel
3. ✅ Add environment variables
4. ✅ Test the deployment
5. ✅ Initialize database (first API call will do this)

## Need Help?

See `VERCEL_DEPLOY.md` for detailed instructions and troubleshooting.
