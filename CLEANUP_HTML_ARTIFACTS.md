# HTML Artifacts Cleanup

## Summary

There are many HTML artifacts from the old Pelican build system that are still tracked in Git but should be removed. These are generated files that Jekyll will create automatically.

## Legitimate HTML Files (Keep)

These are Jekyll source files with YAML front matter:
- `index.html` - Homepage (Jekyll source)
- `tags.html` - Tags listing page (Jekyll source)
- `archives.html` - Archives page (Jekyll source)
- `typewriters.html` - Typewriters main page (Jekyll source)
- `_layouts/*.html` - Layout templates (Jekyll source)

## Generated HTML Artifacts (Remove from Git)

These are Pelican-generated HTML files that should be removed:

### Root Level
- `about/index.html` - Generated (source: `about.md`)
- `my-collection/index.html` - Generated
- `personal-projects/index.html` - Generated (source: `personal-projects.md`)
- `projects/index.html` - Generated (source: `projects.md`)
- `school-projects/index.html` - Generated (source: `school-projects.md`)

### Author Pages
- `author/leonard-chau/index.html` - Generated

### Category Pages
- `category/general/index.html` - Generated (Jekyll plugin generates these)
- `category/personal-projects/index.html` - Generated
- `category/school-projects/index.html` - Generated

### Post Pages
- `posts/2022/11/29/cad-project-self-propelled-wall-leaper/index.html` - Generated (source: `_posts/`)
- `posts/2024/12/15/analog-voltmeter-clock-time-and-environmental-monitor/index.html` - Generated
- `posts/2024/12/20/open-ended-experiment-tensile-testing-of-acrylic-with-geometric-discontinuities/index.html` - Generated
- `posts/2025/02/10/welcome-to-my-engineering-blog/index.html` - Generated
- `posts/2025/11/08/large-laser-cut-vernier-caliper/index.html` - Generated
- `posts/2025/11/08/senior-capstone-ev-battery-management-and-swapping-system/index.html` - Generated

### Tag Pages
- `tag/3d-printing/index.html` - Generated (Jekyll plugin generates these)
- `tag/arduino/index.html` - Generated
- `tag/cad/index.html` - Generated
- `tag/design/index.html` - Generated
- `tag/education/index.html` - Generated
- `tag/electronics/index.html` - Generated
- `tag/embedded-systems/index.html` - Generated
- `tag/engineering/index.html` - Generated
- `tag/fabrication/index.html` - Generated
- `tag/fusion-360/index.html` - Generated
- `tag/fusion360/index.html` - Generated
- `tag/intro/index.html` - Generated
- `tag/laser-cutting/index.html` - Generated
- `tag/materials-testing/index.html` - Generated
- `tag/measurement/index.html` - Generated
- `tag/mechanical-engineering/index.html` - Generated
- `tag/personal-project/index.html` - Generated
- `tag/portfolio/index.html` - Generated
- `tag/python/index.html` - Generated
- `tag/school-project/index.html` - Generated
- `tag/sensors/index.html` - Generated
- `tag/stress-analysis/index.html` - Generated

### Typewriter Pages
- `typewriters/3d-type-elements/index.html` - Generated (source: `typewriters/3d-type-elements.md`)
- `typewriters/bennett-pocket-typewriter-14682/index.html` - Generated (source: `_typewriters/`)
- `typewriters/bennett-pocket-typewriter-18627/index.html` - Generated
- `typewriters/blickensderfer-no-5-133130/index.html` - Generated
- `typewriters/blickensderfer-no-8-135255/index.html` - Generated
- `typewriters/collection/index.html` - Generated (source: `typewriters/collection.md`)
- `typewriters/collection-posts/index.html` - Generated (source: `typewriters/collection-posts.md`)
- `typewriters/continental-standard-26277/index.html` - Generated
- `typewriters/corona-3-231258/index.html` - Generated
- `typewriters/facit-t1-t1-123221/index.html` - Generated
- `typewriters/facit-tp1-p287156/index.html` - Generated
- `typewriters/facit-tp1-p411069/index.html` - Generated
- `typewriters/hammond-model-1-15058/index.html` - Generated
- `typewriters/hammond-multiplex-224478/index.html` - Generated
- `typewriters/hammond-multiplex-cc231416/index.html` - Generated
- `typewriters/harris-visible-no-4-19149/index.html` - Generated
- `typewriters/ibm-model-04-executive-180437/index.html` - Generated
- `typewriters/index.html` - Generated
- `typewriters/junior-spain-model-58-c2492/index.html` - Generated
- `typewriters/mignon-no-4-352222/index.html` - Generated
- `typewriters/olympia-sg1-7-487163/index.html` - Generated
- `typewriters/olympia-sm3-1205390/index.html` - Generated
- `typewriters/olympia-sm4-490865/index.html` - Generated
- `typewriters/postal-no-3-14550/index.html` - Generated
- `typewriters/remington-17-j794385/index.html` - Generated
- `typewriters/remington-portable-model-1-na13437/index.html` - Generated
- `typewriters/royal-de-luxe-a597665/index.html` - Generated
- `typewriters/royal-quiet-de-luxe-a-873792/index.html` - Generated
- `typewriters/smith-corona-clipper-5c218668/index.html` - Generated
- `typewriters/sun-no-2-standard-8278/index.html` - Generated
- `typewriters/triumph-de-jur-perfekt-1228617/index.html` - Generated
- `typewriters/underwood-4-bank-4b7867/index.html` - Generated
- `typewriters/underwood-champion-typemaster-g1130193/index.html` - Generated
- `typewriters/underwood-no-3-206803/index.html` - Generated
- `typewriters/underwood-quiet-tab-aa2730434/index.html` - Generated
- `typewriters/woodstock-model-5n-n168116e/index.html` - Generated

## Cleanup Commands

To remove these artifacts from Git (they're already deleted from filesystem):

```bash
# Remove all generated HTML artifacts from Git
git rm -r about/index.html
git rm -r author/
git rm -r category/
git rm -r my-collection/index.html
git rm -r personal-projects/index.html
git rm -r posts/
git rm -r projects/index.html
git rm -r school-projects/index.html
git rm -r tag/
git rm -r typewriters/*/index.html
git rm typewriters/index.html
```

Or use a single command to remove all HTML artifacts:

```bash
# Remove all HTML artifacts (except legitimate source files)
git rm about/index.html
git rm -r author/
git rm -r category/
git rm my-collection/index.html
git rm personal-projects/index.html
git rm -r posts/
git rm projects/index.html
git rm school-projects/index.html
git rm -r tag/
git rm typewriters/index.html
# Remove typewriter individual pages (keep the typewriters/ directory structure)
find typewriters -name "index.html" -type f -not -path "typewriters/index.html" | xargs git rm
```

## Why Remove These?

1. **Jekyll generates them automatically** - No need to commit generated files
2. **Source files are in `_posts/` and `_typewriters/`** - These are the real source
3. **Jekyll plugins generate tag/category pages** - No need to commit them
4. **Cleaner repository** - Only source files should be in Git
5. **GitHub Pages will build them** - GitHub generates these on deployment

## After Cleanup

After removing these artifacts:
- Jekyll will generate them automatically when you run `serve.bat` or `build.bat`
- GitHub Pages will generate them when you push to GitHub
- Only source files (Markdown, layouts, config) will be in the repository

