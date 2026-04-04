from pathlib import Path

import dash_particles as dp
from usage import export_config_code, format_python_config, particle_configs


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = PACKAGE_ROOT / "docs"
README_PATH = PACKAGE_ROOT / "README.md"
DOC_FILENAMES = [
    "README.md",
    "getting-started.md",
    "config-model.md",
    "recipes.md",
    "migration.md",
    "troubleshooting.md",
]
README_DOC_LINKS = [
    "docs/getting-started.md",
    "docs/config-model.md",
    "docs/recipes.md",
    "docs/migration.md",
    "docs/troubleshooting.md",
    "docs/README.md",
]


def test_required_docs_guides_exist():
    for filename in DOC_FILENAMES:
        assert (DOCS_ROOT / filename).exists()


def test_readme_links_to_all_docs_guides():
    readme = README_PATH.read_text(encoding="utf-8")

    for link in README_DOC_LINKS:
        assert link in readme


def test_readme_documents_presets_and_runtime_boundary():
    readme = README_PATH.read_text(encoding="utf-8")

    assert "dp.presets.*" in readme
    assert "tsparticles" in readme
    assert "full JavaScript bundle" in readme


def test_recipes_include_official_sample_inspired_examples():
    recipes = (DOCS_ROOT / "recipes.md").read_text(encoding="utf-8")

    for sample_name in [
        "Among Us",
        "Blurred Particles",
        "Font Awesome",
        "Hypno Squares",
        "Multiple Images",
        "Parallax",
    ]:
        assert sample_name in recipes


def test_readme_quickstart_constructs_component():
    background_particles = dp.DashParticles(
        id="page-particles",
        config=dp.Options(
            background=dp.Background(color=dp.Color("transparent")),
            particles=dp.Particles(
                color=dp.Color("#2563eb"),
                number=dp.ParticleNumber(value=80),
                links=dp.Links(
                    enable=True,
                    color="#2563eb",
                    opacity=0.35,
                    distance=140,
                ),
                move=dp.Move(
                    enable=True,
                    speed=2,
                    direction="none",
                    out_modes=dp.OutModes(default="bounce"),
                ),
                size=dp.Size(value=3),
            ),
        ),
        height="100%",
        width="100%",
    )

    assert background_particles.options["particles"]["links"]["enable"] is True
    assert background_particles.options["particles"]["move"]["outModes"]["default"] == "bounce"


def test_migration_example_preserves_legacy_shape():
    legacy_config = {
        "background": {"color": {"value": "#0f172a"}},
        "particles": {
            "color": {"value": "#38bdf8"},
            "number": {"value": 80},
            "links": {
                "enable": True,
                "color": "#38bdf8",
                "opacity": 0.3,
                "distance": 150,
            },
            "move": {
                "enable": True,
                "speed": 2,
                "direction": "none",
                "outModes": {"default": "bounce"},
            },
        },
        "interactivity": {
            "events": {
                "onHover": {"enable": True, "mode": "grab"},
                "onClick": {"enable": True, "mode": "push"},
            }
        },
    }

    structured_config = dp.Options(
        background=dp.Background(color=dp.Color("#0f172a")),
        particles=dp.Particles(
            color=dp.Color("#38bdf8"),
            number=dp.ParticleNumber(value=80),
            links=dp.Links(
                enable=True,
                color="#38bdf8",
                opacity=0.3,
                distance=150,
            ),
            move=dp.Move(
                enable=True,
                speed=2,
                direction="none",
                out_modes=dp.OutModes(default="bounce"),
            ),
        ),
        interactivity=dp.Interactivity(
            events=dp.Events(
                on_hover=dp.Action(enable=True, mode="grab"),
                on_click=dp.Action(enable=True, mode="push"),
            )
        ),
    )

    assert structured_config.to_dict() == legacy_config


def test_usage_export_stays_structured_api_first():
    formatted = format_python_config(particle_configs["connect"])
    exported_code, style = export_config_code(1, particle_configs["connect"])

    assert "dp.Options(" in formatted
    assert "dp.DashParticles(" in exported_code
    assert "config=(" in exported_code
    assert style["display"] == "block"
    compile(exported_code, "<exported-docs>", "exec")
