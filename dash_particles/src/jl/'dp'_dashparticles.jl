# AUTO GENERATED FILE - DO NOT EDIT

export 'dp'_dashparticles

"""
    'dp'_dashparticles(;kwargs...)

A DashParticles component.
DashParticles renders a tsParticles canvas inside Dash.

The component automatically loads the smallest tsParticles runtime tier it
can infer from the provided options, and falls back to the full runtime when
a more specialized plugin is needed.
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `className` (String; optional): Additional CSS class for the container div.
- `height` (String; optional): Height of the particles container. Can be any valid CSS dimension value.
- `options` (Dict; optional): tsParticles options for the canvas.
- `particlesLoaded` (Bool; optional): Boolean flag indicating if particles have been loaded.
This is a read-only prop updated by the component.
- `runtime` (a value equal to: 'auto', 'basic', 'slim', 'full'; optional): tsParticles runtime tier to load. Use "auto" to infer the smallest
runtime from the options, or force "basic", "slim", or "full".
- `style` (Dict; optional): Additional inline styles for the container div.
- `width` (String; optional): Width of the particles container. Can be any valid CSS dimension value.
"""
function 'dp'_dashparticles(; kwargs...)
        available_props = Symbol[:id, :className, :height, :options, :particlesLoaded, :runtime, :style, :width]
        wild_props = Symbol[]
        return Component("'dp'_dashparticles", "DashParticles", "dash_particles", available_props, wild_props; kwargs...)
end

