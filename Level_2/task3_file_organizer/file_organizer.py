"""Automated File Organizer.

Sorts files in a target directory into subfolders by extension.
Never overwrites: name conflicts are resolved by appending _1, _2, ...

Usage:
    python file_organizer.py /path/to/folder            # organize
    python file_organizer.py /path/to/folder --dry-run  # preview only
"""

import argparse
import logging
import shutil
import sys
from pathlib import Path

LOG_FILE = "organizer.log"
NO_EXTENSION_FOLDER = "no_extension"

logger = logging.getLogger("file_organizer")


def setup_logging(log_path=LOG_FILE):
    """Log to both the console and a file."""
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
    for handler in (logging.StreamHandler(sys.stdout), logging.FileHandler(log_path, encoding="utf-8")):
        handler.setFormatter(fmt)
        logger.addHandler(handler)


def unique_destination(dest: Path) -> Path:
    """Return a path that does not exist yet, appending _1, _2... before the suffix."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem}_{counter}{dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def folder_for(file: Path) -> str:
    ext = file.suffix.lower().lstrip(".")
    return ext if ext else NO_EXTENSION_FOLDER


def organize(target: Path, dry_run: bool = False) -> dict:
    """Organize files directly inside `target`. Returns counts of moved/skipped/errors."""
    stats = {"moved": 0, "skipped": 0, "errors": 0}

    if not target.exists() or not target.is_dir():
        logger.error("Target is not a directory: %s", target)
        stats["errors"] += 1
        return stats

    try:
        files = [p for p in target.iterdir() if p.is_file() and not p.is_symlink()]
    except PermissionError:
        logger.error("No permission to read directory: %s", target)
        stats["errors"] += 1
        return stats

    if not files:
        logger.info("Nothing to organize: %s has no files.", target)
        return stats

    prefix = "[DRY RUN] " if dry_run else ""
    for file in sorted(files):
        if file.name == LOG_FILE:  # don't move our own log
            stats["skipped"] += 1
            continue
        dest_dir = target / folder_for(file)
        if dest_dir.exists() and not dest_dir.is_dir():
            logger.warning("Skipped %s: %s exists and is not a folder", file.name, dest_dir.name)
            stats["skipped"] += 1
            continue
        dest = unique_destination(dest_dir / file.name)
        try:
            if not dry_run:
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(file), str(dest))
            note = f" (renamed from {file.name})" if dest.name != file.name else ""
            logger.info("%sMOVED %s | from %s | to %s%s", prefix, file.name, file.parent, dest, note)
            stats["moved"] += 1
        except PermissionError:
            logger.error("Permission denied moving %s", file.name)
            stats["errors"] += 1
        except OSError as exc:
            logger.error("Failed to move %s: %s", file.name, exc)
            stats["errors"] += 1

    logger.info("%sSummary: %d moved, %d skipped, %d errors",
                prefix, stats["moved"], stats["skipped"], stats["errors"])
    return stats


def main(argv=None):
    parser = argparse.ArgumentParser(description="Sort files into subfolders by extension.")
    parser.add_argument("directory", type=Path, help="folder to organize")
    parser.add_argument("--dry-run", action="store_true", help="preview moves without changing anything")
    parser.add_argument("--log", default=LOG_FILE, help="log file path (default: organizer.log)")
    args = parser.parse_args(argv)
    setup_logging(args.log)
    stats = organize(args.directory, dry_run=args.dry_run)
    return 1 if stats["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
