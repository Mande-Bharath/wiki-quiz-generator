# Complete Beginner's Guide to Vercel Deployment

This guide will walk you through deploying your Wiki Quiz Generator to Vercel step-by-step, even if you've never used Vercel before.

## What is Vercel?

Vercel is a platform that makes it easy to deploy web applications. It's free to start and handles all the complex server setup for you.

---

## Step 1: Create a Vercel Account

### Option A: Sign Up with GitHub (Recommended)

1. Go to https://vercel.com
2. Click the **"Sign Up"** button (top right)
3. Click **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub account
5. You're signed up! 🎉

**Why GitHub?** - It's easier to deploy projects directly from GitHub repositories.

### Option B: Sign Up with Email

1. Go to https://vercel.com
2. Click **"Sign Up"**
3. Enter your email and create a password
4. Verify your email address
5. You're signed up! 🎉

---

## Step 2: Prepare Your Code

Before deploying, make sure your code is ready:

### Option A: Push to GitHub (Recommended)

If you haven't already:

1. Create a GitHub account at https://github.com
2. Create a new repository (make it public or private - your choice)
3. Push your code to GitHub:

```bash
# In your project directory (if using git)
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### Option B: Deploy from Local Computer

You can also deploy directly from your computer without GitHub (we'll cover this below).

---

## Step 3: Deploy to Vercel (Two Methods)

### Method 1: Deploy from GitHub (Easiest for Beginners)

#### 3.1: Import Your Project

1. Go to https://vercel.com/dashboard
2. Click **"Add New..."** button (top right)
3. Click **"Project"**
4. You'll see a list of your GitHub repositories
5. Find your project repository and click **"Import"**

#### 3.2: Configure Project

Vercel will automatically detect your project settings. You can usually leave everything as default:

- **Project Name**: `wiki-quiz-generator` (or keep default)
- **Framework Preset**: Leave as "Other" (or "Vite" if detected)
- **Root Directory**: `./` (leave as default)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: Leave empty (handled in build command)

**Important**: Make sure the build command and output directory match above!

#### 3.3: Add Environment Variables (We'll do this in a moment)

For now, you can skip environment variables. We'll add them after deployment.

#### 3.4: Deploy!

Click the **"Deploy"** button at the bottom.

**Wait 2-3 minutes** for the deployment to complete. You'll see a progress screen.

#### 3.5: View Your Deployment

Once deployed, you'll see:
- ✅ "Congratulations! Your project has been deployed"
- A URL like: `https://wiki-quiz-generator-abc123.vercel.app`

Click the URL to see your app! 🎉

**Note**: The frontend will work, but the backend won't work yet until we set up the database.

---

### Method 2: Deploy from Local Computer (Using CLI)

If you don't want to use GitHub:

#### 2.1: Install Vercel CLI

```bash
npm install -g vercel
```

#### 2.2: Login to Vercel

```bash
vercel login
```

This will open your browser to login.

#### 2.3: Deploy from Project Directory

```bash
# Go to your project root directory
cd /path/to/ai-wiki-quiz-generator

# Deploy
vercel
```

#### 2.4: Answer the Questions

- **Set up and deploy?** → Type `Y` and press Enter
- **Which scope?** → Select your account (usually just press Enter)
- **Link to existing project?** → Type `N` and press Enter
- **What's your project's name?** → Type `wiki-quiz-generator` (or press Enter for default)
- **In which directory is your code located?** → Type `./` and press Enter
- **Want to override the settings?** → Type `N` and press Enter

**Wait for deployment** (takes 2-3 minutes).

#### 2.5: Production Deployment

For production deployment:

```bash
vercel --prod
```

---

## Step 4: Set Up PostgreSQL Database

Now we need to set up the database so your backend can work.

### 4.1: Create Postgres Database in Vercel

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Click on your deployed project (`wiki-quiz-generator`)
3. Click on the **"Storage"** tab (top menu)
4. Click **"Create Database"** button
5. Select **"Postgres"**
6. Fill in the form:
   - **Name**: `wiki-quiz-db` (or any name you like)
   - **Region**: Choose the closest to you (e.g., `us-east-1` for US East)
7. Click **"Create"**
8. Wait 1-2 minutes for the database to be created

### 4.2: Get the Connection String

Once the database is created:

1. Click on your database name (`wiki-quiz-db`)
2. You'll see several tabs - click on **".env.local"** tab
3. You'll see something like:
   ```
   POSTGRES_URL="postgres://default:xxxxx@xxxxx.xxxxx.vercel-storage.com:5432/verceldb"
   ```
4. **Copy the entire `POSTGRES_URL` value** (including the quotes, but you'll remove them when adding to environment variables)

---

## Step 5: Add Environment Variables

Now we need to add your API keys and database connection.

### 5.1: Get Your Google Gemini API Key

If you don't have one:

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (looks like: `AIzaSy...`)

### 5.2: Add Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Click **"Settings"** (top menu)
3. Click **"Environment Variables"** (left sidebar)
4. Add the following variables one by one:

#### Variable 1: DATABASE_URL

1. Click **"Add New"**
2. **Key**: `DATABASE_URL`
3. **Value**: Paste the `POSTGRES_URL` value you copied (remove quotes if present)
   - Should look like: `postgres://default:xxxxx@xxxxx.xxxxx.vercel-storage.com:5432/verceldb`
4. **Environment**: Select all three (Production, Preview, Development)
5. Click **"Save"**

#### Variable 2: GEMINI_API_KEY

1. Click **"Add New"** again
2. **Key**: `GEMINI_API_KEY`
3. **Value**: Paste your Google Gemini API key
4. **Environment**: Select all three (Production, Preview, Development)
5. Click **"Save"**

#### Variable 3: LLM_MODEL (Optional)

1. Click **"Add New"** again
2. **Key**: `LLM_MODEL`
3. **Value**: `gemini-2.0-flash`
4. **Environment**: Select all three
5. Click **"Save"**

### 5.3: Redeploy Your Application

After adding environment variables, you need to redeploy:

1. Go to the **"Deployments"** tab (top menu)
2. Click the three dots (⋯) on the latest deployment
3. Click **"Redeploy"**
4. Click **"Redeploy"** again to confirm
5. Wait for the redeployment to complete (2-3 minutes)

**OR** if you used GitHub:

- Just push any small change to GitHub, and Vercel will automatically redeploy
- Or manually trigger a redeploy from the Deployments tab

---

## Step 6: Test Your Deployment

### 6.1: Test the Frontend

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. You should see your Wiki Quiz Generator interface

### 6.2: Test the Backend API

1. Try generating a quiz:
   - Enter a Wikipedia URL (e.g., `https://en.wikipedia.org/wiki/Alan_Turing`)
   - Click "Generate Quiz"
   - Wait for it to generate (may take 30-60 seconds)

### 6.3: Check for Errors

If something doesn't work:

1. Go to your Vercel dashboard
2. Click **"Deployments"** tab
3. Click on the latest deployment
4. Check the **"Functions"** tab for any errors
5. Check the **"Logs"** for error messages

---

## Common Issues and Solutions

### Issue: "Failed to generate quiz"

**Possible causes:**
- Database not set up correctly
- Missing environment variables
- API key invalid

**Solution:**
1. Check environment variables are set correctly
2. Make sure database was created and connection string is correct
3. Verify your Gemini API key is valid

### Issue: Frontend loads but backend doesn't work

**Solution:**
1. Check Functions tab in deployment logs
2. Verify environment variables are set
3. Make sure database connection string is correct

### Issue: Build fails

**Solution:**
1. Check the build logs in the deployment
2. Make sure `buildCommand` and `outputDirectory` are correct in project settings
3. Check that all dependencies are in `package.json`

### Issue: Database connection error

**Solution:**
1. Verify `DATABASE_URL` environment variable is set correctly
2. Make sure you removed quotes from the connection string
3. Check that the database is active in Vercel Storage

---

## Understanding Your Vercel Dashboard

### Main Sections:

1. **Overview**: See your deployment status and URL
2. **Deployments**: See all your deployments and their status
3. **Analytics**: View traffic and performance (Pro feature)
4. **Storage**: Manage your databases
5. **Settings**: Configure your project
   - **Environment Variables**: Add/edit secrets
   - **General**: Project settings
   - **Domains**: Add custom domain

### Deployment Status:

- ✅ **Ready**: Deployment successful
- 🔄 **Building**: Currently deploying
- ❌ **Error**: Something went wrong (check logs)

---

## Next Steps After Successful Deployment

1. ✅ **Test all features**: Generate quizzes, view history
2. ✅ **Check logs**: Make sure there are no errors
3. ✅ **Custom domain** (optional): Add your own domain in Settings → Domains
4. ✅ **Monitor usage**: Check Storage tab to see database usage

---

## Free Tier Limitations

Vercel Free Tier includes:
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth per month
- ✅ Automatic SSL certificates
- ✅ 256 MB Postgres storage (per database)
- ✅ Serverless functions

**Note**: For production use with high traffic, you may need to upgrade to Pro plan ($20/month).

---

## Getting Help

If you run into issues:

1. **Check the logs** in your Vercel dashboard
2. **Review this guide** for common issues
3. **Vercel Documentation**: https://vercel.com/docs
4. **Vercel Community**: https://github.com/vercel/vercel/discussions

---

## Quick Reference: Checklist

Before deploying:
- [ ] Code is ready and working locally
- [ ] GitHub repository created (optional but recommended)
- [ ] Google Gemini API key ready

During deployment:
- [ ] Project imported/created in Vercel
- [ ] Build settings configured correctly
- [ ] Initial deployment completed

After deployment:
- [ ] Postgres database created
- [ ] Environment variables added (DATABASE_URL, GEMINI_API_KEY)
- [ ] Application redeployed
- [ ] Tested quiz generation
- [ ] Verified everything works

---

Congratulations! You've successfully deployed your app to Vercel! 🎉

If you get stuck at any step, feel free to ask for help!
