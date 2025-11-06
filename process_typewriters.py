#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Process typewriter CSV and generate JSON for website display.
Run this script after updating content/typewriters.csv
"""

import pandas as pd
import json
import os
from pathlib import Path

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

def process_typewriters():
    """Process CSV and generate JSON."""
    csv_path = Path('content/typewriters.csv')
    json_path = Path('content/extra/typewriters.json')
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found!")
        return
    
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
    
    # Save JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(typewriters, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(typewriters)} typewriters")
    print(f"JSON saved to {json_path}")

if __name__ == '__main__':
    process_typewriters()

