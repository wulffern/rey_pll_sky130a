#!/usr/bin/env python3
"""Generate REY_PLL_ROSC.sch/.sym: current starved ring oscillator.

Topology (osc_ring_adv_tikz.svg):
  Bias, BIAS=gm (default): constant-gm (beta multiplier) cell
    MP0_<j>     PMOS diode on VBP, drain of MN2
    MPB_<j>     PMOS mirror into MN1
    MN1         NMOS diode on VBN (NCH_2C5F0)
    MN2_<j>     K=4 x NCH_2C5F0, source on RS, so gm(MN1) ~ 1/R
    XR*         R from RS to VSS: 7.7k fixed (2 x RPPO2 parallel), then trim
                sections 0.96k (4 x HRPPO8), 1.91k (2 x HRPPO8), 3.83k
                (1 x HRPPO8), all four HRPPO8 resistors in parallel. Each
                section is shorted by NMOS switches when TRIM<k> is high
                (less R, more current, higher frequency)
    MS1-3       startup: MS1/MS2 inverter on VBN, MS3 pulls VBP low while
                no current flows
  Bias, BIAS=r: PMOS diode on VBP with an RPPO ladder to VSS
  Bias, BIAS=vt: Vgs/R source, MN1 gate on R, MN2 follower; R is the
                trim ladder (46k fixed + 7.7k, 15.4k, 30.8k switched)
  Bias, BIAS=ext: PMOS diode on pin VBP, current from outside (CELL=..._IEXT)
  MPF<k>_<j>    PMOS mirror, S=VDD G=VBP D=VS<k>    fixed current, sets f_min
  MPC<k>_<j>    PMOS mirror, S=VDD G=VBP D=NC<k>    tunable current
  MPV<k>        PMOS, S=NC<k> G=VCTRL D=VS<k>       steers the tunable current,
                f falls as VCTRL rises, never below f_min
Usage: python3 py/gen_rosc.py design/REY_PLL_SKY130A
  XIP<k>,XIN<k> inverter supplied from VS<k>, long channel (INVP/INVN cells),
                PMOS bulk on VDD_1V8 so all PMOS share one n-well
  XC<k>         load cap on each stage output
  XO0, XO1      IVX1 then IVX4 on VDD_1V8 from the last ring node to CK
"""
import sys, os

N = int(os.environ.get("NSTAGE", 7))
USE_CAP = int(os.environ.get("USE_CAP", 0))
BIAS = os.environ.get("BIAS", "gm")
ND = int(os.environ.get("ND", 9 if BIAS == "r" else 4))   # diode units
K = int(os.environ.get("K", 4))     # beta multiplier ratio
NF = int(os.environ.get("NF", 2))   # fixed units per stage
NT = int(os.environ.get("NT", 1))   # tunable units per stage
lib = "REY_PLL_SKY130A"
cell = os.environ.get("CELL", "REY_PLL_ROSC")
outdir = sys.argv[1]

PCH_MIR = "REY_ATR_SKY130A/" + os.environ.get("MIR", "REYATR_LVT_PCH_8C5F0") + ".sym"
PCH_CTL = "REY_ATR_SKY130A/" + os.environ.get("CTL", "REYATR_LVT_PCH_4C5F0") + ".sym"
INV = "REY_TR_SKY130A/REYTR_IVX1_CV.sym"
INVP = "REY_ATR_SKY130A/" + os.environ.get("INVP", "REYATR_PCH_2C1F2") + ".sym"
INVN = "REY_ATR_SKY130A/" + os.environ.get("INVN", "REYATR_NCH_2C1F2") + ".sym"
BUF = "REY_TR_SKY130A/REYTR_IVX4_CV.sym"
CAP = "REY_ATR_SKY130A/REYATR_CAPX1.sym"

pins = [("VDD_1V8", "in"), ("VSS", "in"), ("TRIM0", "in"), ("TRIM1", "in"),
        ("TRIM2", "in"), ("VCTRL", "in"), ("CK", "out")]
if BIAS == "ext":
    #- ideal bias current pulled out of the PMOS diode, for characterizing
    #- the ring alone
    pins = [("VDD_1V8", "in"), ("VSS", "in"), ("VBP", "in"),
            ("VCTRL", "in"), ("CK", "out")]

L = ["v {xschem version=3.4.7 file_version=1.2}", "G {}", "K {}", "V {}", "S {}", "E {}"]
L.append("T {Current starved ring oscillator. Coarse frequency from IBNS_20U, "
         "fine from VCTRL (f falls as VCTRL rises)} 0 -500 0 0 0.4 0.4 {}")
lab_i = [0]


def lab(x, y, rot, net):
    lab_i[0] += 1
    L.append(f"C {{devices/lab_pin.sym}} {x} {y} {rot} 0 "
             f"{{name=l{lab_i[0]} sig_type=std_logic lab={net}}}")


for i, (p, d) in enumerate(pins):
    sym = {"in": "ipin", "out": "opin", "inout": "iopin"}[d]
    L.append(f"C {{devices/{sym}.sym}} -400 {-300 + 40*i} 0 0 {{name=p{i} lab={p}}}")


def pch(sym, name, x, y, d, g, s, b):
    L.append(f"C {{{sym}}} {x} {y} 0 0 {{name={name}}}")
    lab(x + 40, y + 30, 1, d)
    lab(x, y, 0, g)
    lab(x + 40, y - 30, 3, s)
    lab(x + 40, y, 2, b)


def nch(sym, name, x, y, d, g, s, b):
    L.append(f"C {{{sym}}} {x} {y} 0 0 {{name={name}}}")
    lab(x + 40, y - 30, 3, d)
    lab(x, y, 0, g)
    lab(x + 40, y + 30, 1, s)
    lab(x + 40, y, 2, b)


def inv(sym, name, x, y, a, yy, vdd, vss):
    L.append(f"C {{{sym}}} {x} {y} 0 0 {{name={name}}}")
    lab(x, y, 0, a)
    lab(x + 80, y, 2, yy)
    lab(x + 40, y - 40, 3, vdd)
    lab(x + 40, y + 40, 1, vss)


def cap(name, x, y, a, b):
    L.append(f"C {{{CAP}}} {x} {y} 0 0 {{name={name}}}")
    lab(x, y - 60, 3, a)
    lab(x, y + 10, 1, b)


# Bias diode
RPPO2 = "REY_ATR_SKY130A/REYATR_RPPO2.sym"
RPPO4 = "REY_ATR_SKY130A/REYATR_RPPO4.sym"
SW = "REY_ATR_SKY130A/" + os.environ.get("SW", "REYATR_NCH_4C1F2") + ".sym"


def res(sym, name, x, y, p, n):
    L.append(f"C {{{sym}}} {x} {y} 0 0 {{name={name}}}")
    lab(x, y, 0, p)
    lab(x + 80, y, 2, n)
    lab(x + 40, y + 20, 1, "VSS")


HRPPO8 = "REY_ATR_SKY130A/REYATR_HRPPO8.sym"
NCH5 = "REY_ATR_SKY130A/REYATR_NCH_2C5F0.sym"
PCH5 = "REY_ATR_SKY130A/REYATR_PCH_2C5F0.sym"


def hr8(name, x, y, p, n):
    """HRPPO8 with its four resistors in parallel"""
    L.append(f"C {{{HRPPO8}}} {x} {y} 0 0 {{name={name}}}")
    for i in range(4):
        lab(x - 20, y + 40*i, 0, p)
        lab(x - 20, y + 40*i + 20, 0, n)
    lab(x - 20, y + 160, 0, "VSS")


xr = -600
if BIAS == "gm":
    for j in range(ND):
        pch(PCH_MIR, f"XMP0_{j}", -200, -200 - 120*j, "VBP", "VBP", "VDD_1V8", "VDD_1V8")
        pch(PCH_MIR, f"XMPB_{j}", -350, -200 - 120*j, "VBN", "VBP", "VDD_1V8", "VDD_1V8")
    nch(NCH5, "XMN1", -350, 100, "VBN", "VBN", "VSS", "VSS")
    for j in range(K):
        nch(NCH5, f"XMN2_{j}", -200, 100 + 120*j, "VBP", "VBN", "RS", "VSS")
    # Startup
    pch(PCH5, "XMS1", -500, 100, "XST", "VBN", "VDD_1V8", "VDD_1V8")
    for j in range(2):
        nch(SW, f"XMS2_{j}", -500, 220 + 120*j, "XST", "VBN", "VSS", "VSS")
    nch(SW, "XMS3", -500, 500, "VBP", "XST", "VSS", "VSS")
    # Trimmed R, top to bottom: fixed, bit0, bit1, bit2
    res(RPPO2, "XRF_0", xr, -400, "RS", "RT0")
    res(RPPO2, "XRF_1", xr, -340, "RS", "RT0")
    sec = [("RT0", "RT1", 4, 4), ("RT1", "RT2", 2, 2), ("RT2", "VSS", 1, 1)]
    y = -280
    for bit, (p_, n_, nr, ns) in enumerate(sec):
        for j in range(nr):
            hr8(f"XRT{bit}_{j}", xr, y, p_, n_)
            y += 200
        for j in range(ns):
            nch(SW, f"XST{bit}_{j}", xr + 200, y - 100 - 120*j, p_, f"TRIM{bit}", n_, "VSS")
elif BIAS == "vt":
    #- Vgs/R (threshold referenced) source: R carries Vgs(MN1)/R. The
    #- ring's swing tracks the thresholds too, so f ~ 1/(R C) and the
    #- temperature drift of Vgs mostly cancels
    for j in range(ND):
        pch(PCH_MIR, f"XMP0_{j}", -200, -200 - 120*j, "VBP", "VBP", "VDD_1V8", "VDD_1V8")
        pch(PCH_MIR, f"XMPB_{j}", -350, -200 - 120*j, "VX", "VBP", "VDD_1V8", "VDD_1V8")
    nch(NCH5, "XMN1", -350, 100, "VX", "VG", "VSS", "VSS")
    nch(NCH5, "XMN2", -200, 100, "VBP", "VX", "VG", "VSS")
    # Startup: while VG (= I R) is low, MS3 pulls VBP down INTO VG, so
    # the startup current goes through R and lifts VG until the MS1/MS2
    # inverter turns MS3 off (to VSS it latched: VG never rose)
    pch(PCH5, "XMS1", -500, 100, "XST", "VG", "VDD_1V8", "VDD_1V8")
    for j in range(2):
        nch(SW, f"XMS2_{j}", -500, 220 + 120*j, "XST", "VG", "VSS", "VSS")
    nch(SW, "XMS3", -500, 500, "VBP", "XST", "VG", "VSS")
    # R from VG to VSS: fixed 3 x RPPO2 (46k), then trim 7.7k, 15.4k, 30.8k
    res(RPPO4, "XRF0", xr, -400, "VG", "RF")
    res(RPPO2, "XRF1", xr, -340, "RF", "RT0")
    res(RPPO2, "XRT0_0", xr, -280, "RT0", "RT1")
    res(RPPO2, "XRT0_1", xr, -220, "RT0", "RT1")
    nch(SW, "XST0", xr + 200, -250, "RT0", "TRIM0", "RT1", "VSS")
    res(RPPO2, "XRT1", xr, -160, "RT1", "RT2")
    nch(SW, "XST1", xr + 200, -160, "RT1", "TRIM1", "RT2", "VSS")
    res(RPPO4, "XRT2", xr, -100, "RT2", "VSS")
    nch(SW, "XST2", xr + 200, -70, "RT2", "TRIM2", "VSS", "VSS")
elif BIAS == "ext":
    for j in range(ND):
        pch(PCH_MIR, f"XMP0_{j}", -200, -200 - 120*j, "VBP", "VBP", "VDD_1V8", "VDD_1V8")
else:
    res(RPPO4, "XRF0", xr, -400, "VBP", "RF")
    res(RPPO2, "XRF1", xr, -340, "RF", "RT0")
    res(RPPO2, "XRT0_0", xr, -280, "RT0", "RT1")      # bit0: 2 x RPPO2 parallel
    res(RPPO2, "XRT0_1", xr, -220, "RT0", "RT1")
    nch(SW, "XST0", xr + 200, -250, "RT0", "TRIM0", "RT1", "VSS")
    res(RPPO2, "XRT1", xr, -160, "RT1", "RT2")        # bit1
    nch(SW, "XST1", xr + 200, -160, "RT1", "TRIM1", "RT2", "VSS")
    res(RPPO4, "XRT2", xr, -100, "RT2", "VSS")        # bit2
    nch(SW, "XST2", xr + 200, -70, "RT2", "TRIM2", "VSS", "VSS")
    for j in range(ND):
        pch(PCH_MIR, f"XMP0_{j}", -200, -200 - 120*j, "VBP", "VBP", "VDD_1V8", "VDD_1V8")

nodes = [f"N{k}" for k in range(N)]
for k in range(N):
    x = 100 + 300*k
    for j in range(NF):
        pch(PCH_MIR, f"XMPF{k}_{j}", x + 150, -200 - 120*j, f"VS{k}", "VBP", "VDD_1V8", "VDD_1V8")
    for j in range(NT):
        pch(PCH_MIR, f"XMPC{k}_{j}", x, -200 - 120*j, f"NC{k}", "VBP", "VDD_1V8", "VDD_1V8")
    pch(PCH_CTL, f"XMPV{k}", x, -50, f"VS{k}", "VCTRL", f"NC{k}", "VDD_1V8")
    pch(INVP, f"XIP{k}", x, 100, nodes[k], nodes[k-1], f"VS{k}", "VDD_1V8")
    nch(INVN, f"XIN{k}", x, 200, nodes[k], nodes[k-1], "VSS", "VSS")
    if USE_CAP:
        cap(f"XC{k}", x + 150, 300, nodes[k], "VSS")

INV1 = "REY_TR_SKY130A/REYTR_IVX1_CV.sym"
x0 = 300 + 300*N
# Small first buffer keeps the load on the last ring node low, the ring
# swing (0 to ~1.5 V) is enough for an inverter on VDD_1V8
inv(INV1, "XO0", x0, 150, nodes[N-1], "CKN", "VDD_1V8", "VSS")
inv(BUF, "XO1", x0 + 200, 150, "CKN", "CK", "VDD_1V8", "VSS")

with open(os.path.join(outdir, cell + ".sch"), "w") as f:
    f.write("\n".join(L) + "\n")

# Symbol: inputs left, outputs right
S = ["v {xschem version=3.4.7 file_version=1.2}",
     'K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}',
     "T {@symname} -60 -6 0 0 0.3 0.3 {}", "T {@name} 135 -52 0 0 0.2 0.2 {}"]
ins = [p for p, d in pins if d != "out"]
outs = [p for p, d in pins if d == "out"]
h = 20*max(len(ins), len(outs)) + 10
S.append(f"P 4 5 130 {-h} -130 {-h} -130 {h} 130 {h} 130 {-h} {{}}")
for i, p in enumerate(ins):
    y = -h + 20 + 20*i
    S += [f"B 5 -152.5 {y-2.5} -147.5 {y+2.5} {{name={p} dir=in}}",
          f"L 4 -150 {y} -130 {y} {{}}", f"T {{{p}}} -125 {y-4} 0 0 0.2 0.2 {{}}"]
for i, p in enumerate(outs):
    y = -h + 20 + 20*i
    S += [f"B 5 147.5 {y-2.5} 152.5 {y+2.5} {{name={p} dir=out}}",
          f"L 4 130 {y} 150 {y} {{}}", f"T {{{p}}} 125 {y-4} 0 1 0.2 0.2 {{}}"]
with open(os.path.join(outdir, cell + ".sym"), "w") as f:
    f.write("\n".join(S) + "\n")
print("wrote", cell)
