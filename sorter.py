
"""
Task 1: Recursive file copy & sort by extension.
"""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Recursively copy files and sort them into subfolders by extension.")
    parser.add_argument("source", type=Path, help="Path to source directory")
    parser.add_argument("dest", nargs="?", type=Path, default=Path("dist"), help="Path to destination directory (default: ./dist)")
    return parser.parse_args()

def safe_copy(src: Path, dst_dir: Path) -> None:
    dst_dir.mkdir(parents=True, exist_ok=True)
    name = src.name
    stem = src.stem
    suffix = src.suffix
    target = dst_dir / name
    i = 1
    while target.exists():
        target = dst_dir / f"{stem}__{i}{suffix}"
        i += 1
    shutil.copy2(src, target)

def ext_bucket(p: Path) -> str:
    return p.suffix.lower().lstrip(".") if p.suffix else "noext"

def walk_and_collect(src_dir: Path) -> list[Path]:
    files: list[Path] = []
    for path in src_dir.rglob("*"):
        try:
            if path.is_file():
                files.append(path)
        except OSError:
            continue
    return files

def main() -> None:
    args = parse_args()
    src: Path = args.source.resolve()
    dest: Path = args.dest.resolve()

    if not src.exists() or not src.is_dir():
        raise SystemExit(f"Source directory does not exist or is not a directory: {src}")

    try:
        dest.relative_to(src)
        raise SystemExit("Destination directory must not be inside the source directory.")
    except ValueError:
        pass

    files = walk_and_collect(src)
    errors: list[str] = []
    copied = 0

    for f in files:
        try:
            bucket = ext_bucket(f)
            safe_copy(f, dest / bucket)
            copied += 1
        except (PermissionError, FileNotFoundError, OSError) as e:
            errors.append(f"Skip {f}: {e}")

    print(f"Copied {copied} files into '{dest}'.")
    if errors:
        print("\nSome files were skipped:")
        for msg in errors:
            print(" -", msg)

if __name__ == "__main__":
    main()
