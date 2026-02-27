# RobUtils

A comprehensive, production-ready Python utilities library providing robust tools for common programming tasks. RobUtils consolidates essential functionality for text processing, mathematical operations, data management, and system operations into a single, well-organized package.

## Overview

RobUtils is designed to reduce code duplication and provide reliable, thoroughly-tested utilities for everyday Python development. Whether you're building data pipelines, processing strings, performing calculations, or managing files, RobUtils has you covered.

**Version**: 0.2.0

## What's New in 0.2.0

- Package initialization is now lazy and safer (reduced circular import risk).
- `robutils.tools` now exposes a canonical API surface with consistent export names.
- Import-time demo side effects were removed from markdown utilities.
- `robutils.math` no longer re-exports container types.
- Added a versioned changelog at `CHANGELOG.md`.

### Breaking Changes (0.2.0)

- Use `from robutils.containers import Hashtable` instead of importing `Hashtable` from `robutils.math`.
- Deprecated compatibility names in older `robutils.tools` exports were removed; use canonical names from `filesystemManager`, `databaseManager`, and `passwordManager`.

## Upgrade Guide (0.1.x → 0.2.0)

Use this quick mapping to migrate existing code.

### Package imports

```python
# Old (0.1.x)
from robutils.math import Hashtable

# New (0.2.0)
from robutils.containers import Hashtable
```

### Tools: database manager

```python
# Old (0.1.x)
from robutils.tools import DBManager

# New (0.2.0)
from robutils.tools import DatabaseManager
```

### Tools: password helpers

```python
# Old (0.1.x)
from robutils.tools import generate_password, get_password_strength

# New (0.2.0)
from robutils.tools import generate_strong_password, calculate_entropy
```

### Tools: filesystem helpers

```python
# Old (0.1.x)
from robutils.tools import copy_file, move_file, delete_file, list_directory, find_files

# New (0.2.0)
from robutils.tools import copy_path, move_path, delete_path, list_directory_contents, walk_directory_contents
```

### Notes

- `robutils` package initialization is lazy in 0.2.0 to avoid circular imports.
- Prefer importing only the symbols you use instead of broad wildcard imports.

## Deprecation Timeline

### 0.2.x (Current)
- Canonical APIs are the supported long-term surface.
- Migration guide mappings in this document should be used for all new or updated code.

### 0.3.0 (Planned)
- Remove any remaining compatibility aliases that may still exist in downstream forks or consumer wrappers.
- Keep only canonical import paths for `robutils.tools`, `robutils.math`, `robutils.text`, and `robutils.containers`.

### Upgrade Policy
- Minor versions may include deprecations and migration guidance.
- Major behavioral removals are planned for the next minor cycle and documented in `CHANGELOG.md` first.

## Maintainer Release Checklist

Use this checklist for every robutils release.

- Update `robutils/__init__.py` version (`__version__`).
- Add or update release notes in `CHANGELOG.md` with `Added/Changed/Fixed/Removed` sections.
- Verify canonical exports in package `__init__.py` files (`robutils`, `tools`, `math`, `text`, `containers`).
- Run import smoke tests for major modules:
    - `import robutils`
    - `import robutils.text`
    - `import robutils.math`
    - `import robutils.tools`
    - `import robutils.containers`
- Run syntax validation for touched files using `py_compile`.
- Update `README.md` examples if any public API names changed.
- If there are breaking changes, update the Upgrade Guide section.

### Optional automation

Run the helper script to execute the import smoke tests and compile validation in one step:

```powershell
./release.ps1
```

To include `rJournaler` import checks as part of the run:

```powershell
./release.ps1 -IncludeAppImports
```

## Features

### 📝 Text Processing (`robutils.text`)
Complete text manipulation, analysis, and validation suite:
- **Analysis**: Word counting, frequency analysis, unique word extraction
- **Manipulation**: String reversal, case conversion (camelCase, snake_case, kebab-case, etc.), truncation, padding, URL encoding
- **Markdown**: Generate and parse Markdown tables, format text with bold/italic, link generation, element counting
- **Statistics**: Word/sentence/paragraph counting, character analysis, palindrome detection, substring operations
- **Validation**: Email/URL/UUID/IP address validation, character set checking, length constraints, HTML sanitization

**Example**:
```python
from robutils.text import (
    to_snake_case, count_words, is_valid_email,
    bold, italic, parse_markdown_table
)

# Text transformation
print(to_snake_case("HelloWorld"))  # hello_world

# Analysis
print(count_words("The quick brown fox"))  # 4

# Validation
print(is_valid_email("user@example.com"))  # True

# Markdown generation
print(bold("Important"))  # **Important**
```

### 🔢 Math & Numbers (`robutils.math`)
Mathematical utilities spanning multiple domains:

**Numbers**:
- **Fibonacci**: nth Fibonacci calculation, Fibonacci number detection
- **Prime Numbers**: Prime checking, generating primes up to a limit
- **Validation**: Integer/float checking, numeric range validation, perfect square detection, power-of-two checking, hexadecimal/binary/octal/Roman numeral validation, ISBN validation, UUID/IP address validation

**Measurements**:
- **Area**: Convert between all standard area units (sq_in, sq_ft, sq_yd, acre, sq_km, etc.), calculate triangle and circle areas
- **Distance**: Convert between imperial and metric units (inches, feet, miles, meters, kilometers, etc.)
- **Temperature**: Convert between Celsius, Fahrenheit, Kelvin, and Rankine
- **Volume**: Convert between imperial and metric volumes (cups, gallons, liters, milliliters, etc.)
- **Weight**: Convert between various weight units (ounces, pounds, grams, kilograms, tonnes, etc.)

**Example**:
```python
from robutils.math import (
    is_prime, get_primes_up_to,
    convert_distance, convert_temperature
)

# Prime numbers
print(is_prime(17))  # True
print(get_primes_up_to(20))  # [2, 3, 5, 7, 11, 13, 17, 19]

# Unit conversions
distance_km = convert_distance(5, 'mile', 'kilometer')
temp_f = convert_temperature(25, 'Celsius', 'Fahrenheit')

```

### 📦 Containers (`robutils.containers`)
Data structures and container utilities:
- **Hashtable**: Custom implementation with separate chaining, automatic resizing, and flexible API

**Example**:
```python
from robutils.containers import Hashtable

ht = Hashtable()
ht.put('key', 'value')
print(ht.get('key'))  # 'value'
```

### 🛠️ Tools & Utilities (`robutils.tools`)
Enterprise-grade tools for real-world applications:

**Configuration Management**:
- INI, JSON, and XML configuration file handling
- Dotted-path notation for nested access (e.g., `'database.host'`)
- Automatic file loading and saving

**CSV Management**:
- Read/write CSV files with custom delimiters and quoting
- In-memory data manipulation
- Advisory file locking for concurrent access safety

**Database Operations**:
- SQLite (built-in), MySQL, and PostgreSQL support
- Abstracted connection interface with common operations
- Advanced query construction (JOINs, WHERE clauses, ORDER BY, LIMIT)
- Connection pooling and error handling

**DateTime Management**:
- Comprehensive date/time operations using Python's standard library
- Timezone handling with fixed UTC offsets
- Formatting, parsing, and arithmetic operations
- US timezone abbreviations with daylight saving time awareness

**File System Operations**:
- Read/write files with atomic operations
- Directory creation, traversal, and cleanup
- File checksums and metadata retrieval
- Recursive file searching and tree generation

**Hashing & Security**:
- Support for all available algorithms (MD5, SHA-256, BLAKE2, etc.)
- HMAC calculations with optional keys
- File hashing with streaming for large files
- Password hashing with PBKDF2-HMAC-SHA256 and salting
- Secure password generation and strength validation

**Logging**:
- Multiple handlers (console, file, SQLite)
- Sophisticated filtering system (by level, logger name, context)
- Context-aware logging with optional metadata
- Formatted output with timestamps

**Example**:
```python
from robutils.tools import (
    CSVManager, DateTimeManager, HashTools,
    hash_password, verify_password,
    read_file_content, get_logger
)

# CSV handling
csv = CSVManager()
csv.add_row({'name': 'Alice', 'age': 30})
csv.save_to_file('data.csv')

# DateTime operations
dt = DateTimeManager()
iso_date = dt.to_iso8601('2025-01-15')

# Hashing
file_hash = HashTools.calculate_digest('myfile.txt', algorithm='sha256')

# Password security
hash_obj = hash_password('mypassword')
is_valid, new_hash = verify_password('mypassword', hash_obj)

# Logging
logger = get_logger('app')
logger.info('Application started', context={'version': '1.0'})
```

## Installation

### From Source
Clone the repository and install in development mode:

```bash
git clone https://github.com/roblammert/python_robutils.git
cd python_robutils
pip install -e .
```

### Direct Import
Simply copy the `robutils` directory to your project and import:

```python
import robutils
```

## Quick Start

### Basic Text Operations
```python
from robutils.text import to_snake_case, is_valid_email, bold

# Convert strings
result = to_snake_case("HelloWorld")  # "hello_world"

# Validate input
if is_valid_email(user_input):
    print("Valid email")

# Generate markup
heading = bold("Title")  # "**Title**"
```

### Numeric Operations
```python
from robutils.math import is_prime, convert_distance

# Check prime numbers
if is_prime(7):
    print("Prime number found")

# Convert units
meters = convert_distance(100, 'foot', 'meter')
```

### File and Configuration Management
```python
from robutils.tools import read_file_content, CSVManager

# Read files
content = read_file_content('input.txt')

# Manage CSV data
csv = CSVManager('data.csv')
for row in csv.get_all_rows():
    print(row)
```

## Package Structure

```
robutils/
├── text/                    # String processing and analysis
│   ├── analysis.py
│   ├── manipulate.py
│   ├── markdown.py
│   ├── statistics.py
│   └── validate.py
├── math/                    # Mathematical utilities
│   ├── measurements/        # Unit conversions
│   │   ├── area.py
│   │   ├── distance.py
│   │   ├── temperature.py
│   │   ├── volume.py
│   │   └── weight.py
│   ├── numbers/            # Numeric operations
│   │   ├── fibonacci.py
│   │   ├── prime.py
│   │   └── validate.py
├── containers/              # Data structures
│   └── hashtable.py
└── tools/                   # Utility tools
    ├── configFactory.py     # Configuration handling
    ├── CSVManager.py        # CSV operations
    ├── databaseManager.py   # Database connectivity
    ├── datetimeManager.py   # Date/time utilities
    ├── filesystemManager.py # File operations
    ├── HashTools.py         # Hashing utilities
    ├── logger.py            # Logging framework
    └── passwordManager.py   # Password security
```

## API Reference

For full release history and migration notes, see `CHANGELOG.md`.

### Text Module

#### Analysis
- `count_words(text: str) -> int` - Count words in text
- `get_unique_words(text: str) -> set` - Get unique words
- `get_word_frequency(text: str) -> dict` - Get word frequency counts

#### Manipulation
- `to_snake_case(text: str) -> str` - Convert to snake_case
- `to_camel_case(text: str, upper: bool = False) -> str` - Convert to camelCase or PascalCase
- `to_kebab_case(text: str) -> str` - Convert to kebab-case
- `truncate(text: str, max_length: int, suffix: str = '...') -> str` - Truncate with suffix
- `reverse_string(text: str) -> str` - Reverse string
- `slugify(text: str, separator: str = '-') -> str` - Create URL-friendly slug

#### Markdown
- `bold(text: str) -> str` - Format as bold markdown
- `italic(text: str) -> str` - Format as italic markdown
- `heading(text: str, level: int = 1) -> str` - Create markdown heading
- `parse_markdown_table(text: str) -> list[dict]` - Parse markdown table
- `generate_markdown_table(data: list[dict]) -> str` - Generate markdown table

#### Statistics
- `word_count(text: str) -> int` - Count words
- `char_count(text: str) -> int` - Count characters
- `sentence_count(text: str) -> int` - Count sentences
- `is_palindrome(text: str) -> bool` - Check if palindrome
- `average_word_length(text: str) -> float` - Calculate average word length

#### Validation
- `is_valid_email(email: str) -> bool` - Validate email format
- `is_valid_url(url: str) -> bool` - Validate URL
- `is_valid_uuid(uuid: str) -> bool` - Validate UUID
- `is_valid_ip_address(ip: str) -> bool` - Validate IP address
- `has_min_length(text: str, min_len: int) -> bool` - Check minimum length
- `has_max_length(text: str, max_len: int) -> bool` - Check maximum length
- `contains_only_allowed_chars(text: str, allowed: str) -> bool` - Validate character set

### Math Module

#### Numbers
- `is_prime(n: int) -> bool` - Check if prime
- `get_primes_up_to(limit: int) -> list` - Generate primes
- `get_nth_fibonacci(n: int) -> int` - Calculate nth Fibonacci
- `is_fibonacci(num: int) -> bool` - Check if Fibonacci number
- `is_perfect_square(n: int) -> bool` - Check if perfect square
- `is_power_of_two(n: int) -> bool` - Check if power of two

#### Measurements
- `convert_distance(value: float, from_unit: str, to_unit: str) -> float`
- `convert_temperature(value: float, from_unit: str, to_unit: str) -> float`
- `convert_volume(value: float, from_unit: str, to_unit: str) -> float`
- `convert_area(value: float, from_unit: str, to_unit: str) -> float`
- `convert_weight(value: float, from_unit: str, to_unit: str) -> float`
- `calculate_triangle_area(base: float, height: float) -> float`
- `calculate_circle_area(radius: float) -> float`

### Tools Module

#### Configuration
- `INIConfig(filepath)` - INI file configuration handler
- `JSONConfig(filepath)` - JSON file configuration handler
- `XMLConfig(filepath)` - XML file configuration handler

#### CSV Management
- `CSVManager(filepath=None, headers=None)` - CSV file manager
  - `load_from_file(filepath)` - Load CSV file
  - `save_to_file(filepath)` - Save to CSV file
  - `add_row(row_dict)` - Add data row
  - `get_all_rows()` - Get all rows

#### Database
- `DBManager.connect(db_type, config)` - Create database connection
  - Supports: `sqlite`, `mysql`, `postgresql`
- `execute(query, params)` - Execute query
- `fetch_all(query, params)` - Fetch all results
- `fetch_advanced(select_fields, table, join_clause, where_clause, order_by, limit)` - Advanced queries

#### DateTime
- `DateTimeManager()` - Datetime utility class
  - `to_iso8601(date_str)` - Convert to ISO 8601
  - `from_timestamp(timestamp)` - Create from Unix timestamp
  - `add_days(dt, days)` - Add days to date

#### File System
- `read_file_content(filepath)` - Read file content
- `write_file_content(filepath, content)` - Write file content
- `atomic_write_file_content(filepath, content)` - Atomic write
- `file_exists(filepath)` - Check if file exists
- `get_file_size(filepath)` - Get file size in bytes
- `get_file_checksum(filepath, algorithm='sha256')` - Get file hash
- `copy_file(src, dst)` - Copy file
- `delete_file(filepath)` - Delete file
- `create_directory(dirpath)` - Create directory
- `list_directory(dirpath)` - List directory contents
- `find_files(dirpath, pattern)` - Find files by pattern

#### Hashing
- `HashTools.calculate_digest(data, algorithm='sha256', key=None)` - Calculate hash
- `HashTools.get_algorithms()` - List available algorithms
- `HashTools.is_supported(algorithm)` - Check if algorithm supported

#### Password Security
- `hash_password(password: str) -> str` - Hash password with PBKDF2
- `verify_password(password: str, stored_hash: str) -> tuple[bool, str|None]` - Verify password
- `generate_password(length=16, use_special=True)` -> str` - Generate secure password
- `get_password_strength(password: str) -> str` - Evaluate password strength
- `is_strong_password(password: str) -> bool` - Check if password is strong

#### Logging
- `get_logger(name: str) -> Logger` - Get logger instance
- `logger.debug(message, context=None)` - Log debug message
- `logger.info(message, context=None)` - Log info message
- `logger.warning(message, context=None)` - Log warning message
- `logger.error(message, context=None)` - Log error message
- `logger.critical(message, context=None)` - Log critical message

## Testing

Run the included test suite:

```bash
python -m pytest test_*.py -v
```

Test files available:
- `test_area.py` - Area conversion tests
- `test_distance.py` - Distance conversion tests
- `test_temperature.py` - Temperature conversion tests
- `test_volume.py` - Volume conversion tests
- `test_weight.py` - Weight conversion tests

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup
```bash
git clone https://github.com/roblammert/python_robutils.git
cd python_robutils
pip install -e ".[dev]"
```

## License

This project is open source and available under the MIT License.

## Changelog

### Version 0.1.0 (Current)
- Initial release
- Text processing and analysis utilities
- Mathematical functions and unit conversions
- File system and configuration management
- Database connectivity abstractions
- Comprehensive logging framework
- Password security utilities
- Hashing and cryptographic functions

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/roblammert/python_robutils/issues).

## Author

**Rob Lammert**

Project: [python_robutils](https://github.com/roblammert/python_robutils)

---

**Note**: This is a general-purpose utility library designed for production use. All functions are thoroughly tested and designed to handle edge cases gracefully.
