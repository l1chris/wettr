from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="wettr",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "wettr=weather_cli.main:main",
        ]
    },
)
