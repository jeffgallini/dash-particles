# Changelog

# 1.0.0

- Promoted the Python package to the stable `v1.0.0` release.
- Stabilized the Python-first config API around `dp.Options(...)`, structured helper classes, and `dp.presets.*`.
- Documented runtime auto-loading for packaged basic, slim, and full tsParticles tiers.
- Refreshed release documentation, getting-started paths, and support-boundary notes for the stable release.
- Preserved compatibility for raw dict configs through `config={...}` and legacy `options={...}` usage.

# 0.0.1

- Initial release of tsParticles, but in Dash!

# 0.0.3

- Added a structured Python config API for `DashParticles` with composable helper classes like `Background`, `Particles`, `Interactivity`, and `Options`.
- Added Python-side `config=`, `background=`, `particles=`, `interactivity=`, `fps_limit=`, and `detect_retina=` convenience arguments that serialize into the existing `options` prop.
- Kept raw dictionary configs backward-compatible for existing apps.
