import pytest

import dash_particles as dp


def test_options_serialize_pythonic_names():
    config = dp.Options(
        auto_play=True,
        background=dp.Background(color=dp.Color("transparent")),
        fps_limit=60,
        detect_retina=True,
        full_screen=dp.FullScreen(enable=False, z_index=0),
        particles=dp.Particles(
            color=dp.Color("#0075FF"),
            number=dp.ParticleNumber(
                value=80,
                density=dp.Density(enable=True, area=800),
            ),
            move=dp.Move(
                enable=True,
                direction="none",
                speed=3,
                random=False,
                straight=False,
                out_modes=dp.OutModes(default="bounce"),
            ),
            size=dp.Size(value=dp.RangeValue(min=1, max=5)),
        ),
        interactivity=dp.Interactivity(
            detects_on="canvas",
            events=dp.Events(
                on_click=dp.Action(enable=True, mode="push"),
                on_hover=dp.Action(enable=True, mode="repulse"),
            ),
        ),
        motion=dp.Motion(reduce=dp.MotionReduce(factor=2, value=True)),
        pause_on_blur=True,
        pause_on_outside_viewport=True,
        preset="links",
    )

    assert config.to_dict() == {
        "autoPlay": True,
        "background": {"color": {"value": "transparent"}},
        "fpsLimit": 60,
        "detectRetina": True,
        "fullScreen": {"enable": False, "zIndex": 0},
        "particles": {
            "color": {"value": "#0075FF"},
            "number": {
                "value": 80,
                "density": {"enable": True, "area": 800},
            },
            "move": {
                "enable": True,
                "direction": "none",
                "speed": 3,
                "random": False,
                "straight": False,
                "outModes": {"default": "bounce"},
            },
            "size": {"value": {"min": 1, "max": 5}},
        },
        "interactivity": {
            "detectsOn": "canvas",
            "events": {
                "onClick": {"enable": True, "mode": "push"},
                "onHover": {"enable": True, "mode": "repulse"},
            },
        },
        "motion": {"reduce": {"factor": 2, "value": True}},
        "pauseOnBlur": True,
        "pauseOnOutsideViewport": True,
        "preset": "links",
    }


def test_options_support_responsive_themes_and_manual_particles():
    config = dp.Options(
        manual_particles=[
            dp.ManualParticle(
                position=dp.Position(x=25, y=50),
                options=dp.Options(
                    particles=dp.Particles(move=dp.Move(speed=0.5)),
                ),
            )
        ],
        responsive=[
            dp.Responsive(
                max_width=768,
                options=dp.Options(particles=dp.Particles(number=dp.ParticleNumber(value=30))),
            )
        ],
        themes=[
            dp.Theme(
                name="dark",
                options=dp.Options(background=dp.Background(color=dp.Color("#020617"))),
            )
        ],
    )

    assert config.to_dict() == {
        "manualParticles": [
            {
                "position": {"x": 25, "y": 50},
                "options": {"particles": {"move": {"speed": 0.5}}},
            }
        ],
        "responsive": [
            {
                "maxWidth": 768,
                "options": {"particles": {"number": {"value": 30}}},
            }
        ],
        "themes": [
            {
                "name": "dark",
                "options": {"background": {"color": {"value": "#020617"}}},
            }
        ],
    }


def test_options_support_background_mask_and_hover_parallax():
    config = dp.Options(
        background_mask=dp.BackgroundMask(
            enable=True,
            composite="destination-out",
            cover=dp.BackgroundMaskCover(color="#111827", opacity=1),
        ),
        interactivity=dp.Interactivity(
            events=dp.Events(
                on_hover=dp.Action(
                    enable=True,
                    mode="repulse",
                    parallax={"enable": True, "force": 60, "smooth": 10},
                )
            )
        ),
    )

    assert config.to_dict() == {
        "backgroundMask": {
            "enable": True,
            "composite": "destination-out",
            "cover": {"color": "#111827", "opacity": 1},
        },
        "interactivity": {
            "events": {
                "onHover": {
                    "enable": True,
                    "mode": "repulse",
                    "parallax": {"enable": True, "force": 60, "smooth": 10},
                }
            }
        },
    }


def test_interactivity_events_support_documented_click_and_hover_modes():
    config = dp.Options(
        interactivity=dp.Interactivity(
            events=dp.Events(
                on_click=dp.Action(enable=True, mode=["pause", "push"]),
                on_hover=dp.Action(
                    enable=True,
                    mode=["grab", "connect"],
                    parallax={"enable": True, "force": 60, "smooth": 10},
                ),
            )
        )
    )

    assert config.to_dict() == {
        "interactivity": {
            "events": {
                "onClick": {"enable": True, "mode": ["pause", "push"]},
                "onHover": {
                    "enable": True,
                    "mode": ["grab", "connect"],
                    "parallax": {"enable": True, "force": 60, "smooth": 10},
                },
            }
        }
    }


def test_move_supports_center_configuration():
    config = dp.Options(
        particles=dp.Particles(
            move=dp.Move(
                enable=True,
                center={"x": 50, "y": 50, "mode": "percent", "radius": 0},
            )
        )
    )

    assert config.to_dict() == {
        "particles": {
            "move": {
                "enable": True,
                "center": {"x": 50, "y": 50, "mode": "percent", "radius": 0},
            }
        }
    }


def test_extra_values_merge_with_structured_config():
    config = dp.Options(
        particles=dp.Particles(
            color=dp.Color("#ffffff"),
            extra={"links": {"enable": True}},
        ),
        extra={"fullScreen": {"enable": False}},
    )

    assert config.to_dict() == {
        "fullScreen": {"enable": False},
        "particles": {
            "links": {"enable": True},
            "color": {"value": "#ffffff"},
        },
    }


def test_dash_particles_accepts_structured_config_and_overrides():
    component = dp.DashParticles(
        id="particles",
        config=dp.Options(background=dp.Background(color=dp.Color("transparent"))),
        particles=dp.Particles(number=dp.ParticleNumber(value=24)),
        full_screen=dp.FullScreen(enable=False, z_index=0),
    )

    assert component.options == {
        "fullScreen": {"enable": False, "zIndex": 0},
        "background": {"color": {"value": "transparent"}},
        "particles": {"number": {"value": 24}},
    }


def test_explicit_sections_override_overlapping_config_keys():
    component = dp.DashParticles(
        id="particles",
        config={
            "particles": {
                "number": {"value": 12},
                "links": {"enable": False},
            },
            "pauseOnBlur": False,
        },
        particles=dp.Particles(
            number=dp.ParticleNumber(value=24),
            links=dp.Links(enable=True, color="#38bdf8"),
        ),
        pause_on_blur=True,
    )

    assert component.options == {
        "fullScreen": {"enable": False, "zIndex": 0},
        "particles": {
            "number": {"value": 24},
            "links": {"enable": True, "color": "#38bdf8"},
        },
        "pauseOnBlur": True,
    }


def test_dash_particles_default_to_embedded_canvas_mode():
    component = dp.DashParticles(id="particles", options={"particles": {"number": {"value": 12}}})

    assert component.options["fullScreen"] == {"enable": False, "zIndex": 0}
    assert component.options["particles"]["number"]["value"] == 12


def test_presets_are_available_from_top_level_package():
    stars = dp.presets.stars().to_dict()
    among_us = dp.presets.among_us().to_dict()
    multiple_images = dp.presets.multiple_images().to_dict()
    parallax = dp.presets.parallax().to_dict()
    fontawesome = dp.presets.fontawesome().to_dict()
    blurred_particles = dp.presets.blurred_particles().to_dict()
    hypno_squares = dp.presets.hypno_squares().to_dict()

    assert {"stars", "among_us", "fontawesome", "parallax", "blurred_particles", "hypno_squares"}.issubset(
        set(dp.presets.names())
    )
    assert stars["particles"]["twinkle"]["particles"]["enable"] is True
    assert "emitters" in among_us
    assert among_us["key"] == "amongUs"
    assert among_us["name"] == "Among Us"
    assert among_us["emitters"]["position"] == {"x": -5, "y": 55}
    assert among_us["emitters"]["particles"]["shape"]["options"]["images"]["src"].startswith("https://")
    assert among_us["preload"][0]["src"].startswith("https://")
    assert len(multiple_images["preload"]) == 3
    assert parallax["key"] == "parallax"
    assert parallax["name"] == "Parallax"
    assert parallax["interactivity"]["events"]["onHover"]["mode"] == "grab"
    assert parallax["interactivity"]["events"]["onHover"]["parallax"]["enable"] is True
    assert fontawesome["key"] == "fontawesome"
    assert fontawesome["name"] == "Font Awesome"
    assert fontawesome["particles"]["shape"]["type"] == "char"
    assert fontawesome["particles"]["shape"]["options"]["char"]["font"] == "Font Awesome 6 Brands"
    assert fontawesome["particles"]["shape"]["options"]["char"]["value"] == "\uf179"
    assert fontawesome["particles"]["links"]["enable"] is True
    assert fontawesome["particles"]["stroke"]["width"] == 0
    assert blurred_particles["key"] == "blurredParticles"
    assert blurred_particles["name"] == "Blurred Particles"
    assert blurred_particles["style"]["filter"] == "blur(50px)"
    assert blurred_particles["emitters"]["position"] == {"x": 50, "y": 150}
    assert blurred_particles["particles"]["size"]["random"]["minimumValue"] == 200
    assert len(blurred_particles["themes"]) == 2
    assert blurred_particles["themes"][0]["name"] == "light"
    assert blurred_particles["themes"][1]["name"] == "dark"
    assert hypno_squares["key"] == "hypnoSquares"
    assert hypno_squares["name"] == "Hypno Squares"
    assert hypno_squares["background"]["color"]["value"] == "#000"
    assert hypno_squares["particles"]["shape"]["type"] == "square"
    assert hypno_squares["particles"]["shape"]["options"]["square"]["fill"] is False
    assert hypno_squares["particles"]["stroke"]["width"] == 5
    assert hypno_squares["particles"]["rotate"]["direction"] == "counter-clockwise"
    assert hypno_squares["particles"]["size"]["animation"]["destroy"] == "max"
    assert hypno_squares["emitters"]["position"] == {"x": 50, "y": 50}


def test_fontawesome_preset_allows_older_fontawesome_family_names():
    config = dp.presets.fontawesome(
        brand_font_family="Font Awesome 5 Brands",
        solid_font_family="Font Awesome 5 Free",
        solid_glyph="\uf5d1",
    ).to_dict()

    assert config["particles"]["shape"]["options"]["char"][0]["font"] == "Font Awesome 5 Brands"
    assert config["particles"]["shape"]["options"]["char"][1]["font"] == "Font Awesome 5 Free"
    assert config["particles"]["shape"]["options"]["char"][1]["value"] == "\uf5d1"


def test_dash_particles_rejects_options_and_config_together():
    with pytest.raises(TypeError, match="either `options=` or `config=`"):
        dp.DashParticles(id="particles", options={}, config={})
