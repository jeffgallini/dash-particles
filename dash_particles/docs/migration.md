# Migration Guide

## Before: Giant Raw Dict

```python
legacy_config = {
    "background": {"color": {"value": "#0f172a"}},
    "particles": {
        "color": {"value": "#38bdf8"},
        "number": {"value": 80},
        "links": {
            "enable": True,
            "color": "#38bdf8",
            "opacity": 0.3,
            "distance": 150,
        },
        "move": {
            "enable": True,
            "speed": 2,
            "direction": "none",
            "outModes": {"default": "bounce"},
        },
    },
    "interactivity": {
        "events": {
            "onHover": {"enable": True, "mode": "grab"},
            "onClick": {"enable": True, "mode": "push"},
        }
    },
}
```

## After: Structured Python Config

```python
import dash_particles as dp

config = dp.Options(
    background=dp.Background(color=dp.Color("#0f172a")),
    particles=dp.Particles(
        color=dp.Color("#38bdf8"),
        number=dp.ParticleNumber(value=80),
        links=dp.Links(
            enable=True,
            color="#38bdf8",
            opacity=0.3,
            distance=150,
        ),
        move=dp.Move(
            enable=True,
            speed=2,
            direction="none",
            out_modes=dp.OutModes(default="bounce"),
        ),
    ),
    interactivity=dp.Interactivity(
        events=dp.Events(
            on_hover=dp.Action(enable=True, mode="grab"),
            on_click=dp.Action(enable=True, mode="push"),
        )
    ),
)
```

## Minimal Migration Strategy

1. Move the outer dict to `dp.Options(...)`
2. Convert the sections you touch most often first
3. Keep unconverted keys in `extra={...}` while you migrate gradually
4. Use `config=` as the main component argument instead of `options=`

## Compatibility Rules

- `config=` accepts both structured objects and raw dicts
- `options=` still works for legacy code
- `options=` and `config=` cannot be passed together
- explicit section overrides on `dp.DashParticles(...)` take precedence over overlapping keys in `config=`

## Migration with Presets

If your old config is close to a common visual pattern, you may be able to
replace most of it with a preset plus a small override:

```python
import dash_particles as dp

particles = dp.DashParticles(
    id="particles",
    config=dp.presets.connect(),
    particles=dp.Particles(color=dp.Color("#22c55e")),
)
```
