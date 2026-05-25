# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- New commands

## [1.20.0] - 2026-04-18
### Added
- In session macros
- Add slop-generated documentation pages

### Removed
- Remove AI interface feature

## [1.19.4] - 2024-10-23
### Fixed
- Handle EOFError gracefully when cancelling an edit on both Windows and Unix input paths
- Fix re-entrant readline crash when user dismisses the confirm-exit prompt
### Changed
- Update documentation and improve docs generation scripts

## [1.19.3] - 2024-09-28
### Added
- Add confirm exit

### Fixed
- Fix missing newline for search and replace

## [1.19.2] - 2024-09-28
### Fixed
- Fix missing about file

## [1.19.1] - 2024-02-18
### Added
- Add `__about__.py` package metadata module with version, author, and license fields
### Changed
- Expose version string from `__about__` in CLI `--version` output
- Update coverage configuration and improve CI build scripts

## [1.19.0] - 2023-12-27
### Added
- Add `COMMENT` and `NOOP` commands for ed-compatibility and macro annotation
### Fixed
- Fix `save_on_crash` signature to pass exception type correctly
- Fix `BROWSE` command guard to avoid URL fetch when phrase is None
### Changed
- Tighten protocol types for `inputter` and `insert_document_inputter` constructor parameters
- Replace `null_printer` function with `NullPrinter` callable class

## [1.18.0] - 2023-12-14
### Added
- Add `WRITE` command alias for ed-script compatibility
- Add `Command.comment` field and format support for COMMENT and UNKNOWN commands
### Fixed
- Fix INSERT to correctly advance current line so sequential scripted inserts do not skip lines
- Fix document invariant to allow current_line at len+1 boundary during editing
- Fix cancel-out-of-edit log messages to include leading newline for clean display

## [1.17.0] - 2023-12-13
### Added
- Add `StringCommandGenerator` for in-memory headless command feeding
- Add `HistoryLog(persist=False)` mode for headless use without filesystem side-effects
- Add `WRITE` command skeleton for headless script compatibility
### Changed
- Expose `StringCommandGenerator` in the package public API

## [1.16.0] - 2023-12-12
### Changed
- Downgrade mistune dependency to restore compatibility with the rest of the toolchain
- Improve internal build and CI configuration

## [1.15.0] - 2023-12-11
### Added
- Prepare codebase for use as a library

## [1.14.0] - 2023-05-29
### Added
- Add experimental AI interface (`ai_interface.py`) for OpenAI-backed command generation
- Add `file_converters.py` module for document format conversion helpers
### Changed
- Migrate build from Pipenv to Poetry
- Migrate GitHub Actions workflow from YAML to updated format with Python matrix

## [1.13.0] - 2023-05-13
### Added
- Implement string commands

### Changed
- Add internationalization Makefile for future i18n support
- Improve pre-commit configuration and linting setup

## [1.12.0] - 2022-12-29
### Added
- Add Docker support
- Add random macro generator

### Fixed
- Fix DELETE to recover gracefully from out-of-bounds IndexError instead of crashing
- Fix COPY command to use structured `LineRange` argument instead of positional integers
- Fix line-range parser to clamp start value to 1 when a zero or negative index is supplied

## [1.11.0] - 2022-07-31
### Added
- Add `PrefillInputter` for pre-populated edit prompts
- Add `plain_printer` output helper that strips trailing newlines for consistent display
### Fixed
- Fix line-number display in LIST to use a local counter instead of mutating `current_line`
- Fix `to_slice` off-by-one so ranges include the end line
- Add `CRASH` command variant for internal error-recovery testing

## [1.10.0] - 2022-07-31
### Added
- Add `EditStatus` dataclass to report edit outcome (can_edit_again, line_edited, text)
- Switch contract library from `dpcontracts` to `icontract` with `DBC` base class
### Fixed
- Fix bugs surfaced by updated dependency versions
- Add `icontract` requires-annotation to `basic_types` data classes

## [1.8.0] - 2022-07-05
### Added
- Add logging support
- Add verbose mode
### Changed
- Improve vim mode behavior
- Improve echo output

## [1.7.0] - 2022-07-03
### Changed
- Improve mypy type coverage across main, parsers, and command sources modules
- Replace concrete class references in `Dedlin.__init__` with protocol types (`CommandGeneratorProtocol`, `StringGeneratorProtocol`)
- Switch prompt session style from monokai to borland theme

## [1.6.0] - 2022-07-02
### Changed
- Refactor document input handling into `document_sources.py` and remove `editable_input_prompt.py`
- Add hypothesis-based property tests for parser and document operations
- Expand test suite to cover macro runner scenarios

## [1.5.0] - 2022-06-25
### Added
- Add `CURRENT` and `PUSH` command variants
### Fixed
- Fix `list_doc` (renamed from `list`) off-by-one in page display
- Fix `spell` command to reset current_line to start of range before iterating
### Changed
- Make Phrases fields optional (second through fifth default to None)
- Update docopt version string in CLI entry point

## [1.4.0] - 2022-06-25
### Added
- Add vim mode
- Add arrow-up command history
### Fixed
- Fix file save so documents are actually written to disk
- Fix filesystem path bugs on initial file creation
### Changed
- Implement meta commands and macro file loading
- Add formatter for command round-trip serialization
- Make project cross-platform

[Unreleased]: https://github.com/matthewdeanmartin/dedlin/compare/v1.20.0...HEAD
[1.20.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.19.4...v1.20.0
[1.19.4]: https://github.com/matthewdeanmartin/dedlin/compare/v1.19.3...v1.19.4
[1.19.3]: https://github.com/matthewdeanmartin/dedlin/compare/v1.19.2...v1.19.3
[1.19.2]: https://github.com/matthewdeanmartin/dedlin/compare/v1.19.1...v1.19.2
[1.19.1]: https://github.com/matthewdeanmartin/dedlin/compare/v1.19.0...v1.19.1
[1.19.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.18.0...v1.19.0
[1.18.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.17.0...v1.18.0
[1.17.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.16.0...v1.17.0
[1.16.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.15.0...v1.16.0
[1.15.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.14.0...v1.15.0
[1.14.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.13.0...v1.14.0
[1.13.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.12.0...v1.13.0
[1.12.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.11.0...v1.12.0
[1.11.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.10.0...v1.11.0
[1.10.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.8.0...v1.10.0
[1.8.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/matthewdeanmartin/dedlin/compare/v1.3.0...v1.4.0
