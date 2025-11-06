#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""
Publishing configuration for GitHub Pages deployment.
This file extends pelicanconf.py with production settings.
"""

from pelicanconf import *

# Production URL (update this when deploying to GitHub Pages or custom domain)
# For GitHub Pages: https://username.github.io or https://yourdomain.com
SITEURL = 'https://dairyking98.github.io/Portfolio'
RELATIVE_URLS = False

# Disable feeds in production if not needed
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

# Enable Google Analytics or other tracking (optional)
# GOOGLE_ANALYTICS = 'UA-XXXXX-Y'

# Enable Disqus comments (optional)
# DISQUS_SITENAME = 'your-disqus-shortname'

# Production optimizations
LOAD_CONTENT_CACHE = True

