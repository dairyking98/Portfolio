# What is `build.bat` for?

## Quick Answer

`build.bat` generates the static HTML files but **doesn't start a web server**. For development, use `serve.bat` instead (it builds AND serves).

## Detailed Explanation

### `jekyll build` (build.bat)
- **What it does:** Converts your Markdown files, layouts, and assets into static HTML files
- **Output:** Creates a `_site/` directory with all the generated HTML, CSS, and JS files
- **Server:** Does NOT start a web server
- **Use cases:**
  - Testing that your site builds without errors
  - Inspecting the generated HTML files directly
  - Production builds (though GitHub Pages does this automatically)
  - CI/CD pipelines that need the built files

### `jekyll serve` (serve.bat) - **Recommended for Development**
- **What it does:** Builds the site AND starts a local web server
- **Output:** Creates `_site/` directory AND serves it at http://localhost:4000
- **Server:** Starts a web server you can access in your browser
- **Auto-reload:** Automatically rebuilds when you change files
- **Use cases:**
  - Daily development and testing
  - Previewing changes in a browser
  - This is what you'll use 99% of the time

## When to Use Each

### Use `serve.bat` When:
- ✅ Developing locally (daily use)
- ✅ Testing changes in a browser
- ✅ Writing new blog posts
- ✅ Updating layouts or CSS
- ✅ **This is what you should use for development**

### Use `build.bat` When:
- ✅ Testing that the site builds without errors
- ✅ Inspecting generated HTML files
- ✅ Debugging build issues
- ✅ Verifying production build works
- ⚠️ **Not needed for normal development**

## Workflow Comparison

### Development Workflow (Recommended)
```bash
# 1. Make changes to files
# 2. Run serve (builds AND serves)
serve.bat

# 3. View at http://localhost:4000
# 4. Edit files, refresh browser
# 5. When done, commit and push
```

### Build-Only Workflow (Rarely Needed)
```bash
# 1. Make changes to files
# 2. Run build (generates files only)
build.bat

# 3. Inspect _site/ directory
# 4. No web server - can't view in browser easily
# 5. Would need to serve _site/ with another tool
```

## Key Points

1. **For development:** Use `serve.bat` - it does everything
2. **`serve` includes `build`:** When you run `serve`, it automatically builds first
3. **No need to build separately:** You don't need to run `build.bat` before `serve.bat`
4. **GitHub Pages builds automatically:** When you push to GitHub, it builds for you
5. **`_site/` is generated:** Don't commit `_site/` to Git - it's build output (already in `.gitignore`)

## Example

```bash
# Normal development session:
serve.bat
# → Builds site
# → Starts server at http://localhost:4000
# → Watches for changes
# → Auto-rebuilds when you save files

# You can now:
# - Edit _posts/2025-02-15-new-post.md
# - Save the file
# - Refresh browser at http://localhost:4000
# - See your changes immediately

# When you're done:
# - Stop server (Ctrl+C)
# - Commit changes
# - Push to GitHub
# - GitHub Pages builds and deploys automatically
```

## Summary

- **`serve.bat`** = Build + Serve + Watch (use this for development)
- **`build.bat`** = Build only (rarely needed, mainly for testing)

For 99% of your development work, just use `serve.bat` and you're all set!

