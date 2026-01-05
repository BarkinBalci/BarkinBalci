#!/usr/bin/env python3

import random
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO_ROOT = Path(__file__).parent.parent
GOPHERS_DIR = REPO_ROOT / "gophers"
README_PATH = REPO_ROOT / "README.md"

GOPHER_START_MARKER = "<!-- GOPHER_START -->"
GOPHER_END_MARKER = "<!-- GOPHER_END -->"

SPECIAL_GOPHERS = {
    (2, 14): "heart-hug.svg",
    (1, 21): "birthday.svg",
}

def get_all_gophers() -> list[str]:
    """Get all gopher SVG files from the gophers directory."""
    return sorted([f.name for f in GOPHERS_DIR.glob("*.svg")])

def get_current_gopher() -> str:
    """Extract the current gopher filename from README.md."""
    content = README_PATH.read_text(encoding='utf-8')
    match = re.search(r'\./gophers/([^"]+)', content)
    if not match:
        raise ValueError("Could not find gopher in README.md")
    return match.group(1)

def get_regular_gophers() -> list[str]:
    """Get all non-special gopher SVG files."""
    all_gophers = get_all_gophers()
    special_files = set(SPECIAL_GOPHERS.values())
    return [g for g in all_gophers if g not in special_files]

def select_gopher() -> str:
    """Select a gopher based on the current date."""
    today = datetime.now(ZoneInfo("Etc/GMT-3"))
    date_key = (today.month, today.day)

    if date_key in SPECIAL_GOPHERS:
        return SPECIAL_GOPHERS[date_key]

    available_gophers = get_regular_gophers()
    current_gopher = get_current_gopher()

    candidates = [g for g in available_gophers if g != current_gopher]
    return random.choice(candidates if candidates else available_gophers)

def update_readme(gopher_file: str) -> None:
    """Update the README.md with the selected gopher."""
    try:
        content = README_PATH.read_text(encoding='utf-8')

        gopher_markdown = f'<img src="./gophers/{gopher_file}" height="300" alt="Daily Gopher">'

        start_idx = content.index(GOPHER_START_MARKER) + len(GOPHER_START_MARKER)
        end_idx = content.index(GOPHER_END_MARKER)
        new_content = content[:start_idx] + f"\n{gopher_markdown}\n" + content[end_idx:]

        README_PATH.write_text(new_content, encoding='utf-8')
        print(f"Updated README with: {gopher_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    gopher = select_gopher()
    update_readme(gopher)
    print(f"GOPHER_FILE={gopher}")
