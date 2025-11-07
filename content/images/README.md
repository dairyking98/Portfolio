# Images Organization System

This directory contains images organized by year and project for use in blog posts.

## Directory Structure

```
images/
├── YYYY/                    # Year-based organization
│   └── project-name/         # Project-specific folder
│       ├── image1.jpg
│       ├── image2.png
│       └── ...
└── README.md                 # This file
```

## Usage in Posts

Images can be referenced in markdown posts using the following path format:

```markdown
![Alt text](/images/YYYY/project-name/filename.jpg)
```

Or as a link:
```markdown
[![Alt text](/images/2022/cad-project/device-photo.jpg)](/images/2022/cad-project/device-photo.jpg)
```

## Benefits

- **Organized by year and project**: Easy to find and manage images
- **Reusable across posts**: Same image can be used in multiple posts
- **Static file serving**: Pelican automatically serves files from this directory
- **Optimization ready**: Easy to batch process images by project

## Naming Conventions

- Use lowercase with hyphens for folder names: `cad-project`, `senior-design`
- Use descriptive, hyphenated filenames: `device-photo.jpg`, `design-iteration-01.png`
- Avoid spaces in filenames (use hyphens instead)
- Consider using consistent prefixes: `photo-`, `diagram-`, `screenshot-`

## Image Formats

Recommended formats:
- **Photos**: JPG for photos, PNG for graphics with transparency
- **Diagrams**: PNG or SVG (if supported)
- **Screenshots**: PNG

