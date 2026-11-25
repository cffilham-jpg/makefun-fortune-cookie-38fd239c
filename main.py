"""Write a deterministic UTF-8 fortune and validate its exact bytes.
Honor the output directory, with a temporary fallback for an unwritable default.
"""

import hashlib
import os
from pathlib import Path
import tempfile


LINE = "May your next margin call be a butt dial."
CHAR_LIMIT = 160
WORD_LIMIT = 20


def _resolve_output_dir() -> Path:
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured is not None:
        output_dir = Path(configured)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir

    output_dir = Path("out")
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        if not os.access(output_dir, os.W_OK | os.X_OK):
            raise PermissionError("Default output directory is not writable")
    except OSError:
        return Path(tempfile.mkdtemp(prefix="makefun-fortune-"))
    return output_dir


def validate(path: Path) -> None:
    content = path.read_bytes()
    assert content == LINE.encode("utf-8"), "Output bytes changed"
    text = content.decode("utf-8")
    assert text == LINE
    assert 1 <= len(text) <= CHAR_LIMIT
    assert len(text.split()) <= WORD_LIMIT
    assert "\n" not in text and "\r" not in text
    assert not content.endswith((b"\n", b"\r"))
    assert text == text.strip()


def main() -> None:
    path = _resolve_output_dir() / "entry.txt"
    path.write_bytes(LINE.encode("utf-8"))
    validate(path)
    print(hashlib.sha256(LINE.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
