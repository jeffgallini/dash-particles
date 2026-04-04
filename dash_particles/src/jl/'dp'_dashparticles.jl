# AUTO GENERATED FILE - DO NOT EDIT

export 'dp'_dashparticles

"""
    'dp'_dashparticles(;kwargs...)

A DashParticles component.
DashParticles renders a tsParticles canvas inside Dash.

The package currently loads the `tsparticles` full runtime bundle plus the
extra plugins needed for click-pop interactions, image shapes, text shapes,
and canvas masks.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `className` (String; optional): Additional CSS class for the container div.
- `height` (String; optional): Height of the particles container. Can be any valid CSS dimension value.
- `options` (Dict; optional): tsParticles options for the canvas.

This package currently ships with the `tsparticles` full bundle plus the
click-pop, image-shape, text-shape, and canvas-mask plugins. That covers
examples such as Among Us and Font Awesome out of the box. More exotic
plugins can still require additional frontend work.
- `particlesLoaded` (Bool; optional): Boolean flag indicating if particles have been loaded.
This is a read-only prop updated by the component.
- `style` (Dict; optional): Additional inline styles for the container div.
- `width` (String; optional): Width of the particles container. Can be any valid CSS dimension value.
"""
function 'dp'_dashparticles(; kwargs...)
        available_props = Symbol[:id, :className, :height, :options, :particlesLoaded, :style, :width]
        wild_props = Symbol[]
        return Component("'dp'_dashparticles", "DashParticles", "dash_particles", available_props, wild_props; kwargs...)
end

