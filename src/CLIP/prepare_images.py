"""Dump ImageNet val images per class into src/clip/imagenette/.

Run once from the project root:  python src/clip/prepare_images.py

Uses Imagenette, a 10-class subset of ImageNet-1k, because torchvision's
ImageNet class can no longer download anything -- it requires a manual
~6.3 GB download from image-net.org behind a login. Imagenette pulls 341 MB
with no account, and the files are genuine ILSVRC2012_val_* images.
"""

from pathlib import Path

from PIL import Image
from torchvision.datasets import Imagenette

PROJECT = Path(__file__).resolve().parents[2]
DATA = PROJECT / "data"
OUT = PROJECT / "src" / "clip" / "imagenette"

# visually distinct ImageNet classes, mapped to (filename stem, how many)
WANTED = {
    "n02102040": ("springer", 5),  # English springer (dog)
    "n03028079": ("church", 5),  # church building
    "n03417042": ("truck", 1),  # garbage truck
    "n03888257": ("parachute", 1),  # parachute
}
SIZE = 384

DATA.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

ds = Imagenette(
    root=str(DATA),
    split="val",
    size="320px",
    download=not (DATA / "imagenette2-320").exists(),
)

idx_to_wnid = dict(enumerate(ds.wnids))

buckets = {wnid: [] for wnid in WANTED}
for path, label in ds._samples:
    wnid = idx_to_wnid[label]
    if wnid in buckets and len(buckets[wnid]) < WANTED[wnid][1]:
        buckets[wnid].append(path)
    if all(len(buckets[w]) == n for w, (_, n) in WANTED.items()):
        break

for wnid, paths in buckets.items():
    for i, path in enumerate(paths):
        img = Image.open(path).convert("RGB")
        # center square crop so every sample tiles at the same aspect ratio
        side = min(img.size)
        left = (img.width - side) // 2
        top = (img.height - side) // 2
        img = img.crop((left, top, left + side, top + side))
        img = img.resize((SIZE, SIZE), Image.LANCZOS)
        dst = OUT / f"{WANTED[wnid][0]}_{i}.png"
        img.save(dst)
        print(f"{dst.name}  <-  {Path(path).name}")

print()
for wnid, (name, _) in WANTED.items():
    print(f'"{name}": "{Imagenette._WNID_TO_CLASS[wnid][0]}",')
