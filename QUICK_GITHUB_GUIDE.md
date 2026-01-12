# Quick Start: Push to GitHub

Follow these steps to push your code to GitHub.

---

## Step 1: Create GitHub Repository

1. Go to https://github.com and sign in
2. Click **"+"** (top right) → **"New repository"**
3. Repository name: `wiki-quiz-generator`
4. Choose **Public** or **Private**
5. **DO NOT** check any boxes (README, .gitignore, license)
6. Click **"Create repository"**

**Copy the repository URL** (you'll need it later)
- Looks like: `https://github.com/yourusername/wiki-quiz-generator.git`

---

## Step 2: Open Terminal

Open Terminal on your Mac (Applications → Utilities → Terminal)

---

## Step 3: Run These Commands

Copy and paste these commands one by one into your terminal:

### 1. Go to your project folder:
```bash
cd /Users/mandebharath/Documents/project7890/ai-wiki-quiz-generator
```

### 2. Initialize Git:
```bash
git init
```

### 3. Configure Git (first time only - replace with your info):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 4. Add all files:
```bash
git add .
```

### 5. Create commit:
```bash
git commit -m "Initial commit: Wiki Quiz Generator"
```

### 6. Rename branch to main:
```bash
git branch -M main
```

### 7. Connect to GitHub (REPLACE with your repository URL):
```bash
git remote add origin https://github.com/yourusername/wiki-quiz-generator.git
```

### 8. Push to GitHub:
```bash
git push -u origin main
```

---

## Step 4: Authentication

When you run `git push`, GitHub will ask for:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your password!)

### Create Personal Access Token:

1. Go to GitHub → Your profile (top right) → **Settings**
2. Scroll down → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. **Note**: "Vercel Deployment"
6. Check **"repo"** checkbox
7. Click **"Generate token"**
8. **COPY THE TOKEN** (starts with `ghp_...`)

Use this token as your password when Git asks!

---

## Step 5: Verify

Go to https://github.com/yourusername/wiki-quiz-generator
You should see all your files! 🎉

---

## Troubleshooting

**"Authentication failed"**: Use Personal Access Token (see Step 4)

**"Repository not found"**: Make sure you created the repository on GitHub first

**"remote origin already exists"**: Run `git remote remove origin` first, then try again

---

## What's Next?

✅ Code is on GitHub → Now go to [VERCEL_BEGINNER_GUIDE.md](VERCEL_BEGINNER_GUIDE.md) to deploy!
