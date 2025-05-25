# kicad-version-ctrl

## KiCad Git Version Control - Installation Guide

This guide will install the KiCad version control system into your existing PCB project repository.

## Quick Installation

Run these commands from your existing KiCad project root directory:

```bash
# 1. Download the main script
curl -o update_kicad_version.py https://raw.githubusercontent.com/MarkusVLA/kicad-version-ctrl/main/update_kicad_version.py

# 2. Download the pre-commit hook
curl -o .git/hooks/pre-commit https://raw.githubusercontent.com/MarkusVLA/kicad-version-ctrl/main/pre-commit

# 3. Make the hook executable
chmod +x .git/hooks/pre-commit

# 4. Test the installation
python3 update_kicad_version.py
```

## What This Does

- **Automatic version updates**: Every commit will update your `.kicad_pro` files with current git information
- **Text variables created**: `${GIT_TAG}`, `${GIT_SHORT_HASH}`, `${GIT_BRANCH}`, `${GIT_DATE}`, etc.
- **Silkscreen ready**: Place these variables on your PCB silkscreen for permanent version tracking

## Using in KiCad

1. Open your `.kicad_pcb` file
2. Add text to your silkscreen layer
3. Use variables like: `v${GIT_TAG} | ${GIT_SHORT_HASH}`
4. The text will automatically update with each commit

## Verification

```bash
# Check files are installed
ls -la update_kicad_version.py .git/hooks/pre-commit

# Test a commit
echo "# Version control test" >> README.md
git add README.md
git commit -m "Test version control"

# Check your .kicad_pro file for new text_variables section
```

## Troubleshooting

**Script fails?**
```bash
# Check Python version
python3 --version

# Test script manually
python3 update_kicad_version.py
```

**No .kicad_pro files found?**
- Make sure you're in your KiCad project root directory
- The script will find all `.kicad_pro` files in subdirectories too

**Want to disable temporarily?**
```bash
# Rename the hook to disable
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```

## Creating Releases

For production boards, create git releases:
```bash
git tag -a v1.0.0 -m "First production release"
git push origin v1.0.0
```

Your PCB silkscreen will show: `v1.0.0 | a1b2c3d`

## Available Text Variables

After installation, these variables will be available in your KiCad project:

| Variable | Description | Example |
|----------|-------------|---------|
| `${GIT_HASH}` | Full commit hash | `a1b2c3d4e5f6789...` |
| `${GIT_SHORT_HASH}` | Short commit hash | `a1b2c3d` |
| `${GIT_BRANCH}` | Current branch | `main` |
| `${GIT_TAG}` | Latest tag (if any) | `v1.0.0` |
| `${GIT_DATE}` | Commit date | `2024-03-15` |
| `${GIT_AUTHOR}` | Commit author | `John Doe` |
| `${GIT_DIRTY}` | Repository status | `clean` or `dirty` |

## Example Silkscreen Text

Common patterns for PCB silkscreen:

```
v${GIT_TAG} | ${GIT_SHORT_HASH}
${GIT_BRANCH}-${GIT_SHORT_HASH} ${GIT_DATE}
Rev ${GIT_TAG} (${GIT_SHORT_HASH})
```
