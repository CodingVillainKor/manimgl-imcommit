# Runs tokenizer.py inside examples/.venv (py>=3.12) and returns results as JSON,
# so the manim env (py3.10) never has to import tokenizers itself.
import json
import subprocess
import sys
from functools import cache
from pathlib import Path

_DIR = Path(__file__).parent
_PY = _DIR / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
_VOCAB_CACHE = _DIR / "vocab_cache.json"


def _call(func: str, *args):
    code = (
        "import json, sys; import tokenizer; "
        f"print(json.dumps(tokenizer.{func}(*json.loads(sys.argv[1]))))"
    )
    out = subprocess.run(
        [str(_PY), "-c", code, json.dumps(args)],
        cwd=_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout
    return json.loads(out)


@cache
def tokenize(string: str) -> tuple[list[int], list[str]]:
    ids, tokens = _call("tokenize", string)
    return ids, tokens


@cache
def vocab() -> list[str]:
    # vocab is large and fixed, so keep it on disk to skip the subprocess on re-render
    if _VOCAB_CACHE.exists():
        return json.loads(_VOCAB_CACHE.read_text(encoding="utf-8"))
    v = _call("vocab")
    _VOCAB_CACHE.write_text(json.dumps(v), encoding="utf-8")
    return v
