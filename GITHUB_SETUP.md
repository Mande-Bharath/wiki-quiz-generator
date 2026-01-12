# Complete Guide: Pushing Your Code to GitHub

This guide will help you push your Wiki Quiz Generator code to GitHub step-by-step.

---

## Step 1: Create a GitHub Account (If You Don't Have One)

1. Go to https://github.com
2. Click **"Sign up"** (top right)
3. Enter your email address
4. Create a password
5. Choose a username
6. Verify your email
7. You're all set! 🎉

---

## Step 2: Create a GitHub Repository

1. Go to https://github.com and sign in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in the form:
   - **Repository name**: `wiki-quiz-generator` (or any name you like)
   - **Description**: "AI-powered Wikipedia Quiz Generator" (optional)
   - **Visibility**: 
     - ✅ **Public** (free, anyone can see)
     - ✅ **Private** (only you can see, free)
   - **Initialize repository**: 
     - ❌ **DO NOT** check "Add a README file"
     - ❌ **DO NOT** check "Add .gitignore"
     - ❌ **DO NOT** check "Choose a license"
4. Click **"Create repository"**

5. **IMPORTANT**: After creating, you'll see a page with instructions. **Don't follow those yet** - we'll do it step by step below.

---

## Step 3: Install Git (If Not Already Installed)

### Check if Git is Installed

Open your terminal and type:
```bash
git --version
```

If you see a version number (like `git version 2.39.0`), you're good! ✅

If you see an error, install Git:

### macOS (Your System)

Git usually comes pre-installed on macOS. If not:

**Option A: Install via Xcode Command Line Tools**
```bash
xcode-select --install
```

**Option B: Install via Homebrew**
```bash
brew install git
```

**Option C: Download from official site**
- Go to https://git-scm.com/download/mac
- Download and install the installer

---

## Step 4: Configure Git (First Time Only)

If this is your first time using Git, set up your name and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Replace:**
- `"Your Name"` with your actual name (e.g., "John Doe")
- `"your.email@example.com"` with your GitHub email

---

## Step 5: Initialize Git in Your Project

Open your terminal and navigate to your project:

```bash
cd /Users/mandebharath/Documents/project7890/ai-wiki-quiz-generator
```

Check if Git is already initialized:
```bash
git status
```

### Option A: If Git is NOT initialized (you'll see an error)

Initialize Git:
```bash
git init
```

### Option B: If Git IS already initialized

You'll see something like "On branch main" or "On branch master". You can continue to the next step.

---

## Step 6: Create .gitignore File

This file tells Git which files to ignore (like node_modules, .env files, etc.).

I'll create this file for you - it should already exist, but let's make sure it has the right content.

---

## Step 7: Add All Files to Git

Add all your project files:

```bash
git add .
```

This stages all files for commit (except those in .gitignore).

**Verify what was added:**
```bash
git status
```

You should see a list of files ready to be committed.

---

## Step 8: Create Your First Commit

Commit your files:

```bash
git commit -m "Initial commit: Wiki Quiz Generator"
```

**What's a commit?** - It's like saving a snapshot of your code at a point in time.

---

## Step 9: Connect to GitHub Repository

You need to connect your local project to the GitHub repository you created.

### Get Your Repository URL

1. Go to your GitHub repository page (the one you created in Step 2)
2. Click the green **"Code"** button
3. Make sure **"HTTPS"** is selected
4. Copy the URL (looks like: `https://github.com/yourusername/wiki-quiz-generator.git`)

### Add Remote Repository

In your terminal, run:

```bash
git remote add origin https://github.com/yourusername/wiki-quiz-generator.git
```

**Replace `yourusername/wiki-quiz-generator`** with your actual GitHub username and repository name.

**Verify it was added:**
```bash
git remote -v
```

You should see your repository URL listed.

---

## Step 10: Push to GitHub

Now push your code to GitHub:

### If you're using "main" branch (newer default):

```bash
git branch -M main
git push -u origin main
```

### If you're using "master" branch (older default):

```bash
git push -u origin master
```

**What to expect:**
- GitHub will ask for your username and password
- **Important**: If it asks for a password, use a **Personal Access Token** (not your GitHub password)
  - See "Troubleshooting: Authentication" section below

---

## Step 11: Verify on GitHub

1. Go to your GitHub repository page
2. Refresh the page
3. You should see all your files! 🎉

---

## Troubleshooting

### Issue: "Authentication failed" or "Username/Password"

GitHub no longer accepts passwords. You need a **Personal Access Token**.

#### Create a Personal Access Token:

1. Go to GitHub → Click your profile picture (top right) → **"Settings"**
2. Scroll down → Click **"Developer settings"** (left sidebar)
3. Click **"Personal access tokens"** → **"Tokens (classic)"**
4. Click **"Generate new token"** → **"Generate new token (classic)"**
5. Fill in:
   - **Note**: "Vercel Deployment" (or any name)
   - **Expiration**: Choose how long (30 days, 90 days, or no expiration)
   - **Select scopes**: Check **"repo"** (this selects all repo permissions)
6. Click **"Generate token"** at the bottom
7. **COPY THE TOKEN IMMEDIATELY** (you won't see it again!)
   - Looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### Use the Token:

When Git asks for password, use the token instead:
- **Username**: Your GitHub username
- **Password**: Paste the Personal Access Token

#### Save Token (Optional - to avoid entering it every time):

**macOS:**
```bash
# Install GitHub CLI (easier method)
brew install gh
gh auth login

# OR use credential helper
git config --global credential.helper osxkeychain
```

---

### Issue: "Repository not found"

- Check that the repository URL is correct
- Make sure you created the repository on GitHub first
- Verify your username and repository name are spelled correctly

---

### Issue: "remote origin already exists"

If you already added the remote:

```bash
# Remove existing remote
git remote remove origin

# Add it again with correct URL
git remote add origin https://github.com/yourusername/your-repo.git
```

---

### Issue: "Permission denied"

- Make sure you're using HTTPS (not SSH) if you're new to GitHub
- Check that you created the repository (it exists on GitHub)
- Try creating a Personal Access Token (see above)

---

### Issue: "Everything up-to-date" but no files on GitHub

This means the files were committed but not pushed:

```bash
# Check current branch
git branch

# Push again
git push -u origin main
# or
git push -u origin master
```

---

## Quick Reference: All Commands in Order

If you want to do everything at once, here are all the commands:

```bash
# 1. Navigate to project
cd /Users/mandebharath/Documents/project7890/ai-wiki-quiz-generator

# 2. Initialize Git (if not already done)
git init

# 3. Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 4. Add all files
git add .

# 5. Create commit
git commit -m "Initial commit: Wiki Quiz Generator"

# 6. Rename branch to main (if needed)
git branch -M main

# 7. Add remote (replace with your URL)
git remote add origin https://github.com/yourusername/wiki-quiz-generator.git

# 8. Push to GitHub
git push -u origin main
```

**Replace:**
- `yourusername` with your GitHub username
- `wiki-quiz-generator` with your repository name
- `your.email@example.com` with your email

---

## What's Next?

After successfully pushing to GitHub:

1. ✅ Your code is now on GitHub
2. ✅ Go to the [Vercel Beginner Guide](VERCEL_BEGINNER_GUIDE.md)
3. ✅ Import your GitHub repository to Vercel
4. ✅ Deploy your app!

---

## Need Help?

If you get stuck:
1. Check the error message in your terminal
2. Look at the "Troubleshooting" section above
3. Common issues are usually authentication-related (use Personal Access Token!)

Good luck! 🚀
