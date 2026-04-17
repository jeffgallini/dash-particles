# Changelog

# 0.0.1

- Initial release of tsParticles, but in Dash!

# 0.0.3

- Added a structured Python config API for `DashParticles` with composable helper classes like `Background`, `Particles`, `Interactivity`, and `Options`.
- Added Python-side `config=`, `background=`, `particles=`, `interactivity=`, `fps_limit=`, and `detect_retina=` convenience arguments that serialize into the existing `options` prop.
- Kept raw dictionary configs backward-compatible for existing apps.
