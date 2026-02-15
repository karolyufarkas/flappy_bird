# Modularized Flappy Bird Game

This is a modularized version of the classic Flappy Bird game, originally implemented in a single file and now broken down into separate modules for better maintainability and readability.

## Package Structure

### src/flappy_bird/
- `__init__.py` - Package initialization
- `constants.py` - Contains all game constants such as screen dimensions, physics parameters, biomes, colors, etc.
- `bird.py` - Contains the Bird class with methods for flapping, updating position, drawing, and collision detection.
- `pipe.py` - Contains the Pipe class with methods for updating position, drawing, and collision detection.
- `graphics.py` - Contains all drawing functions including backgrounds, ground, start screen, and game over screen.
- `sounds.py` - Handles sound generation and playback for flap, hit, and point sounds.
- `game.py` - Contains the main game loop, event handling, collision detection logic, and game state management.

## Installation

### From Source
```bash
git clone https://github.com/yourusername/flappy-bird.git
cd flappy-bird
pip install -e .
```

### Or Install via pip
```bash
pip install flappy-bird-game
```

## Running the Game

After installation, you can run the game in several ways:

### Using the console script:
```bash
flappy-bird
```

### Or using Python module execution:
```bash
python -m flappy_bird.game
```

## Game Controls

- Press SPACE to start the game and make the bird flap
- Press R to restart after game over

## Features

- Physics-based gameplay with gravity and flapping mechanics
- Multiple biomes that change as you progress (Day, Evening, Desert, Snow)
- Dynamic background elements that change with the biomes
- Procedurally generated sound effects
- Score tracking and difficulty progression
- Collision detection with pipes and boundaries

## Development

To contribute to this project:

1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install in editable mode: `pip install -e ".[dev]"`

## Building Distribution

To build the package for distribution:

```bash
pip install build
python -m build
```

This will create `dist/` directory with the built packages.

## CI/CD

This project uses GitHub Actions for continuous integration:

- **CI**: Runs tests on multiple Python versions (3.8-3.12) on pushes and PRs to main branch
- **Cross Platform Tests**: Runs tests on multiple platforms (Ubuntu, Windows, macOS)
- **Publish**: Automatically publishes to PyPI on new releases

## Contributing

1. Fork the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install in editable mode: `pip install -e ".[dev]"`
5. Run tests: `pytest tests/`