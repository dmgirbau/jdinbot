# Changelog

All notable changes to the JDINBot project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive docstrings to all database functions
- Logging for debugging database operations
- Better error handling in critical functions
- Connection pooling to improve performance

### Changed
- Updated `balance` function to consistently return a tuple
- Improved structure of database connection management
- Enhanced error messages for better debugging

### Fixed
- Database connection handling in all database operations
- `/tax` command now correctly deducts the specified amount from user balance
- Connection pool management to avoid "threads can only be started once" error
- Proper implementation of async context manager protocol
- Table references in gambling functions to use correct table name (`lojdin_statistics`)

## [1.0.0-pre.1] - 2025-03-26

### Added
- Initial pre-release version of JDINBot
- Telegram bot commands for token management
- Gambling system with multipliers
- User balance tracking
- Solana integration for token management