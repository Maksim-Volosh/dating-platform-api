from pathlib import Path

OUTPUT_FILE = "project_dump.txt"

# Какие файлы включаем
INCLUDE_EXTENSIONS = {".py", ".txt", ".md", ".yml", ".yaml", ".ini"}

# Что игнорируем
IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "tests",
    "app",
    ".idea",
    ".pytest_cache",
    ".ruff_cache",
    ".vscode",
    "node_modules",
}

def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)

def main():
    root = Path.cwd()
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file()
        and p.suffix in INCLUDE_EXTENSIONS
        and not should_skip(p)
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for file in files:
            relative_path = file.relative_to(root)

            out.write(f"{relative_path}:\n")
            out.write("-" * 80 + "\n")

            try:
                content = file.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                out.write("[binary or non-utf8 file skipped]\n\n")
                continue

            out.write(content.rstrip())
            out.write("\n\n")

    print(f"✅ Project dumped into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
