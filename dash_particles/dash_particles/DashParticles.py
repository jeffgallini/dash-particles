# AUTO GENERATED FILE - DO NOT EDIT

from dataclasses import fields as _dataclass_fields
import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)

from .options import ParticlesOptions as _ParticlesOptions
from .options import merge_options as _merge_options


_DEFAULT_OPTIONS = {"fullScreen": {"enable": False, "zIndex": 0}}
_OPTION_FIELDS = tuple(
    (field_info.name, field_info.metadata.get("alias", field_info.name))
    for field_info in _dataclass_fields(_ParticlesOptions)
    if field_info.name != "extra"
)
_OPTION_KWARGS = {"config"}
for _field_name, _field_alias in _OPTION_FIELDS:
    _OPTION_KWARGS.add(_field_name)
    _OPTION_KWARGS.add(_field_alias)


def _resolve_options(options, kwargs, explicit_args):
    if options is not None and "config" in kwargs:
        raise TypeError("DashParticles accepts either `options=` or `config=`, not both.")

    explicit_args = [arg for arg in explicit_args if arg not in _OPTION_KWARGS]
    config = kwargs.pop("config", None)
    override_values = []

    for field_name, field_alias in _OPTION_FIELDS:
        has_field_name = field_name in kwargs
        has_field_alias = field_alias != field_name and field_alias in kwargs

        if has_field_name and has_field_alias:
            raise TypeError(
                f"DashParticles received both `{field_name}=` and `{field_alias}=`; pass only one."
            )

        if has_field_name:
            override_values.append({field_alias: kwargs.pop(field_name)})
        elif has_field_alias:
            override_values.append({field_alias: kwargs.pop(field_alias)})

    resolved_options = _merge_options(_DEFAULT_OPTIONS, options if config is None else config, *override_values)

    if resolved_options is not None and "options" not in explicit_args:
        explicit_args.append("options")

    return resolved_options, explicit_args


class DashParticles(Component):
    """A DashParticles component.
DashParticles renders a tsParticles canvas inside Dash.

The package currently loads the `tsparticles` full runtime bundle plus the
extra plugins needed for click-pop interactions, image shapes, text shapes,
and canvas masks.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    Additional CSS class for the container div.

- height (string; default '400px'):
    Height of the particles container. Can be any valid CSS dimension
    value.

- options (dict; optional):
    tsParticles options for the canvas.  This package currently ships
    with the `tsparticles` full bundle plus the click-pop,
    image-shape, text-shape, and canvas-mask plugins. That covers
    examples such as Among Us and Font Awesome out of the box. More
    exotic plugins can still require additional frontend work.

- particlesLoaded (boolean; optional):
    Boolean flag indicating if particles have been loaded.  This is a
    read-only prop updated by the component.

- width (string; default '100%'):
    Width of the particles container. Can be any valid CSS dimension
    value."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_particles'
    _type = 'DashParticles'

    @_explicitize_args
    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        options: typing.Optional[dict] = None,
        height: typing.Optional[str] = None,
        width: typing.Optional[str] = None,
        className: typing.Optional[str] = None,
        style: typing.Optional[typing.Any] = None,
        particlesLoaded: typing.Optional[bool] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'className', 'height', 'options', 'particlesLoaded', 'style', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'height', 'options', 'particlesLoaded', 'style', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        options, _explicit_args = _resolve_options(options, kwargs, _explicit_args)
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashParticles, self).__init__(**args)
