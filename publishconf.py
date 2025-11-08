#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""
Publishing configuration for GitHub Pages deployment.
This file extends pelicanconf.py with production settings.
"""

import os
import sys
# Ensure we can import pelicanconf.py regardless of the working directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pelicanconf import *

# Production URL (update this when deploying to GitHub Pages or custom domain)
# For GitHub Pages: https://username.github.io or https://yourdomain.com
SITEURL = 'https://dairyking98.github.io/Portfolio'
RELATIVE_URLS = False

# Write generated site to repository root (so index.html is at project root)
OUTPUT_PATH = '.'
# Never delete the output directory when set to project root
DELETE_OUTPUT_DIRECTORY = False
# Ensure theme assets do not conflict with the repository's theme source folder
THEME_STATIC_DIR = 'site_theme'

# Disable feeds in production if not needed
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# Enable Google Analytics or other tracking (optional)
# GOOGLE_ANALYTICS = 'UA-XXXXX-Y'

# Enable Disqus comments (optional)
# DISQUS_SITENAME = 'your-disqus-shortname'

# Production optimizations
LOAD_CONTENT_CACHE = True

