# Contributing

Thanks for helping improve `dash-particles`.

## Project Layout

- `dash_particles/dash_particles/`: Python package, generated Dash wrapper, and structured config helpers
- `dash_particles/src/lib/components/`: React component source
- `dash_particles/docs/`: user-facing documentation
- `dash_particles/usage.py`: companion demo app used for examples and docs
- `dash_particles/tests/`: Python-side smoke tests

## Local Setup

From the repository root:

```bash
cd dash_particles
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
npm install
```

## Development Workflow

### Python changes only

If you are editing structured config helpers, docs, presets, or the manual
Python wrapper, these are usually enough:

```bash
pytest tests
python usage.py
```

### Frontend or prop changes

If you change the React component or anything that affects generated metadata,
rebuild the JavaScript bundle and Dash backends:

```bash
npm run build:js
npm run build:backends
```

Then re-run:

```bash
pytest tests
python usage.py
```

## Runtime Support Notes

The package currently uses the `tsparticles` full runtime bundle in
`src/lib/components/DashParticles.react.js`.

- Adding a Python option helper does not automatically make a tsParticles plugin available in the browser.
- The shipped full bundle covers the common plugin-backed features used in the current docs and demo, including emitters and text or character shapes.
- If you want features beyond the documented preset surface, expand the frontend runtime first and document that change in the README and troubleshooting guide.
- Keep the Python docs explicit about what is supported directly, what works through `extra`, and what still needs frontend bundle work.

## Documentation Expectations

- Treat `dash_particles/README.md` as the main onboarding document.
- Keep examples structured-API-first.
- Prefer `dp.presets.*` for quick examples, then show how to override with explicit sections.
- When adding a new helper class, update:
  - `README.md`
  - `docs/config-model.md`
  - `docs/recipes.md` or `docs/migration.md` if relevant
  - tests that cover representative snippets

## Release Checklist

Before cutting a release, make sure:

1. Python package metadata and `package.json` describe the same runtime story.
2. The docs mention any new helpers, presets, or support boundaries.
3. `usage.py` still matches the examples shown in the docs.
4. Tests pass.
5. Generated assets are rebuilt if the React wrapper or prop metadata changed.
