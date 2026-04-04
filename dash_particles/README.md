# Dash Particles

[![PyPI version](https://badge.fury.io/py/dash-particles.svg)](https://badge.fury.io/py/dash-particles)
[![npm version](https://badge.fury.io/js/dash-particles.svg)](https://badge.fury.io/js/dash-particles)

`dash-particles` brings tsParticles backgrounds to Dash with a Python-first API.
Instead of building one giant nested dict, you can compose configs with
`dp.Options(...)`, `dp.Particles(...)`, `dp.Interactivity(...)`, and curated
`dp.presets.*` helpers.

[Live demo](https://app.py.cafe/jeffgallini/dash-particle-system-visualizer)

## Why Use It

- Build particle configs with Python classes instead of raw JSON-shaped dicts.
- Start quickly with `dp.presets.*`, then override only the sections you need.
- Drop animated backgrounds into full pages, hero sections, login screens, and dashboards.

## Installation

```bash
pip install dash-particles
```

## 60-Second Quickstart

This is the fastest path to a visible background while still showing the
structured API clearly.

```python
import dash
from dash import html
import dash_particles as dp

app = dash.Dash(__name__)

background_particles = dp.DashParticles(
    id="page-particles",
    config=dp.Options(
        background=dp.Background(color=dp.Color("transparent")),
        particles=dp.Particles(
            color=dp.Color("#2563eb"),
            number=dp.ParticleNumber(value=80),
            links=dp.Links(
                enable=True,
                color="#2563eb",
                opacity=0.35,
                distance=140,
            ),
            move=dp.Move(
                enable=True,
                speed=2,
                direction="none",
                out_modes=dp.OutModes(default="bounce"),
            ),
            size=dp.Size(value=3),
        ),
    ),
    height="100%",
    width="100%",
)

app.layout = html.Div(
    [
        html.Div(
            background_particles,
            style={
                "position": "fixed",
                "inset": 0,
                "zIndex": 0,
            },
        ),
        html.Div(
            [
                html.H1("Dash Particles"),
                html.P("Your app content stays above the animated background."),
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

if __name__ == "__main__":
    app.run(debug=True)
```

## The Main Mental Model

The recommended entry point is:

```python
import dash_particles as dp

config = dp.Options(
    background=dp.Background(color=dp.Color("transparent")),
    fps_limit=60,
    detect_retina=True,
    full_screen=dp.FullScreen(enable=False, z_index=0),
    particles=dp.Particles(
        color=dp.Color("#0075FF"),
        number=dp.ParticleNumber(
            value=80,
            density=dp.Density(enable=True, area=800),
        ),
        size=dp.Size(value=dp.RangeValue(min=1, max=5)),
        opacity=dp.Opacity(value=0.5),
        links=dp.Links(enable=True, color="#0075FF", opacity=0.5, width=1),
        move=dp.Move(
            enable=True,
            speed=3,
            direction="none",
            random=False,
            straight=False,
            out_modes=dp.OutModes(default="bounce"),
        ),
        shape=dp.Shape(type="circle"),
    ),
    interactivity=dp.Interactivity(
        events=dp.Events(
            on_click=dp.Action(enable=True, mode="push"),
            on_hover=dp.Action(enable=True, mode="repulse"),
        ),
    ),
)

particles = dp.DashParticles(id="particles", config=config, height="400px")
```

You can also override top-level sections directly in the component call:

```python
import dash_particles as dp

dp.DashParticles(
    id="particles",
    background=dp.Background(color=dp.Color("#0f172a")),
    particles=dp.Particles(color=dp.Color("#ffffff")),
    interactivity=dp.Interactivity(
        events=dp.Events(on_hover=dp.Action(enable=True, mode="grab"))
    ),
)
```

## Built-In Presets

`dp.presets.*` gives you fast, readable starting points:

```python
import dash_particles as dp

hero_particles = dp.DashParticles(
    id="hero-particles",
    config=dp.presets.stars(),
    height="100%",
    width="100%",
)
```

That includes both general-purpose presets and richer sample-inspired ones such
as `dp.presets.among_us()`, `dp.presets.parallax()`, `dp.presets.fontawesome()`,
`dp.presets.blurred_particles()`, `dp.presets.hypno_squares()`, and `dp.presets.multiple_images()`.

You can still layer overrides on top of a preset:

```python
import dash_particles as dp

hero_particles = dp.DashParticles(
    id="hero-particles",
    config=dp.presets.connect(),
    particles=dp.Particles(
        color=dp.Color("#22c55e"),
        links=dp.Links(enable=True, color="#22c55e", opacity=0.25),
    ),
)
```

## Public Python API

| Use case | Main helpers |
|----------|--------------|
| Render the component | `dp.DashParticles(...)` |
| Top-level config object | `dp.Options(...)` / `dp.ParticlesOptions(...)` |
| Presets | `dp.presets.default()`, `dp.presets.stars()`, `dp.presets.connect()`, `dp.presets.among_us()`, `dp.presets.fontawesome()`, `dp.presets.blurred_particles()`, `dp.presets.hypno_squares()` |
| Background color and layout | `dp.Background`, `dp.BackgroundMask`, `dp.BackgroundMaskCover`, `dp.Color`, `dp.FullScreen` |
| Particle counts and density | `dp.ParticleNumber`, `dp.Density` |
| Particle appearance | `dp.Particles`, `dp.Size`, `dp.Opacity`, `dp.Shape`, `dp.RangeValue` |
| Motion and edges | `dp.Move`, `dp.OutModes`, `dp.Motion` |
| Interactivity | `dp.Interactivity`, `dp.Events`, `dp.Action`, `dp.Modes` |
| Advanced top-level config | `dp.Responsive`, `dp.Theme`, `dp.ManualParticle`, `dp.Position` |

## Support Boundaries

`dash-particles` currently ships with the `tsparticles` full JavaScript bundle
plus the image-shape, text-shape, and canvas-mask plugins.

- The structured Python API is the default and recommended way to author configs.
- Raw dicts remain supported through `config={...}` and `options={...}`.
- `extra={...}` is the escape hatch for tsParticles keys that do not yet have a dedicated Python helper.
- `extra` and raw dicts do not load missing JavaScript plugins by themselves.
- Common advanced features like `emitters`, `backgroundMask`, `canvasMask`, and Font Awesome or character-style particles now work with the shipped bundle.
- The bundled presets cover emitters, image particles, background masks, character particles, themeable blur effects, and animated geometric effects through the shipped runtime.

## Compatibility And Precedence

- `config=` accepts `dp.Options(...)`, `dp.ParticlesOptions(...)`, or raw dictionaries.
- `options=` is still supported for backward compatibility, but new code should prefer `config=`.
- `options=` and `config=` cannot be used together in the same component call.
- Explicit top-level sections like `particles=...`, `background=...`, or `full_screen=...` override overlapping keys from `config=`.
- Use `extra={...}` on any structured config object for unsupported tsParticles keys inside the current runtime bundle.

Example escape hatch:

```python
import dash_particles as dp

config = dp.Options(
    particles=dp.Particles(
        color=dp.Color(["#ff5722", "#ff9800", "#ffeb3b"]),
        extra={"shadow": {"enable": True, "blur": 8, "color": "#ff9800"}},
    ),
    extra={"fullScreen": {"enable": False}},
)
```

## Where To Go Next

- [Docs Landing Page](docs/README.md)
- [Getting Started](docs/getting-started.md)
- [Config Model](docs/config-model.md)
- [Recipes](docs/recipes.md)
- [Migration Guide](docs/migration.md)
- [Troubleshooting](docs/troubleshooting.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
