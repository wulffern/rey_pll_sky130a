# REY_PLL layout plan

## Target: one Tiny Tapeout tile

A 1x1 tile is 161 x 111.52 um (17 950 um2), see `tt_block_1x1_pg.def`
in lelo_temp_sky130a. We follow lelo_temp's recipe:

- the core, REY_PLL, is laid out to fit the tile, about 155 x 110.5 um,
  with its own supply rings
- the wrapper `tt_um_rey_pll_wulffern.mag` is GENERATED from the DEF (copy
  `design/LELO_TEMP_SKY130A/gen_tt_um.py`). It adds two west met4 power
  rails with via stacks onto the core rings, the signal routes to the met4
  port pads on the top edge, antenna diodes on the inputs, and the uio_oe
  tie-low through res_generic_m4
- `make deliver` / `make precheck` (tech/make/core.make) copy gds, lef,
  spice and reports into the `tapeout/` submodule

lelo_temp ships as `tiles: "1x1"` with `analog_pins: 0`; check that the
current shuttle still accepts that for an analog project.

## Pins (proposal)

| TT pin     | Signal   | At lock (512 MHz)                                         |
|:-----------|:---------|:----------------------------------------------------------|
| clk        | CK_REF   | 8 MHz reference                                           |
| ui_in[0]   | PWRUP    | powers the bias and the oscillator up                     |
| ui_in[3:1] | TRIM     | oscillator bias trim, set per die                         |
| uo_out[0]  | CK/8     | 64 MHz, may be more than the TT output path carries       |
| uo_out[1]  | CK/16    | 32 MHz                                                    |
| uo_out[2]  | CK/32    | 16 MHz                                                    |
| uo_out[3]  | CK/64    | 8 MHz, the PLL feedback clock, compare with CK_REF        |
| uo_out[4]  | CK/128   | 4 MHz                                                     |
| uo_out[5]  | CK/256   | 2 MHz                                                     |
| uo_out[6]  | CK/512   | 1 MHz                                                     |
| uo_out[7]  | CK/1024  | 500 kHz                                                   |

All eight uo_out pins carry a divider tap, so the oscillator can be measured
at as many ratios as the pins allow. DIVN is a ripple chain of ten flops:
the PLL feedback is taken after the sixth (/64), and the four flops after it
only feed the pins. Every tap gets its own output buffer, so the pin load
does not slow the chain. CK/2 (256 MHz) and CK/4 (128 MHz) are left off,
since the TT output path cannot carry them. If the shuttle's I/O turns out
faster than expected, shift the window down one step.

With the PLL open (VCTRL forced) the taps also measure the free running
oscillator over TRIM, which is the per-die trim procedure: pick the code
whose CK/64 lands closest to 8 MHz.

## Area budget

Transistor cells are all 8 x 4 um (FIXED_BBOX 1600 x 800), RPPO2 is
8 x 20.8 um and HRPPO8 16 x 20.8 um.

| Block                | Content                                        | Estimate um2 |
|:---------------------|:-----------------------------------------------|-------------:|
| REY_PLL_ROSC         | ~66 transistors, taps and rings; 6 RPPO cells  | 5 000        |
| PFD + CP             | rey_tr cells, CP mirrors                       | 1 500        |
| DIVN (/1024)         | 10 x REYTR_DFRNQNX1, 8 output buffers          | 1 600        |
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

## REY_PLL_ROSC floorplan (cicpy sidecar)

`design/REY_PLL_SKY130A/REY_PLL_ROSC.py`, a SidecarCell. Two rows, because
an nmos column abutted to a pmos one breaks the well rules (REY_LDO):

```
top row (n-well):    p_bias | p_st0 | p_st1 | ... | p_st6 | p_out
bottom row (p-sub):  n_bias | n_sw  | n_st0 | ... | n_st6 | n_out | r_lad
```

- `p_st<k>`, one column per stage, bottom to top: inverter PMOS xip<k>
  (drain N<k>, nearest the nmos row), VCTRL device xmpv<k>, tunable mirror
  xmpc<k>, fixed mirrors xmpf<k>. VS<k> and NC<k> stay inside the column;
  VBP and VCTRL run as gate rails on the tab lane
- `n_st<k>` under it: xin<k>. The ring nodes N<k-1>/N<k> are the only nets
  between stage columns, plus the wrap N6 -> stage 0, one channel track
- `p_bias`: xmp0 diodes, xmpb mirror, xms1. `n_bias`: xmn1, xmn2 followers
- `n_sw`: startup xms2/xms3 and trim switches xst
- `r_lad`: the RPPO ladder, mirrored and ascending as in REY_LDO's `_ResCol`
- supplies through the guard (`addPowerGuardConnection`), not straps

Before the first `make mag`, the generator needs:

1. lowercase instance names (cicpy groups by `^(x\D+)`, and the conventions
   say lowercase), named per column: xip<k>, xmpv<k>, xmpc<k>, xmpf<k>_<j>,
   xin<k>, ...
2. the output buffer (REYTR_IVX1/IVX4) as discrete rey_atr devices in the
   `p_out`/`n_out` columns, so the whole cell is from one library
3. every transistor cell has the same 8 x 4 um box, so mixed device types
   stack in one column (the rule is one WIDTH per column)

Order of work: ROSC layout (DRC/LVS clean, then extracted Kvco and corners
with `Lay`), then the loop filter, CP/PFD/DIVN, the top, and the wrapper.
