# Step-by-Step GitHub Push Guide

This document provides complete, copy-pasteable instructions for publishing and pushing the **AI Voice IT Helpdesk Agent** codebase to GitHub.

---

## Pre-Push Checklist

Before initializing git and pushing, verify that:
1. **Secrets are safe**: Your `.env` file containing real secret keys is in `.gitignore` (only `.env.example` will be tracked).
2. **Binaries & Logs excluded**: Large binaries like `cloudflared` and runtime logs (`*.log`, `*.db`, `*.out`) are excluded by `.gitignore`.
3. **Tests Pass**: Run local tests:
   ```bash
   pytest -v
   ```

---

## Option A: Quick Push Using GitHub CLI (`gh`)

If you have the GitHub CLI installed and authenticated:

```bash
# 1. Navigate to project root
cd /home/pulkit/AI_IT_assistant

# 2. Initialize local Git repository
git init

# 3. Create main branch
git branch -M main

# 4. Stage all tracked files
git add .

# 5. Make initial commit
git commit -m "feat: initial commit for AI Voice IT Helpdesk Agent"

# 6. Create repository on GitHub & push directly
gh repo create AI-Voice-IT-Agent --public --source=. --remote=origin --push
```

---

## Option B: Push Using Standard Git & Web Browser

### Step 1: Create Repository on GitHub Web Interface
1. Go to [github.com/new](https://github.com/new).
2. Set Repository Name: `AI-Voice-IT-Agent` (or your preferred name).
3. Select Visibility: **Public** or **Private**.
4. **IMPORTANT**: Do **NOT** initialize the repository with a README, `.gitignore`, or License (we have already created all of these locally).
5. Click **Create repository**.

---

### Step 2: Initialize Git & Commit Locally

Open your Linux terminal in the workspace directory and execute:

```bash
# 1. Go to project directory
cd /home/pulkit/AI_IT_assistant

# 2. Initialize Git
git init

# 3. Check git status to ensure ignored files (cloudflared, .env, *.db) are excluded
git status

# 4. Stage all project files
git add .

# 5. Create initial commit
git commit -m "feat: initial release of AI Voice IT Helpdesk Agent"

# 6. Rename branch to main
git branch -M main
```

---

### Step 3: Link Remote & Push Code

Replace `<your-github-username>` with your actual GitHub username:

#### Using HTTPS:
```bash
git remote add origin https://github.com/<your-github-username>/AI-Voice-IT-Agent.git
git push -u origin main
```
> *Note for HTTPS*: When prompted for a password, enter your **GitHub Personal Access Token (PAT)** rather than your account password.

#### Using SSH:
```bash
git remote add origin git@github.com:<your-github-username>/AI-Voice-IT-Agent.git
git push -u origin main
```

---

## Post-Push Setup on GitHub

### 1. Configure Repository Secrets (For CI/CD or Deployment)
If you deploy to Render/Railway or run GitHub Actions:
1. Go to your GitHub repository -> **Settings** -> **Secrets and variables** -> **Actions**.
2. Click **New repository secret** and add:
   - `DATABASE_URL`: `sqlite+aiosqlite:///./helpdesk.db` (or Supabase Postgres connection string)
   - `JWT_SECRET_KEY`: `your_random_secret_key`
   - `OPENAI_API_KEY`: `sk-...`
   - `ELEVENLABS_API_KEY`: `your_elevenlabs_key`

### 2. Verify Repository Content
Check your GitHub repository page:
- `README.md` is automatically rendered on the main page.
- `LICENSE`, `CONTRIBUTING.md`, and `SECURITY.md` are linked in the repository sidebar.
- `.env` and `cloudflared` are NOT present.

---

## Troubleshooting Common Push Errors

### 1. `Support for password authentication was removed`
- **Cause**: GitHub no longer accepts account passwords for `git push` over HTTPS.
- **Fix**: Generate a Personal Access Token (PAT):
  1. Go to GitHub **Settings** -> **Developer Settings** -> **Personal Access Tokens (Tokens classic)**.
  2. Click **Generate new token (classic)** with `repo` scope.
  3. Copy the token and paste it when prompted for a password during `git push`.

### 2. `remote origin already exists`
- **Fix**: Reset the remote origin URL:
  ```bash
  git remote remove origin
  git remote add origin https://github.com/<your-username>/AI-Voice-IT-Agent.git
  ```

### 3. Accidental Large File Staging (`cloudflared` / `.env`)
- **Fix**: Unstage everything, ensure `.gitignore` is active, and re-stage:
  ```bash
  git reset
  git add .
  git status
  ```
