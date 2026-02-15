# Python Code Modularization Skill

This skill helps with Python code refactoring, modularization, and best practices.

## Capabilities

- Analyze existing codebases to identify logical modules
- Break down monolithic files into smaller, well-organized modules
- Apply separation of concerns principles
- Create proper imports and dependencies between modules
- Follow Python packaging best practices
- Generate documentation for modularized code

## Usage Examples

### Modularizing a Single-File Application
```
User: I have a Python application in one file, how can I break it up?
Skill: I'll help you analyze your code and create logical modules based on functionality.
```

### Refactoring Classes and Functions
```
User: How do I organize my classes into separate modules?
Skill: I'll identify cohesive groups of classes/functions and suggest appropriate module structures.
```

### Creating Proper Package Structure
```
User: How do I make my code into a proper Python package?
Skill: I'll help you create __init__.py files, setup.py, and proper import structures.
```

## Best Practices Applied

- Single Responsibility Principle: Each module should have one clear purpose
- Separation of Concerns: Different aspects (UI, logic, data, config) in separate modules
- Maintainable Code: Organized structure that's easy to extend and modify
- Import Management: Use absolute imports for clarity and to avoid issues with package structure
- Avoid Relative Imports: Prefer absolute imports over relative imports for better clarity and fewer import-related issues
- Type Hints: Always include type hints for function parameters and return values to improve code clarity and catch errors early
- Documentation: Clear README and docstrings for each module

## Common Module Types

- Configuration/constants modules
- Data/models modules
- Business logic modules
- UI/graphics modules
- Utility/helper modules
- Main application/control modules