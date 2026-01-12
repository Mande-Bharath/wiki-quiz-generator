# PostgreSQL Database Setup Guide

This guide will help you set up a PostgreSQL database for your Wiki Quiz Generator deployment.

## Option 1: Vercel Postgres (Recommended - Easiest)

### Step 1: Create Vercel Project (if not already created)

1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository (or skip for now if deploying via CLI)

### Step 2: Create Postgres Database

1. In your Vercel project dashboard, click on the **"Storage"** tab
2. Click **"Create Database"**
3. Select **"Postgres"**
4. Configure:
   - **Name**: `wiki-quiz-db` (or any name you prefer)
   - **Region**: Choose closest to you (e.g., `us-east-1`, `eu-west-1`)
5. Click **"Create"**

### Step 3: Get Connection String

**Method A: From .env.local tab (Recommended)**
1. In your database page, click on the **".env.local"** tab
2. Copy the `POSTGRES_URL` value
3. It looks like: `postgres://default:password@host:port/database?sslmode=require`

**Method B: From Settings**
1. Click on **"Settings"** tab in your database
2. Find the **"Connection String"** section
3. Copy the connection string

### Step 4: Use in Environment Variables

The connection string format is:
```
POSTGRES_URL=postgres://default:password@host:port/database?sslmode=require
```

**For Vercel deployment:**
- Go to your project → Settings → Environment Variables
- Add `DATABASE_URL` with the `POSTGRES_URL` value you copied
- Or use `POSTGRES_URL` directly (the code supports both)

---

## Option 2: Supabase (Free Tier Available)

### Step 1: Create Supabase Account

1. Go to https://supabase.com
2. Sign up for free
3. Create a new project

### Step 2: Get Connection String

1. Go to your project dashboard
2. Click **"Settings"** → **"Database"**
3. Scroll down to **"Connection string"**
4. Select **"URI"** tab
5. Copy the connection string (it includes password)
   - Format: `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`

### Step 3: Use Connection String

Add to Vercel environment variables as `DATABASE_URL`

---

## Option 3: Neon (Serverless Postgres - Free Tier)

### Step 1: Create Neon Account

1. Go to https://neon.tech
2. Sign up for free
3. Create a new project

### Step 2: Get Connection String

1. In your project dashboard, go to **"Connection Details"**
2. Copy the connection string
   - Format: `postgresql://user:password@host/database?sslmode=require`

### Step 3: Use Connection String

Add to Vercel environment variables as `DATABASE_URL`

---

## Option 4: Railway (Free Tier Available)

### Step 1: Create Railway Account

1. Go to https://railway.app
2. Sign up with GitHub
3. Create a new project

### Step 2: Add PostgreSQL Service

1. Click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Wait for provisioning (takes a minute)

### Step 3: Get Connection String

1. Click on the PostgreSQL service
2. Go to **"Variables"** tab
3. Copy the `DATABASE_URL` value

### Step 4: Use Connection String

Add to Vercel environment variables as `DATABASE_URL`

---

## Option 5: Render (Free Tier Available)

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up for free
3. Create a new PostgreSQL database

### Step 2: Get Connection String

1. In your database dashboard
2. Go to **"Info"** tab
3. Copy the **"Internal Database URL"** (for same region) or **"External Database URL"**

### Step 3: Use Connection String

Add to Vercel environment variables as `DATABASE_URL`

---

## Connection String Format

All PostgreSQL connection strings follow this format:
```
postgresql://username:password@host:port/database?sslmode=require
```

Example:
```
postgresql://postgres:mypassword@db.example.com:5432/mydb?sslmode=require
```

---

## Environment Variable Setup

### For Vercel Deployment

1. Go to your Vercel project dashboard
2. Click **"Settings"** → **"Environment Variables"**
3. Add the following variables:

```
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-2.0-flash
```

**Important Notes:**
- Use `DATABASE_URL` (the code checks for this environment variable)
- Vercel Postgres provides `POSTGRES_URL` - you can use either name
- Make sure `sslmode=require` is included for secure connections

### For Local Development (Optional)

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
GEMINI_API_KEY=your_gemini_api_key_here
LLM_MODEL=gemini-2.0-flash
```

---

## Testing the Connection

After setting up the database, you can test the connection:

### Option 1: Use psql (Command Line)

```bash
psql "your_connection_string_here"
```

### Option 2: Use a GUI Tool

- **pgAdmin**: https://www.pgadmin.org/
- **DBeaver**: https://dbeaver.io/
- **TablePlus**: https://tableplus.com/

### Option 3: Test via API (After Deployment)

Once deployed, the database tables will be created automatically on the first API call.

---

## Free Tier Comparison

| Provider | Free Tier | Limitations |
|----------|-----------|-------------|
| **Vercel Postgres** | ✅ Yes | 256 MB storage, 1 database per project |
| **Supabase** | ✅ Yes | 500 MB database, 2 GB bandwidth |
| **Neon** | ✅ Yes | 0.5 GB storage, serverless |
| **Railway** | ✅ Yes | $5 credit/month, pay-as-you-go after |
| **Render** | ✅ Yes | 90-day free trial, then paid |

---

## Recommendation

**For Vercel deployment**: Use **Vercel Postgres** - it's the easiest:
- Integrated with Vercel dashboard
- Automatically configured
- No additional setup needed
- Connection string automatically available

---

## Next Steps

After setting up the database:

1. ✅ Copy your connection string
2. ✅ Add `DATABASE_URL` to Vercel environment variables
3. ✅ Deploy to Vercel
4. ✅ Test the deployment
5. ✅ Database tables will be created automatically on first API call

---

## Troubleshooting

### Connection Refused
- Check if the database is running/active
- Verify the connection string is correct
- Ensure SSL is enabled (`sslmode=require`)

### Authentication Failed
- Verify username and password in connection string
- Check if IP whitelist is configured (some providers require this)

### SSL Required
- Make sure `sslmode=require` is in the connection string
- Some providers require SSL connections

---

Need help? Check the main deployment guide: `VERCEL_DEPLOY.md`
