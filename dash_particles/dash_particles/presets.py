"""Curated structured presets for `dash-particles`.

These helpers return `dp.Options(...)` objects so users can start from a
well-named preset and then override only the pieces they care about.
"""

from __future__ import annotations

from urllib.parse import quote

from .options import (
    Action,
    Background,
    BackgroundMask,
    BackgroundMaskCover,
    Bubble,
    Color,
    Density,
    Events,
    FullScreen,
    Grab,
    GrabLinks,
    Interactivity,
    Links,
    Modes,
    Motion,
    MotionReduce,
    Move,
    Opacity,
    Options,
    OutModes,
    ParticleNumber,
    Particles,
    Push,
    RangeValue,
    Remove,
    Repulse,
    Shape,
    Size,
    Theme,
    Twinkle,
    TwinkleParticles,
)


def _svg_data_uri(svg_markup: str) -> str:
    return "data:image/svg+xml;utf8," + quote(svg_markup)


def _preload_image(src: str, width: int | None = None, height: int | None = None) -> dict:
    preload = {"src": src}
    if width is not None:
        preload["width"] = width
    if height is not None:
        preload["height"] = height
    return preload


AMONG_US_IMAGE = "https://particles.js.org/images/cyan_amongus.png"

STAR_IMAGE = _svg_data_uri(
    """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
      <path d="M32 4l8 17 19 3-14 13 3 19-16-9-16 9 3-19L5 24l19-3 8-17z" fill="#facc15"/>
    </svg>
    """
)

PLANET_IMAGE = _svg_data_uri(
    """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r="18" fill="#60a5fa"/>
      <ellipse cx="36" cy="36" rx="30" ry="10" fill="none" stroke="#bfdbfe" stroke-width="6"/>
    </svg>
    """
)

COMET_IMAGE = _svg_data_uri(
    """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 40">
      <path d="M6 20c16-10 28-15 44-16-9 5-16 10-24 16 8 6 15 11 24 16-16-1-28-6-44-16z" fill="#c4b5fd"/>
      <circle cx="60" cy="20" r="12" fill="#f8fafc"/>
    </svg>
    """
)

PRESET_LABELS = {
    "default": "Default Network",
    "bubbles": "Bubbles",
    "snow": "Snow",
    "fire": "Fire",
    "stars": "Stars",
    "connect": "Connected Network",
    "among_us": "Among Us",
    "multiple_images": "Multiple Images",
    "parallax": "Parallax",
    "fontawesome": "Font Awesome",
    "blurred_particles": "Blurred Particles",
    "hypno_squares": "Hypno Squares",
}

PRESET_DESCRIPTIONS = {
    "default": "A simple network of connected particles with click interaction and hover disabled.",
    "bubbles": "Floating bubbles of different sizes with a deep blue background.",
    "snow": "Falling snowflakes against a dark blue night sky.",
    "fire": "Rising fire particles with warm colors against a black background.",
    "stars": "A starry night sky with twinkling stars.",
    "connect": "An interactive network that responds to mouse movements and clicks.",
    "among_us": "The official Among Us-style preset with the fuller tsParticles option surface and emitter-driven image particles.",
    "multiple_images": "An image-based particle scene that rotates through multiple inline assets.",
    "parallax": "A linked particle field with hover parallax for a more spatial feel.",
    "fontawesome": "Character-based particles that work well with Font Awesome icons once the font is loaded.",
    "blurred_particles": "Large blurred particles with light and dark themes, inspired by the themeable blur demo.",
    "hypno_squares": "Rotating outlined squares that expand and self-destroy from a centered emitter.",
}


def default() -> Options:
    """Return the default interactive network preset."""
    return Options(
        background=Background(color=Color("#f0f0f0")),
        particles=Particles(
            color=Color("#000000"),
            number=ParticleNumber(value=50),
            size=Size(value=5),
            links=Links(enable=True, color="#000000", opacity=0.8, width=2),
        ),
        interactivity=Interactivity(
            events=Events(
                on_click=Action(enable=True, mode="push"),
                on_hover=Action(enable=False, mode="none"),
            )
        ),
    )


def bubbles() -> Options:
    """Return a soft bubble-style preset."""
    return Options(
        background=Background(color=Color("#0d47a1")),
        particles=Particles(
            color=Color("#ffffff"),
            number=ParticleNumber(value=100),
            size=Size(value=10, random=True),
            opacity=Opacity(value=0.7, random=True),
            move=Move(enable=True, speed=2, direction="none", random=True),
            links=Links(enable=False),
        ),
        interactivity=Interactivity(
            events=Events(
                on_hover=Action(enable=False, mode="none"),
            )
        ),
    )


def snow() -> Options:
    """Return a falling snow preset."""
    return Options(
        background=Background(color=Color("#2c3e50")),
        particles=Particles(
            color=Color("#ffffff"),
            number=ParticleNumber(value=200),
            size=Size(value=3, random=True),
            opacity=Opacity(value=0.8),
            move=Move(enable=True, speed=1, direction="bottom", straight=False),
            links=Links(enable=False),
        ),
        interactivity=Interactivity(
            events=Events(
                on_hover=Action(enable=False, mode="none"),
            )
        ),
    )


def fire() -> Options:
    """Return a rising ember-style preset."""
    return Options(
        background=Background(color=Color("#000000")),
        particles=Particles(
            color=Color(["#ff5722", "#ff9800", "#ffeb3b"]),
            number=ParticleNumber(value=80),
            shape=Shape(type="circle"),
            size=Size(value=8, random=True),
            opacity=Opacity(value=0.7, random=True),
            move=Move(
                enable=True,
                speed=5,
                direction="top",
                random=True,
                out_modes=OutModes(default="out"),
            ),
            links=Links(enable=False),
        ),
        interactivity=Interactivity(
            events=Events(
                on_hover=Action(enable=False, mode="none"),
            )
        ),
    )


def stars() -> Options:
    """Return a night-sky preset with twinkling particles."""
    return Options(
        background=Background(color=Color("#0a0a29")),
        particles=Particles(
            color=Color("#ffffff"),
            number=ParticleNumber(value=150),
            size=Size(value=2, random=True),
            opacity=Opacity(value=1, random=True),
            move=Move(enable=True, speed=0.2, direction="none", random=True),
            links=Links(enable=False),
            twinkle=Twinkle(
                particles=TwinkleParticles(enable=True, frequency=0.05, opacity=1),
            ),
        ),
        interactivity=Interactivity(
            events=Events(
                on_hover=Action(enable=False, mode="none"),
            )
        ),
    )


def connect() -> Options:
    """Return an interactive connected-network preset."""
    return Options(
        background=Background(color=Color("#ffffff")),
        particles=Particles(
            color=Color("#3498db"),
            number=ParticleNumber(value=120),
            size=Size(value=3),
            links=Links(enable=True, color="#3498db", opacity=0.4, width=1, distance=150),
            move=Move(enable=True, speed=2),
        ),
        interactivity=Interactivity(
            events=Events(
                on_hover=Action(enable=True, mode="grab"),
                on_click=Action(enable=True, mode="push"),
            ),
            modes=Modes(
                grab=Grab(distance=200, links=GrabLinks(opacity=1)),
            ),
        ),
    )


def among_us(image_src: str = AMONG_US_IMAGE) -> Options:
    """Return the official Among Us-style preset."""
    return Options(
        auto_play=True,
        background=Background(
            color=Color("#000000"),
            image="",
            position="",
            repeat="",
            size="",
            opacity=1,
        ),
        background_mask=BackgroundMask(
            enable=False,
            composite="destination-out",
            cover=BackgroundMaskCover(color=Color(""), opacity=1),
        ),
        full_screen=FullScreen(enable=True, z_index=0),
        particles=Particles(
            collisions={
                "absorb": {"speed": 2},
                "bounce": {"horizontal": {"value": 1}, "vertical": {"value": 1}},
                "enable": False,
                "maxSpeed": 50,
                "mode": "bounce",
                "overlap": {"enable": True, "retries": 0},
            },
            color=Color(
                "#fff",
                extra={
                    "animation": {
                        "h": {
                            "count": 0,
                            "enable": False,
                            "speed": 20,
                            "decay": 0,
                            "delay": 0,
                            "sync": True,
                            "offset": 0,
                        },
                        "s": {
                            "count": 0,
                            "enable": False,
                            "speed": 1,
                            "decay": 0,
                            "delay": 0,
                            "sync": True,
                            "offset": 0,
                        },
                        "l": {
                            "count": 0,
                            "enable": False,
                            "speed": 1,
                            "decay": 0,
                            "delay": 0,
                            "sync": True,
                            "offset": 0,
                        },
                    }
                },
            ),
            move=Move(
                angle={"offset": 0, "value": 10},
                attract={
                    "distance": 200,
                    "enable": False,
                    "rotate": {"x": 3000, "y": 3000},
                },
                center={"x": 50, "y": 50, "mode": "percent", "radius": 0},
                decay=0,
                drift=0,
                enable=True,
                direction="right",
                gravity={
                    "acceleration": 9.81,
                    "enable": False,
                    "inverse": False,
                    "maxSpeed": 50,
                },
                path={"clamp": True, "delay": {"value": 0}, "enable": False, "options": {}},
                random=False,
                extra={
                    "distance": {},
                    "size": False,
                    "spin": {"acceleration": 0, "enable": False},
                    "trail": {"enable": False, "length": 10, "fill": {}},
                    "vibrate": False,
                    "warp": False,
                },
                speed=5,
                out_modes=OutModes(default="out", bottom="out", left="out", right="out", top="out"),
                straight=False,
            ),
            number=ParticleNumber(
                value=200,
                density=Density(enable=False, extra={"width": 1920, "height": 1080}),
                extra={"limit": {"mode": "delete", "value": 0}},
            ),
            opacity=Opacity(
                value=1,
                animation={
                    "count": 0,
                    "enable": False,
                    "speed": 2,
                    "decay": 0,
                    "delay": 0,
                    "sync": False,
                    "mode": "auto",
                    "startValue": "random",
                    "destroy": "none",
                },
            ),
            shape=Shape(type="circle", extra={"close": True, "fill": True, "options": {}}),
            size=Size(
                value=3,
                animation={
                    "count": 0,
                    "enable": False,
                    "speed": 5,
                    "decay": 0,
                    "delay": 0,
                    "sync": False,
                    "mode": "auto",
                    "startValue": "random",
                    "destroy": "none",
                },
            ),
            links=Links(
                color=Color("#fff"),
                distance=100,
                enable=False,
                opacity=1,
                width=1,
                warp=False,
                triangles={"enable": False, "frequency": 1},
                extra={
                    "blink": False,
                    "consent": False,
                    "frequency": 1,
                    "shadow": {
                        "blur": 5,
                        "color": {"value": "#000"},
                        "enable": False,
                    }
                },
            ),
            twinkle=Twinkle(
                lines=TwinkleParticles(enable=False, frequency=0.05, opacity=1),
                particles=TwinkleParticles(enable=False, frequency=0.05, opacity=1),
            ),
            extra={
                "bounce": {"horizontal": {"value": 1}, "vertical": {"value": 1}},
                "destroy": {
                    "bounds": {},
                    "mode": "none",
                    "split": {
                        "count": 1,
                        "factor": {"value": 3},
                        "rate": {"value": {"min": 4, "max": 9}},
                        "sizeOffset": True,
                        "particles": {},
                    },
                },
                "effect": {"close": True, "fill": True, "options": {}, "type": {}},
                "groups": [],
                "life": {
                    "count": 0,
                    "delay": {"value": 0, "sync": False},
                    "duration": {"value": 0, "sync": False},
                },
                "orbit": {
                    "animation": {
                        "count": 0,
                        "enable": False,
                        "speed": 1,
                        "decay": 0,
                        "delay": 0,
                        "sync": False,
                    },
                    "enable": False,
                    "opacity": 1,
                    "rotation": {"value": 45},
                    "width": 1,
                },
                "reduceDuplicates": False,
                "repulse": {
                    "value": 0,
                    "enabled": False,
                    "distance": 1,
                    "duration": 1,
                    "factor": 1,
                    "speed": 1,
                },
                "roll": {
                    "darken": {"enable": False, "value": 0},
                    "enable": False,
                    "enlighten": {"enable": False, "value": 0},
                    "mode": "vertical",
                    "speed": 25,
                },
                "rotate": {
                    "value": 0,
                    "animation": {"enable": False, "speed": 0, "decay": 0, "sync": False},
                    "direction": "clockwise",
                    "path": False,
                },
                "shadow": {
                    "blur": 0,
                    "color": {"value": "#000"},
                    "enable": False,
                    "offset": {"x": 0, "y": 0},
                },
                "stroke": {"width": 0},
                "tilt": {
                    "value": 0,
                    "animation": {"enable": False, "speed": 0, "decay": 0, "sync": False},
                    "direction": "clockwise",
                    "enable": False,
                },
                "wobble": {
                    "distance": 5,
                    "enable": False,
                    "speed": {"angle": 50, "move": 10},
                },
                "zIndex": {
                    "value": 5,
                    "opacityRate": 0.5,
                    "sizeRate": 1,
                    "velocityRate": 1,
                },
            },
        ),
        interactivity=Interactivity(
            detects_on="window",
            events=Events(
                on_click=Action(enable=False, mode={}),
                on_hover=Action(
                    enable=False,
                    mode={},
                    parallax={"enable": False, "force": 2, "smooth": 10},
                ),
                on_div={"selectors": [], "enable": False, "mode": {}, "type": "circle"},
                resize={"delay": 0.5, "enable": True},
            ),
            modes=Modes(
                bubble=Bubble(distance=200, duration=0.4, extra={"mix": False}),
                grab=Grab(
                    distance=100,
                    links=GrabLinks(opacity=1, extra={"blink": False, "consent": False}),
                ),
                push=Push(quantity=4, extra={"default": True, "groups": []}),
                remove=Remove(quantity=2),
                repulse=Repulse(
                    distance=200,
                    duration=0.4,
                    extra={"factor": 100, "speed": 1, "maxSpeed": 50, "easing": "ease-out-quad"},
                ),
                extra={
                    "trail": {"delay": 1, "pauseOnStop": False, "quantity": 1},
                    "attract": {
                        "distance": 200,
                        "duration": 0.4,
                        "easing": "ease-out-quad",
                        "factor": 1,
                        "maxSpeed": 50,
                        "speed": 1,
                    },
                    "bounce": {"distance": 200},
                    "connect": {"distance": 80, "links": {"opacity": 0.5}, "radius": 60},
                    "slow": {"factor": 3, "radius": 200},
                    "particle": {
                        "replaceCursor": False,
                        "pauseOnStop": False,
                        "stopDelay": 0,
                    },
                    "light": {
                        "area": {
                            "gradient": {
                                "start": {"value": "#ffffff"},
                                "stop": {"value": "#000000"},
                            },
                            "radius": 1000,
                        },
                        "shadow": {
                            "color": {"value": "#000000"},
                            "length": 2000,
                        },
                    },
                },
            ),
        ),
        detect_retina=True,
        fps_limit=120,
        manual_particles=[],
        motion=Motion(disable=True, reduce=MotionReduce(factor=4, value=True)),
        pause_on_blur=True,
        pause_on_outside_viewport=True,
        responsive=[],
        themes=[],
        extra={
            "clear": True,
            "defaultThemes": {},
            "delay": 0,
            "duration": 0,
            "preload": [_preload_image(image_src, width=500, height=634)],
            "emitters": {
                "autoPlay": True,
                "fill": True,
                "life": {"wait": False},
                "rate": {"quantity": 1, "delay": 7},
                "shape": {
                    "type": "square",
                    "options": {},
                    "replace": {"color": False, "opacity": False},
                },
                "startCount": 0,
                "size": {"mode": "percent", "height": 0, "width": 0},
                "particles": {
                    "shape": {
                        "type": "images",
                        "options": {"images": {"src": image_src, "width": 500, "height": 634}},
                    },
                    "size": {"value": 40},
                    "move": {
                        "speed": 10,
                        "straight": True,
                        "outModes": {"default": "none", "right": "destroy"},
                    },
                    "rotate": {
                        "value": {"min": 0, "max": 360},
                        "animation": {"enable": True, "speed": 10, "sync": True},
                    },
                    "zIndex": {"value": 0},
                },
                "position": {"x": -5, "y": 55},
            },
            "key": "amongUs",
            "name": "Among Us",
            "smooth": False,
            "style": {},
            "zLayers": 100,
        },
    )


def multiple_images(image_sources=None) -> Options:
    """Return a preset that cycles through multiple image-based particles."""
    if image_sources is None:
        image_sources = [
            {"src": STAR_IMAGE, "width": 64, "height": 64},
            {"src": PLANET_IMAGE, "width": 72, "height": 72},
            {"src": COMET_IMAGE, "width": 80, "height": 40},
        ]

    return Options(
        background=Background(color=Color("#020617")),
        particles=Particles(
            number=ParticleNumber(value=24),
            links=Links(enable=False),
            move=Move(enable=True, speed=1.1, out_modes=OutModes(default="bounce")),
            size=Size(value=24),
            shape=Shape(type="image", options={"image": image_sources}),
        ),
        extra={"preload": image_sources},
    )


def _parallax_full_sample() -> Options:
    """Return the official Parallax-style preset."""
    return Options(
        auto_play=True,
        background=Background(
            color=Color("#0d47a1"),
            image="",
            position="",
            repeat="",
            size="",
            opacity=1,
        ),
        background_mask=BackgroundMask(
            enable=False,
            composite="destination-out",
            cover=BackgroundMaskCover(color=Color(""), opacity=1),
        ),
        full_screen=FullScreen(enable=True, z_index=0),
        interactivity=Interactivity(
            detects_on="window",
            events=Events(
                on_click=Action(enable=True, mode="push"),
                on_hover=Action(
                    enable=True,
                    mode="grab",
                    parallax={"enable": True, "force": 60, "smooth": 10},
                ),
                on_div={"selectors": [], "enable": False, "mode": {}, "type": "circle"},
                resize={"delay": 0.5, "enable": True},
            ),
            modes=Modes(
                bubble=Bubble(
                    distance=400,
                    duration=2,
                    opacity=0.8,
                    size=40,
                    extra={
                        "mix": False,
                        "divs": {
                            "distance": 200,
                            "duration": 0.4,
                            "mix": False,
                            "selectors": [],
                        },
                    },
                ),
                grab=Grab(
                    distance=400,
                    links=GrabLinks(opacity=1, extra={"blink": False, "consent": False}),
                ),
                push=Push(quantity=4, extra={"default": True, "groups": [], "particles": {}}),
                remove=Remove(quantity=2),
                repulse=Repulse(
                    distance=200,
                    duration=0.4,
                    extra={
                        "factor": 100,
                        "speed": 1,
                        "maxSpeed": 50,
                        "easing": "ease-out-quad",
                        "divs": {
                            "distance": 200,
                            "duration": 0.4,
                            "factor": 100,
                            "speed": 1,
                            "maxSpeed": 50,
                            "easing": "ease-out-quad",
                            "selectors": [],
                        },
                    },
                ),
                extra={
                    "trail": {"delay": 1, "pauseOnStop": False, "quantity": 1},
                    "attract": {
                        "distance": 200,
                        "duration": 0.4,
                        "easing": "ease-out-quad",
                        "factor": 1,
                        "maxSpeed": 50,
                        "speed": 1,
                    },
                    "bounce": {"distance": 200},
                    "connect": {"distance": 80, "links": {"opacity": 0.5}, "radius": 60},
                    "slow": {"factor": 3, "radius": 200},
                    "particle": {
                        "replaceCursor": False,
                        "pauseOnStop": False,
                        "stopDelay": 0,
                    },
                    "light": {
                        "area": {
                            "gradient": {
                                "start": {"value": "#ffffff"},
                                "stop": {"value": "#000000"},
                            },
                            "radius": 1000,
                        },
                        "shadow": {
                            "color": {"value": "#000000"},
                            "length": 2000,
                        },
                    },
                },
            ),
        ),
        particles=Particles(
            collisions={
                "absorb": {"speed": 2},
                "bounce": {"horizontal": {"value": 1}, "vertical": {"value": 1}},
                "enable": False,
                "maxSpeed": 50,
                "mode": "bounce",
                "overlap": {"enable": True, "retries": 0},
            },
            color=Color(
                "#ffffff",
                extra={
                    "animation": {
                        "h": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                        "s": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                        "l": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                    }
                },
            ),
            links=Links(
                color=Color("#ffffff"),
                distance=150,
                enable=True,
                opacity=0.4,
                width=1,
                warp=False,
                triangles={"enable": False, "frequency": 1},
                extra={
                    "blink": False,
                    "consent": False,
                    "frequency": 1,
                    "shadow": {"blur": 5, "color": {"value": "#000"}, "enable": False},
                },
            ),
            move=Move(
                angle={"offset": 0, "value": 90},
                attract={"distance": 200, "enable": False, "rotate": {"x": 3000, "y": 3000}},
                center={"x": 50, "y": 50, "mode": "percent", "radius": 0},
                decay=0,
                drift=0,
                enable=True,
                direction="none",
                gravity={"acceleration": 9.81, "enable": False, "inverse": False, "maxSpeed": 50},
                path={"clamp": True, "delay": {"value": 0}, "enable": False, "options": {}},
                random=False,
                extra={
                    "distance": {},
                    "size": False,
                    "spin": {"acceleration": 0, "enable": False},
                    "trail": {"enable": False, "length": 10, "fill": {}},
                    "vibrate": False,
                    "warp": False,
                },
                speed=2,
                out_modes=OutModes(default="out", bottom="out", left="out", right="out", top="out"),
                straight=False,
            ),
            number=ParticleNumber(
                value=100,
                density=Density(enable=True, extra={"width": 1920, "height": 1080}),
                extra={"limit": {"mode": "delete", "value": 0}},
            ),
            opacity=Opacity(
                value=RangeValue(min=0.1, max=0.5),
                animation={
                    "count": 0,
                    "enable": True,
                    "speed": 3,
                    "decay": 0,
                    "delay": 0,
                    "sync": False,
                    "mode": "auto",
                    "startValue": "random",
                    "destroy": "none",
                },
            ),
            shape=Shape(type="circle", extra={"close": True, "fill": True, "options": {}}),
            size=Size(
                value=RangeValue(min=1, max=10),
                animation={
                    "count": 0,
                    "enable": True,
                    "speed": 20,
                    "decay": 0,
                    "delay": 0,
                    "sync": False,
                    "mode": "auto",
                    "startValue": "random",
                    "destroy": "none",
                },
            ),
            twinkle=Twinkle(
                lines=TwinkleParticles(enable=False, frequency=0.05, opacity=1),
                particles=TwinkleParticles(enable=False, frequency=0.05, opacity=1),
            ),
            extra={
                "bounce": {"horizontal": {"value": 1}, "vertical": {"value": 1}},
                "destroy": {
                    "bounds": {},
                    "mode": "none",
                    "split": {
                        "count": 1,
                        "factor": {"value": 3},
                        "rate": {"value": {"min": 4, "max": 9}},
                        "sizeOffset": True,
                        "particles": {},
                    },
                },
                "effect": {"close": True, "fill": True, "options": {}, "type": {}},
                "groups": [],
                "life": {
                    "count": 0,
                    "delay": {"value": 0, "sync": False},
                    "duration": {"value": 0, "sync": False},
                },
                "orbit": {
                    "animation": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": False},
                    "enable": False,
                    "opacity": 1,
                    "rotation": {"value": 45},
                    "width": 1,
                },
                "reduceDuplicates": False,
                "repulse": {"value": 0, "enabled": False, "distance": 1, "duration": 1, "factor": 1, "speed": 1},
                "roll": {
                    "darken": {"enable": False, "value": 0},
                    "enable": False,
                    "enlighten": {"enable": False, "value": 0},
                    "mode": "vertical",
                    "speed": 25,
                },
                "rotate": {
                    "value": 0,
                    "animation": {"enable": False, "speed": 0, "decay": 0, "sync": False},
                    "direction": "clockwise",
                    "path": False,
                },
                "shadow": {"blur": 0, "color": {"value": "#000"}, "enable": False, "offset": {"x": 0, "y": 0}},
                "stroke": {"width": 0},
                "tilt": {
                    "value": 0,
                    "animation": {"enable": False, "speed": 0, "decay": 0, "sync": False},
                    "direction": "clockwise",
                    "enable": False,
                },
                "wobble": {"distance": 5, "enable": False, "speed": {"angle": 50, "move": 10}},
                "zIndex": {"value": 0, "opacityRate": 1, "sizeRate": 1, "velocityRate": 1},
            },
        ),
        detect_retina=True,
        fps_limit=120,
        manual_particles=[],
        motion=Motion(disable=True, reduce=MotionReduce(factor=4, value=True)),
        pause_on_blur=True,
        pause_on_outside_viewport=True,
        responsive=[],
        themes=[],
        extra={
            "clear": True,
            "defaultThemes": {},
            "delay": 0,
            "duration": 0,
            "key": "parallax",
            "name": "Parallax",
            "smooth": False,
            "style": {},
            "zLayers": 100,
        },
    )


def fontawesome(
    brand_font_family: str = "Font Awesome 6 Brands",
    brand_glyph: str = "\uf179",
    brand_weight: str = "400",
    solid_font_family: str | None = None,
    solid_glyph: str | None = None,
    solid_weight: str = "900",
) -> Options:
    """Return the official Font Awesome-style preset.

    The default font family names target the Font Awesome 6 stylesheet used by
    the demo app. Pass Font Awesome 5 family names explicitly if your page loads
    the older assets from the original tsParticles sample. By default this uses
    the Apple brand icon (`fa-brands fa-apple`) for every particle.
    """
    brand_option = {
        "fill": True,
        "font": brand_font_family,
        "style": "",
        "value": brand_glyph,
        "weight": brand_weight,
    }

    char_options: dict | list = brand_option

    if solid_font_family and solid_glyph:
        char_options = [brand_option, {
            "fill": True,
            "font": solid_font_family,
            "style": "",
            "value": solid_glyph,
            "weight": solid_weight,
        }]

    return Options(
        auto_play=True,
        background=Background(
            color=Color("#0d47a1"),
            image="",
            position="50% 50%",
            repeat="no-repeat",
            size="cover",
            opacity=1,
        ),
        background_mask=BackgroundMask(
            enable=False,
            composite="destination-out",
            cover=BackgroundMaskCover(color=Color(""), opacity=1),
        ),
        full_screen=FullScreen(enable=True, z_index=0),
        particles=Particles(
            collisions={
                "absorb": {"speed": 2},
                "bounce": {"horizontal": {"value": 1}, "vertical": {"value": 1}},
                "enable": False,
                "maxSpeed": 50,
                "mode": "bounce",
                "overlap": {"enable": True, "retries": 0},
            },
            color=Color(
                "#ffffff",
                extra={
                    "animation": {
                        "h": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                        "s": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                        "l": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                    }
                },
            ),
            move=Move(
                angle={"offset": 0, "value": 90},
                attract={"distance": 200, "enable": False, "rotate": {"x": 3000, "y": 3000}},
                center={"x": 50, "y": 50, "mode": "percent", "radius": 0},
                decay=0,
                drift=0,
                enable=True,
                direction="none",
                gravity={"acceleration": 9.81, "enable": False, "inverse": False, "maxSpeed": 50},
                path={"clamp": True, "delay": {"value": 0}, "enable": False, "options": {}},
                random=False,
                extra={
                    "distance": {},
                    "size": False,
                    "spin": {"acceleration": 0, "enable": False},
                    "trail": {"enable": False, "length": 10, "fill": {}},
                    "vibrate": False,
                    "warp": False,
                },
                speed=2,
                out_modes=OutModes(default="out", bottom="out", left="out", right="out", top="out"),
                straight=False,
            ),
            number=ParticleNumber(
                value=80,
                density=Density(enable=True, extra={"width": 1920, "height": 1080}),
                extra={"limit": {"mode": "delete", "value": 0}},
            ),
            opacity=Opacity(
                value=RangeValue(min=0.1, max=0.5),
                animation={
                    "count": 0,
                    "enable": True,
                    "speed": 1,
                    "decay": 0,
                    "delay": 0,
                    "sync": False,
                    "mode": "auto",
                    "startValue": "random",
                    "destroy": "none",
                },
            ),
            shape=Shape(
                type="char",
                options={"char": char_options},
                extra={
                    "close": True,
                    "fill": True,
                },
            ),
            size=Size(
                value=16,
                animation={
                    "count": 0,
                    "enable": False,
                    "speed": 5,
                    "decay": 0,
                    "delay": 0,
                    "sync": False,
                    "mode": "auto",
                    "startValue": "random",
                    "destroy": "none",
                },
            ),
            links=Links(
                color=Color("#ffffff"),
                distance=150,
                enable=True,
                opacity=0.4,
                width=1,
                warp=False,
                triangles={"enable": False, "frequency": 1},
                extra={
                    "blink": False,
                    "consent": False,
                    "frequency": 1,
                    "shadow": {"blur": 5, "color": {"value": "lime"}, "enable": False},
                },
            ),
            twinkle=Twinkle(
                lines=TwinkleParticles(enable=False, frequency=0.05, opacity=1),
                particles=TwinkleParticles(enable=False, frequency=0.05, opacity=1),
            ),
            extra={
                "bounce": {"horizontal": {"value": 1}, "vertical": {"value": 1}},
                "destroy": {
                    "bounds": {},
                    "mode": "none",
                    "split": {
                        "count": 1,
                        "factor": {"value": 3},
                        "rate": {"value": {"min": 4, "max": 9}},
                        "sizeOffset": True,
                        "particles": {},
                    },
                },
                "effect": {"close": True, "fill": True, "options": {}, "type": {}},
                "groups": [],
                "life": {
                    "count": 0,
                    "delay": {"value": 0, "sync": False},
                    "duration": {"value": 0, "sync": False},
                },
                "orbit": {
                    "animation": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": False},
                    "enable": False,
                    "opacity": 1,
                    "rotation": {"value": 45},
                    "width": 1,
                },
                "reduceDuplicates": False,
                "repulse": {"value": 0, "enabled": False, "distance": 1, "duration": 1, "factor": 1, "speed": 1},
                "roll": {
                    "darken": {"enable": False, "value": 0},
                    "enable": False,
                    "enlighten": {"enable": False, "value": 0},
                    "mode": "vertical",
                    "speed": 25,
                },
                "rotate": {
                    "value": 0,
                    "animation": {"enable": False, "speed": 0, "decay": 0, "sync": False},
                    "direction": "clockwise",
                    "path": False,
                },
                "shadow": {"blur": 0, "color": {"value": "#000"}, "enable": False, "offset": {"x": 0, "y": 0}},
                "stroke": {
                    "width": 0,
                    "color": {
                        "value": "#ffffff",
                        "animation": {
                            "h": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                            "s": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                            "l": {"count": 0, "enable": False, "speed": 1, "decay": 0, "delay": 0, "sync": True, "offset": 0},
                        },
                    },
                },
                "tilt": {
                    "value": 0,
                    "animation": {"enable": False, "speed": 0, "decay": 0, "sync": False},
                    "direction": "clockwise",
                    "enable": False,
                },
                "wobble": {"distance": 5, "enable": False, "speed": {"angle": 50, "move": 10}},
                "zIndex": {"value": 0, "opacityRate": 1, "sizeRate": 1, "velocityRate": 1},
            },
        ),
        interactivity=Interactivity(
            detects_on="window",
            events=Events(
                on_click=Action(enable=True, mode="push"),
                on_hover=Action(enable=True, mode="repulse", parallax={"enable": False, "force": 2, "smooth": 10}),
                on_div={"selectors": [], "enable": False, "mode": {}, "type": "circle"},
                resize={"delay": 0.5, "enable": True},
            ),
            modes=Modes(
                bubble=Bubble(
                    distance=200,
                    duration=0.4,
                    extra={"mix": False, "divs": {"distance": 200, "duration": 0.4, "mix": False, "selectors": []}},
                ),
                grab=Grab(distance=100, links=GrabLinks(opacity=1, extra={"blink": False, "consent": False})),
                push=Push(quantity=4, extra={"default": True, "groups": [], "particles": {}}),
                remove=Remove(quantity=2),
                repulse=Repulse(
                    distance=200,
                    duration=0.4,
                    extra={
                        "factor": 100,
                        "speed": 1,
                        "maxSpeed": 50,
                        "easing": "ease-out-quad",
                        "divs": {
                            "distance": 200,
                            "duration": 0.4,
                            "factor": 100,
                            "speed": 1,
                            "maxSpeed": 50,
                            "easing": "ease-out-quad",
                            "selectors": [],
                        },
                    },
                ),
                extra={
                    "trail": {"delay": 1, "pauseOnStop": False, "quantity": 1},
                    "attract": {"distance": 200, "duration": 0.4, "easing": "ease-out-quad", "factor": 1, "maxSpeed": 50, "speed": 1},
                    "bounce": {"distance": 200},
                    "connect": {"distance": 80, "links": {"opacity": 0.5}, "radius": 60},
                    "slow": {"factor": 3, "radius": 200},
                    "particle": {"replaceCursor": False, "pauseOnStop": False, "stopDelay": 0},
                    "light": {
                        "area": {
                            "gradient": {"start": {"value": "#ffffff"}, "stop": {"value": "#000000"}},
                            "radius": 1000,
                        },
                        "shadow": {"color": {"value": "#000000"}, "length": 2000},
                    },
                },
            ),
        ),
        detect_retina=True,
        fps_limit=120,
        manual_particles=[],
        motion=Motion(disable=True, reduce=MotionReduce(factor=4, value=True)),
        pause_on_blur=True,
        pause_on_outside_viewport=True,
        responsive=[],
        themes=[],
        extra={
            "clear": True,
            "defaultThemes": {},
            "delay": 0,
            "duration": 0,
            "key": "fontawesome",
            "name": "Font Awesome",
            "smooth": False,
            "style": {},
            "zLayers": 100,
        },
    )


def blurred_particles() -> Options:
    """Return a blurred emitter-driven preset with light and dark themes."""
    return Options(
        fps_limit=60,
        full_screen=FullScreen(enable=True),
        particles=Particles(
            number=ParticleNumber(value=50),
            shape=Shape(type="circle"),
            opacity=Opacity(value=0.5),
            size=Size(value=400, random={"enable": True, "minimumValue": 200}),
            move=Move(
                enable=True,
                speed=10,
                direction="top",
                out_modes=OutModes(default="out", top="destroy", bottom="none"),
            ),
        ),
        interactivity=Interactivity(
            detects_on="canvas",
            events=Events(resize=True),
        ),
        detect_retina=True,
        themes=[
            Theme(
                name="light",
                default={"value": True, "mode": "light"},
                options=Options(
                    background=Background(color=Color("#f7f8ef")),
                    particles=Particles(
                        color=Color(["#5bc0eb", "#fde74c", "#9bc53d", "#e55934", "#fa7921"]),
                    ),
                ),
            ),
            Theme(
                name="dark",
                default={"value": True, "mode": "dark"},
                options=Options(
                    background=Background(color=Color("#080710")),
                    particles=Particles(
                        color=Color(["#004f74", "#5f5800", "#245100", "#7d0000", "#810c00"]),
                    ),
                ),
            ),
        ],
        extra={
            "emitters": {
                "direction": "top",
                "position": {"x": 50, "y": 150},
                "rate": {"delay": 0.2, "quantity": 2},
                "size": {"width": 100, "height": 0},
            },
            "key": "blurredParticles",
            "name": "Blurred Particles",
            "style": {"filter": "blur(50px)"},
        },
    )


def hypno_squares() -> Options:
    """Return a rotating outlined-square emitter preset."""
    return Options(
        background=Background(color=Color("#000")),
        particles=Particles(
            shape=Shape(
                type="square",
                options={"square": {"fill": False}},
            ),
            size=Size(
                value=RangeValue(min=1, max=500),
                animation={
                    "enable": True,
                    "startValue": "min",
                    "speed": 60,
                    "sync": True,
                    "destroy": "max",
                },
            ),
            extra={
                "stroke": {
                    "width": 5,
                    "color": {
                        "value": [
                            "#5bc0eb",
                            "#fde74c",
                            "#9bc53d",
                            "#e55934",
                            "#fa7921",
                            "#2FF3E0",
                            "#F8D210",
                            "#FA26A0",
                            "#F51720",
                        ]
                    },
                },
                "rotate": {
                    "value": 0,
                    "direction": "counter-clockwise",
                    "animation": {
                        "enable": True,
                        "speed": 2,
                        "sync": True,
                    },
                },
            },
        ),
        extra={
            "emitters": {
                "direction": "top",
                "position": {"x": 50, "y": 50},
                "rate": {"delay": 1, "quantity": 1},
            },
            "key": "hypnoSquares",
            "name": "Hypno Squares",
        },
    )


def parallax() -> Options:
    """Return a linked network preset with hover parallax enabled."""
    return Options(
        auto_play=True,
        background=Background(color=Color("#0d47a1"), opacity=1),
        full_screen=FullScreen(enable=True, z_index=0),
        interactivity=Interactivity(
            detects_on="window",
            events=Events(
                on_click=Action(enable=True, mode="push"),
                on_hover=Action(
                    enable=True,
                    mode="grab",
                    parallax={"enable": True, "force": 60, "smooth": 10},
                ),
                resize=True,
            ),
            modes=Modes(
                bubble=Bubble(distance=200, duration=0.4),
                grab=Grab(distance=220, links=GrabLinks(opacity=1)),
                push=Push(quantity=4),
            ),
        ),
        particles=Particles(
            color=Color("#ffffff"),
            number=ParticleNumber(value=100, density=Density(enable=True, area=800)),
            opacity=Opacity(value=0.35),
            size=Size(value=RangeValue(min=1, max=6)),
            links=Links(enable=True, color="#ffffff", opacity=0.35, width=1, distance=150),
            move=Move(enable=True, speed=2, out_modes=OutModes(default="out")),
        ),
        detect_retina=True,
        fps_limit=120,
        extra={"key": "parallax", "name": "Parallax"},
    )


PRESET_BUILDERS = {
    "default": default,
    "bubbles": bubbles,
    "snow": snow,
    "fire": fire,
    "stars": stars,
    "connect": connect,
    "among_us": among_us,
    "multiple_images": multiple_images,
    "parallax": parallax,
    "fontawesome": fontawesome,
    "blurred_particles": blurred_particles,
    "hypno_squares": hypno_squares,
}


def names():
    """Return the available preset names."""
    return tuple(PRESET_BUILDERS.keys())


def all_presets():
    """Return all curated presets as structured `Options` objects."""
    return {name: build() for name, build in PRESET_BUILDERS.items()}


__all__ = [
    "PRESET_BUILDERS",
    "PRESET_DESCRIPTIONS",
    "PRESET_LABELS",
    "all_presets",
    "among_us",
    "bubbles",
    "connect",
    "default",
    "fire",
    "blurred_particles",
    "fontawesome",
    "hypno_squares",
    "multiple_images",
    "names",
    "parallax",
    "snow",
    "stars",
]
