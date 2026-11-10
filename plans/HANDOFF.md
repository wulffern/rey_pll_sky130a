# REY_PLL handoff (2026-11-10)

## Where it stands

The whole PLL is laid out with cicpy sidecars and checks clean:

| Cell              | Size (um)    | DRC | LVS   |
|:------------------|:-------------|:----|:------|
| REY_PLL (top)     | 209 x 155    | OK  | match |
| REY_PLL_ROSC      | 150.8 x 43.7 | OK  | match |
| REY_PLL_ROSC_BIAS | 75 x 36.8    | OK  | match |
| REY_PLL_ROSC_STAGE|              | OK  | match |
| REY_PLL_CP        | 17 x 38.6    | OK  | match |
| REY_PLL_DIVN      | 57.9 x 52.2  | OK  | match |
| REY_PLL_PFD       | 37.7 x 95.8  | OK  | match |
| REY_PLL_CTRL      | 17.3 x 29    | OK  | match |
| REY_PLL_LPF       | 73.4 x 49    | OK  | match |

DRC is magic. KLayout DRC (kdrc) has not been run on ROSC or the top.

Commits (both pushed):
- rey_pll_sky130a `c43658e` "REY_PLL top assembled, DRC and LVS clean"
- cicpy `e455c4a` on branch `fix/route-pad-spacing`. Earlier commits on
  that branch are `19234af` and `2e66d45`.

## The open problem: size

The top is 209 x 155 um, but the tile is 161 x 111.52 um (core about
155 x 110.5). The plan, in order:

1. **PFD rework.** The PFD is a 10 um column of cells inside ten M5 signal
   rings (`rtbl`, 1.02 um pitch), so it is 37.7 x 95.8 um. That height also
   sets the top row's height. Rebuild it as two mirrored columns, an UP
   half and a DN half (DFF, NR, OR, AN, IV), with directed paths instead of
   rings. That should come to about 1300 um2, against 3600 now.
2. **Re-floorplan the top** around the 150.8 um ROSC strip. The ROSC
   already fits the tile width. Squeeze the whitespace and reshape the LPF
   (73.4 x 49 is the next largest block).
3. **TT wrapper.** Copy `gen_tt_um.py` from lelo_temp and route the IO
   pins to the edges: PWRUP_1V8, CK_REF, TRIM0-2, OLH, OLL, CK, CKO0-7.
4. **Wrap-up.**
   - Run kdrc on the top.
   - Rerun the corner sims on the extracted netlist.
   - Update README, `plans/LAYOUT.md` and this file.

## How to build

Run these in `work/`:

    make mag CELL=REY_PLL     # about 18 min for the top
    make drc CELL=REY_PLL
    make lvs CELL=REY_PLL     # needs cdl/REY_PLL.spice
    make gds CELL=REY_PLL

- xschem netlisting is intermittent. If LVS fails at readnet, or
  `cdl/<CELL>.spice` is missing, run `make cdl CELL=...` again.
- `work/Makefile` adds `mag: OPT += --tech ../cic/sky130A.tech`. That is a
  **local** copy of the tech file with `"area": 2400` on M4/M5. Never edit
  the shared `aicex/ip/tech_sky130A`.
- To locate a magic DRC error, write a tcl script with `drc listall why`.
  The extraction is in `lvs/<CELL>.spi`.
- A repository hook blocks `git add -A` / `.` / `--all`. Name the paths
  instead, for example `git add -u design py cic`.

## Layout conventions (user's direction)

- Hierarchical: lay out and check the small cells, group them, route the
  groups, then route further up.
- No absolute coordinates or routes. Every path is anchored to a pin, a
  channel track, a ring or a whole number of PITCH from one.
- Supplies are routed by hand (`paths` to `rail_*`), not by the recipe.
- When an automatic route causes a DRC error, fix cicpy rather than
  patching the design. Rerun the cicpy unit tests (133) and check that
  REY_LDO stays clean afterwards.
- Commit and push at milestones, and keep the docs up to date.

## Gotchas found so far

- The rey_tr cells stand 0.75 um past their box, the stage guards 0.44 um
  and the pmos guards 0.4-0.7 um. Abutting blocks can short VDD to VSS.
  `xspace=1.6` fixes it; it is used for ROSC `dig` and stage ORDER[0], and
  top `blk_cp`.
- li->M5 stacks need the M4/M5 area rule. cicpy `Cut` grows the
  intermediate metal pads square to min area.
- A top-level render needs a GDS. A `.cic` from a build still in progress
  is stale.
- The REY_LDO working tree has regenerated files that are not committed.
  Leave them for the user.

## Key files

- `design/REY_PLL_SKY130A/REY_PLL.py` is the top: the rows, the rings in
  beforeRoute, and the PFD/CTRL->CP, CK_FB, channel and supply paths.
- `design/REY_PLL_SKY130A/REY_PLL_ROSC.py`, `REY_PLL_ROSC_BIAS.py` and
  `REY_PLL_CP.py` are the blocks.
- `py/gen_pll.py` is the generator. `divn_layout` publishes CK_FB on the
  top edge.
- `cic/sky130A.tech` is the local tech file.
- cicpy changes:
  - `core/layoutcell.py`: promoteInstancePort with offset/jog,
    promoteRailPort and rail cut reuse.
  - `core/cut.py`: pad growth.
  - `core/rules.py`: getArea.
  - `core/sidecarcell.py`: the single-row channel.
  - `cic.py`: the `--tech` option.
