# Config Model

## The Main Idea

`dash-particles` wraps the tsParticles options object in Python classes so you
can write:

```python
import dash_particles as dp

config = dp.Options(
    background=dp.Background(color=dp.Color("#0f172a")),
    particles=dp.Particles(
        color=dp.Color("#38bdf8"),
        number=dp.ParticleNumber(value=80),
        links=dp.Links(enable=True, color="#38bdf8", opacity=0.3, distance=150),
        move=dp.Move(enable=True, speed=2, out_modes=dp.OutModes(default="bounce")),
    ),
    interactivity=dp.Interactivity(
        events=dp.Events(on_hover=dp.Action(enable=True, mode="grab"))
    ),
)
```

instead of maintaining one large nested dictionary by hand.

## Canonical Entry Points

- `dp.DashParticles(config=...)`: recommended component API
- `dp.Options(...)` or `dp.ParticlesOptions(...)`: top-level config object
- `dp.presets.*`: curated starting points that return `dp.Options(...)`, including
  `default`, `stars`, `connect`, `among_us`, `parallax`, `fontawesome`,
  `blurred_particles`, `hypno_squares`,
  and `multiple_images`

## Common Helper Classes

| Area | Helpers |
|------|---------|
| Background | `Background`, `BackgroundMask`, `BackgroundMaskCover`, `Color`, `FullScreen` |
| Particle styling | `Particles`, `Shape`, `Size`, `Opacity`, `RangeValue` |
| Counts and layout | `ParticleNumber`, `Density`, `ManualParticle`, `Position` |
| Motion | `Move`, `OutModes`, `Motion`, `MotionReduce` |
| Interactivity | `Interactivity`, `Events`, `Action`, `Modes`, `Grab`, `Repulse`, `Bubble`, `Push`, `Remove` |
| Advanced top-level config | `Responsive`, `Theme` |

## Pythonic Name Mapping

The Python model uses snake_case names and serializes them to tsParticles'
camelCase keys.

| Python helper field | Serialized tsParticles key |
|---------------------|----------------------------|
| `fps_limit` | `fpsLimit` |
| `detect_retina` | `detectRetina` |
| `full_screen` | `fullScreen` |
| `background_mask` | `backgroundMask` |
| `z_index` | `zIndex` |
| `pause_on_blur` | `pauseOnBlur` |
| `pause_on_outside_viewport` | `pauseOnOutsideViewport` |
| `on_click` | `onClick` |
| `on_hover` | `onHover` |
| `on_div` | `onDiv` |
| `parallax` | `parallax` |
| `detects_on` | `detectsOn` |
| `out_modes` | `outModes` |
| `manual_particles` | `manualParticles` |
| `max_width` | `maxWidth` |
| `auto_play` | `autoPlay` |

## Convenience Overrides on the Component

You do not have to build a full `Options` object up front.

```python
import dash_particles as dp

dp.DashParticles(
    id="particles",
    config=dp.presets.stars(),
    full_screen=dp.FullScreen(enable=False, z_index=0),
    particles=dp.Particles(color=dp.Color("#fde047")),
)
```

Explicit section overrides win when they overlap with `config=`.

## `extra` for Unsupported Keys

Any helper can accept `extra={...}`.

```python
import dash_particles as dp

config = dp.Options(
    particles=dp.Particles(
        color=dp.Color("#ffffff"),
        extra={"shadow": {"enable": True, "blur": 8, "color": "#ffffff"}},
    )
)
```

Use `extra` when:

- a tsParticles key exists but does not have a first-class Python helper yet
- you want to bridge a small gap without dropping back to a full raw dict

## Runtime Support Boundary

The current frontend loads the `tsparticles` full bundle.

- Many common features work directly with the shipped bundle.
- Emitters, background masks, themeable blur effects, animated geometric effects, and text or character-based particles are included in the shipped runtime.
- `extra` can set keys for features inside that bundle, even if the Python helper is missing.
- `extra` does not load missing JavaScript plugins.
- Features outside the documented presets may still need the frontend runtime expanded before they will work in the browser.

If you need those features today, treat it as a frontend-bundle task, not just a Python-API task.
