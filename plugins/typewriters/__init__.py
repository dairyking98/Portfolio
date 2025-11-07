"""
Pelican plugin to automatically convert typewriters.csv to typewriters.json
during the build process.
"""

from pelican import signals
from pathlib import Path
import pandas as pd
import json


def clean_value(val):
    """Clean and format values for display."""
    if pd.isna(val) or val == 'NaN' or val == '':
        return None
    if isinstance(val, (int, float)):
        if pd.isna(val):
            return None
        # Format years as integers
        if isinstance(val, float) and val.is_integer():
            return int(val)
        return val
    val_str = str(val).strip()
    if val_str.lower() in ['nan', 'none', '']:
        return None
    return val_str


def process_typewriters(sender):
    """Process CSV and generate JSON before content generation."""
    csv_path = Path('content/typewriters.csv')
    json_path = Path('content/extra/typewriters.json')
    
    if not csv_path.exists():
        # CSV doesn't exist, skip processing
        return
    
    try:
        # Read CSV
        df = pd.read_csv(csv_path)
        
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Process each row
        typewriters = []
        for idx, row in df.iterrows():
            tw = {}
            for col in df.columns:
                value = clean_value(row[col])
                if value is not None:
                    tw[col] = value
            
            # Ensure we have at least a brand/model
            if 'Typewriter Brand' in tw or 'Model' in tw:
                typewriters.append(tw)
        
        # Ensure output directory exists
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(typewriters, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Processed {len(typewriters)} typewriters from CSV")
    except Exception as e:
        print(f"[WARNING] Could not process typewriters.csv: {e}")


def cache_articles_and_tags(article_generator):
    """After articles are finalized, cache articles and tags into settings."""
    settings = article_generator.settings
    settings['ALL_ARTICLES'] = list(article_generator.articles)
    settings['ALL_TAGS'] = article_generator.tags
    print(f"[OK] Cached {len(settings['ALL_ARTICLES'])} articles and tags for page templates")


def inject_into_page_context(page_generator, metadata):
    """Ensure page templates receive ALL_ARTICLES and ALL_TAGS in context."""
    settings = page_generator.settings
    ctx = page_generator.context
    if 'articles' not in ctx and 'ALL_ARTICLES' in settings:
        ctx['articles'] = settings['ALL_ARTICLES']
    if 'tags' not in ctx and 'ALL_TAGS' in settings:
        ctx['tags'] = settings['ALL_TAGS']


# (No per-content attachment needed with the context injection above)


def register():
    """Register the plugin with Pelican."""
    signals.initialized.connect(process_typewriters)
    # After articles are generated, cache lists into settings
    signals.article_generator_finalized.connect(cache_articles_and_tags)
    # Inject cached values into page template context
    signals.page_generator_context.connect(inject_into_page_context)

