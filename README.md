# Python to Maestro Converter

A simple tool to convert existing Python automation scripts (Selenium, Appium) into [Maestro](https://maestro.mobile.dev/) YAML flows.

## Installation

```bash
pip install pythontomaestro
```

## Usage

```bash
pythontomaestro <input_file_or_dir> <output_dir>
```

Example:

```bash
pythontomaestro tests/my_test.py output/
```

This will read `tests/my_test.py`, convert the automation steps, and save the resulting YAML flows into the `output/` directory (e.g., `output/test_login_success.yaml`).

## Features

- Parses Python AST to extract automation steps.
- Maps Selenium/Appium commands (click, input, navigate) to Maestro commands (tapOn, inputText, openLink).
- Generates valid Maestro YAML flows.

## ⚠️ Limitations & Manual Review

**Not everything can be converted automatically.**

Python scripts often contain complex logic (loops, conditionals, custom helper methods) that do not map 1:1 to Maestro's declarative YAML syntax.

When the tool encounters such logic, it will:
1.  **Log a warning** in the console.
2.  **Insert a `TODO_UNSUPPORTED_ACTION`** in the generated YAML file.
3.  **Add a top-level warning comment** to the file.

**Example:**

```yaml
# WARNING: This flow contains unsupported actions (TODOs). Manual review required.
- tapOn:
    text: Login
- TODO_UNSUPPORTED_ACTION: 'Unsupported control flow: If statement (Suggestion: Unroll loops or use runScript for simple logic)'
```

**You must manually review the generated YAML files and address any `TODO` items.**
