"""Render a StarCraft .scx/.scm/.chk map file to a PNG image.

Usage:     python scripts/render_map.py <map_file> <tileset_dir> [output.png]

Arguments:     map_file     Path to a .scx, .scm, or .chk file     tileset_dir Directory
containing tileset files (*.cv5, *.vx4, *.vr4, *.wpe)     output.png   Output path
(default: <map_file>.png)

Example:     python scripts/render_map.py examples/maps/base-map.scx
.context/mpq/tileset

The tileset directory should contain files for all 8 tilesets:     badlands.cv5,
badlands.vx4, badlands.vr4, badlands.wpe     platform.cv5, platform.vx4, platform.vr4,
platform.wpe     install.cv5,  install.vx4,  install.vr4,  install.wpe     ashworld.cv5,
ashworld.vx4, ashworld.vr4, ashworld.wpe     jungle.cv5,   jungle.vx4,   jungle.vr4,
jungle.wpe     desert.cv5,   desert.vx4,   desert.vr4,   desert.wpe     ice.cv5,
ice.vx4,      ice.vr4,      ice.wpe     twilight.cv5, twilight.vx4, twilight.vr4,
twilight.wpe

These can be obtained from the bwmapgfx project:
https://github.com/dada78641/bwmapgfx/tree/main/resources/tileset

Requires: Pillow, numpy
"""

import argparse
import os
import struct
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

TILESET_NAMES = [
    "badlands",
    "platform",
    "install",
    "ashworld",
    "jungle",
    "desert",
    "ice",
    "twilight",
]


def load_tileset(
    tileset_dir: str, tileset_id: int
) -> tuple[np.ndarray, bytes, bytes, bytes]:
    name = TILESET_NAMES[tileset_id]
    base = os.path.join(tileset_dir, name)

    with open(f"{base}.wpe", "rb") as f:
        wpe = f.read()
    palette = np.array(
        [(wpe[i * 4], wpe[i * 4 + 1], wpe[i * 4 + 2]) for i in range(256)],
        dtype=np.uint8,
    )

    with open(f"{base}.cv5", "rb") as f:
        cv5 = f.read()
    with open(f"{base}.vx4", "rb") as f:
        vx4 = f.read()
    with open(f"{base}.vr4", "rb") as f:
        vr4 = f.read()

    return palette, cv5, vx4, vr4


def extract_chk_from_mpq(map_path: str) -> bytes:
    from richchk.io.mpq.starcraft_mpq_io_helper import StarCraftMpqIoHelper
    from richchk.model.mpq.stormlib.stormlib_archive_mode import StormLibArchiveMode

    mpq_io = StarCraftMpqIoHelper.create_mpq_io()
    wrapper = mpq_io._stormlib_wrapper
    archive = wrapper.open_archive(map_path, StormLibArchiveMode.STORMLIB_READ_ONLY)

    from richchk.util.fileutils import CrossPlatformSafeTemporaryNamedFile

    with CrossPlatformSafeTemporaryNamedFile() as tmp:
        wrapper.extract_file(
            archive, "staredit\\scenario.chk", tmp, overwrite_existing=True
        )
        wrapper.close_archive(archive)
        with open(tmp, "rb") as f:
            return f.read()


def parse_chk(
    data: bytes,
) -> tuple[int, int, int, tuple[int, ...] | None]:
    pos = 0
    mtxm_tiles = None
    map_w = map_h = 0
    tileset_id = 0
    while pos < len(data) - 8:
        name = data[pos : pos + 4].decode("utf-8", errors="replace")
        size = struct.unpack_from("<I", data, pos + 4)[0]
        if name == "DIM ":
            map_w, map_h = struct.unpack_from("<HH", data, pos + 8)
        elif name == "ERA ":
            tileset_id = struct.unpack_from("<H", data, pos + 8)[0]
        elif name == "MTXM":
            n = size // 2
            mtxm_tiles = struct.unpack_from(f"<{n}H", data, pos + 8)
        pos += 8 + size
    return map_w, map_h, tileset_id, mtxm_tiles


def render_map(
    map_w: int,
    map_h: int,
    mtxm_tiles: tuple[int, ...],
    palette: np.ndarray,
    cv5: bytes,
    vx4: bytes,
    vr4: bytes,
) -> Image.Image:
    img = np.zeros((map_h * 32, map_w * 32, 3), dtype=np.uint8)
    cv5_len = len(cv5)
    vx4_len = len(vx4)
    vr4_len = len(vr4)

    t0 = time.time()
    for ty in range(map_h):
        for tx in range(map_w):
            tile_id = mtxm_tiles[ty * map_w + tx]
            group_idx = (tile_id >> 4) & 0x7FF
            subtile_idx = tile_id & 0xF

            cv5_off = group_idx * 52
            if cv5_off + 52 > cv5_len:
                continue
            megatile_idx = struct.unpack_from("<16H", cv5, cv5_off + 20)[subtile_idx]

            vx4_off = megatile_idx * 32
            if vx4_off + 32 > vx4_len:
                continue
            minitile_refs = struct.unpack_from("<16H", vx4, vx4_off)

            base_y = ty * 32
            base_x = tx * 32
            for mt_y in range(4):
                for mt_x in range(4):
                    ref = minitile_refs[mt_y * 4 + mt_x]
                    vr4_idx = ref >> 1
                    flip_h = ref & 1
                    vr4_off = vr4_idx * 64
                    if vr4_off + 64 > vr4_len:
                        continue
                    for py in range(8):
                        for px in range(8):
                            ci = vr4[vr4_off + py * 8 + px]
                            apx = (7 - px) if flip_h else px
                            img[
                                base_y + mt_y * 8 + py, base_x + mt_x * 8 + apx
                            ] = palette[ci]

        if ty % 32 == 0 and ty > 0:
            elapsed = time.time() - t0
            pct = ty / map_h * 100
            print(f"  {pct:.0f}% ({ty}/{map_h} rows, {elapsed:.1f}s)")

    elapsed = time.time() - t0
    print(f"  100% ({map_h}/{map_h} rows, {elapsed:.1f}s)")
    return Image.fromarray(img)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render a StarCraft map file to a PNG image."
    )
    parser.add_argument("map_file", help="Path to .scx, .scm, or .chk file")
    parser.add_argument(
        "tileset_dir", help="Directory containing tileset files (cv5, vx4, vr4, wpe)"
    )
    parser.add_argument(
        "output", nargs="?", default=None, help="Output PNG path (default: <map>.png)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.map_file):
        print(f"Error: map file not found: {args.map_file}")
        sys.exit(1)
    if not os.path.isdir(args.tileset_dir):
        print(f"Error: tileset directory not found: {args.tileset_dir}")
        sys.exit(1)

    output = args.output or Path(args.map_file).stem + ".png"

    ext = Path(args.map_file).suffix.lower()
    if ext in (".scx", ".scm"):
        print(f"Extracting CHK from {args.map_file}...")
        chk_data = extract_chk_from_mpq(args.map_file)
    elif ext == ".chk":
        with open(args.map_file, "rb") as f:
            chk_data = f.read()
    else:
        print(f"Error: unsupported file type: {ext}")
        sys.exit(1)

    map_w, map_h, tileset_id, mtxm_tiles = parse_chk(chk_data)
    if mtxm_tiles is None:
        print("Error: no MTXM section found in CHK data")
        sys.exit(1)

    tileset_name = TILESET_NAMES[tileset_id]
    print(
        f"Map: {map_w}x{map_h} tiles ({map_w * 32}x{map_h * 32} px), tileset: {tileset_name}"
    )

    palette, cv5, vx4, vr4 = load_tileset(args.tileset_dir, tileset_id)
    print(f"Loaded tileset: {tileset_name}")

    print("Rendering...")
    img = render_map(map_w, map_h, mtxm_tiles, palette, cv5, vx4, vr4)

    img.save(output)
    size = os.path.getsize(output)
    print(f"Saved: {output} ({size:,} bytes)")


if __name__ == "__main__":
    main()
