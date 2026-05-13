# Math and Puzzles

A small collection of weekend math/logic tests, mid-week practice sets, and interactive lessons.

- **Saturday tests** — eight problems, ~15 minutes, across three sections (Numbers and Shapes · Counting Carefully · Reasoning). Print-ready PDFs with parent answer keys.
- **Practice sets** — tighter, untimed sequences focused on one concept at a time.
- **Interactive lessons** — single-file HTML experiments where the math is something you *do*, not something you read about.

Browse the site at the project's GitHub Pages URL (linked from the repository description).

## Build scripts

The PDFs are generated from the Python files in this repo (`build_*.py`). They depend on `reportlab`. To regenerate any PDF:

```
python3 build_test_04.py
```

The HTML lessons are hand-written, single-file, vanilla JS + SVG. No build step.
