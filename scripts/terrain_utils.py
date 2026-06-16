"""Terrain utilities for reading, rendering, and writing StarCraft map tiles."""

import struct
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image

from richchk.editor.richchk.rich_chk_editor import RichChkEditor
from richchk.io.mpq.starcraft_mpq_io_helper import StarCraftMpqIoHelper
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil
from richchk.model.richchk.dim.rich_dim_section import RichDimSection
from richchk.model.richchk.era.rich_era_section import RichEraSection
from richchk.model.richchk.era.tileset import StarCraftTileset
from richchk.model.richchk.mtxm.rich_mtxm_section import RichMtxmSection
from richchk.model.richchk.mtxm.rich_tile import RichTile
from richchk.model.richchk.rich_chk import RichChk

TILESET_DATA_DIR = Path(__file__).resolve().parent / "tileset_data"

TILESET_FILE_NAMES: dict[StarCraftTileset, str] = {
    StarCraftTileset.BADLANDS: "badlands",
    StarCraftTileset.SPACE_PLATFORM: "platform",
    StarCraftTileset.INSTALLATION: "install",
    StarCraftTileset.ASHWORLD: "ashworld",
    StarCraftTileset.JUNGLE: "jungle",
    StarCraftTileset.DESERT: "desert",
    StarCraftTileset.ICE: "ice",
    StarCraftTileset.TWILIGHT: "twilight",
}


class TilesetData:
    """Loaded tileset binary data needed for rendering tiles to images."""

    def __init__(
        self,
        tileset: StarCraftTileset,
        cv5: bytes,
        vx4: bytes,
        vr4: bytes,
        palette: np.ndarray,
    ) -> None:
        self.tileset = tileset
        self.cv5 = cv5
        self.vx4 = vx4
        self.vr4 = vr4
        self.palette = palette


def load_tileset(
    tileset: StarCraftTileset,
    tileset_data_dir: Optional[Path] = None,
) -> TilesetData:
    """Load tileset binary data for rendering.

    :param tileset: which tileset to load
    :param tileset_data_dir: directory containing .cv5/.vx4/.vr4/.wpe files
    :return: TilesetData with cv5, vx4, vr4, and palette arrays
    """
    data_dir = tileset_data_dir or TILESET_DATA_DIR
    name = TILESET_FILE_NAMES[tileset]
    cv5 = (data_dir / f"{name}.cv5").read_bytes()
    vx4 = (data_dir / f"{name}.vx4").read_bytes()
    vr4 = (data_dir / f"{name}.vr4").read_bytes()
    wpe_data = (data_dir / f"{name}.wpe").read_bytes()
    palette = np.zeros((256, 3), dtype=np.uint8)
    for i in range(256):
        palette[i, 0] = wpe_data[i * 4]
        palette[i, 1] = wpe_data[i * 4 + 1]
        palette[i, 2] = wpe_data[i * 4 + 2]
    return TilesetData(tileset=tileset, cv5=cv5, vx4=vx4, vr4=vr4, palette=palette)


def detect_tileset(map_path: str) -> StarCraftTileset:
    """Detect which tileset a .scx/.scm map uses.

    :param map_path: path to the StarCraft map file
    :return: the StarCraftTileset enum value
    """
    mpqio = StarCraftMpqIoHelper.create_mpq_io()
    chk = mpqio.read_chk_from_mpq(str(map_path))
    era = ChkQueryUtil.find_only_rich_section_in_chk(RichEraSection, chk)
    return era.tileset


def read_mtxm(map_path: str) -> tuple[list[list[int]], int, int]:
    """Read MTXM tile data from a .scx/.scm map file.

    :param map_path: path to the StarCraft map file
    :return: (grid, width, height) where grid is a 2D list of tile IDs grid[row][col]
        gives the tile ID at that position
    """
    mpqio = StarCraftMpqIoHelper.create_mpq_io()
    chk = mpqio.read_chk_from_mpq(str(map_path))
    dim = ChkQueryUtil.find_only_rich_section_in_chk(RichDimSection, chk)
    mtxm = ChkQueryUtil.find_only_rich_section_in_chk(RichMtxmSection, chk)
    w, h = dim.width, dim.height
    grid: list[list[int]] = []
    for y in range(h):
        row: list[int] = []
        for x in range(w):
            row.append(mtxm.tiles[y * w + x].id)
        grid.append(row)
    return grid, w, h


def read_mtxm_from_chk(chk: RichChk) -> tuple[list[list[int]], int, int]:
    """Read MTXM tile data from an already-parsed RichChk.

    :param chk: a parsed RichChk object
    :return: (grid, width, height) where grid is a 2D list of tile IDs
    """
    dim = ChkQueryUtil.find_only_rich_section_in_chk(RichDimSection, chk)
    mtxm = ChkQueryUtil.find_only_rich_section_in_chk(RichMtxmSection, chk)
    w, h = dim.width, dim.height
    grid: list[list[int]] = []
    for y in range(h):
        row: list[int] = []
        for x in range(w):
            row.append(mtxm.tiles[y * w + x].id)
        grid.append(row)
    return grid, w, h


def render_tile_id(
    tile_id: int,
    tileset_data: TilesetData,
) -> np.ndarray:
    """Render a single tile ID to a 32x32 RGB numpy array.

    :param tile_id: raw u16 tile value
    :param tileset_data: loaded tileset binary data
    :return: (32, 32, 3) uint8 numpy array
    """
    cv5 = tileset_data.cv5
    vx4 = tileset_data.vx4
    vr4 = tileset_data.vr4
    palette = tileset_data.palette

    group_idx = (tile_id >> 4) & 0x7FF
    subtile_idx = tile_id & 0xF
    cv5_off = group_idx * 52
    megatile_idx = struct.unpack_from("<16H", cv5, cv5_off + 20)[subtile_idx]
    tile = np.zeros((32, 32, 3), dtype=np.uint8)
    vx4_off = megatile_idx * 32
    minitile_refs = struct.unpack_from("<16H", vx4, vx4_off)
    for mt_y in range(4):
        for mt_x in range(4):
            ref = minitile_refs[mt_y * 4 + mt_x]
            vr4_idx = ref >> 1
            flip_h = ref & 1
            vr4_off = vr4_idx * 64
            for py in range(8):
                for px in range(8):
                    ci = vr4[vr4_off + py * 8 + px]
                    apx = (7 - px) if flip_h else px
                    tile[mt_y * 8 + py, mt_x * 8 + apx] = palette[ci]
    return tile


def render_tiles(
    grid: list[list[int]],
    tileset_data: TilesetData,
    scale: int = 1,
) -> Image.Image:
    """Render a 2D grid of tile IDs to a PIL Image.

    :param grid: 2D list of tile IDs, grid[row][col]
    :param tileset_data: loaded tileset binary data
    :param scale: multiply tile size (32px * scale per tile); use 1 for full resolution
    :return: PIL Image of the rendered terrain
    """
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    tile_px = 32 * scale
    img = np.zeros((h * tile_px, w * tile_px, 3), dtype=np.uint8)
    tile_cache: dict[int, np.ndarray] = {}
    for y in range(h):
        for x in range(w):
            tid = grid[y][x]
            if tid not in tile_cache:
                rendered = render_tile_id(tid, tileset_data)
                if scale != 1:
                    rendered = np.array(
                        Image.fromarray(rendered).resize(
                            (tile_px, tile_px), Image.LANCZOS
                        )
                    )
                tile_cache[tid] = rendered
            img[
                y * tile_px : (y + 1) * tile_px,
                x * tile_px : (x + 1) * tile_px,
            ] = tile_cache[tid]
    return Image.fromarray(img)


def replace_mtxm(
    grid: list[list[int]],
    input_map_path: str,
    output_map_path: str,
    overwrite_existing: bool = False,
) -> None:
    """Replace the MTXM terrain in a map and save a new map file.

    The input map is used as a template — all non-terrain sections (triggers, units,
    locations, etc.) are preserved. Only the MTXM tile data is replaced.

    :param grid: 2D list of tile IDs, grid[row][col]
    :param input_map_path: path to the source .scx/.scm map file
    :param output_map_path: path for the new map file to write
    :param overwrite_existing: if True, overwrite output_map_path if it exists
    """
    mpqio = StarCraftMpqIoHelper.create_mpq_io()
    chk = mpqio.read_chk_from_mpq(str(input_map_path))
    new_chk = replace_mtxm_in_chk(grid, chk)
    mpqio.save_chk_to_mpq(
        new_chk,
        str(input_map_path),
        str(output_map_path),
        overwrite_existing=overwrite_existing,
    )


def replace_mtxm_in_chk(
    grid: list[list[int]],
    chk: RichChk,
) -> RichChk:
    """Replace the MTXM terrain in a RichChk and return the new RichChk.

    :param grid: 2D list of tile IDs, grid[row][col]
    :param chk: the parsed RichChk to modify
    :return: new RichChk with the MTXM section replaced
    """
    tiles: list[RichTile] = []
    for row in grid:
        for tid in row:
            tiles.append(RichTile(_id=tid))
    new_mtxm = RichMtxmSection(_tiles=tiles)
    return RichChkEditor().replace_chk_section(new_mtxm, chk)


def render_map(
    map_path: str,
    scale: int = 1,
    tileset_data: Optional[TilesetData] = None,
) -> Image.Image:
    """Render an entire .scx/.scm map file to a PIL Image.

    :param map_path: path to the StarCraft map file
    :param scale: multiply tile size (32px * scale per tile)
    :param tileset_data: pre-loaded tileset data; auto-detected if not provided
    :return: PIL Image of the full map terrain
    """
    mpqio = StarCraftMpqIoHelper.create_mpq_io()
    chk = mpqio.read_chk_from_mpq(str(map_path))
    grid, w, h = read_mtxm_from_chk(chk)
    if tileset_data is None:
        era = ChkQueryUtil.find_only_rich_section_in_chk(RichEraSection, chk)
        tileset_data = load_tileset(era.tileset)
    return render_tiles(grid, tileset_data, scale=scale)
