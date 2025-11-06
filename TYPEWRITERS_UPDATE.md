# Updating the Typewriter Collection

## Quick Update Instructions

1. **Edit the CSV file**: Open `content/typewriters.csv` in Excel, Google Sheets, or any spreadsheet editor
2. **Make your changes**: Add, remove, or modify typewriter entries
3. **Save the CSV file**
4. **Rebuild site**: Run your normal Pelican build process (CSV to JSON conversion happens automatically!)

## File Structure

- **`content/typewriters.csv`** - Master spreadsheet (edit this!)
- **`content/extra/typewriters.json`** - Generated JSON file (auto-generated during build, don't edit manually)
- **`plugins/typewriters/`** - Pelican plugin that automatically converts CSV to JSON during build
- **`process_typewriters.py`** - Standalone utility script (optional, for manual testing)

## CSV Format

The CSV should have these columns (case-sensitive):
- Location
- Typewriter Brand
- Model
- Size
- Electric/Manual
- Length, Width, Height (dimensions)
- Color
- Serial No
- Year
- Pitch
- Typeface
- Layout
- New Rubber?
- Sale Price
- Purchase Price
- Value
- Date Acquired
- From Where & Who
- Notes
- Work Needed

## Features

The typewriter collection page includes:
- **List View**: Full table with all details, searchable and sortable
- **Pivot View**: Grouped statistics by Brand, Size, Type, Location, or Year
- **Search**: Filter typewriters by any field
- **Sorting**: Sort by Brand, Year, Model, Location, Value, or Purchase Price

## Notes

- Empty cells will display as "—" in the table
- The JSON file is automatically generated during the Pelican build - don't edit it manually
- **No manual conversion step needed!** Just edit the CSV and rebuild - the plugin handles the rest
- The conversion happens automatically via the Pelican plugin when you run `pelican` or `build.py build`

