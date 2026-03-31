import dash
from dash import html, dcc, callback, Input, Output, State, ALL
import dash_particles
import json
import pprint  # Added for exporting config

app = dash.Dash(__name__)

# Define 6 different particle configurations
particle_configs = {
    "default": {
        "background": {
            "color": {
                "value": "#f0f0f0"
            }
        },
        "particles": {
            "color": {
                "value": "#000000"
            },
            "number": {
                "value": 50
            },
            "size": {
                "value": 5
            },
            "links": {
                "enable": True,
                "color": "#000000",
                "opacity": 0.8,
                "width": 2
            }
        },
        "interactivity": {
            "events": {
                "onClick": {
                    "enable": True,
                    "mode": "push"
                },
                "onHover": {
                    "enable": True,
                    "mode": "repulse"
                }
            }
        }
    },
    "bubbles": {
        "background": {
            "color": {
                "value": "#0d47a1"
            }
        },
        "particles": {
            "color": {
                "value": "#ffffff"
            },
            "number": {
                "value": 100
            },
            "size": {
                "value": 10,
                "random": True
            },
            "opacity": {
                "value": 0.7,
                "random": True
            },
            "move": {
                "enable": True,
                "speed": 2,
                "direction": "none",
                "random": True
            },
            "links": {
                "enable": False
            }
        }
    },
    "snow": {
        "background": {
            "color": {
                "value": "#2c3e50"
            }
        },
        "particles": {
            "color": {
                "value": "#ffffff"
            },
            "number": {
                "value": 200
            },
            "size": {
                "value": 3,
                "random": True
            },
            "opacity": {
                "value": 0.8
            },
            "move": {
                "enable": True,
                "speed": 1,
                "direction": "bottom",
                "straight": False
            },
            "links": {
                "enable": False
            }
        }
    },
    "fire": {
        "background": {
            "color": {
                "value": "#000000"
            }
        },
        "particles": {
            "color": {
                "value": ["#ff5722", "#ff9800", "#ffeb3b"]
            },
            "number": {
                "value": 80
            },
            "shape": {
                "type": "circle"
            },
            "size": {
                "value": 8,
                "random": True
            },
            "opacity": {
                "value": 0.7,
                "random": True
            },
            "move": {
                "enable": True,
                "speed": 5,
                "direction": "top",
                "random": True,
                "out_mode": "out"
            },
            "links": {
                "enable": False
            }
        }
    },
    "stars": {
        "background": {
            "color": {
                "value": "#0a0a29"
            }
        },
        "particles": {
            "color": {
                "value": "#ffffff"
            },
            "number": {
                "value": 150
            },
            "size": {
                "value": 2,
                "random": True
            },
            "opacity": {
                "value": 1,
                "random": True
            },
            "move": {
                "enable": True,
                "speed": 0.2,
                "direction": "none",
                "random": True
            },
            "links": {
                "enable": False
            },
            "twinkle": {
                "particles": {
                    "enable": True,
                    "frequency": 0.05,
                    "opacity": 1
                }
            }
        }
    },
    "connect": {
        "background": {
            "color": {
                "value": "#ffffff"
            }
        },
        "particles": {
            "color": {
                "value": "#3498db"
            },
            "number": {
                "value": 120
            },
            "size": {
                "value": 3
            },
            "links": {
                "enable": True,
                "color": "#3498db",
                "opacity": 0.4,
                "width": 1,
                "distance": 150
            },
            "move": {
                "enable": True,
                "speed": 2
            }
        },
        "interactivity": {
            "events": {
                "onHover": {
                    "enable": True,
                    "mode": "grab"
                },
                "onClick": {
                    "enable": True,
                    "mode": "push"
                }
            },
            "modes": {
                "grab": {
                    "distance": 200,
                    "links": {
                        "opacity": 1
                    }
                }
            }
        }
    }
}

# Color options for dropdowns
color_options = [
    {"label": "Black", "value": "#000000"},
    {"label": "White", "value": "#ffffff"},
    {"label": "Red", "value": "#ff0000"},
    {"label": "Green", "value": "#00ff00"},
    {"label": "Blue", "value": "#0000ff"},
    {"label": "Yellow", "value": "#ffff00"},
    {"label": "Cyan", "value": "#00ffff"},
    {"label": "Magenta", "value": "#ff00ff"},
    {"label": "Orange", "value": "#ff9800"},
    {"label": "Purple", "value": "#9c27b0"},
    {"label": "Teal", "value": "#009688"},
    {"label": "Pink", "value": "#e91e63"},
    {"label": "Deep Blue", "value": "#0d47a1"},
    {"label": "Dark Gray", "value": "#333333"},
    {"label": "Light Gray", "value": "#cccccc"},
]

app.layout = html.Div([
    html.H1("Dash Particles Demo",
            style={"textAlign": "center", "marginBottom": "20px", "position": "relative", "zIndex": 10}),

    # Main content container with particles and controls
    html.Div([
        # Left side - Particles container
        html.Div([
            # Particles container - positioned absolutely to be behind everything
            html.Div(id="particles-container", style={
                "position": "absolute",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "zIndex": 1  # Low z-index to be behind other elements
            }),

            # Dropdown overlay
            html.Div([
                dcc.Dropdown(
                    id="particle-preset-dropdown",
                    options=[
                        {"label": "Default Network", "value": "default"},
                        {"label": "Bubbles", "value": "bubbles"},
                        {"label": "Snow", "value": "snow"},
                        {"label": "Fire", "value": "fire"},
                        {"label": "Stars", "value": "stars"},
                        {"label": "Connected Network", "value": "connect"}
                    ],
                    value="default",
                    style={
                        "width": "300px",
                        "backgroundColor": "rgba(255, 255, 255, 0.8)",
                    },
                    placeholder="Select a preset"
                ),
            ], style={
                "position": "relative",
                "top": "20px",
                "left": "20px",
                "zIndex": 10,  # Higher z-index to appear above particles
            }),

            # Description overlay
            html.Div(
                id="description",
                style={
                    "position": "relative",
                    "bottom": "-500px",  # Position at the bottom
                    "left": "20px",
                    "backgroundColor": "rgba(255, 255, 255, 0.8)",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "zIndex": 10,  # Higher z-index to appear above particles
                    "maxWidth": "60%"
                }
            )
        ], style={
            "position": "relative",
            "height": "600px",
            "width": "65%",
            "backgroundColor": "transparent",  # Make transparent to see particles
            "borderRadius": "10px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            "marginRight": "20px",
            "overflow": "hidden"  # Ensure particles don't overflow
        }),

        # Right side - Controls
        html.Div([
            html.H3("Customize Particles", style={"marginTop": "0", "marginBottom": "20px"}),

            # Background settings
            html.Div([
                html.H4("Background", style={"marginBottom": "10px"}),
                html.Label("Background Color"),
                dcc.Dropdown(
                    id={"type": "particle-control", "param": "background.color.value"},
                    options=color_options,
                    value="#f0f0f0",
                    clearable=False
                ),
            ], style={"marginBottom": "20px"}),

            # Particle settings
            html.Div([
                html.H4("Particles", style={"marginBottom": "10px"}),

                html.Label("Particle Color"),
                dcc.Dropdown(
                    id={"type": "particle-control", "param": "particles.color.value"},
                    options=color_options,
                    value="#000000",
                    clearable=False
                ),

                html.Label("Number of Particles", style={"marginTop": "10px"}),
                dcc.Slider(
                    id={"type": "particle-control", "param": "particles.number.value"},
                    min=10,
                    max=300,
                    step=10,
                    value=50,
                    marks={10: "10", 150: "150", 300: "300"},
                ),

                html.Label("Particle Size", style={"marginTop": "10px"}),
                dcc.Slider(
                    id={"type": "particle-control", "param": "particles.size.value"},
                    min=1,
                    max=20,
                    step=1,
                    value=5,
                    marks={1: "1", 10: "10", 20: "20"},
                ),

                html.Label("Opacity", style={"marginTop": "10px"}),
                dcc.Slider(
                    id={"type": "particle-control", "param": "particles.opacity.value"},
                    min=0.1,
                    max=1,
                    step=0.1,
                    value=0.8,
                    marks={0.1: "0.1", 0.5: "0.5", 1: "1"},
                ),
            ], style={"marginBottom": "20px"}),

            # Links settings
            html.Div([
                html.H4("Links", style={"marginBottom": "10px"}),

                html.Label("Enable Links"),
                dcc.RadioItems(
                    id={"type": "particle-control", "param": "particles.links.enable"},
                    options=[
                        {"label": "Enabled", "value": True},
                        {"label": "Disabled", "value": False}
                    ],
                    value=True,
                    inline=True
                ),

                html.Div(id="links-controls", children=[
                    html.Label("Link Color", style={"marginTop": "10px"}),
                    dcc.Dropdown(
                        id={"type": "particle-control", "param": "particles.links.color"},
                        options=color_options,
                        value="#000000",
                        clearable=False
                    ),

                    html.Label("Link Width", style={"marginTop": "10px"}),
                    dcc.Slider(
                        id={"type": "particle-control", "param": "particles.links.width"},
                        min=1,
                        max=5,
                        step=0.5,
                        value=2,
                        marks={1: "1", 3: "3", 5: "5"},
                    ),

                    html.Label("Link Opacity", style={"marginTop": "10px"}),
                    dcc.Slider(
                        id={"type": "particle-control", "param": "particles.links.opacity"},
                        min=0.1,
                        max=1,
                        step=0.1,
                        value=0.8,
                        marks={0.1: "0.1", 0.5: "0.5", 1: "1"},
                    ),
                ]),
            ], style={"marginBottom": "20px"}),

            # Movement settings
            html.Div([
                html.H4("Movement", style={"marginBottom": "10px"}),

                html.Label("Enable Movement"),
                dcc.RadioItems(
                    id={"type": "particle-control", "param": "particles.move.enable"},
                    options=[
                        {"label": "Enabled", "value": True},
                        {"label": "Disabled", "value": False}
                    ],
                    value=True,
                    inline=True
                ),

                html.Div(id="movement-controls", children=[
                    html.Label("Speed", style={"marginTop": "10px"}),
                    dcc.Slider(
                        id={"type": "particle-control", "param": "particles.move.speed"},
                        min=1,
                        max=10,
                        step=1,
                        value=3,
                        marks={1: "1", 5: "5", 10: "10"},
                    ),

                    html.Label("Direction", style={"marginTop": "10px"}),
                    dcc.Dropdown(
                        id={"type": "particle-control", "param": "particles.move.direction"},
                        options=[
                            {"label": "None", "value": "none"},
                            {"label": "Top", "value": "top"},
                            {"label": "Bottom", "value": "bottom"},
                            {"label": "Left", "value": "left"},
                            {"label": "Right", "value": "right"},
                        ],
                        value="none",
                        clearable=False
                    ),
                ]),
            ], style={"marginBottom": "20px"}),

            # Interactivity settings
            html.Div([
                html.H4("Interactivity", style={"marginBottom": "10px"}),

                html.Label("Hover Effect"),
                dcc.Dropdown(
                    id={"type": "particle-control", "param": "interactivity.events.onHover.mode"},
                    options=[
                        {"label": "None", "value": "none"},
                        {"label": "Repulse", "value": "repulse"},
                        {"label": "Attract", "value": "attract"},
                        {"label": "Grab", "value": "grab"},
                        {"label": "Bubble", "value": "bubble"},
                    ],
                    value="repulse",
                    clearable=False
                ),

                html.Label("Click Effect", style={"marginTop": "10px"}),
                dcc.Dropdown(
                    id={"type": "particle-control", "param": "interactivity.events.onClick.mode"},
                    options=[
                        {"label": "None", "value": "none"},
                        {"label": "Push", "value": "push"},
                        {"label": "Remove", "value": "remove"},
                        {"label": "Repulse", "value": "repulse"},
                        {"label": "Bubble", "value": "bubble"},
                    ],
                    value="push",
                    clearable=False
                ),
            ]),

            # Button container
            html.Div([
                html.Button("Apply Changes", id="apply-changes", n_clicks=0,
                            style={
                                "padding": "10px 20px", "backgroundColor": "#4CAF50", "color": "white",
                                "border": "none", "borderRadius": "5px", "cursor": "pointer",
                                "fontSize": "16px", "marginRight": "10px"
                            }),
                html.Button("Reset", id="reset-controls", n_clicks=0,
                            style={
                                "padding": "10px 20px", "backgroundColor": "#f44336", "color": "white",
                                "border": "none", "borderRadius": "5px", "cursor": "pointer",
                                "fontSize": "16px", "marginRight": "10px"
                            }),
                html.Button("Export Config", id="export-config-button", n_clicks=0,
                            style={
                                "padding": "10px 20px", "backgroundColor": "#2196F3", "color": "white",
                                "border": "none", "borderRadius": "5px", "cursor": "pointer",
                                "fontSize": "16px"
                            }),
            ], style={"marginTop": "20px", "display": "flex", "flexWrap": "wrap"}),

            # Exported code display area
            html.Div(id="export-output-container", style={"display": "none", "marginTop": "20px"}, children=[
                html.H4("Exported Component Code"),
                dcc.Textarea(
                    id="export-code-output",
                    readOnly=True,
                    style={"width": "100%", "height": "300px", "fontFamily": "monospace", "fontSize": "12px",
                           "border": "1px solid #ccc", "padding": "10px"},
                    placeholder="Click 'Export Config' to generate the code..."
                )
            ]),

            # Store for current configuration
            dcc.Store(id="current-config", data=particle_configs["default"]),

        ], style={
            "width": "35%",
            "padding": "20px",
            "backgroundColor": "rgba(248, 249, 250, 0.9)",  # Semi-transparent background
            "borderRadius": "10px",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            "overflowY": "auto",
            "maxHeight": "600px",
            "position": "relative",
            "zIndex": 10  # Higher z-index to appear above particles
        }),
    ], style={
        "display": "flex",
        "marginBottom": "20px",
        "justifyContent": "center",
        "position": "relative"  # Needed for absolute positioning of children
    }),
], style={
    "position": "relative",  # Needed for absolute positioning of children
    "minHeight": "100vh"
})


# Callback to update links controls visibility
@callback(
    Output("links-controls", "style"),
    Input({"type": "particle-control", "param": "particles.links.enable"}, "value")
)
def toggle_links_controls(enable_links):
    if enable_links:
        return {"display": "block"}
    else:
        return {"display": "none"}


# Callback to update movement controls visibility
@callback(
    Output("movement-controls", "style"),
    Input({"type": "particle-control", "param": "particles.move.enable"}, "value")
)
def toggle_movement_controls(enable_movement):
    if enable_movement:
        return {"display": "block"}
    else:
        return {"display": "none"}


# Initial load of particles
@callback(
    Output("particles-container", "children"),
    Input("current-config", "data"),
)
def initial_load(config):
    particles = dash_particles.DashParticles(
        id="particles-initial",
        options=config,
        height="100%",
        width="100%",
    )

    return particles


# Callback to update description
@callback(
    Output("description", "children"),
    Input("particle-preset-dropdown", "value")
)
def update_description(preset_name):
    descriptions = {
        "default": "A simple network of connected particles with hover and click interactions.",
        "bubbles": "Floating bubbles of different sizes with a deep blue background.",
        "snow": "Falling snowflakes against a dark blue night sky.",
        "fire": "Rising fire particles with warm colors against a black background.",
        "stars": "A starry night sky with twinkling stars.",
        "connect": "An interactive network that responds to mouse movements and clicks."
    }
    return descriptions[preset_name]


# Callback to load preset configuration
@callback(
    [Output("current-config", "data"),
     Output({"type": "particle-control", "param": ALL}, "value")],
    Input("particle-preset-dropdown", "value"),
    State({"type": "particle-control", "param": ALL}, "id"),
)
def load_preset(preset_name, control_ids):
    config = particle_configs[preset_name]

    # Extract values for each control from the config
    control_values = []
    for control_id in control_ids:
        param_path = control_id["param"].split(".")
        value = config
        try:
            for key in param_path:
                value = value[key]
            control_values.append(value)
        except (KeyError, TypeError):
            # If path doesn't exist in config, use default value
            control_values.append(None)

    return config, control_values


# Callback to apply changes from controls
@callback(
    [Output("particles-container", "children", allow_duplicate=True),
     Output("current-config", "data", allow_duplicate=True)],
    Input("apply-changes", "n_clicks"),
    State({"type": "particle-control", "param": ALL}, "id"),
    State({"type": "particle-control", "param": ALL}, "value"),
    State("current-config", "data"),
    prevent_initial_call=True
)
def apply_changes(n_clicks, control_ids, control_values, current_config):
    if n_clicks > 0:
        # Create a deep copy of the current config
        updated_config = json.loads(json.dumps(current_config))

        # Update config with values from controls
        for i, control_id in enumerate(control_ids):
            param_path = control_id["param"].split(".")
            value = control_values[i]

            # Skip if value is None
            if value is None:
                continue

            # Navigate to the right place in the config
            config_section = updated_config
            for j, key in enumerate(param_path):
                if j == len(param_path) - 1:
                    # Last key, set the value
                    config_section[key] = value
                else:
                    # Create nested dict if it doesn't exist
                    if key not in config_section:
                        config_section[key] = {}
                    config_section = config_section[key]

        # Create a new DashParticles component with the updated configuration
        particles = dash_particles.DashParticles(
            id="particles-custom",
            options=updated_config,
            height="100%",
            width="100%",
        )

        return particles, updated_config

    # Default return if button not clicked
    return dash.no_update, dash.no_update


# Callback to reset controls to current config
@callback(
    Output({"type": "particle-control", "param": ALL}, "value", allow_duplicate=True),
    Input("reset-controls", "n_clicks"),
    State("current-config", "data"),
    State({"type": "particle-control", "param": ALL}, "id"),
    prevent_initial_call=True
)
def reset_controls(n_clicks, current_config, control_ids):
    if n_clicks > 0:
        # Extract values for each control from the current config
        control_values = []
        for control_id in control_ids:
            param_path = control_id["param"].split(".")
            value = current_config
            try:
                for key in param_path:
                    value = value[key]
                control_values.append(value)
            except (KeyError, TypeError):
                # If path doesn't exist in config, use None
                control_values.append(None)

        return control_values

    # Default return if button not clicked
    return dash.no_update


# Callback to export configuration as code
@callback(
    Output("export-code-output", "value"),
    Output("export-output-container", "style"),
    Input("export-config-button", "n_clicks"),
    State("current-config", "data"),
    prevent_initial_call=True
)
def export_config_code(n_clicks, current_config_data):
    if n_clicks > 0 and current_config_data:
        # Format the dictionary string using pprint
        # Use sort_dicts=False if Python version supports it and order is preferred
        # (dict key order is preserved in Python 3.7+)
        try:
            config_py_str = pprint.pformat(current_config_data, indent=4, width=100, sort_dicts=False)
        except TypeError:  # sort_dicts might not be available in older Python versions
            config_py_str = pprint.pformat(current_config_data, indent=4, width=100)

        exported_code = f"""
# 1. Make sure to import dash_particles:
# import dash_particles

# 2. Here is the component code with your current configuration:

your_particles_component = dash_particles.DashParticles(
    id="particles-initial", # You can change this ID
    options={config_py_str},
    height="100%", # Adjust as needed
    width="100%"   # Adjust as needed
)

# 3. You can then add 'your_particles_component' to your Dash app's layout.
# For example:
#
# from dash import html # Assuming you use html.Div or similar
#
# # app.layout = html.Div([
# #     html.H1("My Page with Particles"),
# #     # If your page content needs to be above particles, ensure proper z-indexing
# #     # and positioning. For a background effect, the particle container might
# #     # need absolute positioning and a lower z-index.
# #
# #     # Example: Particles as a background for the whole page
# #     html.Div(style={{
# #         "position": "fixed", # Use "fixed" for viewport-relative positioning
# #         "top": 0,
# #         "left": 0,
# #         "width": "100%",
# #         "height": "100%",
# #         "zIndex": -1 # Ensure it's behind other content
# #     }}, children=[your_particles_component]),
# #     
# #     # Your foreground content (ensure it has a higher z-index or is in a new stacking context)
# #     html.Div(style={{"position": "relative", "zIndex": 1}}, children=[
# #         # html.H1("Content on top!"),
# #         # ... your main page content ...
# #     ])
# # ])
"""
        return exported_code, {"display": "block", "marginTop": "20px"}

    # If button not clicked or no data, keep textarea hidden and its content unchanged
    return dash.no_update, {"display": "none", "marginTop": "20px"}


if __name__ == '__main__':
    app.run(debug=True)