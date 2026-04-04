# Getting Started

## Install

```bash
pip install dash-particles
```

## Your First Component

```python
import dash
from dash import html
import dash_particles as dp

app = dash.Dash(__name__)

app.layout = html.Div(
    dp.DashParticles(
        id="particles",
        config=dp.presets.default(),
        height="400px",
        width="100%",
    )
)
```

## Full-Page Background Pattern

The two most common reasons particles are "missing" are:

- the component has no visible size
- the content layer is covering it

Use this pattern for a page-wide background:

```python
import dash
from dash import html
import dash_particles as dp

app = dash.Dash(__name__)

background = dp.DashParticles(
    id="page-particles",
    config=dp.presets.connect(),
    height="100%",
    width="100%",
)

app.layout = html.Div(
    [
        html.Div(
            background,
            style={
                "position": "fixed",
                "inset": 0,
                "zIndex": 0,
            },
        ),
        html.Div(
            [
                html.H1("Foreground content"),
                html.P("Keep this layer above the particles."),
            ],
            style={
                "position": "relative",
                "zIndex": 1,
                "padding": "4rem",
            },
        ),
    ],
    style={"minHeight": "100vh"},
)
```

## When To Use Presets vs Custom Configs

- Use `dp.presets.*` when you want a fast starting point.
- Use `dp.Options(...)` when you want to author the whole config yourself.
- Use top-level overrides like `particles=...` when you want to tweak part of an existing config or preset.

## Next Steps

- Learn the structured helpers in [Config Model](config-model.md)
- Copy practical patterns from [Recipes](recipes.md)
- Check [Troubleshooting](troubleshooting.md) if nothing appears on screen
