#!/usr/bin/env python3
"""Generate REY_PLL_ROSC.sch/.sym: a current starved ring oscillator.

Usage: python3 py/gen_rosc.py design/REY_PLL_SKY130A

The schematic is drawn to be read: one ring stage drawn once as BUS
instances (xip[6:0] is the seven inverter PMOS), wires for the local
nets, labels only for supplies and the nets that cross blocks.

Ring (osc_ring_adv_tikz.svg), per stage k:
  xmpf<a..>[k]  PMOS mirror, S=VDD G=VBP D=VS<k>   fixed current, sets f_min
  xmpc<a..>[k]  PMOS mirror, S=VDD G=VBP D=NC<k>   tunable current
  xmpv[k]       PMOS, S=NC<k> G=VCTRL D=VS<k>      steers the tunable current,
                f falls as VCTRL rises, never below f_min
  xip[k],xin[k] the inverter, PMOS source on VS<k>, PMOS bulk on VDD_1V8
                so all PMOS share one n-well
  The ring nets are N0..N<n-1>: stage k drives N<k> from N<k-1>, stage 0
  takes N<n-1>.

Bias, BIAS=vt (default): a Vgs/R source, so the current falls with
temperature the way the ring's swing does and f ~ 1/(R C)
  xmpd[]        PMOS diode on VBP
  xmpb[]        PMOS mirror into MN1 (VX)
  xmn1          NMOS, gate on VG, R from VG to VSS: I = Vgs(MN1)/R
  xmn2[]        LVT follower VX -> VG, closes the loop
  xms1, xms2[], xms3  startup: an inverter on VG; while VG is low MS3 pulls
                VBP down and returns the current into VG, through R
  xrf*, xrt*    R in REYATR_RES_36C2F0 units (15.3 kOhm): 38.3 kOhm fixed
                (2 in series + 2 in parallel), then 7.65, 15.3 and 30.6 kOhm
                sections, each shorted by xst<k> when TRIM<k> is high (less
                R, more current, higher frequency)
Bias, BIAS=ext: only the PMOS diode, VBP is a pin (CELL=REY_PLL_ROSC_IEXT)

Output: REYTR_IVX1 then REYTR_IVX4 on VDD_1V8, from the last ring node to
CK. The first must be small, it loads the ring.

Settings (environment): NSTAGE, BIAS, ND, NF, NT, NFOL, MIR, CTL, INVP,
INVN, FOL, CELL.
"""
import sys, os
from cicpy.eda.schgen import frame

N = int(os.environ.get("NSTAGE", 7))
BIAS = os.environ.get("BIAS", "vt")
ND = int(os.environ.get("ND", 4))       # diode units (and MPB units)
NFOL = int(os.environ.get("NFOL", 4))   # MN2 follower units
NF = int(os.environ.get("NF", 2))       # fixed mirror units per stage
NT = int(os.environ.get("NT", 1))       # tunable mirror units per stage
cell = os.environ.get("CELL", "REY_PLL_ROSC")
outdir = sys.argv[1]

A = "REY_ATR_SKY130A/"
MIR = A + os.environ.get("MIR", "REYATR_LVT_PCH_8C5F0") + ".sym"
CTL = A + os.environ.get("CTL", "REYATR_LVT_PCH_4C5F0") + ".sym"
INVP = A + os.environ.get("INVP", "REYATR_PCH_2C1F2") + ".sym"
INVN = A + os.environ.get("INVN", "REYATR_NCH_2C1F2") + ".sym"
FOL = A + os.environ.get("FOL", "REYATR_LVT_NCH_2C5F0") + ".sym"
NCH5 = A + "REYATR_NCH_2C5F0.sym"
PCH5 = A + "REYATR_PCH_2C5F0.sym"
SW = A + "REYATR_NCH_4C1F2.sym"
RES = A + "REYATR_RES_36C2F0.sym"

VDD, VSS = "VDD_1V8", "VSS"

pins = [(VDD, "in"), (VSS, "in"), ("TRIM0", "in"), ("TRIM1", "in"),
        ("TRIM2", "in"), ("VCTRL", "in"), ("CK", "out"), ("VBP", "out")]
if BIAS == "ext":
    pins = [(VDD, "in"), (VSS, "in"), ("VBP", "in"), ("VCTRL", "in"),
            ("CK", "out")]

L = ["v {xschem version=3.4.7 file_version=1.2}", "G {}", "K {}", "V {}",
     "S {}", "E {}"]
_n = [0]


def nid():
    _n[0] += 1
    return _n[0]


def text(s, x, y, size=0.4):
    L.append(f"T {{{s}}} {x} {y} 0 0 {size} {size} {{}}")


def wire(x1, y1, x2, y2):
    L.append(f"N {x1} {y1} {x2} {y2} {{}}")


def lab(x, y, rot, net):
    """A label pin; rot 0 has its text to the left (pin on its right), 2
    to the right, 1 standing up from the pin, 3 hanging below it."""
    L.append(f"C {{devices/lab_pin.sym}} {x} {y} {rot} 0 "
             f"{{name=l{nid()} sig_type=std_logic lab={net}}}")


def wlab(x1, y1, x2, y2, rot, net):
    """A straight wire with a label at its midpoint, split there so the
    label lands on a wire END (xschem joins pins at wire ends)."""
    xm, ym = (x1 + x2)//2, (y1 + y2)//2
    wire(x1, y1, xm, ym)
    wire(xm, ym, x2, y2)
    lab(xm, ym, rot, net)


def inst(sym, name, x, y):
    L.append(f"C {{{sym}}} {x} {y} 0 0 {{name={name}}}")


#- Symbol pins, relative to the instance origin (rey_atr cells):
#-   PCH: G (0,0)  S (40,-30)  D (40,30)   B (40,0)
#-   NCH: G (0,0)  D (40,-30)  S (40,30)   B (40,0)
#-   RPPO: P (0,0) N (80,0)    B (40,20)


def pch(sym, name, x, y, g=None, s=None, d=None, b=VDD):
    inst(sym, name, x, y)
    if g: lab(x, y, 0, g)
    if s: lab(x + 40, y - 30, 1, s)
    if d: lab(x + 40, y + 30, 3, d)
    if b: lab(x + 40, y, 2, b)


def nch(sym, name, x, y, g=None, d=None, s=None, b=VSS):
    inst(sym, name, x, y)
    if g: lab(x, y, 0, g)
    if d: lab(x + 40, y - 30, 1, d)
    if s: lab(x + 40, y + 30, 3, s)
    if b: lab(x + 40, y, 2, b)


def res(sym, name, x, y, p=None, n=None):
    inst(sym, name, x, y)
    if p: lab(x, y, 0, p)
    if n: lab(x + 80, y, 2, n)
    lab(x + 40, y + 20, 3, VSS)


def bus(name, w):
    return f"{name}[{w-1}:0]" if w > 1 else name


#- ------------------------------------------------------------------
#- Ports
#- ------------------------------------------------------------------
text("REY_PLL_ROSC: current starved ring oscillator. TRIM sets the bias "
     "(coarse), VCTRL steers part of each stage's current (f falls as "
     "VCTRL rises)", -1450, -820, 0.5)
for i, (p, d) in enumerate(pins):
    sym = {"in": "ipin", "out": "opin"}[d]
    L.append(f"C {{devices/{sym}.sym}} {-1400 + 160*i} -740 0 0 "
             f"{{name=p{i} lab={p}}}")

#- ------------------------------------------------------------------
#- Bias
#- ------------------------------------------------------------------
BIASCELL = "REY_PLL_ROSC_BIAS"
BIAS_PINS = [(VDD, "in"), (VSS, "in"), ("TRIM0", "in"), ("TRIM1", "in"),
             ("TRIM2", "in"), ("VBP", "out")]


def draw_bias():
    """The Vgs/R bias on its own sheet: VBP out, TRIM in."""
    text("REY_PLL_ROSC_BIAS: the Vgs/R bias of the ring, VBP out",
         -1450, -820, 0.5)
    for i, (p, d) in enumerate(BIAS_PINS):
        sym = {"in": "ipin", "out": "opin"}[d]
        L.append(f"C {{devices/{sym}.sym}} {-1400 + 160*i} -740 0 0 "
                 f"{{name=p{i} lab={p}}}")
    text("Bias: I = Vgs(MN1) / R", -1450, -620)
    #- PMOS diode xmpd, its drain down to the follower xmn2
    x, y = -1200, -500
    pch(MIR, bus("xmpd", ND), x, y, s=VDD)
    wire(x + 40, y + 30, x + 40, y + 60)          # drain down
    wire(x + 40, y + 60, x - 30, y + 60)          # diode tie
    wire(x - 30, y + 60, x - 30, y)
    wire(x - 30, y, x, y)
    lab(x - 30, y, 0, "VBP")
    nch(FOL, bus("xmn2", NFOL), x, y + 150, g="VX", s="VG")
    wire(x + 40, y + 60, x + 40, y + 120)          # VBP to MN2 drain
    #- PMOS mirror xmpb into MN1, VX between them
    x2 = -950
    pch(MIR, bus("xmpb", ND), x2, y, g="VBP", s=VDD)
    nch(NCH5, "xmn1", x2, y + 150, g="VG", s=VSS)
    wlab(x2 + 40, y + 30, x2 + 40, y + 120, 2, "VX")
    text("MPB mirrors the diode current into MN1. MN2 (LVT) follows VX "
         "down to VG, so R carries Vgs(MN1)/R", -1450, -280, 0.3)

    #- Startup
    text("Startup", -700, -620)
    x3 = -650
    pch(PCH5, "xms1", x3, y, g="VG", s=VDD)
    nch(SW, bus("xms2", 2), x3, y + 150, g="VG", s=VSS)
    wlab(x3 + 40, y + 30, x3 + 40, y + 120, 2, "XST")
    nch(SW, "xms3", x3 + 260, y + 150, g="XST", d="VBP", s="VG")
    text("While VG is low, XST is high and MS3 pulls VBP down into VG, "
         "through R, until MN1 turns on", -700, -280, 0.3)

    #- Trim resistor, a chain left to right from VG down to VSS, in
    #- REYATR_RES_36C2F0 units (15.3 kOhm, 16 x 4 um, stacks like a
    #- transistor). The composite RPPO cells lose their bulk pin when
    #- cicpy splits the cell into columns.
    xr, yr, dx = -1450, -100, 190
    chain = [  # (name, from, to, note)
        ("xrf0", "VG", "RFA"),
        ("xrf1", "RFA", "RF"),
        ("xrf2[1:0]", "RF", "RT0"),     # 2 in parallel
        ("xrt0[1:0]", "RT0", "RT1"),    # bit 0, 2 in parallel
        ("xrt1", "RT1", "RT2"),         # bit 1
        ("xrt2a", "RT2", "RT2B"),       # bit 2, 2 in series
        ("xrt2b", "RT2B", VSS),
    ]
    for i, (name, a_, b_) in enumerate(chain):
        x = xr + dx*i
        res(RES, name, x, yr, p=a_ if i == 0 else None,
            n=b_ if i == len(chain) - 1 else None)
        if i:
            wlab(x - dx + 80, yr, x, yr, 3, a_)
    #- each trim section shorted by its switch, drawn under it
    for k, (a_, b_, i) in enumerate((("RT0", "RT1", 3), ("RT1", "RT2", 4),
                                     ("RT2", VSS, 5))):
        nch(SW, f"xst{k}", xr + dx*i + 40, yr + 120, g=f"TRIM{k}",
            d=a_, s=b_)
    text("38.5k fixed, then 7.7k / 15.4k / 30.8k, each shorted when "
         "TRIM<k> is high", xr, yr + 200, 0.3)



if BIAS == "vt":
    from cicpy.eda.schgen import write_box_symbol, box_symbol
    _main = L
    L = ["v {xschem version=3.4.7 file_version=1.2}", "G {}", "K {}",
         "V {}", "S {}", "E {}"]
    draw_bias()
    with open(os.path.join(outdir, BIASCELL + ".sch"), "w") as f:
        f.write("\n".join(frame(L)) + "\n")
    write_box_symbol(os.path.join(outdir, BIASCELL + ".sym"), BIAS_PINS)
    L = _main
    #- the bias block, its own cell
    text("Bias: I = Vgs(MN1) / R, its own cell", -1450, -620)
    _bsym = box_symbol(BIAS_PINS)
    xb, yb = -1100, -350
    inst(f"REY_PLL_SKY130A/{BIASCELL}.sym", "xbias", xb, yb)
    for p, _ in BIAS_PINS:
        px, py, side = _bsym.pins[p]
        lab(xb + px, yb + py, side, p)
elif BIAS == "ext":
    text("Bias: external current into VBP", -1450, -620)
    x, y = -1200, -500
    pch(MIR, bus("xmpd", ND), x, y, s=VDD)
    wire(x + 40, y + 30, x + 40, y + 60)
    wire(x + 40, y + 60, x - 30, y + 60)
    wire(x - 30, y + 60, x - 30, y)
    wire(x - 30, y, x, y)
    lab(x - 30, y, 0, "VBP")

#- ------------------------------------------------------------------
#- Ring stage: its own cell, REY_PLL_ROSC_STAGE, laid out and routed on
#- its own; the oscillator places seven of them
#- ------------------------------------------------------------------
STAGE = "REY_PLL_ROSC_STAGE"
STAGE_PINS = [(VDD, "in"), (VSS, "in"), ("VBP", "in"), ("VCTRL", "in"),
              ("A", "in"), ("Y", "out")]


def draw_stage():
    """One stage on its own sheet: A in, Y out."""
    x0 = -1300
    text("REY_PLL_ROSC_STAGE: one ring stage, a starved inverter A -> Y",
         -1450, -820, 0.5)
    for i, (p, d) in enumerate(STAGE_PINS):
        sym = {"in": "ipin", "out": "opin"}[d]
        L.append(f"C {{devices/{sym}.sym}} {-1400 + 160*i} -740 0 0 "
                 f"{{name=p{i} lab={p}}}")
    #- tunable branch: mirror then VCTRL device, NC between them
    xt = x0 + 100
    for j in range(NT):
        pch(MIR, f"xmpc{chr(97+j)}", xt - 150*j, -490, g="VBP", s=VDD)
        if j:
            wire(xt - 150*j + 40, -460, xt + 40, -460)
    wlab(xt + 40, -460, xt + 40, -410, 0, "NC")
    pch(CTL, "xmpv", xt, -380, g="VCTRL")
    #- fixed branch, drains on VS
    xf = xt + 300
    for j in range(NF):
        pch(MIR, f"xmpf{chr(97+j)}", xf + 260*j, -380, g="VBP", s=VDD)
    yvs = -300
    wire(xt + 40, -350, xt + 40, yvs)
    for j in range(NF):
        wire(xf + 260*j + 40, -350, xf + 260*j + 40, yvs)
    wire(xt + 40, yvs, xf + 260*(NF - 1) + 40, yvs)
    lab(xf + 260*(NF - 1) + 40, yvs, 2, "VS")
    #- the inverter, PMOS source on VS
    xi = xt
    pch(INVP, "xip", xi, -230)
    wire(xi + 40, yvs, xi + 40, -260)
    nch(INVN, "xin", xi, -110, s=VSS)
    wire(xi + 40, -200, xi + 40, -170)
    wire(xi + 40, -170, xi + 40, -140)
    wire(xi + 40, -170, xi + 140, -170)
    lab(xi + 140, -170, 2, "Y")
    wire(xi, -230, xi - 40, -230)
    wire(xi - 40, -230, xi - 40, -170)
    wire(xi - 40, -170, xi - 40, -110)
    wire(xi - 40, -110, xi, -110)
    lab(xi - 40, -170, 0, "A")
    text("fixed mirror: sets f_min; tunable mirror through the VCTRL "
         "device: the rest", x0, -30, 0.3)


from cicpy.eda.schgen import write_box_symbol, box_symbol
_main = L
L = ["v {xschem version=3.4.7 file_version=1.2}", "G {}", "K {}", "V {}",
     "S {}", "E {}"]
draw_stage()
with open(os.path.join(outdir, STAGE + ".sch"), "w") as f:
    f.write("\n".join(frame(L)) + "\n")
write_box_symbol(os.path.join(outdir, STAGE + ".sym"), STAGE_PINS)
L = _main

#- the ring: seven stages as one bus instance, stage k drives N<k> from
#- N<k-1>, stage 0 takes the last node
S = range(N - 1, -1, -1)
nets = lambda p, idx: ",".join(f"{p}{i}" for i in idx)
x0, y0 = -700, -620
text(f"Ring: {N} stages of REY_PLL_ROSC_STAGE", x0, y0)
_sym = box_symbol(STAGE_PINS)
xs, ys = x0 + 300, -350
inst(f"REY_PLL_SKY130A/{STAGE}.sym", f"xstg[{N-1}:0]", xs, ys)
for p, net in ((VDD, VDD), (VSS, VSS), ("VBP", "VBP"), ("VCTRL", "VCTRL"),
               ("A", nets("N", [(k - 1) % N for k in S])),
               ("Y", nets("N", S))):
    px, py, side = _sym.pins[p]
    lab(xs + px, ys + py, side, net)
text("stage k: N<k-1> -> N<k>", x0, -180, 0.3)

#- ------------------------------------------------------------------
#- Output buffer
#- ------------------------------------------------------------------
xo = x0 + 800
text("Output buffer", xo, y0)
#- REYTR_IVX1 then IVX4. The first one must be small: it loads the last
#- ring node, and a 2C1F2 pair there (2x the gate cap of IVX1) slowed the
#- ring by 20 %. Pins: A (0,0) Y (80,0) AVDD (40,-40) AVSS (40,40)
T = "REY_TR_SKY130A/"


def inv(sym, name, x, y, a, yy):
    inst(sym, name, x, y)
    lab(x + 40, y - 40, 1, VDD)
    lab(x + 40, y + 40, 3, VSS)
    if a: lab(x, y, 0, a)
    if yy: lab(x + 80, y, 2, yy)


#- on the row of the two blocks
yo = ys
inv(T + "REYTR_IVX1_CV.sym", "xo0", xo, yo, f"N{N-1}", None)
wlab(xo + 80, yo, xo + 200, yo, 3, "CKN")
inv(T + "REYTR_IVX4_CV.sym", "xo1", xo + 200, yo, None, "CK")
#- every rey_tr column needs a TAPCELLB (well and substrate taps) to be
#- LVS clean. Pins: AVDD (0,-20) AVSS (0,20)
inst(T + "REYTR_TAPCELLB_CV.sym", "xotap", xo + 420, yo)
lab(xo + 420, yo - 20, 1, VDD)
lab(xo + 420, yo + 20, 3, VSS)

with open(os.path.join(outdir, cell + ".sch"), "w") as f:
    f.write("\n".join(frame(L)) + "\n")

#- ------------------------------------------------------------------
#- Symbol: inputs left, outputs right
#- ------------------------------------------------------------------
Y = ["v {xschem version=3.4.7 file_version=1.2}",
     'K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\n}',
     "T {@symname} -60 -6 0 0 0.3 0.3 {}"]
ins = [p for p, d in pins if d != "out"]
outs = [p for p, d in pins if d == "out"]
h = 20*max(len(ins), len(outs)) + 10
#- the name over the corner, as cicpy's box symbols have it
Y.append(f"T {{@name}} -130 {-h - 22} 0 0 0.25 0.25 {{}}")
Y.append(f"P 4 5 130 {-h} -130 {-h} -130 {h} 130 {h} 130 {-h} {{}}")
for i, p in enumerate(ins):
    y = -h + 20 + 20*i
    Y += [f"B 5 -152.5 {y-2.5} -147.5 {y+2.5} {{name={p} dir=in}}",
          f"L 4 -150 {y} -130 {y} {{}}", f"T {{{p}}} -125 {y-4} 0 0 0.2 0.2 {{}}"]
for i, p in enumerate(outs):
    y = -h + 20 + 20*i
    Y += [f"B 5 147.5 {y-2.5} 152.5 {y+2.5} {{name={p} dir=out}}",
          f"L 4 130 {y} 150 {y} {{}}", f"T {{{p}}} 125 {y-4} 0 1 0.2 0.2 {{}}"]
with open(os.path.join(outdir, cell + ".sym"), "w") as f:
    f.write("\n".join(Y) + "\n")
print("wrote", cell)
