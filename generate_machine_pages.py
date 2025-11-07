#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate machine page files for typewriters that have make, model, and serial.
Run this script to create placeholder pages for machines that don't have pages yet.
"""

import pandas as pd
from pathlib import Path
import re

def slugify(text):
    """Generate URL slug from text."""
    if not text or pd.isna(text):
        return ''
    text_str = str(text).strip()
    return re.sub(r'[^\w\s-]', '', text_str.lower()).strip().replace(' ', '-').replace('_', '-')

def generate_machine_page(tw, output_dir):
    """Generate a machine page file if it doesn't exist.
    Requires make, model, and serial number. Pages without serial numbers
    are handled by the Pelican plugin based on CSV data.
    """
    make = tw.get('Typewriter Brand', '')
    model = tw.get('Model', '')
    serial = tw.get('Serial No', '')
    
    # Only generate if all three exist (serial is required - no serial means no page)
    if not make or not model or not serial or pd.isna(make) or pd.isna(model) or pd.isna(serial):
        return None
    
    make_slug = slugify(make)
    model_slug = slugify(model)
    serial_slug = slugify(serial)
    
    if not make_slug or not model_slug or not serial_slug:
        return None
    
    # Generate filename
    filename = f"{make_slug}-{model_slug}-{serial_slug}.md"
    filepath = Path(output_dir) / filename
    
    # Skip if file already exists
    if filepath.exists():
        return None
    
    # Generate page content
    title = f"{make} {model} - Serial {serial}"
    
    # Build metadata section
    metadata_lines = [f"Title: {title}"]
    metadata_lines.append("Date: 2025-02-10")
    metadata_lines.append("Category: machine")
    metadata_lines.append("template: typewriter_machine")
    metadata_lines.append(f"Save_as: typewriters/{make_slug}-{model_slug}-{serial_slug}/index.html")
    metadata_lines.append(f"URL: typewriters/{make_slug}-{model_slug}-{serial_slug}/")
    metadata_lines.append("")
    
    # Add custom metadata
    if make:
        metadata_lines.append(f"make: {make}")
    if model:
        metadata_lines.append(f"model: {model}")
    if serial:
        metadata_lines.append(f"serial: {serial}")
    if tw.get('Year') and not pd.isna(tw.get('Year')):
        metadata_lines.append(f"year: {tw['Year']}")
    if tw.get('Size') and not pd.isna(tw.get('Size')):
        metadata_lines.append(f"size: {tw['Size']}")
    if tw.get('Electric/Manual') and not pd.isna(tw.get('Electric/Manual')):
        metadata_lines.append(f"type: {tw['Electric/Manual']}")
    if tw.get('Pitch') and not pd.isna(tw.get('Pitch')):
        metadata_lines.append(f"pitch: {tw['Pitch']}")
    if tw.get('Typeface') and not pd.isna(tw.get('Typeface')):
        metadata_lines.append(f"typeface: {tw['Typeface']}")
    if tw.get('Layout') and not pd.isna(tw.get('Layout')):
        metadata_lines.append(f"layout: {tw['Layout']}")
    if tw.get('Color') and not pd.isna(tw.get('Color')):
        metadata_lines.append(f"color: {tw['Color']}")
    if tw.get('Location') and not pd.isna(tw.get('Location')):
        metadata_lines.append(f"location: {tw['Location']}")
    if tw.get('Notes') and not pd.isna(tw.get('Notes')):
        metadata_lines.append(f"notes: {tw['Notes']}")
    if tw.get('Work Needed') and not pd.isna(tw.get('Work Needed')):
        metadata_lines.append(f"work_needed: {tw['Work Needed']}")
    
    metadata_section = "\n".join(metadata_lines)
    
    content = f"""{metadata_section}

# {title}

## Overview

This page documents the {make} {model} typewriter with serial number {serial}.

## Description

Add description, photos, and details about this typewriter here.
"""
    
    # Write file
    filepath.write_text(content, encoding='utf-8')
    return filepath

def main():
    """Generate machine pages for all typewriters."""
    csv_path = Path('content/typewriters.csv')
    output_dir = Path('content/typewriters')
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found!")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    generated = 0
    skipped = 0
    
    for idx, row in df.iterrows():
        tw = row.to_dict()
        result = generate_machine_page(tw, output_dir)
        if result:
            print(f"Generated: {result.name}")
            generated += 1
        else:
            skipped += 1
    
    print(f"\n[OK] Generated {generated} machine pages")
    print(f"  Skipped {skipped} (already exist or missing required fields)")

if __name__ == '__main__':
    main()

