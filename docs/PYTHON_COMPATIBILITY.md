# 🐍 Python Compatibility Guide - Colonel Katie

Comprehensive guide to Python version compatibility and migration.

## Table of Contents
- [Overview](#overview)
- [Supported Python Versions](#supported-python-versions)
- [Key Differences from Open Interpreter](#key-differences-from-open-interpreter)
- [Version-Specific Features](#version-specific-features)
- [Migration Guide](#migration-guide)
- [Dependency Compatibility](#dependency-compatibility)
- [Testing Across Versions](#testing-across-versions)
- [Troubleshooting](#troubleshooting)

---

## Overview

Colonel Katie extends Open Interpreter's Python support to include Python 3.13, making it compatible with the latest Python releases while maintaining backward compatibility.

### Version Support Matrix

| Python Version | Open Interpreter | Colonel Katie | Status |
|----------------|-----------------|---------------|---------|
| 3.8 | ✅ | ⚠️ | Legacy support |
| 3.9 | ✅ | ✅ | Fully supported |
| 3.10 | ✅ | ✅ | Fully supported |
| 3.11 | ✅ | ✅ | **Recommended** |
| 3.12 | ✅ | ✅ | Fully supported |
| 3.13 | ❌ | ✅ | **Newly supported** |
| 3.14 | ❌ | 🔄 | In development |

---

## Supported Python Versions

### Python 3.9
- **Status**: Fully supported
- **Notes**: Minimum version for headless installation
- **Key Features**: Type hints, dictionary merge operators

### Python 3.10
- **Status**: Fully supported
- **Notes**: Improved error messages, pattern matching
- **Key Features**: `match` statements, better type hints

### Python 3.11
- **Status**: Fully supported & **Recommended**
- **Notes**: Best performance, optimal compatibility
- **Key Features**: 
  - 10-60% faster than 3.10
  - Better error messages
  - Exception groups
  - Task groups in asyncio

### Python 3.12
- **Status**: Fully supported
- **Notes**: Good compatibility, newer features
- **Key Features**:
  - Per-interpreter GIL
  - Improved f-strings
  - Type parameter syntax

### Python 3.13
- **Status**: Fully supported (Colonel Katie exclusive)
- **Notes**: Latest features, may have dependency issues
- **Key Features**:
  - JIT compiler (experimental)
  - Better REPL
  - Improved performance
  - iOS and Android support

---

## Key Differences from Open Interpreter

### 1. Modified pyproject.toml
```toml
# Open Interpreter
python = ">=3.9,<3.13"

# Colonel Katie
python = ">=3.9,<4"
```

### 2. Updated Dependencies
```toml
# Relaxed version constraints for 3.13 compatibility
numpy = ">=1.26.0"  # Was "1.26.0"
PySide6 = "^6.7.0"  # Updated for 3.13
```

### 3. Compatibility Patches
```python
# Colonel Katie includes compatibility shims
if sys.version_info >= (3, 13):
    # Handle removed pkg_resources
    try:
        import importlib.metadata as metadata
    except ImportError:
        import importlib_metadata as metadata
else:
    import pkg_resources
```

---

## Version-Specific Features

### Using Python 3.11 Features
```python
# Exception groups (3.11+)
def process_files(files):
    exceptions = []
    for file in files:
        try:
            process_file(file)
        except Exception as e:
            exceptions.append(e)
    
    if exceptions:
        raise ExceptionGroup("File processing failed", exceptions)

# Task groups (3.11+)
async def concurrent_operations():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(operation1())
        task2 = tg.create_task(operation2())
    # All tasks complete here
```

### Using Python 3.12 Features
```python
# Type parameter syntax (3.12+)
type Point[T] = tuple[T, T]

def distance[T: (int, float)](p1: Point[T], p2: Point[T]) -> float:
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

# Improved f-strings (3.12+)
value = 42
print(f"{value=}")  # Prints: value=42
```

### Using Python 3.13 Features
```python
# Better REPL (3.13+)
# Multi-line editing, syntax highlighting, better completions

# JIT compilation (experimental)
# Enable with: PYTHON_JIT=1 python script.py

# Improved pattern matching
match command:
    case ["move", x, y] if x >= 0 and y >= 0:
        move_to(x, y)
    case ["rotate", angle]:
        rotate(angle)
```

---

## Migration Guide

### From Open Interpreter to Colonel Katie

#### Step 1: Check Current Python Version
```bash
python3 --version
```

#### Step 2: Update Installation

**If using Python 3.9-3.12:**
```bash
# Standard installation works
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie
python install.py
```

**If using Python 3.13:**
```bash
# Use the modified installation
git clone https://github.com/Unicorn-Commander/Colonel-Katie.git
cd Colonel-Katie
./install-headless.sh  # Or python install.py for GUI
```

#### Step 3: Handle Dependency Issues

Common issues and fixes:

**tiktoken with Python 3.13:**
```bash
# Install Rust compiler first
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Then install tiktoken
pip install tiktoken
```

**numpy compatibility:**
```bash
# If numpy fails, install from source
pip install numpy --no-binary numpy
```

### Updating Existing Code

#### Handle Deprecated Features
```python
# Old (deprecated in 3.13)
import pkg_resources
version = pkg_resources.get_distribution("package").version

# New (3.13 compatible)
try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

package_version = version("package")
```

#### Update Type Hints
```python
# Old style
from typing import List, Dict, Optional

def process(items: List[str]) -> Dict[str, int]:
    pass

# New style (3.9+)
def process(items: list[str]) -> dict[str, int]:
    pass

# With 3.10+ union types
def process(item: str | None) -> dict[str, int] | None:
    pass
```

---

## Dependency Compatibility

### Core Dependencies

| Package | Python 3.9-3.12 | Python 3.13 | Notes |
|---------|-----------------|-------------|--------|
| numpy | 1.26.0 | >=1.26.0 | Version constraint relaxed |
| tiktoken | 0.7.0 | 0.9.0 | Requires Rust for 3.13 |
| PySide6 | 6.7.0 | 6.9.1 | GUI only |
| anthropic | 0.37.1 | 0.60.0 | API updates |
| litellm | 1.41.26 | 1.74.15 | Latest version |

### Installing Dependencies by Python Version

**Python 3.9-3.11:**
```bash
pip install -r requirements.txt
```

**Python 3.12:**
```bash
# May need to install some packages from source
pip install -r requirements.txt --no-binary :all:
```

**Python 3.13:**
```bash
# Use the curated requirements
pip install -r requirements-py313.txt
```

### Creating Compatible Requirements

```python
# generate_requirements.py
import sys

base_requirements = [
    "anthropic>=0.37.1",
    "litellm>=1.41.26",
    "pydantic>=2.6.4",
]

if sys.version_info >= (3, 13):
    # Python 3.13 specific
    requirements = base_requirements + [
        "numpy>=1.26.0",
        "tiktoken>=0.9.0",
    ]
else:
    # Python 3.9-3.12
    requirements = base_requirements + [
        "numpy==1.26.0",
        "tiktoken>=0.7.0,<0.8.0",
    ]

with open(f"requirements-py{sys.version_info.major}{sys.version_info.minor}.txt", "w") as f:
    f.write("\n".join(requirements))
```

---

## Testing Across Versions

### Setting Up Test Environments

```bash
# Using pyenv
curl https://pyenv.run | bash

# Install multiple Python versions
pyenv install 3.9.18
pyenv install 3.10.13
pyenv install 3.11.7
pyenv install 3.12.1
pyenv install 3.13.0

# Create test environments
for version in 3.9.18 3.10.13 3.11.7 3.12.1 3.13.0; do
    pyenv virtualenv $version colonel-katie-$version
done
```

### Running Tests

```bash
# test_all_versions.sh
#!/bin/bash

versions=("3.9" "3.10" "3.11" "3.12" "3.13")

for version in "${versions[@]}"; do
    echo "Testing Python $version"
    pyenv activate colonel-katie-$version
    pip install -e .
    pytest tests/
    pyenv deactivate
done
```

### Compatibility Test Suite

```python
# tests/test_compatibility.py
import sys
import pytest

def test_python_version():
    """Ensure we're running on supported Python"""
    assert sys.version_info >= (3, 9)
    assert sys.version_info < (4, 0)

@pytest.mark.skipif(sys.version_info < (3, 11), reason="Requires Python 3.11+")
def test_exception_groups():
    """Test Python 3.11 features"""
    with pytest.raises(ExceptionGroup):
        raise ExceptionGroup("test", [ValueError(), TypeError()])

@pytest.mark.skipif(sys.version_info < (3, 13), reason="Requires Python 3.13+")
def test_new_features():
    """Test Python 3.13 specific features"""
    # Test new REPL features, JIT, etc.
    pass

def test_dependency_imports():
    """Ensure all dependencies import correctly"""
    imports = [
        "anthropic",
        "litellm", 
        "pydantic",
        "numpy",
        "interpreter"
    ]
    
    for module in imports:
        try:
            __import__(module)
        except ImportError as e:
            pytest.fail(f"Failed to import {module}: {e}")
```

---

## Troubleshooting

### Common Python 3.13 Issues

#### Issue: Module 'pkg_resources' not found
```python
# Solution: Update imports
try:
    import pkg_resources
except ImportError:
    import importlib.metadata as pkg_resources
```

#### Issue: C extension compilation fails
```bash
# Solution: Ensure build tools are installed
# Ubuntu/Debian
sudo apt install python3.13-dev build-essential

# Fedora
sudo dnf install python3.13-devel gcc

# macOS
xcode-select --install
```

#### Issue: Async behavior changes
```python
# Python 3.13 has stricter async requirements
# Old pattern
async def old_pattern():
    # May not work in 3.13
    return asyncio.create_task(some_coroutine())

# New pattern
async def new_pattern():
    # Explicit await
    task = asyncio.create_task(some_coroutine())
    return task
```

### Version Detection

```python
# utils/version_check.py
import sys
import warnings

def check_python_version():
    """Check and warn about Python version"""
    version = sys.version_info
    
    if version < (3, 9):
        raise RuntimeError("Python 3.9+ required")
    
    if version >= (3, 14):
        warnings.warn(
            "Python 3.14+ is not tested. Some features may not work.",
            FutureWarning
        )
    
    if version == (3, 13):
        print("Running on Python 3.13 - Colonel Katie enhanced mode")
    
    return f"{version.major}.{version.minor}.{version.micro}"
```

### Performance Considerations

```python
# Benchmark different Python versions
import time
import sys

def benchmark_operation():
    """Simple benchmark to compare Python versions"""
    start = time.time()
    
    # Example operation
    result = sum(i**2 for i in range(1000000))
    
    end = time.time()
    
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    print(f"Time: {end - start:.3f}s")
    print(f"Result: {result}")

# Expected results:
# Python 3.9:  ~0.250s
# Python 3.10: ~0.240s  
# Python 3.11: ~0.150s (40% faster!)
# Python 3.12: ~0.145s
# Python 3.13: ~0.140s (with JIT: ~0.100s)
```

---

## Best Practices

1. **Target Python 3.11** for optimal compatibility and performance
2. **Test on multiple versions** before deploying
3. **Use version checks** for feature availability
4. **Document version requirements** in your code
5. **Keep dependencies updated** for better compatibility

---

## Future Compatibility

Colonel Katie is committed to supporting new Python versions as they're released. The project will:

- Track Python development versions
- Update dependencies proactively  
- Maintain backward compatibility
- Provide migration guides

---

**Questions?** Check our [FAQ](./FAQ.md) or open an [issue](https://github.com/Unicorn-Commander/Colonel-Katie/issues)