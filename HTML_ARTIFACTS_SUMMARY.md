# HTML Artifacts Summary

## Current Status

Based on the repository analysis, here's what we found:

### ✅ Legitimate HTML Source Files (Keep)
These are Jekyll source files with YAML front matter:
- `index.html` - Homepage
- `tags.html` - Tags listing page  
- `archives.html` - Archives page
- `typewriters.html` - Typewriters main page
- `_layouts/*.html` - Layout templates

### ⚠️ HTML Artifacts (Need to Remove from Git)
Many HTML artifacts from Pelican are still tracked in Git. These are generated files that Jekyll creates automatically:

1. **Root-level generated pages:**
   - `about/index.html` (source: `about.md`)
   - `my-collection/index.html`
   - `personal-projects/index.html` (source: `personal-projects.md`)
   - `projects/index.html` (source: `projects.md`)
   - `school-projects/index.html` (source: `school-projects.md`)

2. **Generated directories:**
   - `author/` - Author pages
   - `category/` - Category pages (Jekyll plugin generates these)
   - `posts/` - Post pages (source: `_posts/`)
   - `tag/` - Tag pages (Jekyll plugin generates these)
   - `typewriters/*/index.html` - Typewriter pages (source: `_typewriters/`)

## Solution

### Option 1: Remove from Git (Recommended)
Run the cleanup script:
```bash
.\remove_html_artifacts.bat
```

Or manually remove:
```bash
git rm about/index.html
git rm -r author/ category/ posts/ tag/
git rm my-collection/index.html personal-projects/index.html projects/index.html school-projects/index.html
git rm typewriters/index.html
# Remove individual typewriter pages
git rm typewriters/*/index.html
```

### Option 2: Add to .gitignore (Prevention)
The `.gitignore` has been updated to prevent future HTML artifacts from being added. However, files already tracked in Git need to be explicitly removed.

## Why Remove These?

1. **Jekyll generates them automatically** - No need to commit generated files
2. **Source files are the source of truth** - Markdown files in `_posts/`, `_typewriters/`, etc.
3. **Cleaner repository** - Only source files should be in Git
4. **GitHub Pages builds them** - GitHub generates these on deployment
5. **Prevents conflicts** - Generated files can cause merge conflicts

## After Cleanup

- ✅ Only source files (Markdown, layouts, config) in repository
- ✅ Jekyll generates HTML automatically when running `serve.bat` or `build.bat`
- ✅ GitHub Pages generates HTML automatically on deployment
- ✅ `.gitignore` prevents future HTML artifacts from being added

## Verification

After cleanup, verify:
```bash
# Check that only legitimate HTML files remain
git ls-files "*.html" | Where-Object { $_ -notlike "*_layouts*" -and $_ -notlike "*deprecated*" -and $_ -notlike "*theme*" }

# Should only show:
# - index.html
# - tags.html
# - archives.html
# - typewriters.html
```

## Next Steps

1. **Review the artifacts** - Check `CLEANUP_HTML_ARTIFACTS.md` for the full list
2. **Run cleanup script** - Execute `remove_html_artifacts.bat` to remove artifacts from Git
3. **Commit the cleanup** - `git commit -m "Remove HTML artifacts - Jekyll generates these automatically"`
4. **Verify locally** - Run `serve.bat` to ensure Jekyll generates the HTML correctly
5. **Push to GitHub** - GitHub Pages will build the site correctly

