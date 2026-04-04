import json
from pathlib import Path

from setuptools import setup


here = Path(__file__).parent
package_path = here / "package.json"
readme_path = here / "README.md"

with package_path.open(encoding="utf-8") as f:
    package = json.load(f)

try:
    long_description = readme_path.read_text(encoding="utf-8")
except UnicodeDecodeError:
    long_description = "dash-particles provides structured tsParticles backgrounds for Dash."

package_name = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package["author"],
    packages=[package_name],
    include_package_data=True,
    license=package["license"],
    description=package.get("description", package_name),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=[
        "dash>=2.0.0",
    ],
    project_urls={
        "Documentation": "https://github.com/jeffgallini/dash-particles/tree/master/dash_particles",
        "Source": "https://github.com/jeffgallini/dash-particles",
        "Issue Tracker": "https://github.com/jeffgallini/dash-particles/issues",
    },
    classifiers=[
        "Framework :: Dash",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
