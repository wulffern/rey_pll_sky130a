# REY_PLL handoff (2026-11-11)

## Where it stands

The PLL fits one Tiny Tapeout tile, and the core and the wrapper check
clean. **The extracted layout does not lock**: the oscillator runs at less
than half its schematic frequency, see "The open problem" below. The
layout is not ready for tapeout.

| Cell                   | Size (um)       | DRC | KLayout DRC | LVS   | Antenna |
|:-----------------------|:----------------|:----|:------------|:------|:--------|
| tt_um_rey_pll_wulffern | 161 x 111.52    | OK  | OK          | match | 0 errors |
| REY_PLL (core)         | 156.96 x 106.94 | OK  | OK          | match |         |
| REY_PLL_ROSC           | 150.78 x 43.66  | OK  |             | match |         |
| REY_PLL_ROSC_BIAS      | 74.96 x 36.80   | OK  |             | match |         |
| REY_PLL_ROSC_STAGE     | 8.96 x 40.60    | OK  |             | match |         |
| REY_PLL_LPF            | 66.04 x 45.28   | OK  |             | match |         |
| REY_PLL_DIVN           | 30.72 x 50.08   | OK  |             | match |         |
| REY_PLL_PFD            | 19.94 x 40.40   | OK  |             | match |         |
| REY_PLL_CP             | 16.96 x 38.60   | OK  |             | match |         |
| REY_PLL_CTRL           | 9.90 x 26.72    | OK  |             | match |         |

DRC is magic. KLayout DRC was run on the core and the wrapper, which hold
every block.

Commits (all pushed to `main`):

- `e02d2d0` REY_PLL_PFD as two mirrored columns
- `79468c7` Top re-floorplanned to fit one Tiny Tapeout tile
- `17a33aa` Tiny Tapeout wrapper tt_um_rey_pll_wulffern, generated
- cicpy `e455c4a` on branch `fix/route-pad-spacing`, unchanged since the
  first top

## How the size was met

The first top was 209 x 155 um, against a tile of 161 x 111.52. The
decision (user, 2026-11-10) was "squeeze, taps last": stay on a 1x1 tile,
first make the changes that leave the circuit alone, measure, and drop
divider taps only if it is still short.

Without touching the circuit:

- the blocks of the top row lost their own rings. Their supply rails run
  along their tops and are strapped on M4 to the top's two M1 rings
- PFD as two mirrored columns with directed routes, 19.94 x 40.40
- one row over the oscillator, PFD | CTRL | CP | DIVN | LPF, 1.6 um
  between blocks, a 6 um channel between the rows

It was still short: with ten divider stages the row was 162.8 um against
about 151 inside the rings. So the divider went from ten flops and eight
taps to six flops and four taps (CK/8 to CK/64). This changes the circuit
and the pins: uo_out[7:4] carry no tap and are tied low.

An earlier version of this file listed "ROSC_BIAS rebuilt to the stages'
height: 800 um2" among the savings. That saving did not exist, and it
was not needed.

## The wrapper

`py/gen_tt_um.py` writes `tt_um_rey_pll_wulffern.mag` and `.sch` from one
set of tables (PINS, ROUTES, TIED), the DEF and the core's ports.

- The core is used mirrored in x, 2.66 um from the west edge, so its ring
  columns face the wrapper's rails (VDPWR x 0 to 2.0, VGND 2.4 to 4.4 um).
  Each rail has one met1 to met4 pad onto its ring.
- Each route: the core's met4 riser, a met3 track under the pads, a met4
  drop into the pad. Inputs get a `diode_pw2nd_05v5` at the pad.
- Pin choices made without asking, change them in ROUTES if wanted:
  OLH on ui_in[4], OLL on ui_in[5]; CK (512 MHz) has no pad.
- uio_oe[7:0], uio_out[7:0] and uo_out[7:4] are tied to VGND, each through
  a 0.3 x 0.3 um res_generic_m4 (lelo_temp ties only uio_oe; an undriven
  output pad seemed worse than twelve more resistors).

## The open problem: the extracted oscillator is too slow

Typical corner (Ktt, 27 C, 1.8 V), trim code 3, `sim/REY_PLL`:

| View      | CK        | CK/64     | VCTRL   | Result |
|:----------|:----------|:----------|:--------|:-------|
| Schematic | 512.0 MHz | 8.000 MHz | 0.952 V | locks, ripple 8.5 mV |
| Extracted | 264.9 MHz | 4.139 MHz | 0 V     | no lock: the loop holds VCTRL at VSS, the oscillator's fastest |

The oscillator alone (`sim/REY_PLL_ROSC`, typical), CK at VCTRL = 0, its
fastest:

| Trim code | Schematic, MHz | Extracted, MHz |
|:---------:|:--------------:|:--------------:|
| 0         | 509            | 211            |
| 1         | 545            | 226            |
| 2         | 589            | 245            |
| 3         | 638            | 265            |
| 4         | 704            | 291            |
| 5         | 775            | 318            |
| 6         | 862            | 346            |
| 7         | 953            | 371            |

No code reaches 512 MHz. The bias is the same in both views (VBP 1.258 V,
VG 0.784 V at code 2), so it is the load on the ring nodes, not the
current. The C-only extraction puts about 10 fF of wiring on every ring
node (N6, which also drives the buffer, 12.8 fF):

- 7.4 fF is inside the stages (REY_PLL_ROSC_STAGE extracted alone: the
  input A 4.65 fF, the output Y 2.75 fF). 1.0 fF of each stage is A to
  Y, input to output of an inverter, so it counts about twice
- 2.7 fF is the routing between the stages in REY_PLL_ROSC

With the same current and 2.4 times slower, the devices' own load on a
ring node comes to about 7 fF, and the wiring more than doubles it. The
schematic simulations never had it: the oscillator was not simulated
extracted before the top was built.

The 7.4 fF inside a stage is not split further here, between the rey_atr
unit cells' own rails and the stage's routes. With the routing between
the stages gone altogether the ring would still be 2 times slow, so
shorter hops alone do not close it. The stages need about 2.4 times
their current at the same swing, or the loop a lower target. The
options, none started:

1. More current per stage from the same devices: a smaller R, or fewer
   units in the VBP diode. No area. R alone is weak: code 7 has 2.4
   times less R than code 0 and is 1.76 times faster. The mirrors run at
   a higher overdrive either way, and the MPB mirror had 39 mV of
   headroom at Kfs, -40 C, 1.7 V. Needs the 45 corner oscillator sweep
   again.
2. Five stages, not seven: 1.4 times, and two stage columns of room.
3. Lock at 256 MHz, N = 32 (the feedback after the fifth flop). Codes
   3 to 7 reach it in typical; it gives up the 512 MHz goal.

Whatever the choice: extract and sweep the oscillator (`make lpe
CELL=REY_PLL_ROSC` in `work/`, `cicsim run ... tran Lay ...` in
`sim/REY_PLL_ROSC`) before the top is rebuilt.

The corner runs on the extracted netlist were not started, since typical
already fails. The schematic corners in `sim/REY_PLL/results` are from
before the divider went to six flops; only typical was rerun.

## What else is left

1. **`make lpe` crashes in its last step.** The extraction writes
   `work/lpe/REY_PLL_lpe.spi`, then netgen (1.5.305) dies with a
   segmentation fault comparing the flat netlist against the schematic
   (379 devices and 208 nets on both sides when it dies). The same for
   REY_PLL_ROSC; REY_PLL_ROSC_STAGE runs through. The hierarchical
   LVS matches, so the layout is not in doubt, but `make typical VIEW=Lay`
   stops there. Run `cicsim run ... Lay ...` directly after `make lpe`
   has written the netlist. Not debugged.
2. **Tapeout.** There is no `tapeout/` submodule, so `make deliver` and
   `make precheck` cannot run. lelo_temp_sky130a is the model (`info.yaml`,
   `tiles: "1x1"`, `analog_pins: 0`); check that the shuttle still accepts
   that for an analog project.
3. `info.yaml` lists only REY_PLL_ROSC under `doc`.
4. **Start-up testbench.** `sim/REY_PLL_ROSC/startup.spi` runs on
   schematic with the new probes (four cases, all oscillate). It has
   not been run on the extracted netlist. One thing seen and not
   followed up: at code 0 the ring period 13 us after the ramp is
   22.5 ns per 10 periods with the 10 us supply ramp and 28.7 ns with
   the 100 ns ramp, at the same VG (0.766 V). Code 7 agrees between
   the ramps (15.5 ns).

## How to build

Generators, from the repository root:

    python3 py/gen_pll.py design/REY_PLL_SKY130A      # blocks and top schematic
    python3 py/gen_tt_um.py design/REY_PLL_SKY130A    # the wrapper

Then in `work/`:

    make cic                  # unit cells and digital blocks from cic/*.json
    make mag CELL=REY_PLL     # about 5 min for the top
    make drc CELL=REY_PLL
    make gds cdl lvs CELL=REY_PLL
    make kdrc CELL=REY_PLL
    make ant CELL=tt_um_rey_pll_wulffern

- Read LVS as the "Final result:" line of `work/lvs/<CELL>_lvs.log`. The
  16 "Netlists match uniquely with port errors" lines above it are the
  device cells and have always been there.
- xschem netlisting is intermittent. If LVS fails at readnet, or
  `cdl/<CELL>.spice` is missing, run `make cdl CELL=...` again.
- `work/Makefile` adds `mag: OPT += --tech ../cic/sky130A.tech`. That is a
  **local** copy of the tech file with `"area": 2400` on M4/M5. Never edit
  the shared `aicex/ip/tech_sky130A`.
- To locate a magic DRC error, write a tcl script with `drc listall why`.
  The extraction is in `lvs/<CELL>.spi`.
- `make mag` rewrites the timestamp of every `.mag` it touches. Restore
  the files whose only change is the timestamp before committing.
- A repository hook blocks `git add -A` / `.` / `--all`. Name the paths
  instead, for example `git add -u design py cic`.

## Simulation

`sim/REY_PLL/tran.spi` is the lock testbench: 16 us, the frequency of CK
and CK/64 and the VCTRL ripple measured over the last 2 us. Specs are in
`tran.yaml` (510 to 514 MHz, 7.97 to 8.03 MHz, ripple under 30 mV).

    cd sim/REY_PLL
    make typical              # schematic
    ./corners.sh              # schematic, 20 corners
    ./corners.sh Lay          # extracted, after make lpe in work/

The flat extracted netlist names an inner net after a block that has it
(`xblk_cp.VCTRL`, not `VCTRL`), so the testbenches (`sim/REY_PLL` and
`sim/REY_PLL_ROSC`) copy the inner nets they look at to top-level nodes
`P_<net>` with a unity VCVS per view, and measure those. If a rebuild
moves a name, the list is at PROBE in each `.spi`.

`trim.py` in `sim/REY_PLL_ROSC` reads the ring period (tpd) and prints
nothing for a code where ten periods do not fit the window; the table
above is from the CK period (tck) in the logs.

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
  `xspace=1.6` between blocks fixes it; two n-wells need 2.6.
- li->M5 stacks need the M4/M5 area rule. cicpy `Cut` grows the
  intermediate metal pads square to min area.
- A top-level render needs a GDS. A `.cic` from a build still in progress
  is stale.
- In magic, viali needs 0.06 um of met1 over it, and a met1 strap narrower
  than the stack pad it leaves makes a met1.2 notch against the diode's
  own met1. The wrapper's straps are as wide as their pads.
- TT precheck refuses a power pin with an nwell port (from lelo_temp), so
  the core stands in from the west edge.
- `checkroutes` reports XA1/CKB shorted to XA1/CKN in every flop. That is
  the checker, not the layout: LVS matches.
- The REY_LDO working tree has regenerated files that are not committed.
  Leave them for the user.

## Key files

- `design/REY_PLL_SKY130A/REY_PLL.py` is the top: the rows, the rings in
  beforeRoute, the PFD/CTRL->CP, CK_FB, channel and supply paths, and the
  pins' risers to the top edge in afterRoute.
- `design/REY_PLL_SKY130A/REY_PLL_ROSC.py`, `REY_PLL_ROSC_BIAS.py`,
  `REY_PLL_ROSC_STAGE.py` and `REY_PLL_CP.py` are the analog blocks.
- `py/gen_pll.py` is the generator. `pfd_layout`, `divn_layout`,
  `ctrl_layout` and `lpf_layout` write the routes into `cic/pll.json`.
- `py/gen_tt_um.py` is the wrapper generator.
- `cic/sky130A.tech` is the local tech file.
- cicpy changes (branch `fix/route-pad-spacing`):
  - `core/layoutcell.py`: promoteInstancePort with offset/jog,
    promoteRailPort and rail cut reuse.
  - `core/cut.py`: pad growth.
  - `core/rules.py`: getArea.
  - `core/sidecarcell.py`: the single-row channel.
  - `cic.py`: the `--tech` option.
