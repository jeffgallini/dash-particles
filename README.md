# Dash Particles `dash-particles`

`dash-particles` is a Dash component library for tsParticles backgrounds with a
structured Python API. The actual Python package, docs, demo app, and release
assets live in [`dash_particles/`](./dash_particles/).

![Animated preview of dash-particles presets](./dash_particles/assets/particle_presets.gif)

## Start Here

- Package README: [`dash_particles/README.md`](./dash_particles/README.md)
- Docs landing page: [`dash_particles/docs/README.md`](./dash_particles/docs/README.md)
- Demo app: [`dash_particles/usage.py`](./dash_particles/usage.py)
- Contributing guide: [`dash_particles/CONTRIBUTING.md`](./dash_particles/CONTRIBUTING.md)

## Quick Example

```python
import dash
from dash import html
import dash_particles as dp

app = dash.Dash(__name__)

app.layout = html.Div(
    dp.DashParticles(
        id="particles",
        config=dp.presets.stars(),
        height="100vh",
        width="100%",
    )
)
```

## What v0.0.3 Focuses On

- A structured config model based on `dp.Options(...)` instead of one giant dict
- Curated `dp.presets.*` helpers for faster starts
