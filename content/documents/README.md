# Documents Organization System

This directory contains source documents (PDFs, reports, etc.) organized by year and project.

## Directory Structure

```
documents/
├── YYYY/                    # Year-based organization
│   └── project-name/         # Project-specific folder
│       ├── document1.pdf
│       ├── document2.pdf
│       └── ...
└── README.md                 # This file
```

## Usage in Posts

Documents can be linked in markdown posts using the following path format:

```markdown
[Document Name](/documents/YYYY/project-name/filename.pdf)
```

For example:
```markdown
[Final Report](/documents/2022/cad-project/CAD-Project-Final-Report.pdf)
```

## Benefits

- **Organized by year and project**: Easy to find and manage documents
- **Reusable across posts**: Same document can be linked from multiple posts
- **Static file serving**: Pelican automatically serves files from this directory
- **Version control friendly**: Documents are tracked in git (if desired)

## Naming Conventions

- Use lowercase with hyphens for folder names: `cad-project`, `senior-design`
- Use descriptive, hyphenated filenames: `final-report.pdf`, `progress-report-01.pdf`
- Avoid spaces in filenames (use hyphens instead)

