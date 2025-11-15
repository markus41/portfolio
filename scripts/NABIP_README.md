# NABIP Issues - Quick Start

## Purpose
This directory contains automation tools for creating GitHub issues for the NABIP website integration project.

## Files
- **`nabip_issues_config.json`**: Configuration file with all feature requests and sub-issues
- **`create_nabip_issues.py`**: Python script to create issues in GitHub

## Quick Start

### Prerequisites
1. Install GitHub CLI: `gh --version`
2. Authenticate: `gh auth login`

### Usage
```bash
# Preview issues
python scripts/create_nabip_issues.py --dry-run

# Create all issues
python scripts/create_nabip_issues.py
```

## Documentation
See `docs/NABIP_ISSUES_GUIDE.md` for complete documentation.

## Summary
- 3 feature requests
- 99 sub-issues
- 60+ custom agent mappings
- Comprehensive documentation

For details, see:
- `docs/NABIP_ISSUES_GUIDE.md` - Complete usage guide
- `docs/NABIP_SUMMARY.md` - Project overview  
- `docs/NABIP_AGENTS_REFERENCE.md` - Agent reference
