#!/usr/bin/env python
# -*- coding: utf-8 -*- #
"""
Pelican configuration file for personal portfolio and engineering blog.
"""

import os
from datetime import date

# Basic site information
AUTHOR = 'Leonard Chau'
SITENAME = 'Leonard Chau - Portfolio & Engineering Blog'
SITEURL = os.environ.get('SITEURL', '')
SITEDESCRIPTION = 'Personal portfolio and engineering blog'
RELATIVE_URLS = not SITEURL

# Paths
PATH = 'content'
ARTICLE_PATHS = ['posts']  # Only files in posts/ are articles
PAGE_PATHS = ['', 'typewriters']  # Files in content root and typewriters/ are pages
PAGE_EXCLUDES = ['images', 'documents', 'extra', 'posts']  # Exclude static and article dirs from pages
STATIC_PATHS = ['images', 'extra', 'documents']
EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/typewriters.json': {'path': 'typewriters.json'},
}
IGNORE_FILES = ['README.md']  # Do not try to parse repository READMEs as content

# Time and locale
TIMEZONE = 'America/New_York'
DEFAULT_LANG = 'en'
DATE_FORMATS = {
    'en': '%B %d, %Y',
}

# Feed settings (disabled for now, can enable later)
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Pagination
DEFAULT_PAGINATION = 10
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# URL settings
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
DRAFT_URL = 'drafts/{slug}/'
DRAFT_SAVE_AS = 'drafts/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL = 'tags.html'
TAGS_SAVE_AS = 'tags.html'
ARCHIVES_URL = 'archives.html'
ARCHIVES_SAVE_AS = 'archives.html'
AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
AUTHORS_URL = 'authors.html'
AUTHORS_SAVE_AS = 'authors.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_URL = 'categories.html'
CATEGORIES_SAVE_AS = 'categories.html'

# Theme
THEME = 'theme'
THEME_STATIC_DIR = 'site_theme'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['typewriters']

# Markdown extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'css_class': 'highlight',
            'linenums': True,
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {
            'permalink': False,
        },
    },
    'output_format': 'html5',
}

# Disable unnecessary pages
DIRECT_TEMPLATES = ['index', 'tags', 'archives']
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_SAVE_AS = 'tags.html'

# Site metadata
DEFAULT_METADATA = {
    'status': 'published',
}

# Social links (customize as needed)
SOCIAL = (
    ('GitHub', 'https://github.com/yourusername'),
)

# Typewriter collection links
TYPEWRITERS_SPREADSHEET_URL = ''  # Add your Google Sheets or CSV link here
TYPEWRITERS_GALLERY_URL = ''  # Add gallery link if you have one
TYPEWRITERS_3D_ELEMENTS_GITHUB = ''  # Add GitHub repo link for 3D type elements

# Menu items
MENUITEMS = (
    ('Home', '/'),
    ('About', '/about'),
    ('School Projects', '/school-projects'),
    ('Personal Projects', '/personal-projects'),
    ('Typewriters', '/typewriters'),
    ('Tags', '/tags.html'),
    ('Archives', '/archives.html'),
)

# Footer information
FOOTER_TEXT = f'© {date.today().year} {AUTHOR}. All rights reserved.'

# Output settings
OUTPUT_PATH = 'dev'  # Development builds go to ./dev
DELETE_OUTPUT_DIRECTORY = True

# Typogrify settings (for better typography)
TYPOGRIFY = True

