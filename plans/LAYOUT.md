# REY_PLL layout plan

## Target: one Tiny Tapeout tile

A 1x1 tile is 161 x 111.52 um (17 950 um2), see
`design/REY_PLL_SKY130A/tt_block_1x1_pg.def` (from lelo_temp_sky130a). We
follow lelo_temp's recipe:

- the core, REY_PLL, is laid out to fit the tile, 156.96 x 106.94 um, with
  its own supply rings and every tile pin on a met4 riser at its top edge
- the wrapper `tt_um_rey_pll_wulffern` is GENERATED, layout and schematic,
  by [py/gen_tt_um.py](../py/gen_tt_um.py) from the DEF and the core's
  ports. Never edit it by hand:

      python3 py/gen_tt_um.py design/REY_PLL_SKY130A

  It adds the two west met4 power rails (VDPWR x 0 to 2.0 um, VGND 2.4 to
  4.4 um, full height) with via stacks onto the core's rings, the signal
  routes to the met4 port pads on the top edge, an antenna diode on every
  input, and a tie-low through res_generic_m4 on every pad the PLL does
  not drive
- `make deliver` / `make precheck` (tech/make/core.make) copy gds, lef,
  spice and reports into the `tapeout/` submodule. The submodule does not
  exist yet

lelo_temp ships as `tiles: "1x1"` with `analog_pins: 0`; check that the
current shuttle still accepts that for an analog project.

## Pins

| TT pin       | Signal    | At lock (512 MHz)                                     |
|:-------------|:----------|:------------------------------------------------------|
| clk          | CK_REF    | 8 MHz reference                                       |
| ui_in[0]     | PWRUP_1V8 | powers the loop up, starts the kick pulse             |
| ui_in[3:1]   | TRIM[2:0] | oscillator bias trim, set per die                     |
| ui_in[4]     | OLH       | open loop, VCTRL to VDD_1V8: the oscillator's slowest |
| ui_in[5]     | OLL       | open loop, VCTRL to VSS: the oscillator's fastest     |
| uo_out[0]    | CK/8      | 64 MHz, may be more than the TT output path carries   |
| uo_out[1]    | CK/16     | 32 MHz                                                |
| uo_out[2]    | CK/32     | 16 MHz                                                |
| uo_out[3]    | CK/64     | 8 MHz, the PLL feedback clock, compare with CK_REF    |
| uo_out[7:4]  |           | tied low                                              |
| uio_out[7:0] |           | tied low                                              |
| uio_oe[7:0]  |           | tied low (the uio pins are inputs)                    |
| ui_in[7:6], uio_in[7:0], ena, rst_n | | not connected                          |

DIVN is a ripple chain of six flops: the PLL feedback is taken after the
sixth (/64), and four buffered taps feed the pins, so the pin load does not
slow the chain. The first plan had ten flops and a tap on every uo_out pin
(down to CK/1024); the top row of the floorplan was about 10 um too wide with
them, so the four flops that only fed pins went. CK/2 (256 MHz) and CK/4
(128 MHz) are left off, since the TT output path cannot carry them, and CK
itself (512 MHz) has no pad for the same reason.

With the PLL open (OLH or OLL) the taps also measure the free running
oscillator over TRIM, which is the per-die trim procedure: pick the code
whose CK/64 range, between OLH and OLL, has 8 MHz nearest its middle.

## Area budget (the estimate before layout)

Transistor cells are all 8 x 4 um (FIXED_BBOX 1600 x 800), RPPO2 is
8 x 20.8 um and HRPPO8 16 x 20.8 um.

| Block                | Content                                        | Estimate um2 |
|:---------------------|:-----------------------------------------------|-------------:|
| REY_PLL_ROSC         | ~66 transistors, taps and rings; 6 RPPO cells  | 5 000        |
| PFD + CP             | rey_tr cells, CP mirrors                       | 1 500        |
| DIVN (/1024)         | 10 x REYTR_DFRNQNX1, 8 output buffers (built: six flops, four buffers) | 1 600        |
| Loop filter, Icp 1.6uA | 8 x REYPLL_RCU (R 461 kOhm, C1 3.2 + C2 0.25 pF) | 2 700        |
| Routing, rings       |                                                | 3 000        |
| Total                |                                                | ~13 800 = 77 % |

The loop filter capacitors are MiM (REYATR_CAPX1, cap_mim_m3_1 4.8 x 5 um,
51.2 fF in an 8 x 8 um cell, so 0.8 fF/um2 of footprint), not MOS: MiM is
linear, so C1 does not depend on where VCTRL sits. MiM is met3/met4 and the
HRPPO resistor uses neither, so the cap bank sits on top of R and the
filter costs the larger of the two areas, not the sum.

C area grows with Icp and R area shrinks, so the footprint is smallest
where they meet. From `python3 py/pll.py --icp 1.3e-6` (N = 64,
fc = fref/20, PM 60 degrees, |Kvco| 235 MHz/V):

| Icp    | C1 (CAPX1)     | C2 (CAPX1)     | R        | MiM over R, % of tile |
|:------:|:--------------:|:--------------:|:--------:|:---------------------:|
| 1 uA   | 2.01 pF (40)   | 0.16 pF (4)    | 737 kOhm | 22 %                  |
| 1.3 uA | 2.62 pF (52)   | 0.20 pF (4)    | 567 kOhm | 20 %                  |
| 2 uA   | 4.03 pF (79)   | 0.31 pF (7)    | 369 kOhm | 31 %                  |

### REYPLL_RCU, the stacked unit cell

`cic/lpf.json`, compiled with `cd work && make cic` (cicpy compile against
rey_atr's resistor patterns, prefix REYPLL_):

- REYPLL_MIMU16: a 13 x 17.8 um MiM (473 fF, simulated tt) on a 16 x 20.8 um
  cell, plates 0.4 um and MiM 1.5 um from the edge as in CAPX1
- REYPLL_RCU: a `Layout::LayoutRotateCell`, which places every instance at
  the origin, holding one REYPLL_HRPPO8 (4 x 15.3 kOhm) and one MIMU16 on
  top. Ports P0..P3/N0..N3/BR on M1, A (bottom plate) on M4, B (top) on M5

Both are DRC clean and LVS "Circuits match uniquely". 1.4 fF/um2 of
footprint against 0.8 for CAPX1, and the resistor comes for free underneath.
In RCU cells (`python3 py/pll.py --icp 1.6e-6`):

| Icp    | R kOhm | R cells | C cells | Cells | um2  | Tile |
|:------:|:------:|:-------:|:-------:|:-----:|:----:|:----:|
| 1.3 uA | 567    | 10      | 7       | 10    | 3328 | 19 % |
| 1.6 uA | 461    | 8       | 8       | 8     | 2662 | 15 % |
| 2.0 uA | 369    | 7       | 10      | 10    | 3328 | 19 % |

At 1.6 uA: R is 30 of the 15.3 kOhm resistors (7.5 cells), C1 seven MiMs
(3.3 pF) and C2 one (0.47 pF against 0.25 pF; check the phase margin with
the real values, or make a smaller C2 unit).

C1 and C2 are referenced to VDD_1V8. Put the BOTTOM plate (met3, the one
with the parasitic to substrate) on VDD_1V8 and the top plate on VCTRL, so
the bottom plate parasitic does not couple VCTRL to VSS. In cicpy names the
CAPX1 plates are M4 (A, bottom) and M5 (B, top), see REY_LDO's `_Caps`,
which also draws the bank as a comb.

## Floorplan, as built (2026-11-11)

Every cell is a cicpy sidecar (`design/REY_PLL_SKY130A/<CELL>.py`) or
directed routes written by `py/gen_pll.py` into `cic/pll.json`; each file's
own header describes its floorplan. Hierarchical: a block is laid out,
routed and checked on its own, and the level over it places finished blocks
and routes only between them. No sidecar holds a coordinate.

```
tt_um_rey_pll_wulffern   161 x 111.52     rails west, pads on the top edge
  REY_PLL                156.96 x 106.94  mirrored in x, 2.66 um from the west edge
    top row:     PFD | CTRL | CP | DIVN | LPF
    channel:     6 um, eight M3 tracks (CK, VBP, VCTRL, VLPFZ)
    bottom row:  ROSC = bias | dig | stg0 stg6 stg1 stg5 stg2 stg4 stg3
```

| Cell               | Size (um)       | Content                                      |
|:-------------------|:----------------|:---------------------------------------------|
| REY_PLL            | 156.96 x 106.94 | two M1 rings round the whole, VSS inside VDD_1V8 |
| REY_PLL_ROSC       | 150.78 x 43.66  | seven interleaved stages, bias, output buffer |
| REY_PLL_ROSC_BIAS  | 74.96 x 36.80   | Vgs/R bias, trim ladder and switches         |
| REY_PLL_ROSC_STAGE | 8.96 x 40.60    | one ring stage                               |
| REY_PLL_LPF        | 66.04 x 45.28   | eight REYPLL_RCU (16 x 20.8 each)            |
| REY_PLL_DIVN       | 30.72 x 50.08   | three columns of two flops, four tap buffers |
| REY_PLL_PFD        | 19.94 x 40.40   | two mirrored columns                         |
| REY_PLL_CP         | 16.96 x 38.60   | NMOS under PMOS                              |
| REY_PLL_CTRL       | 9.90 x 26.72    | one column                                   |

The blocks of the top row carry no rings of their own: their supply rails
run along their tops and are strapped to the top's rings on M4. They stand
1.6 um apart (the cells' wells and implants reach 0.4 to 0.75 um past their
boxes), the pump 2.6 um from CTRL (n-well to n-well).

Changes the layout forced on the schematic:

- the trim resistor is REYATR_RES_36C2F0 units (15.3 kOhm), not RPPO2/RPPO4:
  the composite RPPO cells lost their bulk pin when cicpy split the cell
  into columns. Typical is unchanged within 0.3 %
- the output buffer stays REYTR_IVX1 + IVX4: a discrete 2C1F2 first stage
  loads the last ring node and slowed the ring by 20 %
- the divider has six flops and four taps, not ten and eight (see Pins)

Checks: every cell is clean in magic DRC and LVS ("Circuits match
uniquely"); REY_PLL and the wrapper are also clean in KLayout DRC, and the
wrapper in the antenna check.

Not done: the extracted core does not lock. The wiring on the ring nodes
(about 10 fF each, 7.4 fF of it inside a stage) slows the oscillator 2.4
times, to 265 MHz at trim code 3. The first plan was to extract the
oscillator before building on it; that was skipped. See
[HANDOFF.md](HANDOFF.md) for the numbers, the options and the build notes.
