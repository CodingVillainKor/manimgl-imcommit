import sys, re
from pathlib import Path


def _update(path_str):
    path = Path(path_str)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    class_pat = re.compile(r"^class\s+\w+\s*\(([^)]*)\)\s*:")
    def_pat = re.compile(r"^(\s+)def\s+construct\s*\(")

    construct_ranges = []

    i = 0
    while i < len(lines):
        m = class_pat.match(lines[i])
        if m and ("InteractiveScene" in m.group(1) or "Scene2D" in m.group(1)):
            i += 1
            while i < len(lines):
                line = lines[i]
                stripped = line.lstrip()
                if stripped == "" or stripped.startswith("#"):
                    i += 1
                    continue
                if not line.startswith((" ", "\t")):
                    break
                dm = def_pat.match(line)
                if dm:
                    method_indent = dm.group(1)
                    start = i + 1
                    end = len(lines)
                    j = start
                    while j < len(lines):
                        l2 = lines[j]
                        s2 = l2.lstrip()
                        if s2 == "" or s2.startswith("#"):
                            j += 1
                            continue
                        l2_indent = l2[: len(l2) - len(s2)]
                        if len(l2_indent) <= len(method_indent):
                            end = j
                            break
                        j += 1
                    construct_ranges.append((start, end))
                    i = j
                    continue
                i += 1
        else:
            i += 1

    def in_construct(idx):
        return any(s <= idx < e for s, e in construct_ranges)

    new = [
        line
        for idx, line in enumerate(lines)
        if not (in_construct(idx) and line.strip() == "self.embed()")
    ]

    hash_idx = None
    for idx in range(len(new) - 1, -1, -1):
        if new[idx].strip().startswith("##"):
            hash_idx = idx
            break

    if hash_idx is not None:
        hl = new[hash_idx]
        indent = hl[: len(hl) - len(hl.lstrip())]
        new.insert(hash_idx, f"{indent}self.embed()\n")

    out = "".join(new)
    if out != text:
        path.write_text(out, encoding="utf-8")


_f = next((a for a in sys.argv if a.endswith(".py")), None)
if _f:
    _update(_f)
