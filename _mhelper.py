import sys, pyperclip

try:
    checkpoint_paste
except NameError:
    raise SystemExit  # not in manimgl session

_f = next((a for a in sys.argv if a.endswith(".py")), None)
if not _f:
    raise SystemExit

with open(_f, encoding="utf-8") as _fh:
    _lines = _fh.readlines()

for _i in range(len(_lines) - 1, -1, -1):
    if _lines[_i].strip().startswith("#"):
        pyperclip.copy("".join(_lines[_i:]))
        break

checkpoint_paste()
