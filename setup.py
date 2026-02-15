"""
Setup script for the Flappy Bird game package.

This package implements a modularized version of the classic Flappy Bird game.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flappy-bird-game",
    version="1.0.0",
    author="Qwen Assistant",
    author_email="qwen@example.com",
    description="A modularized implementation of the classic Flappy Bird game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flappy-bird",
    project_urls={
        "Bug Reports",
        "https://github.com/yourusername/flappy-bird/issues",
        "Source Code",
        "https://github.com/yourusername/flappy-bird",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src", include=["flappy_bird", "flappy_bird.*"]),
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.0.0",
        "numpy>=1.18.0",
    ],
    entry_points={
        "console_scripts": [
            "flappy-bird=flappy_bird.game:main",
        ],
    },
)