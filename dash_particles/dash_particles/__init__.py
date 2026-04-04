from __future__ import print_function as _

import json
import os as _os
import sys as _sys

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import *
from ._imports_ import __all__ as _component_exports
from . import presets
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
    ManualParticle,
    Modes,
    Motion,
    MotionReduce,
    Move,
    Opacity,
    Options,
    OutModes,
    ParticleNumber,
    Particles,
    ParticlesOptions,
    Position,
    Push,
    RangeValue,
    Remove,
    Repulse,
    Responsive,
    Shape,
    Size,
    Theme,
    Twinkle,
    TwinkleParticles,
)

__all__ = _component_exports + [
    "Action",
    "Background",
    "BackgroundMask",
    "BackgroundMaskCover",
    "Bubble",
    "Color",
    "Density",
    "Events",
    "FullScreen",
    "Grab",
    "GrabLinks",
    "Interactivity",
    "Links",
    "ManualParticle",
    "Modes",
    "Motion",
    "MotionReduce",
    "Move",
    "Opacity",
    "Options",
    "OutModes",
    "ParticleNumber",
    "Particles",
    "ParticlesOptions",
    "Position",
    "presets",
    "Push",
    "RangeValue",
    "Remove",
    "Repulse",
    "Responsive",
    "Shape",
    "Size",
    "Theme",
    "Twinkle",
    "TwinkleParticles",
]

if not hasattr(_dash, "__plotly_dash") and not hasattr(_dash, "development"):
    print(
        'Dash was not successfully imported. Make sure you don\'t have a file named \n"dash.py" in your current directory.',
        file=_sys.stderr,
    )
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, "package-info.json"))
with open(_filepath) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")
__version__ = package["version"]

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]

async_resources = ["DashParticles"]

_js_dist = []

_js_dist.extend(
    [
        {
            "relative_package_path": f"async-{async_resource}.js",
            "external_url": (
                f"https://unpkg.com/{package_name}@{__version__}"
                f"/{__name__}/async-{async_resource}.js"
            ),
            "namespace": package_name,
            "async": True,
        }
        for async_resource in async_resources
    ]
)

_js_dist.extend(
    [
        {
            "relative_package_path": f"async-{async_resource}.js.map",
            "external_url": (
                f"https://unpkg.com/{package_name}@{__version__}"
                f"/{__name__}/async-{async_resource}.js.map"
            ),
            "namespace": package_name,
            "dynamic": True,
        }
        for async_resource in async_resources
    ]
)

_js_dist.extend(
    [
        {
            "relative_package_path": "dash_particles.min.js",
            "namespace": package_name,
        },
        {
            "relative_package_path": "dash_particles.min.js.map",
            "namespace": package_name,
            "dynamic": True,
        },
    ]
)

_css_dist = []

for _component in _component_exports:
    setattr(locals()[_component], "_js_dist", _js_dist)
    setattr(locals()[_component], "_css_dist", _css_dist)
