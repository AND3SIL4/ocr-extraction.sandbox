# AGENTS.md

## Build/Lint/Test Commands

- **Install dependencies**: `uv sync`
- **Run application**: `uv run fastapi dev`
- **Run all tests**: `uv run python -m pytest` (when tests are added)
- **Run single test**: `uv run python -m pytest tests/test_file.py::TestClass::test_method`
- **Lint code**: `uv run python -m flake8` (when flake8 is added)
- **Format code**: `uv run python -m black .` (when black is added)
- **Type check**: `uv run python -m mypy .` (when mypy is added)

## Code Style Guidelines

### Imports
- Use absolute imports
- Group imports: standard library, third-party, local
- Sort imports alphabetically within groups

### Formatting
- Use 4 spaces for indentation
- Line length: 88 characters (Black default)
- Use double quotes for strings

### Types
- Use type hints for function parameters and return values
- Use `typing` module for complex types

### Naming Conventions
- Functions/variables: snake_case
- Classes: PascalCase
- Constants: UPPER_SNAKE_CASE
- Private members: leading underscore

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Use context managers for resource management

### FastAPI Specific
- Use Pydantic models for request/response validation
- Use dependency injection for shared logic
- Return appropriate HTTP status codes