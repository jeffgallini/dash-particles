# Recipes

## Full-Page Background

```python
import dash
from dash import html
import dash_particles as dp

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            dp.DashParticles(
                id="bg",
                config=dp.presets.connect(),
                height="100%",
                width="100%",
            ),
            style={"position": "fixed", "inset": 0, "zIndex": 0},
        ),
        html.Div(
            [html.H1("App content")],
            style={"position": "relative", "zIndex": 1, "padding": "4rem"},
        ),
    ],
    style={"minHeight": "100vh"},
)
```

## Hero or Login Section Background

```python
import dash_particles as dp
from dash import html

hero = html.Div(
    [
        dp.DashParticles(
            id="hero-particles",
            config=dp.presets.stars(),
            height="100%",
            width="100%",
            style={"position": "absolute", "inset": 0},
        ),
        html.Div(
            [
                html.H1("Welcome back"),
                html.P("Sign in to continue"),
            ],
            style={"position": "relative", "zIndex": 1},
        ),
    ],
    style={
        "position": "relative",
        "minHeight": "420px",
        "overflow": "hidden",
    },
)
```

## Preset Switching with Dash Callbacks

```python
import dash
from dash import Input, Output, callback, dcc, html
import dash_particles as dp

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Dropdown(
            id="preset",
            options=[{"label": dp.presets.PRESET_LABELS[name], "value": name} for name in dp.presets.names()],
            value="default",
            clearable=False,
        ),
        html.Div(id="particles-slot"),
    ]
)


@callback(Output("particles-slot", "children"), Input("preset", "value"))
def render_particles(preset_name):
    config = dp.presets.PRESET_BUILDERS[preset_name]()
    return dp.DashParticles(id="particles", config=config, height="500px", width="100%")
```

## Start from a Preset and Override One Section

```python
import dash_particles as dp

particles = dp.DashParticles(
    id="particles",
    config=dp.presets.connect(),
    particles=dp.Particles(
        color=dp.Color("#22c55e"),
        links=dp.Links(enable=True, color="#22c55e", opacity=0.25, distance=140),
    ),
)
```

## Build a Custom Config from Scratch

```python
import dash_particles as dp

config = dp.Options(
    background=dp.Background(color=dp.Color("#020617")),
    full_screen=dp.FullScreen(enable=False, z_index=0),
    motion=dp.Motion(reduce=dp.MotionReduce(factor=2, value=True)),
    particles=dp.Particles(
        color=dp.Color("#f8fafc"),
        number=dp.ParticleNumber(value=60, density=dp.Density(enable=True, area=900)),
        size=dp.Size(value=dp.RangeValue(min=1, max=4)),
        opacity=dp.Opacity(value=0.7),
        links=dp.Links(enable=True, color="#38bdf8", opacity=0.2, distance=150),
        move=dp.Move(enable=True, speed=1.5, out_modes=dp.OutModes(default="bounce")),
    ),
)
```

## Use `extra` for a Missing Python Helper

```python
import dash_particles as dp

config = dp.Options(
    particles=dp.Particles(
        color=dp.Color("#ffffff"),
        extra={"shadow": {"enable": True, "blur": 10, "color": "#ffffff"}},
    )
)
```

Remember: `extra` only helps with option keys. It does not load a missing tsParticles plugin into the browser.

## Lighter Config for Mobile or Busy Pages

```python
import dash_particles as dp

config = dp.Options(
    particles=dp.Particles(
        number=dp.ParticleNumber(value=30),
        links=dp.Links(enable=False),
        move=dp.Move(enable=True, speed=0.8),
        size=dp.Size(value=2),
    ),
    pause_on_blur=True,
    pause_on_outside_viewport=True,
)
```

## Official Sample: Among Us

Inspired by the official sample:
<https://particles.js.org/samples/index.html#amongUs>

This style uses image-shaped particles, which fits well with the current
structured API, and the shipped full runtime also supports the emitter-based
version of the official sample.

```python
import dash_particles as dp

config = dp.presets.among_us()
```

## Official Sample: Multiple Images

Inspired by the official sample:
<https://particles.js.org/samples/index.html#images>

```python
import dash_particles as dp

config = dp.presets.multiple_images()
```

## CodePen Sample: Blurred Particles

Inspired by the CodePen sample:
<https://codepen.io/matteobruni/pen/qBPxjQY>

This preset uses oversized blurred particles, a top-positioned emitter, and
light and dark theme variants.

```python
import dash_particles as dp

config = dp.presets.blurred_particles()
```

## CodePen Sample: Hypno Squares

Inspired by the CodePen sample:
<https://codepen.io/matteobruni/pen/BaGbWdb>

This preset uses rotating outlined squares that grow from a centered emitter
until their size animation destroys them.

```python
import dash_particles as dp

config = dp.presets.hypno_squares()
```

## Official Sample: Parallax

Inspired by the official sample:
<https://particles.js.org/samples/index.html#parallax>

```python
import dash_particles as dp

config = dp.presets.parallax()
```

## Official Sample: Font Awesome

Inspired by the official sample:
<https://particles.js.org/samples/index.html#fontawesome>

This works with the shipped full runtime. The remaining requirement is that the
Font Awesome font itself must be available on the page.

```python
import dash_particles as dp

config = dp.presets.fontawesome()
```

To make this work visually, ensure the Font Awesome font is loaded on the page.
By default, this preset renders the Apple brand icon from
`<i class="fa-brands fa-apple"></i>`.

The preset defaults target Font Awesome 6 family names to match the helper app's
stylesheet. If your page loads Font Awesome 5 instead, override the families:

```python
config = dp.presets.fontawesome(
    brand_font_family="Font Awesome 5 Brands",
    solid_font_family="Font Awesome 5 Free",
    solid_glyph="\uf5d1",
)
```
