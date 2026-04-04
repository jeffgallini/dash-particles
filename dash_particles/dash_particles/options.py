"""Structured Python config models for `dash-particles`.

These helpers make tsParticles options easier to build from Python and
serialize back to the JavaScript `options` shape expected by the Dash
component.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field, fields, is_dataclass
import typing


JsonDict = typing.Dict[str, typing.Any]
ColorValue = typing.Union[str, typing.Sequence[str]]
ModeValue = typing.Union[str, typing.Sequence[str]]
ScalarValue = typing.Union[int, float]


def _deep_merge(base: JsonDict, updates: JsonDict) -> JsonDict:
    merged = dict(base)

    for key, value in updates.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = _deep_merge(current, value)
        else:
            merged[key] = value

    return merged


def _serialize(value: typing.Any) -> typing.Any:
    if value is None:
        return None

    if isinstance(value, OptionsModel):
        return value.to_dict()

    if is_dataclass(value):
        return _serialize_dataclass(value)

    if isinstance(value, Mapping):
        serialized_mapping = {}
        for key, item in value.items():
            serialized_item = _serialize(item)
            if serialized_item is not None:
                serialized_mapping[key] = serialized_item
        return serialized_mapping

    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        serialized_sequence = []
        for item in value:
            serialized_item = _serialize(item)
            if serialized_item is not None:
                serialized_sequence.append(serialized_item)
        return serialized_sequence

    return value


def _serialize_dataclass(instance: typing.Any) -> JsonDict:
    result: JsonDict = {}

    extra = getattr(instance, "extra", None)
    if extra:
        serialized_extra = _serialize(extra)
        if serialized_extra is not None:
            result = _deep_merge(result, serialized_extra)

    for data_field in fields(instance):
        if data_field.name == "extra":
            continue

        value = getattr(instance, data_field.name)
        if value is None:
            continue

        key = data_field.metadata.get("alias", data_field.name)
        serialized_value = _serialize(value)

        if isinstance(result.get(key), dict) and isinstance(serialized_value, dict):
            result[key] = _deep_merge(result[key], serialized_value)
        else:
            result[key] = serialized_value

    return result


def serialize_options(value: typing.Any) -> typing.Optional[JsonDict]:
    """Serialize a config object, dataclass, or dict into tsParticles options."""
    if value is None:
        return None

    serialized = _serialize(value)
    if serialized is None:
        return None

    if not isinstance(serialized, dict):
        raise TypeError(
            "DashParticles config values must serialize to a dictionary of tsParticles options."
        )

    return serialized


def merge_options(*values: typing.Any) -> typing.Optional[JsonDict]:
    """Deep-merge config inputs from left to right after serialization."""
    merged: JsonDict = {}
    has_values = False

    for value in values:
        serialized = serialize_options(value)
        if serialized is None:
            continue

        has_values = True
        merged = _deep_merge(merged, serialized)

    return merged if has_values else None


class OptionsModel:
    """Base class for structured config helpers that can serialize to dicts."""

    def to_dict(self) -> JsonDict:
        """Convert this structured config object into a tsParticles dict."""
        return _serialize_dataclass(self)


@dataclass
class Color(OptionsModel):
    """Color configuration for particle or background elements."""

    value: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Background(OptionsModel):
    """Background styling for the particle canvas."""

    color: typing.Optional[typing.Union[Color, ColorValue, JsonDict]] = None
    image: typing.Optional[str] = None
    position: typing.Optional[str] = None
    repeat: typing.Optional[str] = None
    size: typing.Optional[str] = None
    opacity: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Density(OptionsModel):
    """Density settings used by particle counts."""

    enable: typing.Optional[bool] = None
    area: typing.Optional[ScalarValue] = None
    factor: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class ParticleNumber(OptionsModel):
    """Particle count configuration."""

    value: typing.Optional[ScalarValue] = None
    density: typing.Optional[Density] = None
    limit: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class RangeValue(OptionsModel):
    """A numeric min/max range used by size, opacity, or animation values."""

    min: typing.Optional[ScalarValue] = None
    max: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Links(OptionsModel):
    """Link settings for the lines drawn between particles."""

    enable: typing.Optional[bool] = None
    color: typing.Optional[typing.Any] = None
    opacity: typing.Optional[ScalarValue] = None
    width: typing.Optional[ScalarValue] = None
    distance: typing.Optional[ScalarValue] = None
    warp: typing.Optional[bool] = None
    triangles: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class OutModes(OptionsModel):
    """Behavior to apply when particles reach canvas edges."""

    default: typing.Optional[str] = None
    top: typing.Optional[str] = None
    right: typing.Optional[str] = None
    bottom: typing.Optional[str] = None
    left: typing.Optional[str] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Move(OptionsModel):
    """Motion settings for particle animation."""

    enable: typing.Optional[bool] = None
    speed: typing.Optional[ScalarValue] = None
    direction: typing.Optional[str] = None
    random: typing.Optional[typing.Any] = None
    straight: typing.Optional[bool] = None
    angle: typing.Optional[typing.Any] = None
    attract: typing.Optional[typing.Any] = None
    center: typing.Optional[typing.Any] = None
    decay: typing.Optional[ScalarValue] = None
    drift: typing.Optional[ScalarValue] = None
    gravity: typing.Optional[typing.Any] = None
    path: typing.Optional[typing.Any] = None
    trail: typing.Optional[typing.Any] = None
    out_modes: typing.Optional[OutModes] = field(default=None, metadata={"alias": "outModes"})
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Size(OptionsModel):
    """Size settings for particles."""

    value: typing.Optional[typing.Union[ScalarValue, RangeValue]] = None
    random: typing.Optional[typing.Any] = None
    animation: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Opacity(OptionsModel):
    """Opacity settings for particles."""

    value: typing.Optional[typing.Union[ScalarValue, RangeValue]] = None
    random: typing.Optional[typing.Any] = None
    animation: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Shape(OptionsModel):
    """Shape settings for particles."""

    type: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None
    options: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class TwinkleParticles(OptionsModel):
    """Twinkle effect settings for particles or links."""

    enable: typing.Optional[bool] = None
    color: typing.Optional[typing.Any] = None
    frequency: typing.Optional[ScalarValue] = None
    opacity: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Twinkle(OptionsModel):
    """Container for twinkle effect settings."""

    lines: typing.Optional[TwinkleParticles] = None
    particles: typing.Optional[TwinkleParticles] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Particles(OptionsModel):
    """Main particle appearance and behavior settings."""

    color: typing.Optional[typing.Union[Color, ColorValue, JsonDict]] = None
    collisions: typing.Optional[typing.Any] = None
    links: typing.Optional[Links] = None
    move: typing.Optional[Move] = None
    number: typing.Optional[ParticleNumber] = None
    opacity: typing.Optional[Opacity] = None
    shape: typing.Optional[Shape] = None
    size: typing.Optional[Size] = None
    twinkle: typing.Optional[Twinkle] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Action(OptionsModel):
    """Click, hover, or div action settings."""

    enable: typing.Optional[bool] = None
    mode: typing.Optional[ModeValue] = None
    parallax: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Events(OptionsModel):
    """Interactivity event handlers such as click and hover."""

    on_click: typing.Optional[Action] = field(default=None, metadata={"alias": "onClick"})
    on_hover: typing.Optional[Action] = field(default=None, metadata={"alias": "onHover"})
    on_div: typing.Optional[typing.Any] = field(default=None, metadata={"alias": "onDiv"})
    resize: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class GrabLinks(OptionsModel):
    """Link styling for the grab interaction mode."""

    opacity: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Grab(OptionsModel):
    """Grab interaction mode settings."""

    distance: typing.Optional[ScalarValue] = None
    links: typing.Optional[GrabLinks] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Repulse(OptionsModel):
    """Repulse interaction mode settings."""

    distance: typing.Optional[ScalarValue] = None
    duration: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Push(OptionsModel):
    """Push interaction mode settings."""

    quantity: typing.Optional[int] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Remove(OptionsModel):
    """Remove interaction mode settings."""

    quantity: typing.Optional[int] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Bubble(OptionsModel):
    """Bubble interaction mode settings."""

    distance: typing.Optional[ScalarValue] = None
    duration: typing.Optional[ScalarValue] = None
    opacity: typing.Optional[ScalarValue] = None
    size: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Modes(OptionsModel):
    """Collection of interaction modes used by hover and click events."""

    bubble: typing.Optional[Bubble] = None
    grab: typing.Optional[Grab] = None
    push: typing.Optional[Push] = None
    remove: typing.Optional[Remove] = None
    repulse: typing.Optional[Repulse] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Interactivity(OptionsModel):
    """Interactive behavior such as hover and click responses."""

    detects_on: typing.Optional[str] = field(default=None, metadata={"alias": "detectsOn"})
    events: typing.Optional[Events] = None
    modes: typing.Optional[Modes] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class BackgroundMaskCover(OptionsModel):
    """Color and opacity used for the background mask cover."""

    color: typing.Optional[typing.Any] = None
    opacity: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class BackgroundMask(OptionsModel):
    """Background mask settings for cutout-style effects."""

    enable: typing.Optional[bool] = None
    composite: typing.Optional[str] = None
    cover: typing.Optional[typing.Union[BackgroundMaskCover, Color, JsonDict, str]] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class FullScreen(OptionsModel):
    """Canvas full-screen behavior and stacking order."""

    enable: typing.Optional[bool] = None
    z_index: typing.Optional[int] = field(default=None, metadata={"alias": "zIndex"})
    extra: JsonDict = field(default_factory=dict)


@dataclass
class MotionReduce(OptionsModel):
    """Reduced-motion behavior used by the top-level motion settings."""

    factor: typing.Optional[ScalarValue] = None
    value: typing.Optional[bool] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Motion(OptionsModel):
    """Motion toggles and reduced-motion behavior."""

    disable: typing.Optional[bool] = None
    reduce: typing.Optional[typing.Union[MotionReduce, JsonDict]] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Position(OptionsModel):
    """A percentage-based x/y position for manual particles."""

    x: typing.Optional[ScalarValue] = None
    y: typing.Optional[ScalarValue] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class ManualParticle(OptionsModel):
    """A manually positioned particle definition."""

    position: typing.Optional[Position] = None
    options: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Responsive(OptionsModel):
    """Width-based override rules for responsive particle configs."""

    max_width: typing.Optional[int] = field(default=None, metadata={"alias": "maxWidth"})
    mode: typing.Optional[str] = None
    options: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class Theme(OptionsModel):
    """Named theme variants that can swap particle options."""

    name: typing.Optional[str] = None
    default: typing.Optional[typing.Any] = None
    options: typing.Optional[typing.Any] = None
    extra: JsonDict = field(default_factory=dict)


@dataclass
class ParticlesOptions(OptionsModel):
    """Top-level structured config object for `dp.DashParticles(config=...)`."""

    auto_play: typing.Optional[bool] = field(default=None, metadata={"alias": "autoPlay"})
    background: typing.Optional[Background] = None
    background_mask: typing.Optional[BackgroundMask] = field(
        default=None,
        metadata={"alias": "backgroundMask"},
    )
    detect_retina: typing.Optional[bool] = field(default=None, metadata={"alias": "detectRetina"})
    fps_limit: typing.Optional[ScalarValue] = field(default=None, metadata={"alias": "fpsLimit"})
    full_screen: typing.Optional[FullScreen] = field(default=None, metadata={"alias": "fullScreen"})
    interactivity: typing.Optional[Interactivity] = None
    manual_particles: typing.Optional[typing.Sequence[ManualParticle]] = field(
        default=None,
        metadata={"alias": "manualParticles"},
    )
    motion: typing.Optional[Motion] = None
    particles: typing.Optional[Particles] = None
    pause_on_blur: typing.Optional[bool] = field(default=None, metadata={"alias": "pauseOnBlur"})
    pause_on_outside_viewport: typing.Optional[bool] = field(
        default=None,
        metadata={"alias": "pauseOnOutsideViewport"},
    )
    preset: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None
    responsive: typing.Optional[typing.Sequence[Responsive]] = None
    themes: typing.Optional[typing.Sequence[Theme]] = None
    extra: JsonDict = field(default_factory=dict)


Options = ParticlesOptions


__all__ = [
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
    "merge_options",
    "Modes",
    "Motion",
    "MotionReduce",
    "Move",
    "Opacity",
    "Options",
    "OptionsModel",
    "OutModes",
    "ParticleNumber",
    "Particles",
    "ParticlesOptions",
    "Position",
    "Push",
    "RangeValue",
    "Remove",
    "Repulse",
    "Responsive",
    "serialize_options",
    "Shape",
    "Size",
    "Theme",
    "Twinkle",
    "TwinkleParticles",
]
