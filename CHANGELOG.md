# Changelog

All notable changes to this project are documented in this file.

## [0.2.0] - 2026-02-27

### Added
- Versioned changelog for release tracking.
- Explicit canonical export surface for `robutils.tools`.
- Logger compatibility exports (`StreamHandler`, `get_logger`) for stable imports.
- PowerShell release helper script (`release.ps1`) to automate import and compile validation checks.

### Changed
- Bumped library version to `0.2.0`.
- Updated `README.md` to reflect current package structure and import paths.
- Updated examples to import `Hashtable` from `robutils.containers`.
- `rJournaler` core now imports from cleaned `robutils` package APIs directly.
- Added an explicit 0.1.x → 0.2.0 upgrade guide with old/new import mappings.
- Added a documented deprecation timeline section for planned 0.3.0 API tightening.
- Added a maintainer release checklist to standardize future versioning and validation flow.

### Fixed
- Circular import risk in package initialization by removing eager subpackage imports.
- Invalid math package container import path in `robutils.math.__init__`.
- Broken tools package exports (`DatabaseManager` naming and symbol mismatches).
- Markdown module import side effects (demo code no longer runs on import).
- Markdown heading regex warning in text markdown utilities.

### Removed
- Deprecated compatibility wrapper names in `robutils.tools.__init__`.
- Legacy alias exports that conflicted with canonical APIs.

## [0.1.0] - Initial Release

### Added
- Initial release of `robutils` with `text`, `math`, `tools`, and `containers` modules.
