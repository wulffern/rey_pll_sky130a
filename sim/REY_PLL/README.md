
The loop from power up: `tran.spi` raises PWRUP_1V8 at 200 ns with an
8 MHz reference running, and over the last 2 us of 16 us it measures the
frequency of CK (200 periods), the frequency of CK_FB (8 periods) and the
ripple on VCTRL. Each process corner runs at one trim code, as a die would
after trimming: tt and fs at 3, ss at 6, ff at 0, sf at 4.

```bash
cd sim/REY_PLL
cicsim run --name Lay_typical tran Lay Gt C3 Ktt Tt Vt   # extracted, typical
./corners.sh Lay                                         # extracted, 20 corners
```

The extracted netlist is `work/lpe/REY_PLL_lpe.spi` (`make lpe
CELL=REY_PLL` in `work/`), capacitance only. `make typical VIEW=Lay`
extracts first and then runs the typical corner.

**Extracted layout, N = 16.** All 21 runs lock: CK is 127.99 to
128.01 MHz, VCTRL settles between 0.56 and 1.53 V and its ripple is 8 to
13 mV peak to peak. The limits are 127.5 to 128.5 MHz for CK, 7.97 to
8.03 MHz for CK_FB and 30 mV of ripple.

| Process | Code | T, C | VDD, V | CK, MHz | CK_FB, MHz | VCTRL, V | Ripple, mV |
|:-------:|:----:|-----:|-------:|--------:|-----------:|---------:|-----------:|
| tt | 3 | 27 | 1.8 | 127.99 | 8.001 | 1.077 | 12.6 |
| tt | 3 | -40 | 1.7 | 128.00 | 8.000 | 0.728 | 11.3 |
| tt | 3 | -40 | 1.9 | 128.00 | 8.000 | 1.032 | 12.6 |
| tt | 3 | 125 | 1.7 | 128.00 | 8.000 | 1.187 | 10.3 |
| tt | 3 | 125 | 1.9 | 128.00 | 8.000 | 1.427 | 11.2 |
| ss | 6 | -40 | 1.7 | 128.01 | 8.000 | 0.562 | 7.9 |
| ss | 6 | -40 | 1.9 | 128.00 | 8.000 | 0.880 | 12.2 |
| ss | 6 | 125 | 1.7 | 128.00 | 8.001 | 1.014 | 10.7 |
| ss | 6 | 125 | 1.9 | 128.00 | 8.000 | 1.324 | 11.0 |
| ff | 0 | -40 | 1.7 | 128.00 | 8.000 | 0.928 | 12.2 |
| ff | 0 | -40 | 1.9 | 128.00 | 8.000 | 1.231 | 11.4 |
| ff | 0 | 125 | 1.7 | 128.00 | 8.000 | 1.337 | 10.3 |
| ff | 0 | 125 | 1.9 | 128.00 | 8.000 | 1.512 | 11.8 |
| sf | 4 | -40 | 1.7 | 128.00 | 8.001 | 0.612 | 9.8 |
| sf | 4 | -40 | 1.9 | 128.01 | 8.000 | 0.932 | 10.7 |
| sf | 4 | 125 | 1.7 | 128.00 | 8.000 | 1.163 | 9.9 |
| sf | 4 | 125 | 1.9 | 128.00 | 8.000 | 1.527 | 11.6 |
| fs | 3 | -40 | 1.7 | 128.00 | 8.001 | 0.838 | 11.8 |
| fs | 3 | -40 | 1.9 | 128.01 | 8.000 | 1.130 | 13.4 |
| fs | 3 | 125 | 1.7 | 128.00 | 8.000 | 1.181 | 10.0 |
| fs | 3 | 125 | 1.9 | 128.00 | 8.000 | 1.388 | 11.8 |

VCTRL is closest to a supply at sf, 125 C, 1.9 V (1.53 V, 0.37 V under
VDD_1V8) and at ss, -40 C, 1.7 V (0.56 V).

Not covered by these runs:

- The trim codes are the ones the schematic oscillator needed for 512 MHz.
  The trim sweep has not been repeated on the extracted oscillator for
  128 MHz, so which codes work for each process is not known, only that
  these do.
- The loop filter was sized for N = 64. By hand calculation the phase
  margin at N = 16 is 20 to 38 degrees. The runs show lock, they do not
  measure the margin.
- The extraction has no wire resistance.
- The schematic view cannot lock at N = 16: without the wiring the
  oscillator's slowest is 274 MHz. The schematic was simulated when the
  feedback was CK/64, and locked at 512.0 MHz (typical, VCTRL 0.952 V,
  ripple 8.5 mV). The extracted layout did not: 264.9 MHz with VCTRL at
  VSS, which is why the feedback moved to CK/16.
