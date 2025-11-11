# Personal Portfolio & Engineering Blog

A Jekyll-based static site generator for a personal portfolio and engineering blog.

## Features

- ✅ Clean, minimal engineering aesthetic
- ✅ Responsive design
- ✅ Syntax highlighting for code blocks
- ✅ Tag-based organization
- ✅ Archive pages
- ✅ GitHub Pages ready
- ✅ Typewriter collection with CSV data processing

## Project Structure

```
.
├── _posts/          # Blog posts (Markdown files)
├── _layouts/        # HTML layout templates
├── _includes/       # Reusable template components
├── _plugins/        # Jekyll plugins
├── _data/           # Data files (JSON, YAML, CSV)
├── typewriters/     # Typewriter collection pages
├── assets/          # CSS, JS, and images
├── images/          # Content images
├── documents/       # PDF documents and files
├── _config.yml      # Jekyll configuration
├── Gemfile          # Ruby dependencies
└── index.html       # Homepage
```

## Setup

### 1. Install Ruby and Bundler

**Windows:**
1. Download **Ruby+Devkit** from https://rubyinstaller.org/downloads/
2. Run the installer and check "Add Ruby executables to your PATH"
3. At the end, check "Run 'ridk install'" and select option 3 to install development tools
4. Open a **new** terminal and verify: `ruby --version` and `gem --version`
5. See `INSTALL_RUBY.md` for detailed instructions

**macOS:**
```bash
# Using Homebrew:
brew install ruby
```

**Linux:**
```bash
sudo apt-get install ruby ruby-dev build-essential
```

### 2. Install Jekyll and Dependencies

**On Windows (using batch files):**
```bash
# Double-click install.bat or run in command prompt/PowerShell:
install.bat

# Note: If "gem is not recognized" in Cursor/PowerShell but works in CMD:
# - Restart Cursor completely (close all windows and reopen)
# - Or use the batch files (they work in both CMD and PowerShell)
```

**On Linux/Mac (using command line):**
```bash
# Install Bundler
gem install bundler

# Install dependencies
bundle install
```

### 3. Build and Serve the Site

**For local development and testing before pushing to GitHub:**

**On Windows (using batch files):**
```bash
# Start local development server (recommended)
serve.bat

# Build the site (generates local/_site/ directory)
build.bat
```

**On Linux/Mac (using command line):**
```bash
# Build the site (generates local/_site/ directory)
bundle exec jekyll build --destination local/_site

# Serve locally with auto-reload (recommended for development)
bundle exec jekyll serve --destination local/_site

# Serve on custom port (if default port 4000 is in use)
bundle exec jekyll serve --destination local/_site --port 4001

# Serve with auto-reload and watch for changes
bundle exec jekyll serve --destination local/_site --livereload
```

Then open http://localhost:4000 (or your custom port) in your browser.

**Note:** 
- On Windows: Use `serve.bat` to start the local development server (replaces old `build.py serve` command)
- The server automatically rebuilds the site when you make changes to files
- **Local builds go to `local/_site/`** (not root `_site/`) - root stays clean
- **GitHub Pages builds in root** automatically when you push to GitHub
- No need to manually build before serving - Jekyll handles it automatically
- Source HTML files (`index.html`, `tags.html`, etc.) are in root - these are Jekyll source files, not generated artifacts

## Usage

### Creating Blog Posts

Create a new Markdown file in `_posts/` with the following naming format: `YYYY-MM-DD-slug.md`

```markdown
---
title: Your Post Title
date: 2025-02-10 10:00:00 -0500
tags:
  - tag1
  - tag2
  - tag3
category: Category Name
description: A brief summary of your post
thumbnail: /images/thumbnail.jpg
---

Your post content here...
```

### Adding Pages

Create Markdown files in the root directory or `_pages/` for static pages like About or Projects:

```markdown
---
title: About
layout: page
---

Your page content...
```

### Typewriter Collection

Typewriter collection pages are stored in `typewriters/` directory. The CSV data is automatically processed by the Jekyll plugin in `_plugins/typewriters_generator.rb` and converted to JSON in `_data/typewriters.json`.

## Deployment to GitHub Pages

### Option 1: Native Jekyll Support (Recommended)

1. Push your code to GitHub (Jekyll source files in root)
2. Go to repository Settings → Pages
3. Select source: "Deploy from a branch"
4. Branch: `main` / folder: `/ (root)`
5. GitHub will automatically build and deploy your Jekyll site
6. **Note:** GitHub builds from root. Local builds go to `local/_site/` (gitignored)

### Option 2: GitHub Actions

Create `.github/workflows/jekyll.yml`:

```yaml
name: Jekyll site CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-ruby@v1
      with:
        ruby-version: '3.1'
        bundler-cache: true
    - run: bundle exec jekyll build
    - uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./_site
```

## Custom Domain Setup

1. **Add a `CNAME` file to the root directory:**
   ```
   yourdomain.com
   ```

2. **Update `_config.yml`:**
   ```yaml
   url: "https://yourdomain.com"
   ```

3. **Configure DNS:**
   - Add a CNAME record pointing to `yourusername.github.io`
   - Or add A records for GitHub Pages IPs (see GitHub Pages docs)

4. **Enable custom domain in GitHub:**
   - Repository Settings → Pages → Custom domain
   - Enter your domain name

## Configuration

### Site Information

Edit `_config.yml` to customize:

- `title` - Site title
- `author` - Your name
- `description` - Site description
- `url` - Site URL
- `navigation` - Navigation menu items
- `social` - Social media links

### Theme Customization

The theme is located in `_layouts/` and `assets/`:

- `_layouts/` - HTML layout templates
- `assets/css/main.css` - Main stylesheet
- `assets/js/main.js` - JavaScript

Edit `main.css` to customize colors, fonts, and layout. The CSS uses CSS variables for easy customization:

```css
:root {
    --color-bg: #ffffff;
    --color-text: #1a1a1a;
    --color-accent: #2563eb;
    /* ... */
}
```

## Development Tips

### `serve.bat` vs `build.bat` - What's the Difference?

**`serve.bat` (Recommended for Development):**
- ✅ Builds the site AND starts a local web server
- ✅ Serves at http://localhost:4000
- ✅ Automatically rebuilds when you change files
- ✅ Shows build errors in the terminal
- ✅ **Use this for daily development** - it does everything you need

**`build.bat` (Optional - Testing Only):**
- Builds the site to `local/_site/` directory only
- Does NOT start a web server
- Useful for:
  - Testing that the site builds without errors
  - Inspecting the generated HTML files directly
- **Not needed for normal development** - `serve.bat` builds automatically
- **Note:** Local builds go to `local/_site/` (subdirectory), but GitHub Pages builds from root

### Quick Start Workflow

1. **For local development:** Use `serve.bat` (Windows) or `bundle exec jekyll serve` (Linux/Mac)
   - This builds and serves your site automatically
   - Just edit files and refresh your browser
   - No need to run `build.bat` separately

2. **To test builds:** Run `build.bat` if you want to verify the site builds without errors
   - Generates files in `local/_site/` directory (subdirectory, not root)
   - Check for any build errors in the terminal

3. **For deployment:** Just push to GitHub - GitHub Pages builds automatically
   - No need to build locally before pushing
   - GitHub Pages builds from root (not from `local/` subdirectory)
   - Local builds (`local/_site/`) are gitignored and won't be pushed

### Other Tips

- **File Changes:** Jekyll automatically detects changes and rebuilds (when using `serve`)
- **Browser Refresh:** After Jekyll rebuilds, refresh your browser to see changes
- **Port Already in Use:** Use `bundle exec jekyll serve --port 4001` to use a different port

## Troubleshooting

### Jekyll Not Found

Make sure you've installed Ruby and Bundler, and run `bundle install`:

```bash
gem install bundler
bundle install
```

### Port Already in Use

If port 4000 is in use:

```bash
bundle exec jekyll serve --port 4001
```

### Plugin Errors

Make sure all plugins are listed in `_config.yml` under the `plugins:` section and that the required gems are installed via `Gemfile`.

## Migration from Pelican

This site was migrated from Pelican to Jekyll. Key changes:

- Content files moved from `content/posts/` to `_posts/`
- Templates converted from Jinja2 to Liquid
- Configuration converted from `pelicanconf.py` to `_config.yml`
- Typewriters plugin converted from Python to Ruby
- Build system changed from Python scripts to Jekyll commands
- **Old build scripts removed:** `build.py`, `build.bat`, `build_gui.py` are no longer needed
- **New batch files created:** `serve.bat`, `build.bat`, `install.bat` for Windows users
- **New serve command:** Use `serve.bat` (Windows) or `bundle exec jekyll serve` (Linux/Mac) instead of `python build.py serve`
- **No manual HTML generation:** Jekyll automatically generates HTML from Markdown - no need for custom HTML files
- **Pelican output directories removed:** Old `dev/` directory and all Pelican-generated HTML files have been cleaned up
- **Pelican feeds removed:** Old Atom feeds removed (Jekyll will regenerate them automatically via `jekyll-feed` plugin)
- **Clean structure:** Only Jekyll source files remain - no generated HTML files in the repository

## Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [GitHub Pages Documentation](https://docs.github.com/pages)
- [Markdown Guide](https://www.markdownguide.org/)

## License

This project is open source and available for personal use.
