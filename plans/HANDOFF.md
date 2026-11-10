# REY_PLL handoff (2026-11-10)

## Where it stands

The whole PLL is laid out with cicpy sidecars and checks clean:

| Cell              | Size (um)    | DRC | LVS   |
|:------------------|:-------------|:----|:------|
| REY_PLL (top)     | 209 x 155    | stale, see below |  |
| REY_PLL_ROSC      | 150.8 x 43.7 | OK  | match |
| REY_PLL_ROSC_BIAS | 75 x 36.8    | OK  | match |
| REY_PLL_ROSC_STAGE|              | OK  | match |
| REY_PLL_CP        | 17 x 38.6    | OK  | match |
| REY_PLL_DIVN      | 57.9 x 52.2  | OK  | match |
| REY_PLL_PFD       | 27.2 x 42.7  | OK  | match |
| REY_PLL_CTRL      | 17.3 x 29    | OK  | match |
| REY_PLL_LPF       | 73.4 x 49    | OK  | match |

DRC is magic. KLayout DRC (kdrc) has not been run on ROSC or the top.

Commits (both pushed):
- rey_pll_sky130a `c43658e` "REY_PLL top assembled, DRC and LVS clean"
- cicpy `e455c4a` on branch `fix/route-pad-spacing`. Earlier commits on
  that branch are `19234af` and `2e66d45`.

## The open problem: size

The tile is 161 x 111.52 um. lelo_temp's core is 154.52 x 110.95 in it.

### Step 1, the PFD: done

`pfd_layout` in `py/gen_pll.py`. Two mirrored columns (A: UP flop and its
reset latch, B: DN flop and latch, the two inverters), 21 directed routes
and no signal rings: 27.16 x 42.72 um, 1160 um2 against 3600. DRC clean,
LVS "Circuits match uniquely".

- Three trunk lanes per column: outer (cell edge to input pins, M2/M3,
  output to inputs), middle (between the input pins and the outputs,
  M2/M3, started from an input pin) and edge (M4/M5, input to input).
- Rows line up across the columns, so PWRUP_N, DN and RST each cross as
  one straight M5 bar between two input pins.
- Ports: UP and DN_N on the top edge (M3), CK_FB top (M4), CK_REF and
  PWRUP_1V8 bottom (M4). These sides are provisional.
- Pins A and B are swapped on XA3 and XA4 (symmetric gates), so the
  corner sims in step 4 cover it.
- `checkroutes` reports XA1/CKB shorted to XA1/CKN in every flop, in
  DIVN too. That is the checker, not the layout: LVS matches.

**The top is stale.** `REY_PLL.py` still routes to the old PFD's M5
rings (`_pfd_cp`, `_pwrup`, `_ck_fb`, the PFD supply strap), and
`REY_PLL.mag` was not rebuilt. It gets rewritten with the floorplan.

### Step 2, the floorplan: does not fit as planned

With the new PFD the height is met: ROSC 43.66 + channel 6 + DIVN 52.16
+ rings 6 is about 108 of 110.95. The width is not. The top row is

    DIVN 57.88 + PFD 27.16 + CTRL 17.26 + CP 18.56 + LPF 73.40 = 194.3

against about 151 inside the rings, and it is not a matter of
arrangement: the blocks sum to 15 511 um2, which is 86 % of the raw tile
and 98 % of what is left inside the top's rings, before any routing.

| Block | um2  | Of which rings and margins |
|:------|-----:|---------------------------:|
| ROSC  | 6583 | bias is 75 x 36.8 beside 43.66 tall stages; 13 x 34 empty over `dig` |
| LPF   | 3594 | 930 (the eight RCU cells are 64 x 41.6) |
| DIVN  | 3019 | 800 |
| PFD   | 1160 | 460 |
| CP    |  655 | |
| CTRL  |  500 | 290 |

What squeezing can give without touching the circuit, roughly:

- thinner block rings (`addRouteRings` widthmult 4 to 1 or 2): 900
- LPF without its M2 rings and M5 side rails: 700
- ROSC_BIAS rebuilt to the stages' height: 800

That is 2400 um2, leaving 13 100 (83 % inside the rings), and it needs a
packing that is not one row. Dropping divider taps 7 to 10 (two DIVN
columns) gives another 940. A 1x2 tile (161 x 225.76) fits what exists
today in three rows. This is waiting for the user's decision.

### Steps 3 and 4, unchanged

3. **TT wrapper.** Copy `gen_tt_um.py` from lelo_temp and route the IO
   pins to the edges: PWRUP_1V8, CK_REF, TRIM0-2, OLH, OLL, CK, CKO0-7.
   The wrapper's power rails are met4 (cicpy M5) at x 0 to 4.4 um, full
   height, so the core keeps M5 out of its west 4 um.
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
- `py/gen_pll.py` is the generator. `pfd_layout`, `divn_layout` and
  `lpf_layout` write the routes into `cic/pll.json`; `divn_layout`
  publishes CK_FB on the top edge.
- `cic/sky130A.tech` is the local tech file.
- cicpy changes:
  - `core/layoutcell.py`: promoteInstancePort with offset/jog,
    promoteRailPort and rail cut reuse.
  - `core/cut.py`: pad growth.
  - `core/rules.py`: getArea.
  - `core/sidecarcell.py`: the single-row channel.
  - `cic.py`: the `--tech` option.
