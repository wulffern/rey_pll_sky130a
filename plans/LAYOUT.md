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
| Loop filter, Icp 2uA | C1 4.0 pF, C2 0.31 pF, R 369 kOhm (HRPPO)      | 2 500        |
| Routing, rings       |                                                | 3 000        |
| Total                |                                                | ~13 600 = 76 % |

Loop filter, from `python3 py/pll.py --icp 2e-6` (N = 64, fc = fref/20,
PM 60 degrees, |Kvco| 235 MHz/V):

| Icp  | C1      | R        | Area, MOS C + HRPPO R |
|:----:|:-------:|:--------:|:---------------------:|
| 1 uA | 2.0 pF  | 737 kOhm | 24 % of a tile        |
| 2 uA | 4.0 pF  | 369 kOhm | 14 %                  |
| 4 uA | 8.1 pF  | 184 kOhm | 12 % (30 % as MiM)    |

C1 is referenced to VDD_1V8. As a MOS cap it would be a PMOS with S/D/B
on VDD_1V8 and the gate on VCTRL. It stays in inversion only while
VDD - VCTRL > |Vtp|, so check the capacitance over the locking range of
VCTRL, or use MiM over the resistor (which does not use met3/met4 for
routing).

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
