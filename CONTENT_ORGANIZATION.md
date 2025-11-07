# Content Organization Guide

This document describes the organization system for content, images, and documents in this Pelican portfolio site.

## Directory Structure

```
content/
├── documents/          # Source documents (PDFs, reports, etc.)
│   ├── YYYY/          # Organized by year
│   │   └── project-name/
│   │       └── *.pdf
│   └── README.md
├── images/            # Images for posts
│   ├── YYYY/          # Organized by year
│   │   └── project-name/
│   │       └── *.jpg, *.png
│   └── README.md
├── posts/             # Blog posts (articles)
│   └── YYYY-MM-DD-slug.md
└── extra/             # Extra static files
```

## Organization Principles

### 1. Year-Based Organization
- Both `documents/` and `images/` are organized by year (e.g., `2022/`, `2023/`)
- This makes it easy to find content from specific time periods
- Supports chronological browsing

### 2. Project-Based Subdirectories
- Within each year, create project-specific folders
- Use lowercase with hyphens: `cad-project`, `senior-design`, `typewriter-restoration`
- This allows multiple files per project while keeping things organized

### 3. Reusability
- Documents and images can be referenced from multiple posts
- Use consistent naming so files are easy to find
- Same image/document can appear in multiple posts without duplication

## Usage Examples

### Linking Documents in Posts

```markdown
## Source Documents

- [Final Report](/documents/2022/cad-project/CAD-Project-Final-Report.pdf)
- [Progress Report](/documents/2022/cad-project/Progress-Report-01.pdf)
```

### Including Images in Posts

```markdown
![Device Photo](/images/2022/cad-project/device-photo.jpg)

![Design Iteration](/images/2022/cad-project/design-iteration-02.png)
```

### Multiple Posts Using Same Files

If you have multiple posts about the same project, they can all reference the same files:

**Post 1: `2022-06-15-cad-project.md`**
```markdown
![Device](/images/2022/cad-project/device-photo.jpg)
[Report](/documents/2022/cad-project/final-report.pdf)
```

**Post 2: `2022-07-01-cad-project-update.md`**
```markdown
![Device](/images/2022/cad-project/device-photo.jpg)  <!-- Same image -->
[Report](/documents/2022/cad-project/final-report.pdf)  <!-- Same document -->
```

## File Naming Conventions

### Documents
- Use descriptive, hyphenated names: `final-report.pdf`, `progress-report-01.pdf`
- Avoid spaces: use hyphens instead
- Include version numbers if applicable: `report-v2.pdf`

### Images
- Use descriptive names: `device-photo.jpg`, `design-diagram.png`
- Consider prefixes for organization: `photo-`, `diagram-`, `screenshot-`
- Use appropriate extensions: `.jpg` for photos, `.png` for graphics

### Project Folders
- Lowercase with hyphens: `cad-project`, `senior-design`
- Descriptive and concise
- Match project names used in post slugs when possible

## Pelican Configuration

The `pelicanconf.py` file includes `documents` in `STATIC_PATHS`:

```python
STATIC_PATHS = ['images', 'extra', 'documents']
```

This ensures Pelican copies these directories to the output folder and serves them as static files.

## Migration from Import Folder

When adding new content:
1. Create appropriate year/project directories if they don't exist
2. Copy files from `import/` to the appropriate location
3. Use consistent, hyphenated filenames
4. Update posts to reference the new paths
5. Delete files from `import/` once migrated

## Benefits

1. **Organization**: Easy to find files by year and project
2. **Reusability**: Same files can be used in multiple posts
3. **Scalability**: Structure supports growth over years
4. **Maintainability**: Clear organization makes updates easier
5. **Version Control**: Git-friendly structure with clear organization

