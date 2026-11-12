
The oscillator alone. `tran.spi` steps through the eight trim codes with
VCTRL at 0, 0.6, 1.2 and 1.8 V (relative to VDD_1V8) and measures the
frequency over 10 periods, 100 ns into each step. `trim.py` prints the
range per trim code and the codes whose range holds a target frequency.

```bash
cd sim/REY_PLL_ROSC
make netlist
cicsim run --name Sch_etc --threads 8 tran Sch Gt "Ktt,Kss,Kff,Ksf,Kfs" "Tl,Tt,Th" "Vl,Vt,Vh"
python3 trim.py 512 output_tran/tran_SchGt*.log
```

**Schematic against extracted.** CK at VCTRL = 0, the oscillator's
fastest, typical corner:

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

The extraction (capacitance only) puts about 10 fF of wiring on each ring
node, more than the devices' own load. In the slow corners at -40 C and
1.7 V the extracted oscillator's fastest is 146 to 189 MHz (ss) and 169 to
241 MHz (sf) over the trim codes. That is why the PLL locks at 128 MHz and
not at 512 MHz.

**Trim codes, schematic, 512 MHz.** The 45 corners (five processes, -40,
27 and 125 C, 1.7, 1.8 and 1.9 V) were swept on the schematic for the
original 512 MHz target. For every process there is a trim code that
reaches 512 MHz inside the VCTRL range at every temperature and supply:

| Process | Codes that work over all T and V |
|:-------:|:--------------------------------:|
| Ktt     | 1..6                             |
| Kss     | 4..7                             |
| Kff     | 0..1                             |
| Ksf     | 3..5                             |
| Kfs     | 0..7                             |

This sweep has not been repeated on the extracted oscillator for 128 MHz.
The lock simulations of REY_PLL use one code from each of these ranges.

**Start-up.** `startup.spi` starts the bias from a 10 us and a 100 ns
supply ramp at codes 0 and 7 in the five extreme corners, on the
schematic. The start-up circuit turns off in every corner (XST at most
20 mV). `iext.spi` runs the ring from an ideal bias current
(REY_PLL_ROSC_IEXT).
