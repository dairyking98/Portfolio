# Personal Portfolio & Engineering Blog

A Pelican-based static site generator for a personal portfolio and engineering blog.

## Features

- ✅ Clean, minimal engineering aesthetic
- ✅ Responsive design
- ✅ Syntax highlighting for code blocks
- ✅ Tag-based organization
- ✅ Archive pages
- ✅ GitHub Pages ready

## Project Structure

```
.
├── content/
│   ├── posts/          # Blog posts (Markdown files)
│   └── images/         # Images for posts
├── theme/              # Custom Pelican theme
│   ├── templates/      # HTML templates
│   └── static/         # CSS and static assets
├── output/             # Generated site (gitignored)
├── pelicanconf.py      # Development configuration
├── publishconf.py      # Production configuration
├── build.py            # Python build script
├── build.bat           # Windows batch script
└── requirements.txt    # Python dependencies
```

## Setup

### 1. Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Build the Site

**On Windows:**
```bash
build.bat build
```

**On Linux/Mac:**
```bash
python build.py build
```

### 3. Preview Locally

**On Windows:**
```bash
build.bat serve
```

**On Linux/Mac:**
```bash
python build.py serve
```

Then open http://localhost:8000 in your browser.

## Usage

### Build Script Commands

The `build.py` script supports several commands:

- `build` - Build the site (development mode)
- `build --prod` - Build the site (production mode)
- `serve` - Serve site locally (default port 8000)
- `serve --port 8080` - Serve on custom port
- `clean` - Clean the output directory
- `rebuild` - Clean and rebuild the site
- `rebuild --prod` - Clean and rebuild in production mode

**Windows Example:**
```bash
build.bat build          # Build site
build.bat serve          # Serve locally
build.bat rebuild --prod # Rebuild for production
```

**Linux/Mac Example:**
```bash
python build.py build
python build.py serve
python build.py rebuild --prod
```

### Creating Blog Posts

Create a new Markdown file in `content/posts/` with the following metadata format:

```markdown
Title: Your Post Title
Date: 2025-02-10 10:00
Tags: tag1, tag2, tag3
Category: Category Name
Summary: A brief summary of your post
Thumbnail: /images/thumbnail.jpg

Your post content here...
```

**Example filename:** `content/posts/2025-02-10-my-post.md`

### Adding Pages

Create Markdown files in `content/` (not in `posts/`) for static pages like About or Projects:

```markdown
Title: About
Date: 2025-02-10

Your page content...
```

Pelican will automatically create pages at `/about/`, `/projects/`, etc.

## Deployment to GitHub Pages

### Option 1: Deploy from `output/` folder

1. **Update `publishconf.py`:**
   ```python
   SITEURL = 'https://yourusername.github.io'
   ```

2. **Build for production:**
   ```bash
   build.bat build --prod
   # or
   python build.py build --prod
   ```

3. **Initialize git in output folder (if not already):**
   ```bash
   cd output
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/yourusername.github.io.git
   git push -u origin main
   ```

4. **Enable GitHub Pages:**
   - Go to your repository settings
   - Navigate to Pages section
   - Select source: "Deploy from a branch"
   - Branch: `main` / folder: `/ (root)`

### Option 2: Use GitHub Actions (Recommended)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish Site

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Build site
        run: python build.py build --prod
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./output
```

This will automatically build and deploy your site on every push to main.

## Custom Domain Setup

1. **Add a `CNAME` file to `content/extra/`:**
   ```
   yourdomain.com
   ```

2. **Update `publishconf.py`:**
   ```python
   SITEURL = 'https://yourdomain.com'
   ```

3. **Configure DNS:**
   - Add a CNAME record pointing to `yourusername.github.io`
   - Or add A records for GitHub Pages IPs (see GitHub Pages docs)

4. **Enable custom domain in GitHub:**
   - Repository Settings → Pages → Custom domain
   - Enter your domain name

5. **Rebuild and deploy:**
   ```bash
   build.bat build --prod
   # Then commit and push the output folder
   ```

## Configuration

### Site Information

Edit `pelicanconf.py` to customize:

- `AUTHOR` - Your name
- `SITENAME` - Site title
- `SITEDESCRIPTION` - Site description
- `SOCIAL` - Social media links
- `MENUITEMS` - Navigation menu items

### Theme Customization

The theme is located in `theme/`:

- `theme/templates/` - HTML templates
- `theme/static/css/main.css` - Stylesheet

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

- **Live Reload:** Use `build.bat serve` or `python build.py serve` to preview changes
- **Clean Build:** Use `rebuild` command to ensure a fresh build
- **Production Build:** Always use `--prod` flag when building for deployment

## Troubleshooting

### Port Already in Use

If port 8000 is in use:
```bash
build.bat serve --port 8080
```

### Pelican Not Found

Make sure you've activated the virtual environment and installed requirements:
```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Images Not Showing

- Ensure images are in `content/images/`
- Reference them in posts as `/images/filename.jpg`
- Rebuild the site after adding images

## License

This project is open source and available for personal use.

## Resources

- [Pelican Documentation](https://docs.getpelican.com/)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Pages Documentation](https://docs.github.com/pages)

