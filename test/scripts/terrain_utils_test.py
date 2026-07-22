"""Tests for scripts/terrain_utils.py."""

import sys
from pathlib import Path

# terrain_utils lives in scripts/, not in the installed package
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import numpy as np  # noqa: E402
import pytest  # noqa: E402
from terrain_utils import (  # noqa: E402
    TilesetData,
    load_tileset,
    read_mtxm_from_chk,
    render_tile_id,
    render_tiles,
    replace_mtxm_in_chk,
)

from richchk.io.chk.chk_io import ChkIo  # noqa: E402
from richchk.io.richchk.query.chk_query_util import ChkQueryUtil  # noqa: E402
from richchk.io.richchk.richchk_io import RichChkIo  # noqa: E402
from richchk.model.richchk.dim.rich_dim_section import RichDimSection  # noqa: E402
from richchk.model.richchk.era.tileset import StarCraftTileset  # noqa: E402
from richchk.model.richchk.mtxm.rich_mtxm_section import RichMtxmSection  # noqa: E402
from richchk.model.richchk.rich_chk import RichChk  # noqa: E402

from ..chk_resources import SCX_CHK_FILE  # noqa: E402


@pytest.fixture(scope="module")
def rich_chk() -> RichChk:
    decoded_chk = ChkIo().decode_chk_file(SCX_CHK_FILE)
    return RichChkIo().decode_chk(decoded_chk)


@pytest.fixture(scope="module")
def jungle_tileset() -> TilesetData:
    return load_tileset(StarCraftTileset.JUNGLE)


class TestLoadTileset:
    def test_it_loads_jungle_tileset(self) -> None:
        tsd = load_tileset(StarCraftTileset.JUNGLE)
        assert tsd.tileset == StarCraftTileset.JUNGLE
        assert len(tsd.cv5) > 0
        assert len(tsd.vx4) > 0
        assert len(tsd.vr4) > 0
        assert tsd.palette.shape == (256, 3)

    def test_it_loads_all_tilesets(self) -> None:
        for tileset in StarCraftTileset:
            tsd = load_tileset(tileset)
            assert tsd.tileset == tileset
            assert len(tsd.cv5) > 0
            assert tsd.palette.shape == (256, 3)


class TestReadMtxmFromChk:
    def test_it_reads_tiles_from_chk(self, rich_chk) -> None:
        grid, w, h = read_mtxm_from_chk(rich_chk)
        dim = ChkQueryUtil.find_only_rich_section_in_chk(RichDimSection, rich_chk)
        assert w == dim.width
        assert h == dim.height
        assert len(grid) == h
        assert all(len(row) == w for row in grid)

    def test_it_preserves_tile_ids(self, rich_chk) -> None:
        grid, w, h = read_mtxm_from_chk(rich_chk)
        mtxm = ChkQueryUtil.find_only_rich_section_in_chk(RichMtxmSection, rich_chk)
        for y in range(h):
            for x in range(w):
                assert grid[y][x] == mtxm.tiles[y * w + x].id


class TestRenderTileId:
    def test_it_returns_32x32_rgb_array(self, jungle_tileset) -> None:
        tile = render_tile_id(67, jungle_tileset)
        assert tile.shape == (32, 32, 3)
        assert tile.dtype == np.uint8

    def test_it_renders_different_tiles_differently(self, jungle_tileset) -> None:
        tile_a = render_tile_id(67, jungle_tileset)
        tile_b = render_tile_id(83, jungle_tileset)
        assert not np.array_equal(tile_a, tile_b)


class TestRenderTiles:
    def test_it_renders_grid_to_correct_dimensions(self, jungle_tileset) -> None:
        grid = [[67, 83], [70, 86]]
        img = render_tiles(grid, jungle_tileset)
        assert img.size == (64, 64)

    def test_it_renders_scaled_grid(self, jungle_tileset) -> None:
        grid = [[67, 83], [70, 86]]
        img = render_tiles(grid, jungle_tileset, scale=2)
        assert img.size == (128, 128)

    def test_it_renders_single_tile_grid(self, jungle_tileset) -> None:
        grid = [[67]]
        img = render_tiles(grid, jungle_tileset)
        assert img.size == (32, 32)


class TestReplaceMtxmInChk:
    def test_it_replaces_mtxm_tiles(self, rich_chk) -> None:
        grid, w, h = read_mtxm_from_chk(rich_chk)
        new_grid = [[0 for _ in range(w)] for _ in range(h)]
        new_grid[0][0] = 67
        new_grid[h - 1][w - 1] = 83
        new_chk = replace_mtxm_in_chk(new_grid, rich_chk)
        result_grid, rw, rh = read_mtxm_from_chk(new_chk)
        assert rw == w
        assert rh == h
        assert result_grid[0][0] == 67
        assert result_grid[h - 1][w - 1] == 83
        assert result_grid[1][1] == 0

    def test_it_round_trips_tiles(self, rich_chk) -> None:
        grid, w, h = read_mtxm_from_chk(rich_chk)
        new_chk = replace_mtxm_in_chk(grid, rich_chk)
        result_grid, rw, rh = read_mtxm_from_chk(new_chk)
        assert result_grid == grid
