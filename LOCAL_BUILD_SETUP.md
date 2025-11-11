# Local Build Setup

This project is configured so that:
- **GitHub Pages builds from root** (automatic Jekyll build)
- **Local builds go to `local/_site/`** (subdirectory, gitignored)

## Why This Setup?

- Keeps the repository root clean
- Local build artifacts don't get committed
- GitHub Pages builds independently from root
- No conflicts between local and GitHub builds

## How It Works

### Local Development

When you run `serve.bat` or `build.bat`:
- Jekyll builds to `local/_site/` (not root `_site/`)
- The `local/` directory is gitignored
- Your local builds don't affect the repository

### GitHub Pages

When you push to GitHub:
- GitHub Pages builds from the root directory
- Uses its own build process (not your local `local/_site/`)
- Deploys the built site automatically
- Your local build directory is never pushed (gitignored)

## File Structure

```
.
├── _posts/          # Blog posts (source files)
├── _layouts/        # Layouts (source files)
├── _config.yml      # Jekyll config (source file)
├── local/           # Local build output (gitignored)
│   └── _site/       # Generated HTML files (local only)
├── serve.bat        # Local server (builds to local/_site/)
└── build.bat        # Local build (builds to local/_site/)
```

## Commands

### Local Development

```bash
# Start local server (builds to local/_site/)
serve.bat

# Build locally (builds to local/_site/)
build.bat
```

### Deployment

```bash
# Just push to GitHub - GitHub builds from root
git add .
git commit -m "Update site"
git push origin main
```

## Important Notes

1. **Don't commit `local/`** - It's already in `.gitignore`
2. **GitHub builds from root** - Don't worry about `local/` on GitHub
3. **Local builds are for testing** - GitHub Pages does the real build
4. **`_site/` in root is also gitignored** - Just in case GitHub Pages creates it

## Troubleshooting

### "local/_site/ doesn't exist"
- Run `serve.bat` or `build.bat` first
- Jekyll will create the directory automatically

### "GitHub Pages not building"
- Check repository Settings → Pages
- Make sure source is set to `main` branch, `/ (root)` folder
- GitHub Pages will build from root (not from `local/`)

### "Local build works but GitHub doesn't"
- Check `_config.yml` for GitHub Pages compatibility
- Make sure plugins are allowed on GitHub Pages
- Check GitHub Actions logs for build errors

