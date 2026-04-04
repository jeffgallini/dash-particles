"""Helper and demo app for `dash-particles`.

This module is intentionally lightweight:

1. It showcases the package's built-in presets and official-sample-inspired examples.
2. It gives users a fast way to tweak the current background without learning the
   entire tsParticles surface area first.
3. It lets users inspect the live JSON config and export idiomatic `dp.Options(...)`
   code for the current background.

Dependencies are kept minimal on purpose: only Dash, `dash-particles`, and the
Python standard library are used here.
"""

from dataclasses import fields
import hashlib
import json
import pprint
import textwrap

import dash
from dash import Input, Output, State, dcc, html, no_update
import dash_particles as dp


FONT_AWESOME_STYLESHEET = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"
)


def _official_example(
    label,
    config,
    description,
    official_url,
    support="Works with the current full runtime",
    source="Official sample inspired",
):
    return {
        "label": label,
        "config": config,
        "description": description,
        "official_url": official_url,
        "support": support,
        "source": source,
    }


def _built_in_preset(name):
    return {
        "label": dp.presets.PRESET_LABELS[name],
        "config": dp.presets.PRESET_BUILDERS[name](),
        "description": dp.presets.PRESET_DESCRIPTIONS[name],
        "official_url": None,
        "support": "Works with the current full runtime",
        "source": "Built-in preset",
    }


example_catalog = {
    "default": _built_in_preset("default"),
    "bubbles": _built_in_preset("bubbles"),
    "snow": _built_in_preset("snow"),
    "fire": _built_in_preset("fire"),
    "stars": _built_in_preset("stars"),
    "connect": _built_in_preset("connect"),
    "among_us": _official_example(
        dp.presets.PRESET_LABELS["among_us"],
        dp.presets.among_us(),
        dp.presets.PRESET_DESCRIPTIONS["among_us"],
        "https://particles.js.org/samples/index.html#amongUs",
        support="Works with the current full runtime, including emitter support",
    ),
    "multiple_images": _official_example(
        dp.presets.PRESET_LABELS["multiple_images"],
        dp.presets.multiple_images(),
        dp.presets.PRESET_DESCRIPTIONS["multiple_images"],
        "https://particles.js.org/samples/index.html#images",
    ),
    "parallax": _official_example(
        dp.presets.PRESET_LABELS["parallax"],
        dp.presets.parallax(),
        dp.presets.PRESET_DESCRIPTIONS["parallax"],
        "https://particles.js.org/samples/index.html#parallax",
        support="Works with the current full runtime",
    ),
    "fontawesome": _official_example(
        dp.presets.PRESET_LABELS["fontawesome"],
        dp.presets.fontawesome(),
        dp.presets.PRESET_DESCRIPTIONS["fontawesome"],
        "https://particles.js.org/samples/index.html#fontawesome",
        support="Works with the current full runtime, and this demo loads the Font Awesome stylesheet for you",
    ),
    "blurred_particles": _official_example(
        dp.presets.PRESET_LABELS["blurred_particles"],
        dp.presets.blurred_particles(),
        dp.presets.PRESET_DESCRIPTIONS["blurred_particles"],
        "https://codepen.io/matteobruni/pen/qBPxjQY",
        support="Works with the current full runtime, including emitters and theme switching",
        source="CodePen inspired",
    ),
    "hypno_squares": _official_example(
        dp.presets.PRESET_LABELS["hypno_squares"],
        dp.presets.hypno_squares(),
        dp.presets.PRESET_DESCRIPTIONS["hypno_squares"],
        "https://codepen.io/matteobruni/pen/BaGbWdb",
        support="Works with the current full runtime, including size and rotate animations",
        source="CodePen inspired",
    ),
}


particle_presets = {key: metadata["config"] for key, metadata in example_catalog.items()}
particle_configs = {key: metadata["config"].to_dict() for key, metadata in example_catalog.items()}


STRUCTURED_CLASS_BY_PATH = {
    (): dp.Options,
    ("fullScreen",): dp.FullScreen,
    ("motion",): dp.Motion,
    ("motion", "reduce"): dp.MotionReduce,
    ("background",): dp.Background,
    ("background", "color"): dp.Color,
    ("backgroundMask",): dp.BackgroundMask,
    ("backgroundMask", "cover"): dp.BackgroundMaskCover,
    ("particles",): dp.Particles,
    ("particles", "color"): dp.Color,
    ("particles", "number"): dp.ParticleNumber,
    ("particles", "number", "density"): dp.Density,
    ("particles", "size"): dp.Size,
    ("particles", "opacity"): dp.Opacity,
    ("particles", "links"): dp.Links,
    ("particles", "move"): dp.Move,
    ("particles", "move", "outModes"): dp.OutModes,
    ("particles", "shape"): dp.Shape,
    ("particles", "twinkle"): dp.Twinkle,
    ("particles", "twinkle", "particles"): dp.TwinkleParticles,
    ("interactivity",): dp.Interactivity,
    ("interactivity", "events"): dp.Events,
    ("interactivity", "events", "onClick"): dp.Action,
    ("interactivity", "events", "onHover"): dp.Action,
    ("interactivity", "modes"): dp.Modes,
    ("interactivity", "modes", "grab"): dp.Grab,
    ("interactivity", "modes", "grab", "links"): dp.GrabLinks,
    ("interactivity", "modes", "repulse"): dp.Repulse,
    ("interactivity", "modes", "push"): dp.Push,
    ("interactivity", "modes", "remove"): dp.Remove,
    ("interactivity", "modes", "bubble"): dp.Bubble,
    ("manualParticles", "<item>"): dp.ManualParticle,
    ("manualParticles", "<item>", "position"): dp.Position,
    ("manualParticles", "<item>", "options"): dp.Options,
    ("responsive", "<item>"): dp.Responsive,
    ("responsive", "<item>", "options"): dp.Options,
    ("themes", "<item>"): dp.Theme,
    ("themes", "<item>", "options"): dp.Options,
}

STRUCTURED_LIST_ITEM_CLASS_BY_PATH = {
    ("manualParticles",): dp.ManualParticle,
    ("responsive",): dp.Responsive,
    ("themes",): dp.Theme,
}

COLOR_SUGGESTIONS = [
    "#020617",
    "#0f172a",
    "#111827",
    "#ffffff",
    "#38bdf8",
    "#22c55e",
    "#f97316",
    "#ef4444",
    "#facc15",
    "#c4b5fd",
]

HOVER_MODE_OPTIONS = [
    {"label": "None", "value": "none"},
    {"label": "Grab", "value": "grab"},
    {"label": "Bubble", "value": "bubble"},
    {"label": "Repulse", "value": "repulse"},
    {"label": "Connect", "value": "connect"},
]

CLICK_MODE_OPTIONS = [
    {"label": "None", "value": "none"},
    {"label": "Attract", "value": "attract"},
    {"label": "Bubble", "value": "bubble"},
    {"label": "Pause", "value": "pause"},
    {"label": "Pop", "value": "pop"},
    {"label": "Push", "value": "push"},
    {"label": "Remove", "value": "remove"},
    {"label": "Repulse", "value": "repulse"},
    {"label": "Trail", "value": "trail"},
    {"label": "Emitter", "value": "emitter"},
    {"label": "Absorber", "value": "absorber"},
]

INTERACTIVITY_MODE_DEFAULTS = {
    "attract": {
        "distance": 200,
        "duration": 0.4,
        "easing": "ease-out-quad",
        "factor": 1,
        "maxSpeed": 50,
        "speed": 1,
    },
    "bubble": {
        "distance": 200,
        "duration": 2,
        "opacity": 1,
        "size": 12,
    },
    "connect": {
        "distance": 80,
        "links": {"opacity": 0.5},
        "radius": 60,
    },
    "grab": {
        "distance": 200,
        "links": {"opacity": 1},
    },
    "pause": {},
    "push": {
        "quantity": 4,
    },
    "remove": {
        "quantity": 2,
    },
    "repulse": {
        "distance": 200,
        "duration": 0.4,
    },
    "trail": {
        "delay": 1,
        "pauseOnStop": False,
        "quantity": 1,
    },
}


CONTROL_LABEL_STYLE = {
    "display": "block",
    "fontSize": "14px",
    "fontWeight": "700",
    "color": "#0f172a",
    "marginBottom": "6px",
}

CONTROL_HINT_STYLE = {
    "fontSize": "13px",
    "lineHeight": "1.5",
    "color": "#475569",
    "margin": "0 0 10px 0",
}

CONTROL_BLOCK_STYLE = {"marginBottom": "18px"}


def _control_block(label, hint, control):
    return html.Div(
        [
            html.Label(label, style=CONTROL_LABEL_STYLE),
            html.P(hint, style=CONTROL_HINT_STYLE),
            control,
        ],
        style=CONTROL_BLOCK_STYLE,
    )


def _structured_class_name(path, cls):
    if path == ():
        return "Options"
    return cls.__name__


def _format_literal(value):
    try:
        return pprint.pformat(value, indent=4, width=100, sort_dicts=False)
    except TypeError:
        return pprint.pformat(value, indent=4, width=100)


def _get_field_name(cls, key):
    for field_info in fields(cls):
        if field_info.name == "extra":
            continue
        if field_info.name == key or field_info.metadata.get("alias") == key:
            return field_info.name
    return None


def _format_assignment(name, value_str, indent):
    indent_str = " " * indent
    if "\n" not in value_str or value_str.lstrip().startswith("dp."):
        return f"{indent_str}{name}={value_str},"

    return "\n".join(
        [
            f"{indent_str}{name}=(",
            textwrap.indent(value_str, " " * (indent + 4)),
            f"{indent_str}),",
        ]
    )


def _format_range_value(value, indent):
    lines = ["dp.RangeValue("]
    for key in ("min", "max"):
        if key in value:
            lines.append(f"{' ' * (indent + 4)}{key}={_format_literal(value[key])},")

    extra = {key: item for key, item in value.items() if key not in {"min", "max"}}
    if extra:
        lines.append(_format_assignment("extra", _format_literal(extra), indent + 4))

    lines.append(f"{' ' * indent})")
    return "\n".join(lines)


def _format_structured_value(value, path, indent):
    cls = STRUCTURED_CLASS_BY_PATH.get(path)
    if cls is None:
        return _format_literal(value)

    lines = [f"dp.{_structured_class_name(path, cls)}("]
    extra = {}

    for key, item in value.items():
        field_name = _get_field_name(cls, key)
        if field_name is None:
            extra[key] = item
            continue

        lines.append(
            _format_assignment(
                field_name,
                _format_python_value(item, path + (key,), indent + 4),
                indent + 4,
            )
        )

    if extra:
        lines.append(_format_assignment("extra", _format_literal(extra), indent + 4))

    lines.append(f"{' ' * indent})")
    return "\n".join(lines)


def _format_python_value(value, path=(), indent=0):
    if isinstance(value, list):
        item_cls = STRUCTURED_LIST_ITEM_CLASS_BY_PATH.get(path)
        if item_cls is not None:
            lines = ["["]
            for item in value:
                if isinstance(item, dict):
                    rendered_item = _format_structured_value(item, path + ("<item>",), indent + 4)
                else:
                    rendered_item = _format_literal(item)

                lines.append(textwrap.indent(rendered_item, " " * (indent + 4)) + ",")
            lines.append(f"{' ' * indent}]")
            return "\n".join(lines)

        return _format_literal(value)

    if isinstance(value, dict):
        if value and set(value).issubset({"min", "max"}):
            return _format_range_value(value, indent)
        return _format_structured_value(value, path, indent)

    return _format_literal(value)


def format_python_config(config):
    """Render a serialized config dict back into structured `dp.*` code."""
    return _format_python_value(config, (), 0)


def _deepcopy_config(config):
    return json.loads(json.dumps(config))


def _config_fingerprint(config):
    serialized = json.dumps(config, sort_keys=True)
    return hashlib.md5(serialized.encode("utf-8")).hexdigest()[:12]


def _get_nested(config, path, default=None):
    value = config
    try:
        for key in path:
            value = value[key]
    except (KeyError, TypeError):
        return default
    return value


def _set_nested(config, path, value):
    section = config
    for key in path[:-1]:
        current = section.get(key)
        if not isinstance(current, dict):
            current = {}
            section[key] = current
        section = current
    section[path[-1]] = value


def _deep_merge_dicts(base, updates):
    merged = _deepcopy_config(base)

    for key, value in updates.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, dict):
            merged[key] = _deep_merge_dicts(current, value)
        else:
            merged[key] = value

    return merged


def _ensure_mode_defaults(config, mode_name):
    if mode_name == "none":
        return

    mode_defaults = INTERACTIVITY_MODE_DEFAULTS.get(mode_name)
    if mode_defaults is None:
        return

    modes = config.setdefault("interactivity", {}).setdefault("modes", {})
    existing = modes.get(mode_name)

    if isinstance(existing, dict):
        modes[mode_name] = _deep_merge_dicts(mode_defaults, existing)
    else:
        modes[mode_name] = _deepcopy_config(mode_defaults)


def _coerce_color(value, fallback):
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def _normalize_color_value(value, fallback):
    if isinstance(value, dict):
        nested = value.get("value")
        if isinstance(nested, str) and nested.strip():
            return nested.strip()
        if isinstance(nested, list):
            for item in nested:
                if isinstance(item, str) and item.strip():
                    return item.strip()
        return fallback

    if isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.strip():
                return item.strip()
        return fallback

    if isinstance(value, str) and value.strip():
        return value.strip()

    return fallback


def _coerce_numeric(value, fallback):
    if value is None:
        return fallback
    return value


def _scalar_or_default(value, default):
    if isinstance(value, dict):
        return value.get("max", value.get("min", default))
    if isinstance(value, list):
        return value[0] if value else default
    return value if value is not None else default


def extract_editor_state(config):
    """Extract the simple editor's control values from a serialized config."""
    background_color = _get_nested(config, ["background", "color", "value"], "#0f172a")
    particle_color = _get_nested(config, ["particles", "color", "value"], "#38bdf8")
    link_color = _get_nested(config, ["particles", "links", "color"], particle_color)
    background_color = _normalize_color_value(background_color, "#0f172a")
    particle_color = _normalize_color_value(particle_color, "#38bdf8")
    link_color = _normalize_color_value(link_color, particle_color)

    return {
        "background_color": background_color,
        "particle_color": particle_color,
        "link_color": link_color,
        "particle_count": _coerce_numeric(
            _get_nested(config, ["particles", "number", "value"], 80),
            80,
        ),
        "particle_size": _scalar_or_default(_get_nested(config, ["particles", "size", "value"], 3), 3),
        "particle_opacity": _scalar_or_default(_get_nested(config, ["particles", "opacity", "value"], 0.6), 0.6),
        "move_speed": _coerce_numeric(_get_nested(config, ["particles", "move", "speed"], 1.5), 1.5),
        "links_enabled": bool(_get_nested(config, ["particles", "links", "enable"], False)),
        "hover_mode": _scalar_or_default(_get_nested(config, ["interactivity", "events", "onHover", "mode"], "none"), "none"),
        "click_mode": _scalar_or_default(_get_nested(config, ["interactivity", "events", "onClick", "mode"], "none"), "none"),
    }


def apply_editor_overrides(
    config,
    background_color,
    particle_color,
    link_color,
    particle_count,
    particle_size,
    particle_opacity,
    move_speed,
    links_enabled,
    hover_mode,
    click_mode,
):
    """Apply the simple editor's controls to a serialized config dict."""
    updated = _deepcopy_config(config)

    background_color = _coerce_color(background_color, "#0f172a")
    particle_color = _coerce_color(particle_color, "#38bdf8")
    link_color = _coerce_color(link_color, particle_color)

    _set_nested(updated, ["background", "color", "value"], background_color)
    _set_nested(updated, ["particles", "color", "value"], particle_color)
    _set_nested(updated, ["particles", "number", "value"], particle_count)
    _set_nested(updated, ["particles", "size", "value"], particle_size)
    _set_nested(updated, ["particles", "opacity", "value"], particle_opacity)
    _set_nested(updated, ["particles", "move", "enable"], True)
    _set_nested(updated, ["particles", "move", "speed"], move_speed)
    _set_nested(updated, ["particles", "links", "enable"], links_enabled)
    _set_nested(updated, ["particles", "links", "color"], link_color)

    _set_nested(updated, ["interactivity", "events", "onHover", "enable"], hover_mode != "none")
    _set_nested(updated, ["interactivity", "events", "onHover", "mode"], hover_mode)
    _set_nested(updated, ["interactivity", "events", "onClick", "enable"], click_mode != "none")
    _set_nested(updated, ["interactivity", "events", "onClick", "mode"], click_mode)
    _ensure_mode_defaults(updated, hover_mode)
    _ensure_mode_defaults(updated, click_mode)

    return updated


def export_config_code(n_clicks, current_config_data):
    if n_clicks <= 0 or not current_config_data:
        return no_update, {"display": "none"}

    config_py_str = format_python_config(current_config_data)
    exported_code = f"""import dash_particles as dp

particles = dp.DashParticles(
    id="particles",
    config=(
{textwrap.indent(config_py_str, " " * 8)}
    ),
    height="100%",
    width="100%",
)
"""
    return exported_code, {"display": "block"}


def _build_example_summary(example_name):
    metadata = example_catalog[example_name]
    support_color = "#166534"
    if "require" in metadata["support"].lower() or "may" in metadata["support"].lower():
        support_color = "#92400e"

    children = [
        html.Div(
            [
                html.Span(
                    metadata["source"],
                    style={
                        "display": "inline-block",
                        "padding": "4px 10px",
                        "borderRadius": "999px",
                        "backgroundColor": "#e2e8f0",
                        "fontSize": "12px",
                        "fontWeight": "600",
                    },
                ),
                html.Span(
                    metadata["support"],
                    style={
                        "display": "inline-block",
                        "marginLeft": "8px",
                        "padding": "4px 10px",
                        "borderRadius": "999px",
                        "backgroundColor": "#fef3c7" if support_color != "#166534" else "#dcfce7",
                        "color": support_color,
                        "fontSize": "12px",
                        "fontWeight": "600",
                    },
                ),
            ],
            style={"marginBottom": "12px"},
        ),
        html.H2(metadata["label"], style={"margin": "0 0 8px 0"}),
        html.P(metadata["description"], style={"margin": "0 0 10px 0", "lineHeight": "1.6"}),
    ]

    if metadata["official_url"]:
        children.append(
            html.A(
                "Open the matching official sample",
                href=metadata["official_url"],
                target="_blank",
                style={"color": "#0f172a", "fontWeight": "600"},
            )
        )

    return children


def _load_example_payload(example_name):
    config = _deepcopy_config(particle_configs[example_name])
    editor_state = extract_editor_state(config)
    return (
        config,
        json.dumps(config, indent=2),
        _build_example_summary(example_name),
        editor_state["background_color"],
        editor_state["particle_color"],
        editor_state["link_color"],
        editor_state["particle_count"],
        editor_state["particle_size"],
        editor_state["particle_opacity"],
        editor_state["move_speed"],
        editor_state["links_enabled"],
        editor_state["hover_mode"],
        editor_state["click_mode"],
        "",
    )


def _build_preview_component(config):
    return dp.DashParticles(
        id=f"particles-preview-{_config_fingerprint(config)}",
        config=config,
        full_screen=dp.FullScreen(enable=False, z_index=0),
        height="100%",
        width="100%",
        style={"position": "absolute", "inset": 0, "zIndex": 0},
    )


app = dash.Dash(__name__, external_stylesheets=[FONT_AWESOME_STYLESHEET])

app.layout = html.Div(
    [
        dcc.Store(id="current-config", data=_deepcopy_config(particle_configs["default"])),
        html.Div(
            [
                html.H1("Dash Particles Helper"),
                html.P(
                    "Browse every packaged example, tweak the current background, inspect the JSON, and export structured Python code.",
                    style={"margin": "8px 0 0 0", "maxWidth": "780px", "lineHeight": "1.6"},
                ),
                html.P(
                    "The Font Awesome example works in this helper because the app preloads the Font Awesome stylesheet.",
                    style={"margin": "8px 0 0 0", "maxWidth": "780px", "lineHeight": "1.6", "color": "#475569"},
                ),
            ],
            style={"marginBottom": "24px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            id="particles-preview-slot",
                            children=_build_preview_component(_deepcopy_config(particle_configs["default"])),
                            style={"position": "absolute", "inset": 0, "zIndex": 0},
                        ),
                        html.Div(
                            id="example-summary",
                            style={
                                "position": "relative",
                                "zIndex": 1,
                                "maxWidth": "560px",
                                "margin": "24px",
                                "padding": "18px 20px",
                                "backgroundColor": "rgba(255,255,255,0.84)",
                                "borderRadius": "16px",
                                "boxShadow": "0 18px 40px rgba(15, 23, 42, 0.18)",
                            },
                        ),
                    ],
                    style={
                        "position": "relative",
                        "height": "760px",
                        "minHeight": "760px",
                        "borderRadius": "20px",
                        "overflow": "hidden",
                        "backgroundColor": "#0f172a",
                        "boxShadow": "0 30px 60px rgba(15, 23, 42, 0.2)",
                    },
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Example"),
                                dcc.Dropdown(
                                    id="example-dropdown",
                                    options=[
                                        {"label": metadata["label"], "value": key}
                                        for key, metadata in example_catalog.items()
                                    ],
                                    value="default",
                                    clearable=False,
                                ),
                                html.Button(
                                    "Reset To Example",
                                    id="reset-example",
                                    n_clicks=0,
                                    style={
                                        "marginTop": "12px",
                                        "padding": "10px 14px",
                                        "border": "none",
                                        "borderRadius": "10px",
                                        "backgroundColor": "#0f172a",
                                        "color": "white",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                            style={"marginBottom": "24px"},
                        ),
                        html.Div(
                            [
                                html.H3("Quick Tweaks"),
                                html.Label("Background Color"),
                                dcc.Input(
                                    id="background-color",
                                    type="text",
                                    debounce=True,
                                    placeholder=", ".join(COLOR_SUGGESTIONS[:3]),
                                    style={"width": "100%"},
                                ),
                                html.Label("Particle Color", style={"marginTop": "12px"}),
                                dcc.Input(
                                    id="particle-color",
                                    type="text",
                                    debounce=True,
                                    placeholder=", ".join(COLOR_SUGGESTIONS[3:6]),
                                    style={"width": "100%"},
                                ),
                                html.Label("Link Color", style={"marginTop": "12px"}),
                                dcc.Input(
                                    id="link-color",
                                    type="text",
                                    debounce=True,
                                    placeholder=", ".join(COLOR_SUGGESTIONS[6:9]),
                                    style={"width": "100%"},
                                ),
                                html.Label("Particle Count", style={"marginTop": "14px"}),
                                dcc.Slider(id="particle-count", min=0, max=240, step=4, marks={0: "0", 80: "80", 160: "160", 240: "240"}),
                                html.Label("Particle Size", style={"marginTop": "14px"}),
                                dcc.Slider(id="particle-size", min=1, max=40, step=1, marks={1: "1", 20: "20", 40: "40"}),
                                html.Label("Opacity", style={"marginTop": "14px"}),
                                dcc.Slider(id="particle-opacity", min=0.1, max=1, step=0.05, marks={0.1: "0.1", 0.5: "0.5", 1: "1.0"}),
                                html.Label("Speed", style={"marginTop": "14px"}),
                                dcc.Slider(id="move-speed", min=0, max=8, step=0.1, marks={0: "0", 2: "2", 4: "4", 8: "8"}),
                                html.Label("Links", style={"marginTop": "14px"}),
                                dcc.RadioItems(
                                    id="links-enabled",
                                    options=[
                                        {"label": "Enabled", "value": True},
                                        {"label": "Disabled", "value": False},
                                    ],
                                    inline=True,
                                ),
                                html.Label("Hover Mode", style={"marginTop": "14px"}),
                                dcc.Dropdown(id="hover-mode", options=HOVER_MODE_OPTIONS, clearable=False),
                                html.Label("Click Mode", style={"marginTop": "14px"}),
                                dcc.Dropdown(id="click-mode", options=CLICK_MODE_OPTIONS, clearable=False),
                                html.Button(
                                    "Apply Quick Tweaks",
                                    id="apply-controls",
                                    n_clicks=0,
                                    style={
                                        "marginTop": "16px",
                                        "padding": "10px 14px",
                                        "border": "none",
                                        "borderRadius": "10px",
                                        "backgroundColor": "#2563eb",
                                        "color": "white",
                                        "cursor": "pointer",
                                    },
                                ),
                            ],
                            style={"marginBottom": "28px"},
                        ),
                        html.Div(
                            [
                                html.H3("Raw JSON Config"),
                                html.P(
                                    "Use this when the quick editor is not enough. Paste a serialized config dict, then apply it.",
                                    style={"fontSize": "14px", "lineHeight": "1.6"},
                                ),
                                dcc.Textarea(
                                    id="config-json",
                                    style={"width": "100%", "height": "260px", "fontFamily": "monospace"},
                                ),
                                html.Div(
                                    [
                                        html.Button(
                                            "Apply JSON",
                                            id="apply-json",
                                            n_clicks=0,
                                            style={
                                                "padding": "10px 14px",
                                                "border": "none",
                                                "borderRadius": "10px",
                                                "backgroundColor": "#16a34a",
                                                "color": "white",
                                                "cursor": "pointer",
                                                "marginRight": "10px",
                                            },
                                        ),
                                        html.Button(
                                            "Export Component Code",
                                            id="export-config-button",
                                            n_clicks=0,
                                            style={
                                                "padding": "10px 14px",
                                                "border": "none",
                                                "borderRadius": "10px",
                                                "backgroundColor": "#9333ea",
                                                "color": "white",
                                                "cursor": "pointer",
                                            },
                                        ),
                                    ],
                                    style={"marginTop": "12px"},
                                ),
                                html.Div(id="json-status", style={"marginTop": "12px", "fontSize": "14px"}),
                            ],
                            style={"marginBottom": "28px"},
                        ),
                        html.Div(
                            [
                                html.H3("Structured Python Preview"),
                                dcc.Textarea(
                                    id="python-config-output",
                                    readOnly=True,
                                    style={"width": "100%", "height": "260px", "fontFamily": "monospace"},
                                ),
                            ],
                            style={"marginBottom": "28px"},
                        ),
                        html.Div(
                            [
                                html.H3("Exported Component Snippet"),
                                html.Div(
                                    id="export-output-container",
                                    style={"display": "none"},
                                    children=[
                                        dcc.Textarea(
                                            id="export-code-output",
                                            readOnly=True,
                                            style={"width": "100%", "height": "220px", "fontFamily": "monospace"},
                                        )
                                    ],
                                ),
                            ]
                        ),
                    ],
                    style={
                        "padding": "24px",
                        "backgroundColor": "#f8fafc",
                        "borderRadius": "20px",
                        "boxShadow": "0 18px 40px rgba(15, 23, 42, 0.08)",
                        "position": "relative",
                        "zIndex": 3,
                    },
                ),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "minmax(0, 1.4fr) minmax(320px, 520px)",
                "gap": "24px",
                "alignItems": "start",
                "position": "relative",
                "isolation": "isolate",
            },
        ),
    ],
    style={"padding": "24px", "minHeight": "100vh", "backgroundColor": "#e2e8f0"},
)


@app.callback(
    Output("current-config", "data"),
    Output("config-json", "value"),
    Output("example-summary", "children"),
    Output("background-color", "value"),
    Output("particle-color", "value"),
    Output("link-color", "value"),
    Output("particle-count", "value"),
    Output("particle-size", "value"),
    Output("particle-opacity", "value"),
    Output("move-speed", "value"),
    Output("links-enabled", "value"),
    Output("hover-mode", "value"),
    Output("click-mode", "value"),
    Output("json-status", "children"),
    Input("example-dropdown", "value"),
    Input("reset-example", "n_clicks"),
)
def load_example(example_name, _reset_clicks):
    return _load_example_payload(example_name)


@app.callback(
    Output("particles-preview-slot", "children"),
    Output("python-config-output", "value"),
    Input("current-config", "data"),
)
def render_preview(current_config):
    return (
        _build_preview_component(current_config),
        format_python_config(current_config),
    )


@app.callback(
    Output("current-config", "data", allow_duplicate=True),
    Output("config-json", "value", allow_duplicate=True),
    Output("json-status", "children", allow_duplicate=True),
    Input("apply-controls", "n_clicks"),
    State("current-config", "data"),
    State("background-color", "value"),
    State("particle-color", "value"),
    State("link-color", "value"),
    State("particle-count", "value"),
    State("particle-size", "value"),
    State("particle-opacity", "value"),
    State("move-speed", "value"),
    State("links-enabled", "value"),
    State("hover-mode", "value"),
    State("click-mode", "value"),
    prevent_initial_call=True,
)
def apply_controls(
    n_clicks,
    current_config,
    background_color,
    particle_color,
    link_color,
    particle_count,
    particle_size,
    particle_opacity,
    move_speed,
    links_enabled,
    hover_mode,
    click_mode,
):
    if n_clicks <= 0:
        return no_update, no_update, no_update

    updated = apply_editor_overrides(
        current_config,
        background_color,
        particle_color,
        link_color,
        particle_count,
        particle_size,
        particle_opacity,
        move_speed,
        links_enabled,
        hover_mode,
        click_mode,
    )
    return updated, json.dumps(updated, indent=2), "Quick tweaks applied."


@app.callback(
    Output("current-config", "data", allow_duplicate=True),
    Output("json-status", "children", allow_duplicate=True),
    Input("apply-json", "n_clicks"),
    State("config-json", "value"),
    prevent_initial_call=True,
)
def apply_json_editor(n_clicks, config_text):
    if n_clicks <= 0:
        return no_update, no_update

    try:
        parsed = json.loads(config_text)
    except json.JSONDecodeError as error:
        return no_update, f"JSON error: {error.msg} (line {error.lineno}, column {error.colno})"

    if not isinstance(parsed, dict):
        return no_update, "The JSON editor expects a single config object at the top level."

    return parsed, "JSON config applied."


@app.callback(
    Output("background-color", "value", allow_duplicate=True),
    Output("particle-color", "value", allow_duplicate=True),
    Output("link-color", "value", allow_duplicate=True),
    Output("particle-count", "value", allow_duplicate=True),
    Output("particle-size", "value", allow_duplicate=True),
    Output("particle-opacity", "value", allow_duplicate=True),
    Output("move-speed", "value", allow_duplicate=True),
    Output("links-enabled", "value", allow_duplicate=True),
    Output("hover-mode", "value", allow_duplicate=True),
    Output("click-mode", "value", allow_duplicate=True),
    Input("current-config", "data"),
    prevent_initial_call=True,
)
def sync_controls_from_config(current_config):
    state = extract_editor_state(current_config)
    return (
        state["background_color"],
        state["particle_color"],
        state["link_color"],
        state["particle_count"],
        state["particle_size"],
        state["particle_opacity"],
        state["move_speed"],
        state["links_enabled"],
        state["hover_mode"],
        state["click_mode"],
    )


@app.callback(
    Output("export-code-output", "value"),
    Output("export-output-container", "style"),
    Input("export-config-button", "n_clicks"),
    State("current-config", "data"),
    prevent_initial_call=True,
)
def handle_export_config(n_clicks, current_config_data):
    return export_config_code(n_clicks, current_config_data)


if __name__ == "__main__":
    app.run(debug=True)
