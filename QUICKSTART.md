# Quick Start Guide

## First Time Setup

1. **Install Ruby** (if not already installed)
   - Windows: Download from https://rubyinstaller.org/
   - Mac: `brew install ruby`
   - Linux: `sudo apt-get install ruby ruby-dev`

2. **Install Bundler**
   ```bash
   gem install bundler
   ```

3. **Install Jekyll Dependencies**
   - Windows: Double-click `install.bat` or run `install.bat` in command prompt
   - Linux/Mac: Run `bundle install`

## Daily Development

### Start Local Server

**Windows:**
```bash
serve.bat
```

**Linux/Mac:**
```bash
bundle exec jekyll serve
```

Then open http://localhost:4000 in your browser.

### Make Changes

- Edit Markdown files in `_posts/` for blog posts
- Edit Markdown files in root (e.g., `about.md`) for pages
- Edit files in `_typewriters/` for typewriter collection pages
- Edit files in `_layouts/` for template changes
- Edit files in `assets/` for CSS/JS changes

Jekyll automatically rebuilds when you save files - just refresh your browser!

### Build for Production

**Windows:**
```bash
build.bat
```

**Linux/Mac:**
```bash
bundle exec jekyll build
```

This generates the site in `_site/` directory.

## Deploy to GitHub Pages

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Update site"
   git push
   ```

2. GitHub Pages will automatically build and deploy your site
   - No manual build step needed
   - Site will be live at your GitHub Pages URL

## Troubleshooting

### Port Already in Use

If port 4000 is in use, Jekyll will automatically try port 4001, 4002, etc.

### Changes Not Showing

1. Check that Jekyll server is running
2. Refresh your browser (hard refresh: Ctrl+Shift+R or Cmd+Shift+R)
3. Check the terminal for any error messages

### Bundler Not Found

Make sure Ruby and Bundler are installed:
```bash
ruby --version
bundle --version
```

If Bundler is not installed:
```bash
gem install bundler
```

