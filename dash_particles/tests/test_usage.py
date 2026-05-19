import dash_particles as dp
from usage import (
    CLICK_MODE_OPTIONS,
    HOVER_MODE_OPTIONS,
    _config_fingerprint,
    app,
    apply_editor_overrides,
    example_catalog,
    extract_editor_state,
    particle_configs,
    particle_presets,
    render_preview,
)


def _find_component_by_id(component, component_id):
    if getattr(component, "id", None) == component_id:
        return component

    children = getattr(component, "children", None)
    if isinstance(children, (list, tuple)):
        for child in children:
            found = _find_component_by_id(child, component_id)
            if found is not None:
                return found
    elif children is not None:
        return _find_component_by_id(children, component_id)

    return None


def _iter_components(component):
    yield component

    children = getattr(component, "children", None)
    if isinstance(children, (list, tuple)):
        for child in children:
            yield from _iter_components(child)
    elif children is not None:
        yield from _iter_components(children)


def _has_empty_selector_object(value):
    if isinstance(value, dict):
        if value.get("selectors") == {}:
            return True
        return any(_has_empty_selector_object(child) for child in value.values())

    if isinstance(value, list):
        return any(_has_empty_selector_object(child) for child in value)

    return False


def test_usage_app_layout_exists():
    assert app.layout is not None


def test_usage_initial_layout_seeds_editor_control_values():
    state = extract_editor_state(particle_configs["default"])
    expected_values = {
        "background-color": state["background_color"],
        "particle-color": state["particle_color"],
        "link-color": state["link_color"],
        "particle-count": state["particle_count"],
        "particle-size": state["particle_size"],
        "particle-opacity": state["particle_opacity"],
        "move-speed": state["move_speed"],
        "links-enabled": state["links_enabled"],
        "hover-mode": state["hover_mode"],
        "click-mode": state["click_mode"],
    }

    for component_id, expected_value in expected_values.items():
        component = _find_component_by_id(app.layout, component_id)

        assert component is not None
        assert component.value == expected_value


def test_usage_layout_uses_dropdown_selectors():
    dropdowns = {
        component.id: component
        for component in _iter_components(app.layout)
        if type(component).__name__ == "Dropdown"
    }

    assert {"example-dropdown", "hover-mode", "click-mode"}.issubset(dropdowns)
    assert all(not dropdown.clearable for dropdown in dropdowns.values())


def test_usage_includes_packaged_presets_and_official_examples():
    assert set(dp.presets.names()).issubset(set(example_catalog))
    assert {"among_us", "multiple_images", "parallax", "fontawesome", "blurred_particles", "hypno_squares"}.issubset(
        set(example_catalog)
    )


def test_usage_presets_and_examples_serialize_to_store_configs():
    assert particle_presets["connect"].to_dict() == particle_configs["connect"]
    assert particle_presets["among_us"].to_dict() == particle_configs["among_us"]
    assert particle_presets["fontawesome"].to_dict() == particle_configs["fontawesome"]
    assert particle_presets["blurred_particles"].to_dict() == particle_configs["blurred_particles"]
    assert particle_presets["hypno_squares"].to_dict() == particle_configs["hypno_squares"]
    assert "emitters" in particle_configs["among_us"]


def test_usage_examples_can_be_passed_via_config_alias():
    component = dp.DashParticles(id="particles", config=particle_configs["parallax"])

    assert component.options == particle_configs["parallax"]


def test_usage_mode_controls_match_documented_click_and_hover_modes():
    hover_modes = {option["value"] for option in HOVER_MODE_OPTIONS}
    click_modes = {option["value"] for option in CLICK_MODE_OPTIONS}

    assert hover_modes == {"none", "grab", "bubble", "repulse", "connect"}
    assert click_modes == {
        "none",
        "attract",
        "bubble",
        "pause",
        "pop",
        "push",
        "remove",
        "repulse",
        "trail",
        "emitter",
        "absorber",
    }


def test_usage_advanced_runtime_examples_have_expected_keys():
    assert particle_configs["fontawesome"]["particles"]["shape"]["type"] == "char"
    assert particle_configs["fontawesome"]["key"] == "fontawesome"
    assert particle_configs["blurred_particles"]["key"] == "blurredParticles"
    assert particle_configs["blurred_particles"]["style"]["filter"] == "blur(50px)"
    assert particle_configs["blurred_particles"]["emitters"]["rate"] == {"delay": 0.2, "quantity": 2}
    assert particle_configs["blurred_particles"]["themes"][0]["name"] == "light"
    assert particle_configs["blurred_particles"]["themes"][1]["name"] == "dark"
    assert particle_configs["hypno_squares"]["key"] == "hypnoSquares"
    assert particle_configs["hypno_squares"]["particles"]["stroke"]["width"] == 5
    assert particle_configs["hypno_squares"]["particles"]["rotate"]["animation"]["speed"] == 2
    assert particle_configs["hypno_squares"]["particles"]["size"]["animation"]["destroy"] == "max"
    assert particle_configs["hypno_squares"]["emitters"]["rate"] == {"delay": 1, "quantity": 1}
    assert particle_configs["parallax"]["key"] == "parallax"
    assert particle_configs["parallax"]["interactivity"]["events"]["onHover"]["mode"] == "grab"
    assert particle_configs["parallax"]["interactivity"]["events"]["onHover"]["parallax"]["enable"] is True
    assert "emitters" in particle_configs["among_us"]
    assert particle_configs["among_us"]["emitters"]["position"] == {"x": -5, "y": 55}
    assert particle_configs["among_us"]["preload"][0]["src"].startswith("https://")
    assert len(particle_configs["multiple_images"]["preload"]) == 3


def test_usage_examples_do_not_emit_object_selectors():
    for name in ("among_us", "fontawesome", "parallax", "blurred_particles", "hypno_squares"):
        assert _has_empty_selector_object(particle_configs[name]) is False


def test_usage_editor_state_normalizes_color_objects_for_inputs():
    state = extract_editor_state(particle_configs["among_us"])

    assert isinstance(state["particle_color"], str)
    assert isinstance(state["link_color"], str)
    assert state["link_color"] == "#fff"


def test_usage_editor_state_round_trips_common_fields():
    state = extract_editor_state(particle_configs["connect"])
    updated = apply_editor_overrides(
        particle_configs["connect"],
        background_color="#000000",
        particle_color="#ffffff",
        link_color="#ffffff",
        particle_count=64,
        particle_size=5,
        particle_opacity=0.45,
        move_speed=2.5,
        links_enabled=True,
        hover_mode="grab",
        click_mode="push",
    )

    assert state["links_enabled"] is True
    assert updated["background"]["color"]["value"] == "#000000"
    assert updated["particles"]["number"]["value"] == 64


def test_usage_editor_supports_documented_click_and_hover_modes():
    updated = apply_editor_overrides(
        particle_configs["connect"],
        background_color="#000000",
        particle_color="#ffffff",
        link_color="#ffffff",
        particle_count=64,
        particle_size=5,
        particle_opacity=0.45,
        move_speed=2.5,
        links_enabled=True,
        hover_mode="connect",
        click_mode="pause",
    )

    assert updated["interactivity"]["events"]["onHover"] == {
        "enable": True,
        "mode": "connect",
    }
    assert updated["interactivity"]["events"]["onClick"] == {
        "enable": True,
        "mode": "pause",
    }


def test_usage_editor_seeds_required_mode_configs_for_visible_interactions():
    updated = apply_editor_overrides(
        particle_configs["default"],
        background_color="#000000",
        particle_color="#ffffff",
        link_color="#ffffff",
        particle_count=64,
        particle_size=5,
        particle_opacity=0.45,
        move_speed=2.5,
        links_enabled=True,
        hover_mode="connect",
        click_mode="remove",
    )

    assert updated["interactivity"]["modes"]["connect"] == {
        "distance": 80,
        "links": {"opacity": 0.5},
        "radius": 60,
    }
    assert updated["interactivity"]["modes"]["remove"] == {"quantity": 2}


def test_usage_editor_seeds_bubble_mode_config_for_click_and_hover():
    updated = apply_editor_overrides(
        particle_configs["default"],
        background_color="#000000",
        particle_color="#ffffff",
        link_color="#ffffff",
        particle_count=64,
        particle_size=5,
        particle_opacity=0.45,
        move_speed=2.5,
        links_enabled=True,
        hover_mode="bubble",
        click_mode="bubble",
    )

    assert updated["interactivity"]["modes"]["bubble"] == {
        "distance": 200,
        "duration": 2,
        "opacity": 1,
        "size": 12,
    }


def test_usage_selected_presets_default_hover_mode_to_none():
    for name in ("default", "bubbles", "snow", "fire", "stars"):
        state = extract_editor_state(particle_configs[name])

        assert state["hover_mode"] == "none"
        assert particle_configs[name]["interactivity"]["events"]["onHover"] == {
            "enable": False,
            "mode": "none",
        }


def test_usage_preview_component_reuses_existing_canvas_for_new_config():
    first_component, _ = render_preview(particle_configs["default"])
    second_component, _ = render_preview(particle_configs["parallax"])

    assert _config_fingerprint(particle_configs["default"]) != _config_fingerprint(
        particle_configs["parallax"]
    )
    assert first_component.id == second_component.id == "particles-preview"
    assert first_component.options != second_component.options


def test_usage_preview_forces_embedded_mode_for_fullscreen_presets():
    component, _ = render_preview(particle_configs["among_us"])

    assert component.options["fullScreen"] == {"enable": False, "zIndex": 0}
