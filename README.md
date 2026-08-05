# numerology

A Python library to calculate numerology (Tantric) factors from a birth date.

## Installation

Requirements: Python 3.10 or later. The package is published on PyPI:

```bash
pip install numerology-lib
```

For local development, install in editable mode instead:

```bash
pip install -e ".[dev]"
```

## Development Setup

It is recommended to work inside an isolated virtual environment:

### Windows (PowerShell)

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

Once the environment is active, install the package with its development
dependencies (pytest) in editable mode:

```bash
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

To leave the virtual environment:

```bash
deactivate
```

## Using in another project

Add it to your `requirements.txt`:

```
numerology-lib>=1.2.2
```

Or install the latest development version directly from the GitHub repository:

```bash
pip install git+https://github.com/soluniah/numerology-lib.git
```

## Usage

```python
from numerology import Numerology

numerology = Numerology("1978-10-21")

numerology.get_soul_number()      # {'value': 3, 'master': 0, 'karmic': 0}
numerology.get_karma_number()     # {'value': 10, 'master': 0, 'karmic': 0}
numerology.get_gift_number()      # {'value': 6, 'master': 0, 'karmic': 0}
numerology.get_destiny_number()   # {'value': 7, 'master': 0, 'karmic': 0}
numerology.get_path_number()      # {'value': 11, 'master': 11, 'karmic': 0}
numerology.get_support_number()   # 4
numerology.get_obstacle_number()  # 4
numerology.get_divisible_numbers()  # {'soul': 0, 'karma': 0}
numerology.get_personal_year()    # based on the current year
numerology.get_achievements_and_challenges()  # [{'achievement': 4, 'challenge': 2, 'from': 0, 'to': 25}, ...]
```

`get_personal_year()` uses the current real-world year by default. You can pass a
specific `current_year` to the constructor to make the calculation deterministic:

```python
numerology = Numerology("1978-10-21", current_year=2024)
```

## 🤝 Contributions

Contributions are welcome! Please read the [Contribution Guidelines](CONTRIBUTING.md) before submitting a Pull Request.

For more details, contact us at [omniconscientes@gmail.com].
