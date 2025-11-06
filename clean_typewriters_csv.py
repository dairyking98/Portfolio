#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Clean and standardize the typewriters CSV for consistency.
This script normalizes capitalization, formatting, and data consistency.
"""

import pandas as pd
import re
from pathlib import Path

def clean_year(year_val):
    """Extract and format year consistently."""
    if pd.isna(year_val) or year_val == '':
        return None
    
    year_str = str(year_val).strip()
    
    # Handle date strings like "1901-07-01 00:00:00" -> "1901"
    # Or "2024-10-15 00:00:00" - but this might be in wrong column, skip if > 2000
    year_match = re.search(r'(\d{4})', year_str)
    if year_match:
        year = int(year_match.group(1))
        # Only return reasonable years (1800-2000 for typewriters)
        # Years after 2000 are likely dates in wrong column
        if 1800 <= year <= 2000:
            return str(year)
    
    # Handle year ranges like "1910-13" -> "1910"
    if '-' in year_str and len(year_str) <= 10:
        parts = year_str.split('-')
        if len(parts) == 2 and parts[0].isdigit():
            year = int(parts[0])
            if 1800 <= year <= 2000:
                return parts[0]
    
    return None

def clean_text(text):
    """Clean and standardize text fields."""
    if pd.isna(text) or text == '':
        return None
    
    text_str = str(text).strip()
    
    # Handle special markers
    if text_str.upper() in ['NAN', 'NONE', '???', '??']:
        return None
    
    return text_str

def capitalize_brand(brand):
    """Standardize brand capitalization."""
    if pd.isna(brand) or brand == '':
        return None
    
    brand_str = str(brand).strip()
    
    # Known brand exceptions
    brand_exceptions = {
        'ibm': 'IBM',
        'royal': 'Royal',
        'olympia': 'Olympia',
        'underwood': 'Underwood',
        'remington': 'Remington',
        'smith corona': 'Smith Corona',
        'blickensderfer': 'Blickensderfer',
        'hammond': 'Hammond',
        'corona': 'Corona',
        'facit': 'Facit',
        'hermes': 'Hermes',
        'mercedes': 'Mercedes',
        'triumph': 'Triumph',
        'fox': 'Fox',
        'oliver': 'Oliver',
        'yost': 'Yost',
        'new yost': 'New Yost',
        'postal': 'Postal',
        'emerson': 'Emerson',
        'mercury': 'Mercury',
        'consul': 'Consul',
        'alpina': 'Alpina',
        'everest': 'Everest',
        'antares': 'Antares',
        'mignon': 'Mignon',
        'woodstock': 'Woodstock',
        'continental': 'Continental',
        'harris': 'Harris',
        'bennett': 'Bennett',
        'sun': 'Sun',
        'reliance': 'Reliance',
        'national': 'National',
        'junior': 'Junior',
        'urania': 'Urania',
        'molle': 'Molle',
    }
    
    brand_lower = brand_str.lower()
    if brand_lower in brand_exceptions:
        return brand_exceptions[brand_lower]
    
    # Title case for others
    return brand_str.title()

def capitalize_model(model):
    """Standardize model capitalization."""
    if pd.isna(model) or model == '':
        return None
    
    model_str = str(model).strip()
    
    # Keep common model patterns
    # Models often have numbers and specific formatting
    # Standardize "no. 5" -> "No. 5"
    if re.match(r'^[Nn]o\.?\s*\d+', model_str, re.IGNORECASE):
        return re.sub(r'^([Nn])o\.?', r'No.', model_str, flags=re.IGNORECASE)
    
    # Keep already formatted like "Model 1", "No. 2 Standard"
    if re.match(r'^[A-Z][a-z]+', model_str):
        return model_str
    
    # Title case for others
    return model_str.title()

def clean_size(size):
    """Standardize size values."""
    if pd.isna(size) or size == '':
        return None
    
    size_str = str(size).strip().title()
    
    size_map = {
        'Standard': 'Standard',
        'Portable': 'Portable',
        'Ultra Portable': 'Ultra Portable',
    }
    
    return size_map.get(size_str, size_str)

def clean_typeface(typeface):
    """Standardize typeface values."""
    if pd.isna(typeface) or typeface == '':
        return None
    
    typeface_str = str(typeface).strip()
    
    # Keep asterisk as-is (wildcard)
    if typeface_str == '*':
        return '*'
    
    # Standardize common typefaces
    typeface_map = {
        'standard': 'Standard',
        'italic': 'Italic',
        'tall roman': 'Tall Roman',
        'royal vogue': 'Royal Vogue',
        'double gothic': 'Double Gothic',
        'pin point': 'Pin Point',
        'continental': 'Continental',
        'tall script raro75': 'Tall Script RaRo75',
        'bulletin': 'Bulletin',
        'esquire/bruxelles': 'Esquire/Bruxelles',
        'imperial': 'Imperial',
        'proportional modern': 'Proportional Modern',
        'congressional': 'Congressional',
        'steile zierschrift': 'Steile Zierschrift',
    }
    
    typeface_lower = typeface_str.lower()
    if typeface_lower in typeface_map:
        return typeface_map[typeface_lower]
    
    return typeface_str

def clean_layout(layout):
    """Standardize layout values."""
    if pd.isna(layout) or layout == '':
        return None
    
    layout_str = str(layout).strip()
    
    layout_map = {
        'qwerty': 'QWERTY',
        'qwertz': 'QWERTZ',
        'dhiatensor': 'DHIATENSOR',
        '3 bank': '3 Bank',
        'apothecary': 'Apothecary',
        'index': 'Index',
        'unshifted': 'Unshifted',
        'white russian': 'White Russian',
    }
    
    layout_lower = layout_str.lower()
    if layout_lower in layout_map:
        return layout_map[layout_lower]
    
    return layout_str

def clean_location(location):
    """Standardize location values."""
    if pd.isna(location) or location == '':
        return None
    
    location_str = str(location).strip()
    
    location_map = {
        'san francisco': 'San Francisco',
        'tracy': 'Tracy',
    }
    
    location_lower = location_str.lower()
    if location_lower in location_map:
        return location_map[location_lower]
    
    return location_str.title()

def clean_serial(serial):
    """Clean serial numbers."""
    if pd.isna(serial) or serial == '':
        return None
    
    serial_str = str(serial).strip()
    
    if serial_str.upper() in ['???', '??', 'NAN', 'NONE']:
        return None
    
    return serial_str

def clean_pitch(pitch):
    """Clean pitch values."""
    if pd.isna(pitch) or pitch == '':
        return None
    
    pitch_str = str(pitch).strip()
    
    # Handle date strings that got into pitch column (common data entry error)
    # Dates like "2024-10-15 00:00:00" should be removed
    if re.match(r'\d{4}-\d{2}-\d{2}', pitch_str):
        # This is a date, not a pitch - return None
        return None
    
    # Convert to string, remove decimals if whole number
    try:
        pitch_val = float(pitch_str)
        # Pitch should be reasonable (typically 6, 10, 12, etc.)
        if 0 < pitch_val <= 20:
            if pitch_val.is_integer():
                return str(int(pitch_val))
            return str(pitch_val)
        # Unreasonable pitch value
        return None
    except:
        return None

def clean_csv():
    """Clean the entire CSV file."""
    csv_path = Path('content/typewriters.csv')
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found!")
        return
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Clean each column
    print("Cleaning CSV data...")
    
    # Location
    if 'Location' in df.columns:
        df['Location'] = df['Location'].apply(clean_location)
    
    # Typewriter Brand
    if 'Typewriter Brand' in df.columns:
        df['Typewriter Brand'] = df['Typewriter Brand'].apply(capitalize_brand)
    
    # Model
    if 'Model' in df.columns:
        df['Model'] = df['Model'].apply(capitalize_model)
    
    # Size
    if 'Size' in df.columns:
        df['Size'] = df['Size'].apply(clean_size)
    
    # Year
    if 'Year' in df.columns:
        df['Year'] = df['Year'].apply(clean_year)
    
    # Serial No
    if 'Serial No' in df.columns:
        df['Serial No'] = df['Serial No'].apply(clean_serial)
    
    # Pitch
    if 'Pitch' in df.columns:
        df['Pitch'] = df['Pitch'].apply(clean_pitch)
    
    # Typeface
    if 'Typeface' in df.columns:
        df['Typeface'] = df['Typeface'].apply(clean_typeface)
    
    # Layout
    if 'Layout' in df.columns:
        df['Layout'] = df['Layout'].apply(clean_layout)
    
    # Clean other text fields
    text_columns = ['Color', 'Notes', 'Work Needed', 'From Where & Who']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    
    # Save cleaned CSV
    df.to_csv(csv_path, index=False)
    print(f"[OK] Cleaned CSV saved to {csv_path}")
    print(f"  Total rows: {len(df)}")
    
    return df

if __name__ == '__main__':
    clean_csv()

