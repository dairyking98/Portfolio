# Installing Ruby on Windows

Ruby is required to run Jekyll. Follow these steps to install Ruby on Windows:

## Option 1: RubyInstaller (Recommended)

1. **Download RubyInstaller:**
   - Go to https://rubyinstaller.org/downloads/
   - Download **Ruby+Devkit** version (recommended: Ruby 3.2.x or 3.3.x)
   - Choose the **x64** version for 64-bit Windows

2. **Install Ruby:**
   - Run the installer
   - Check "Add Ruby executables to your PATH" during installation
   - Check "Run 'ridk install' to setup MSYS2 and development toolchain" at the end
   - Click "Finish" to open the MSYS2 setup

3. **Setup MSYS2 (Development Tools):**
   - In the MSYS2 terminal that opens, type: `3` and press Enter
   - This installs the development toolchain needed for building native extensions
   - Wait for the installation to complete

4. **Verify Installation:**
   - Open a **new** Command Prompt or PowerShell window
   - Run: `ruby --version`
   - Run: `gem --version`
   - Both commands should show version numbers

5. **Install Bundler:**
   - Run: `gem install bundler`
   - Verify: `bundle --version`

6. **Install Jekyll Dependencies:**
   - Navigate to your project directory
   - Run: `bundle install`
   - Or use: `install.bat`

## Option 2: Windows Subsystem for Linux (WSL)

If you prefer Linux tools:

1. **Install WSL:**
   - Open PowerShell as Administrator
   - Run: `wsl --install`
   - Restart your computer

2. **Install Ruby in WSL:**
   - Open WSL terminal
   - Run: `sudo apt-get update`
   - Run: `sudo apt-get install ruby ruby-dev build-essential`
   - Run: `gem install bundler`

3. **Use Jekyll in WSL:**
   - Navigate to your project in WSL
   - Run: `bundle install`
   - Run: `bundle exec jekyll serve`

## Troubleshooting

### "gem is not recognized" in Cursor/PowerShell (but works in CMD)
This is a common issue where PowerShell doesn't refresh the PATH after Ruby installation.

**Solution:**
- **Restart Cursor completely** (close all windows and reopen)
- The terminal will pick up the updated PATH after restart
- Alternatively, use the `.bat` files which work in both CMD and PowerShell

### "gem is not recognized" (general)
- Ruby is not installed or not in PATH
- Restart your terminal after installing Ruby
- Verify Ruby is in PATH: `echo $env:PATH` (PowerShell) or `echo %PATH%` (CMD)
- Reinstall Ruby and make sure "Add Ruby executables to your PATH" is checked

### "Failed to build native extension"
- You need the Devkit (development tools)
- Reinstall Ruby with Ruby+Devkit version
- Run `ridk install` and select option 3

### "wdm gem build error" (Ruby 3.3)
- The `wdm` gem is not compatible with Ruby 3.3
- This is already handled in the Gemfile (wdm is commented out)
- Jekyll will use polling instead of native file watching (slightly slower but works fine)
- If you see this error, make sure your Gemfile has wdm commented out

### "SSL certificate verification failed"
- Update RubyGems: `gem update --system`
- Or update certificates: `gem install --trust-policy MediumSecurity gem_name`

### Port 4000 already in use
- Jekyll will automatically try the next available port (4001, 4002, etc.)
- Or specify a port: `bundle exec jekyll serve --port 4001`

## After Installation

Once Ruby is installed:

1. **Install Jekyll dependencies:**
   ```bash
   bundle install
   ```
   Or use: `install.bat`

2. **Start development server:**
   ```bash
   bundle exec jekyll serve
   ```
   Or use: `serve.bat`

3. **Open in browser:**
   - Go to http://localhost:4000

## Alternative: Use GitHub Codespaces or GitHub Actions

If you don't want to install Ruby locally, you can:
- Use GitHub Codespaces (browser-based development environment)
- Use GitHub Actions to build and deploy automatically (no local build needed)
- Push to GitHub and let GitHub Pages build the site automatically


