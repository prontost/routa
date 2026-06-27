"""i18n linter for work.html.

Fails if:
  (A) visible markup contains Cyrillic text in a tag without data-i/data-i-ph/
      data-i-title (applyLang won't translate it);
  (B) a key used in markup (data-i*) or in JS via T('key') is missing from the
      combined Routa + shared Avalone glossary seed.

Runs without importing project dependencies so it can be executed by the
system-Python pre-flight runner.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "src/routa/web/templates/work.html"
SEED = ROOT / "src/routa/core/glossary_seed.py"


def _find_portal_seed() -> Path | None:
    """Try to locate the shared Avalone glossary seed next to this repo."""
    candidates = list(ROOT.parent.glob("*/src/avalone_core/avalone_core/glossary_db.py"))
    return candidates[0] if candidates else None


def _extract_keys(text: str) -> set[str]:
    keys: set[str] = set()
    # Literal _row("key", "ru", "en", "ko", ...) calls used by Routa seed.
    keys |= set(re.findall(r'_row\(\s*"([^"]+)"\s*,', text))
    # Fallback for dict-style seeds: "key": "..."
    keys |= set(re.findall(r'"key"\s*:\s*"([^"]+)"', text))
    return keys


def _load_keys() -> set[str]:
    keys = _extract_keys(SEED.read_text(encoding="utf-8"))
    portal = _find_portal_seed()
    if portal:
        keys |= _extract_keys(portal.read_text(encoding="utf-8"))
    return keys


def main() -> int:
    html = TEMPLATE.read_text(encoding="utf-8")
    seed_keys = _load_keys()

    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    script = "\n".join(scripts)
    markup = re.sub(r"<script>.*?</script>", "", html, flags=re.S)

    errors: list[str] = []

    # --- (A) Cyrillic in visible markup without data-i* ---
    CYR = re.compile(r"[А-Яа-яЁё]")
    for m in re.finditer(r"<(h1|h2|h3|label|button|summary|option|b|p|span|div|a)\b([^>]*)>([^<]*)", markup):
        tag, attrs, text = m.group(1), m.group(2), m.group(3)
        if not CYR.search(text):
            continue
        if "data-i" in attrs:
            continue
        if tag == "option" and text.strip() in ("Русский", "English", "한국어"):
            continue
        line = markup[: m.start()].count("\n") + 1
        errors.append(f"(A) строка {line}: <{tag}> русский текст без data-i: {text.strip()[:50]!r}")
    for m in re.finditer(r'<(input|textarea)\b([^>]*placeholder="[^"]*[А-Яа-я][^"]*"[^>]*)>', markup):
        if "data-i-ph" not in m.group(2):
            line = markup[: m.start()].count("\n") + 1
            errors.append(f"(A) строка {line}: placeholder без data-i-ph")

    # --- (B) all used keys exist in seed ---
    used = set(re.findall(r'data-i(?:-ph|-title)?="([^"]+)"', markup))
    used |= set(re.findall(r"\bT\('([^']+)'\)", script))
    used |= set(re.findall(r'\bT\("([^"]+)"\)', script))
    used -= {"key", "ключ"}

    missing = sorted(used - seed_keys)
    for key in missing:
        errors.append(f"(B) ключ '{key}' отсутствует в глоссарии")

    if errors:
        print(f"✗ i18n-линтер: {len(errors)} проблем\n")
        for e in errors:
            print(" ", e)
        return 1
    print(f"✓ i18n-линтер чист: {len(used)} ключей покрыты, "
          f"непереведённой кириллицы в разметке нет")
    return 0


if __name__ == "__main__":
    sys.exit(main())
