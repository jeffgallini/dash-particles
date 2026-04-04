# Troubleshooting

## Nothing Is Visible

Check these first:

- Give `dp.DashParticles(...)` a visible size with `height`, `width`, or a sized parent container
- Make sure the particle color is not blending into the background color
- If you are using it as a background, keep the particle layer behind the content with `position` and `zIndex`

## The Particles Are Hidden Behind or In Front of the Wrong Layer

Use separate layers:

- particle layer: `position: fixed` or `position: absolute`, low `zIndex`
- content layer: `position: relative`, higher `zIndex`

If everything is inside one parent, give that parent `position: relative`.

## Callbacks Work but the Canvas Does Not Update Cleanly

Prefer returning a fresh `dp.DashParticles(...)` with the new `config=` value in
your callback output. This is the clearest pattern and matches the demo app in
[`usage.py`](../usage.py).

## The Config Serializes Fine but a Feature Still Does Not Work

This usually means the option needs a tsParticles plugin that is not part of the
current frontend runtime.

`dash-particles` currently ships with the `tsparticles` full bundle.

- Common core features work directly
- Emitters, image particles, themeable blur effects, animated geometric presets, background masks, and Font Awesome or character-style particle examples are supported by the shipped runtime
- Polygon-mask scenes still need the separate polygon-mask frontend plugin
- `extra={...}` can help with missing Python helper coverage
- `extra` does not load missing JavaScript plugins
- Features outside the documented preset surface may still need additional frontend runtime work beyond the shipped bundle

## I Need a tsParticles Key That Does Not Have a Python Helper Yet

Use `extra={...}` on the closest structured object:

```python
import dash_particles as dp

config = dp.Options(
    particles=dp.Particles(
        color=dp.Color("#ffffff"),
        extra={"shadow": {"enable": True, "blur": 8, "color": "#ffffff"}},
    )
)
```

If it proves useful and works within the shipped runtime, it is a good candidate
for a first-class helper in a future version.

## Performance Feels Heavy

Try these first:

- lower `particles.number.value`
- disable `links`
- lower `move.speed`
- reduce hover or click interactivity
- enable `pause_on_blur` and `pause_on_outside_viewport`

## Legacy Dict Interop

These are all valid:

- `dp.DashParticles(config=dp.Options(...))`
- `dp.DashParticles(config={...})`
- `dp.DashParticles(options={...})`

For new code, prefer `config=`. It is the cleanest bridge between presets,
structured helpers, and callback-driven overrides.
