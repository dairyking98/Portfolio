# Development Workflow

This guide explains how to develop and test your Jekyll site locally without affecting the live site on GitHub Pages.

## Local Development (No Git Required)

The easiest way to develop locally without touching Git:

1. **Make changes to your files** (posts, layouts, CSS, etc.)
2. **Run the local server:**
   ```bash
   # Windows
   serve.bat
   
   # Linux/Mac
   bundle exec jekyll serve
   ```
3. **View changes at http://localhost:4000**
   - Jekyll automatically rebuilds when you save files
   - Refresh your browser to see changes
4. **Test everything works** before committing
5. **When ready, commit and push to GitHub**

## Branch-Based Development (Recommended)

Use feature branches to develop changes without affecting `main`:

### 1. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/new-post

# Or for a different type of change
git checkout -b update-layout
git checkout -b fix-typo
```

### 2. Make Your Changes

Edit files, create posts, update layouts, etc.

### 3. Test Locally

```bash
# Windows (recommended - builds and serves)
serve.bat

# Linux/Mac (recommended - builds and serves)
bundle exec jekyll serve

# Or just build without serving (optional)
build.bat  # Windows
bundle exec jekyll build  # Linux/Mac
```

Visit http://localhost:4000 to preview your changes.

**Note:** `serve.bat` automatically builds the site AND starts a server. You don't need to run `build.bat` separately - `serve` does it all!

### 4. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add new blog post about X"

# Or commit specific files
git add _posts/2025-02-15-new-post.md
git commit -m "Add new blog post"
```

### 5. Push to GitHub (Optional)

```bash
# Push your branch to GitHub
git push origin feature/new-post
```

This creates the branch on GitHub but **doesn't deploy** to GitHub Pages (only `main` branch deploys).

### 6. Merge to Main (When Ready)

When you're satisfied with your changes:

```bash
# Switch back to main
git checkout main

# Pull latest changes (if working with others)
git pull origin main

# Merge your feature branch
git merge feature/new-post

# Push to main (this will trigger deployment)
git push origin main
```

Or use GitHub's Pull Request workflow (see below).

## Pull Request Workflow (Best Practice)

For code review and safer deployments:

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/new-post
   ```

2. **Make changes and commit:**
   ```bash
   git add .
   git commit -m "Add new blog post"
   ```

3. **Push branch to GitHub:**
   ```bash
   git push origin feature/new-post
   ```

4. **Create a Pull Request on GitHub:**
   - Go to your repository on GitHub
   - Click "Compare & pull request"
   - Review your changes
   - Click "Create pull request"

5. **Review and test** (GitHub Actions will build your branch)

6. **Merge to main** when ready:
   - Click "Merge pull request" on GitHub
   - This will deploy to GitHub Pages automatically

## Stashing Changes (Temporary)

If you need to switch branches but aren't ready to commit:

```bash
# Save your changes temporarily
git stash

# Switch branches
git checkout main

# Do something else...

# Switch back and restore your changes
git checkout feature/new-post
git stash pop
```

## Viewing Branch Changes

To see what files have changed:

```bash
# See modified files
git status

# See differences
git diff

# See differences for a specific file
git diff _posts/2025-02-15-new-post.md
```

## Reverting Changes

If you make a mistake:

```bash
# Discard changes to a specific file
git restore _posts/2025-02-15-new-post.md

# Discard all changes (be careful!)
git restore .

# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Undo last commit (discards changes)
git reset --hard HEAD~1
```

## Workflow Summary

```
1. Create branch          → git checkout -b feature/my-change
2. Make changes          → Edit files
3. Test locally          → serve.bat (or bundle exec jekyll serve)
4. Commit changes        → git add . && git commit -m "Description"
5. Push branch (optional) → git push origin feature/my-change
6. Merge to main         → git checkout main && git merge feature/my-change
7. Push to main          → git push origin main (deploys automatically)
```

## Important Notes

- **Only `main` branch deploys** to GitHub Pages
- **Local changes don't affect the live site** until you push to `main`
- **Test locally first** using `serve.bat` or `bundle exec jekyll serve`
- **GitHub Actions** will automatically build and deploy when you push to `main`
- **Feature branches** are safe to push - they won't deploy

## Quick Commands Reference

```bash
# Local development
serve.bat                    # Start local server (Windows)
bundle exec jekyll serve     # Start local server (Linux/Mac)

# Git workflow
git status                   # See what's changed
git checkout -b feature/name # Create new branch
git add .                    # Stage all changes
git commit -m "Message"      # Commit changes
git push origin branch-name  # Push branch to GitHub
git checkout main            # Switch to main branch
git merge feature/name       # Merge feature into main
git push origin main         # Deploy to GitHub Pages
```

