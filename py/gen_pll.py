#!/usr/bin/env python3
"""Generate the REY_PLL blocks around the oscillator, and the top.

Usage: python3 py/gen_pll.py design/REY_PLL_SKY130A

Ported from sun_pll_sky130nm, with the changes the current starved
oscillator needs (negative Kvco, filter on VDD_1V8, no OTA buffer):

  REY_PLL_CTRL  power up, the start-up KICK pulse (sun_pll's KICK) and
                the open loop test modes
  REY_PLL_PFD   phase frequency detector: two reset flops, the classic
                tri-state PFD (sun_pll's TSPC loop could not be reset)
  REY_PLL_CP    charge pump, biased from the oscillator's VBP, UP and DN
                swapped: UP SINKS current (the VCO is faster at lower
                VCTRL), DN sources. VCTRL is parked at VDD_1V8 (slowest)
                while powered down
  REY_PLL_LPF   loop filter, eight REYPLL_RCU cells: R = 32 x 15.3 kOhm
                from VCTRL to VLPFZ, C1 = 7 MiM from VLPFZ to VDD_1V8,
                C2 = 1 MiM from VCTRL to VDD_1V8 (bottom plates on VDD)
  REY_PLL_DIVN  six flop ripple divider, CK/16 is the feedback (the
                oscillator as laid out reaches 128 MHz in every corner,
                not 512), four buffered taps CK/8..CK/64 for the pins
                (ten flops and eight taps did not fit the tile's width)
  REY_PLL       the top

The schematics are written with cicpy.eda.schgen; the oscillator comes
from py/gen_rosc.py.
"""
import logging
import os
import sys
import textwrap

log = logging.getLogger('gen_pll')

from cicpy.eda.schgen import Sheet, box_symbol, LEFT, RIGHT, UP, DOWN

A = "REY_ATR_SKY130A/"
T = "REY_TR_SKY130A/"
P = "REY_PLL_SKY130A/"
VDD, VSS = "VDD_1V8", "VSS"
SUP = dict(AVDD=VDD, AVSS=VSS)

NDIV = 6                  # flops in the divider
NFB = 4                   # feedback after this many: CK/16
FREF = 8                  # MHz
TAPS = range(2, 6)        # Q2 (CK/8) .. Q5 (CK/64)
NRCU = 8                  # loop filter unit cells
NOTE = 110                # characters a line of notes on a sheet
NC1 = 7                   # of which C1; the last one is C2

outdir = sys.argv[1]
search = [os.path.join(outdir, "..")]


def sheet(cell, pins, title):
    return Sheet(cell, pins, search=search, title=title)


#- --------------------------------------------------------------------
#- The standard cell blocks: ONE definition, two outputs
#- --------------------------------------------------------------------
#- Each block is a list of layout columns, each column a list of
#- instances (name, cell, {pin: net}). The names are the layout's: XA0 is
#- the bottom of column A, and the letter IS the column, which is how
#- ciccreator places a LayoutDigitalCell. From this the generator writes
#- the xschem schematic (each column drawn as a column, so the schematic
#- reads like the layout) and the block's subckt in cic/pll.spi, which
#- cicpy compiles into the layout. Both always carry the same names.

#- port order of each cell in the ciccreator netlists (rey_tr dig.spi,
#- cic/lpf.spi); the symbol pin order is not the subckt's
PORTS = {
    "REYTR_TAPCELLB_CV": ["AVDD", "AVSS"],
    "REYTR_IVX1_CV": ["A", "Y", "AVDD", "AVSS"],
    "REYTR_BFX1_CV": ["A", "Y", "AVDD", "AVSS"],
    "REYTR_NRX1_CV": ["A", "B", "Y", "AVDD", "AVSS"],
    "REYTR_ANX1_CV": ["A", "B", "Y", "AVDD", "AVSS"],
    "REYTR_ORX1_CV": ["A", "B", "Y", "AVDD", "AVSS"],
    "REYTR_DFRNQNX1_CV": ["D", "CK", "RN", "Q", "QN", "AVDD", "AVSS"],
    "REYPLL_RCU": ["P0", "N0", "P1", "N1", "P2", "N2", "P3", "N3", "BR",
                   "A", "B"],
}
#- the symbol library of each cell, and its name while cicpy compiles
#- (cic/ip.json prefixes REYPLL_ at write time, so the build name of
#- REYPLL_RCU is RCU; rey_tr's cells come from a built library as is)
LIBS = {"REYPLL_RCU": P}
BUILD = {"REYPLL_RCU": "RCU"}


#- where a pin's label goes when not straight away from the body. The
#- supplies sit beside their pins; under the flop and the tap the cell's
#- own name is written there, so VSS hangs below, and the flop's reset
#- goes left, clear of the cell under it
BESIDE = dict(AVDD=RIGHT, AVSS=RIGHT)
LABELS = {"REYTR_DFRNQNX1_CV": dict(AVDD=RIGHT, AVSS=DOWN, RN=LEFT),
         "REYTR_TAPCELLB_CV": dict(AVDD=RIGHT, AVSS=DOWN)}


def tap(name):
    return (name, "REYTR_TAPCELLB_CV", {})


def g(name, cell, **conn):
    return (name, "REYTR_" + cell + "_CV", conn)


#- REY_PLL_CTRL ---------------------------------------------------------
CTRL_PINS = [(VDD, "in"), (VSS, "in"), ("PWRUP_1V8", "in"), ("OLH", "in"),
             ("OLL", "in"), ("KICK", "out"), ("VHI_N", "out"),
             ("VLO", "out")]
CTRL = dict(
    cell="REY_PLL_CTRL", pins=CTRL_PINS,
    title="REY_PLL_CTRL: power up, start-up kick and open loop modes",
    notes=["KICK: a pulse when PWRUP_1V8 rises. KD4 is PWRUP_1V8 delayed "
           "by five inverters, so NOR(PWRUP_N, KD4) is high between the "
           "edge and KD4. PWRUP_NB is a second PWRUP_N, local to the "
           "NORs, so no net runs the length of the column",
           "Open loop, for the per-die trim: VHI_N = PWRUP and not OLH "
           "parks VCTRL at VDD_1V8 (slowest), VLO = VHI_N and OLL at VSS "
           "(fastest). Powered down is OLH"],
    columns=[("A: power up, kick, open loop", [
        tap("XA0"),
        #- every internal net is a hop between neighbouring cells, so
        #- no trunk crosses the column: PWRUP_1V8 drives two inverters,
        #- PWRUP_N for the delay line and PWRUP_NB for the two NORs
        g("XA1", "IVX1", A="PWRUP_1V8", Y="PWRUP_N"),
        g("XA2", "IVX1", A="PWRUP_N", Y="KD0"),
        g("XA3", "IVX1", A="KD0", Y="KD1"),
        g("XA4", "IVX1", A="KD1", Y="KD2"),
        g("XA5", "IVX1", A="KD2", Y="KD3"),
        g("XA6", "IVX1", A="KD3", Y="KD4"),
        g("XA7", "IVX1", A="PWRUP_1V8", Y="PWRUP_NB"),
        g("XA8", "NRX1", A="PWRUP_NB", B="KD4", Y="KICK"),
        g("XA9", "NRX1", A="PWRUP_NB", B="OLH", Y="VHI_N"),
        g("XA10", "ANX1", A="VHI_N", B="OLL", Y="VLO")])])

#- REY_PLL_PFD ----------------------------------------------------------
PFD_PINS = [(VDD, "in"), (VSS, "in"), ("PWRUP_1V8", "in"), ("CK_REF", "in"),
            ("CK_FB", "in"), ("UP", "out"), ("DN_N", "out")]
PFD = dict(
    cell="REY_PLL_PFD", pins=PFD_PINS,
    title="REY_PLL_PFD: tri-state phase frequency detector",
    notes=["UP rises on CK_REF, DN on CK_FB. When both are high RST clears "
           "them; the path through the gates is the reset pulse that keeps "
           "the dead zone away",
           "DFRNQNX1 clocks on NAND(CK, RN): released from reset while CK "
           "is high it sees a rising edge and sets again. So each flop's "
           "reset is HELD until its own clock is low:",
           "HU = RST or (HU and CK_REF), RN_U = PWRUP and not HU; the same "
           "for DN on CK_FB"],
    columns=[
        #- two mirrored columns, an UP half and a DN half, each a flop
        #- with its reset latch over it: NR by the flop's RN pin, then
        #- OR and AN. Rows line up across the columns, so a net that
        #- crosses is one straight bar between two input pins at one
        #- height: PWRUP_N (the NRs' B), DN (XB3.A to XA3.A) and RST
        #- (XA4.A to XB5.B: the two inverters in B are 0.8 um less than
        #- the AND beside them, which is the pitch from pin A to pin B).
        #- D is PWRUP_1V8, high whenever the PLL runs (powered down the
        #- flops are held in reset anyway)
        ("A: UP flop, UP latch, RST", [
            tap("XA0"),
            g("XA1", "DFRNQNX1", D="PWRUP_1V8", CK="CK_REF", RN="RN_U",
              Q="UP", QN="UP_N"),
            g("XA2", "NRX1", A="HU", B="PWRUP_N", Y="RN_U"),
            g("XA3", "ANX1", A="DN", B="UP", Y="RST"),
            g("XA4", "ORX1", A="RST", B="HAU", Y="HU"),
            g("XA5", "ANX1", A="HU", B="CK_REF", Y="HAU")]),
        ("B: DN flop, DN latch, DN_N, PWRUP_N", [
            tap("XB0"),
            g("XB1", "DFRNQNX1", D="PWRUP_1V8", CK="CK_FB", RN="RN_D",
              Q="DN", QN="DN_Q_N"),
            g("XB2", "NRX1", A="HD", B="PWRUP_N", Y="RN_D"),
            #- DN_N from DN: the flop's own QN carries a via of the
            #- flop's wiring right on the pin, which an outside stack
            #- cannot share
            g("XB3", "IVX1", A="DN", Y="DN_N"),
            g("XB4", "IVX1", A="PWRUP_1V8", Y="PWRUP_N"),
            g("XB5", "ORX1", A="HAD", B="RST", Y="HD"),
            g("XB6", "ANX1", A="HD", B="CK_FB", Y="HAD")])])

#- REY_PLL_DIVN ---------------------------------------------------------
DIVN_PINS = ([(VDD, "in"), (VSS, "in"), ("CK", "in"),
              ("CK_FB", "out")]
             + [(f"CKO{k}", "out") for k in range(len(TAPS))])


def _q(i):
    return "CK" if i < 0 else ("CK_FB" if i == NFB - 1 else f"Q{i}")


def _divn_columns():
    """Columns of two stages (NDIV / 2 of them). A stage is its flop with the tap
    buffer right above it, so Q reaches the buffer and the next flop's
    CK in one hop; Q of a column's top stage crosses to the next."""
    cols = []
    for c in range(NDIV // 2):
        L = "ABCDE"[c]
        insts = [tap(f"X{L}0")]
        n = 1
        for j in range(2):
            k = 2*c + j
            #- RN tied high: a ripple divider of toggling flops runs from
            #- any state, and the PFD does not care about the divider's
            #- phase. Each RN reaches its own flop's VDD strip on M5
            insts.append(g(f"X{L}{n}", "DFRNQNX1", D=f"QN{k}",
                           CK=_q(k - 1), RN=VDD, Q=_q(k),
                           QN=f"QN{k}"))
            n += 1
            if k == 1:
                #- stage 1 has no tap; a dummy inverter gives its Q an
                #- INPUT pin for the crossing to the next column to start
                #- from (a flop's Q lies under its VSS strip on M4)
                insts.append(g(f"X{L}{n}", "IVX1", A=_q(k), Y="Q1X"))
                n += 1
            if k in TAPS:
                t = list(TAPS).index(k)
                insts.append(g(f"X{L}{n}", "BFX1", A=_q(k), Y=f"CKO{t}"))
                n += 1
        cols.append((f"{L}: stages {2*c} and {2*c+1}", insts))
    return cols


DIVN = dict(
    cell="REY_PLL_DIVN", pins=DIVN_PINS,
    title=f"REY_PLL_DIVN: {NDIV} flop ripple divider, CK/{2**NFB} to the PFD",
    notes=["Flop k divides the previous one by two: Q<k> is CK/2^(k+1), "
           f"D = QN<k>. Q{NFB-1} is CK_FB. No reset: a ripple divider "
           "runs from any state",
           "Each tap has its buffer over its flop, so the pins do not "
           f"load the chain: CKO<t> = Q<t+2>, CK/8 .. CK/{2**(TAPS[-1]+1)}"],
    columns=_divn_columns())

#- REY_PLL_LPF ----------------------------------------------------------
LPF_PINS = [(VDD, "in"), (VSS, "in"), ("VCTRL", "in"), ("VLPFZ", "in")]


def _r(j):
    return {0: "VCTRL", 4*NRCU: "VLPFZ"}.get(j, f"R{j}")


def _lpf_columns():
    cols = []
    for c in range(NRCU // 2):
        L = "ABCD"[c]
        insts = []
        for j in range(2):
            i = 2*c + j
            conn = {}
            for k in range(4):
                conn[f"P{k}"] = _r(4*i + k)
                conn[f"N{k}"] = _r(4*i + k + 1)
            #- C2 is the FIRST cell: VCTRL's resistor end (R0) and its
            #- plate are then both at the left edge, VLPFZ's at the right
            conn.update(BR=VSS, A=VDD,
                        B="VCTRL" if i < NRCU - NC1 else "VLPFZ")
            insts.append((f"X{L}{j}", "REYPLL_RCU", conn))
        cols.append((f"{L}: R{8*c}..R{8*c+8}", insts))
    return cols


LPF = dict(
    cell="REY_PLL_LPF", pins=LPF_PINS,
    title="REY_PLL_LPF: loop filter on VDD_1V8, eight REYPLL_RCU",
    notes=[f"R: {4*NRCU} x 15.3 kOhm in series, VCTRL (R0) to VLPFZ "
           f"(R{4*NRCU}). C2: {NRCU - NC1} MiM (cell XA0), VCTRL to "
           f"VDD_1V8. C1: {NC1} MiM, VLPFZ to VDD_1V8",
           "MiM bottom plates (A) on VDD_1V8, so their parasitic to "
           "substrate does not load VCTRL"],
    columns=_lpf_columns())

BLOCKS = [CTRL, PFD, DIVN, LPF]


def columns(blk):
    """The xschem view: each layout column drawn as a column."""
    sh = sheet(blk["cell"], blk["pins"], blk["title"])
    #- the notes wrapped: one long line sets the width of the sheet, and
    #- the drawing under it shrinks to fit
    lines = [w for n in blk["notes"] for w in textwrap.wrap(n, NOTE)]
    for k, n in enumerate(lines):
        sh.text(n, -1450, -660 + 30*k, 0.3)
    y0 = -560 + 30*len(lines)
    for c, (label, insts) in enumerate(blk["columns"]):
        x = -1300 + 480*c
        sh.text(label, x - 60, y0, 0.35)
        y = y0 + 110
        for name, cell, conn in insts:
            ref = LIBS.get(cell, T) + cell + ".sym"
            sym = sh.symbol(ref)
            ys = [p[1] for p in sym.pins.values()]
            y -= min(ys)
            pins = dict(conn)
            for p in ("AVDD", "AVSS"):
                if p in sym.pins:
                    pins[p] = VDD if p == "AVDD" else VSS
            #- the supplies beside their pins, not stood on end over
            #- and under every gate: the column stays as tight as the
            #- cells, and the nets that matter are the ones that show
            sh.inst(ref, name, x, y, sides=LABELS.get(cell, BESIDE), **pins)
            #- the layout's name above the cell, clear of every label
            sh.text(name, x - 60, y + min(ys) - 32, 0.25)
            y += max(ys) + 70
    return sh


def subckt(blk):
    """The ciccreator view, for cic/pll.spi."""
    L = [f"* {blk['title']}",
         f".subckt {blk['cell']} " + " ".join(p for p, _ in blk["pins"])]
    for _label, insts in blk["columns"]:
        for name, cell, conn in insts:
            nodes = []
            for p in PORTS[cell]:
                if p == "AVDD":
                    nodes.append(conn.get(p, VDD))
                elif p == "AVSS":
                    nodes.append(conn.get(p, VSS))
                else:
                    nodes.append(conn[p])
            L.append(f"{name} {' '.join(nodes)} {BUILD.get(cell, cell)}")
    L.append(".ends")
    return "\n".join(L) + "\n"


def write_spi(path):
    with open(path, "w") as f:
        f.write("* REY_PLL standard cell blocks for cicpy compile "
                "(cic/pll.json).\n* GENERATED by py/gen_pll.py, do not "
                "edit: the same definitions write the\n* xschem "
                "schematics, so names and connections always agree. The\n"
                "* instance letter is the layout column.\n\n")
        for blk in BLOCKS:
            f.write(subckt(blk) + "\n")


#- --------------------------------------------------------------------
#- REY_PLL_CP
#- --------------------------------------------------------------------
CP_PINS = [(VDD, "in"), (VSS, "in"), ("VBP", "in"), ("UP", "in"),
           ("DN_N", "in"), ("VHI_N", "in"), ("VLO", "in"), ("KICK", "in"),
           ("VCTRL", "out"), ("VLPFZ", "out")]
MIR = "REYATR_LVT_PCH_4C5F0"    # 0.56 of the oscillator's 8C5F0 unit
NMIR = "REYATR_NCH_4C5F0"
SWP, SWN = "REYATR_PCH_2C1F2", "REYATR_NCH_2C1F2"
BIG_P, BIG_N = "REYATR_PCH_4C1F2", "REYATR_NCH_4C1F2"


def cp():
    sh = sheet("REY_PLL_CP", CP_PINS,
               "REY_PLL_CP: charge pump, UP sinks and DN sources (negative "
               "Kvco)")
    sh.text("Icp from the oscillator bias: one LVT_PCH_4C5F0 on VBP, "
            "about 1.1 to 2.8 uA over the trim codes", -1450, -640, 0.3)
    #- source branch: mirror, then the DN switch
    x = -1200
    sh.inst(A + MIR + ".sym", "xmpu", x, -500, G="VBP", S=VDD, B=VDD)
    sh.inst(A + SWP + ".sym", "xmpd", x, -380, G="DN_N", B=VDD)
    sh.wlab(*sh.pin("xmpu", "D"), *sh.pin("xmpd", "S"), RIGHT, "VPS")
    #- sink branch: UP switch, then the mirror
    sh.inst(A + SWN + ".sym", "xmnu", x, -230, G="UP", B=VSS)
    sh.inst(A + NMIR + ".sym", "xmns", x, -110, G="VBN", S=VSS, B=VSS)
    sh.wlab(*sh.pin("xmnu", "S"), *sh.pin("xmns", "D"), RIGHT, "VNS")
    #- the output between the switches
    xd, yd = sh.pin("xmpd", "D")
    xs, ys = sh.pin("xmnu", "D")
    sh.path((xd, yd), (xd, (yd + ys)//2))
    sh.path((xs, ys), (xs, (yd + ys)//2))
    sh.wire(xd, (yd + ys)//2, xd + 120, (yd + ys)//2)
    sh.lab(xd + 120, (yd + ys)//2, RIGHT, "VCTRL")
    #- the NMOS mirror's reference: a PMOS copy into a diode
    x = -850
    sh.inst(A + MIR + ".sym", "xmpn", x, -500, G="VBP", S=VDD, B=VDD)
    sh.inst(A + NMIR + ".sym", "xmnd", x, -110, G="VBN", S=VSS, B=VSS)
    xa, ya = sh.pin("xmpn", "D")
    xb, yb = sh.pin("xmnd", "D")
    sh.wlab(xa, ya, xb, yb, RIGHT, "VBN")

    sh.text("Parking and kick", -550, -640)
    x = -500
    sh.inst(A + BIG_P + ".sym", "xmph", x, -500, G="VHI_N", S=VDD,
            D="VCTRL", B=VDD)
    sh.inst(A + BIG_N + ".sym", "xmnl", x, -300, G="VLO", D="VCTRL",
            S=VSS, B=VSS)
    sh.inst(A + BIG_N + ".sym", "xmnk", x, -110, G="KICK", D="VLPFZ",
            S=VSS, B=VSS)
    sh.text("VHI_N low: VCTRL to VDD_1V8 (powered down, or OLH)",
            -550, -20, 0.3)
    sh.text("VLO high: VCTRL to VSS (OLL). KICK pulls C1 down at power up",
            -550, 10, 0.3)
    return sh


#- --------------------------------------------------------------------
#- REY_PLL, the top
#- --------------------------------------------------------------------
ROSC_PINS = [(VDD, "in"), (VSS, "in"), ("TRIM0", "in"), ("TRIM1", "in"),
             ("TRIM2", "in"), ("VCTRL", "in"), ("CK", "out"),
             ("VBP", "out")]
TOP_PINS = ([(VDD, "in"), (VSS, "in"), ("PWRUP_1V8", "in"),
             ("CK_REF", "in"), ("TRIM0", "in"), ("TRIM1", "in"),
             ("TRIM2", "in"), ("OLH", "in"), ("OLL", "in"), ("CK", "out")]
            + [(f"CKO{k}", "out") for k in range(len(TAPS))])


def top(subs):
    sh = sheet("REY_PLL", TOP_PINS,
               f"REY_PLL: {FREF * 2**NFB} MHz from {FREF} MHz, current starved "
               "ring oscillator")
    for name, s in subs.items():
        sh.add_local(P + name + ".sym", s)
    sh.local[P + "REY_PLL_ROSC.sym"] = box_symbol(ROSC_PINS)
    same = {p: p for p, _ in TOP_PINS}

    def place(cell, name, x, y, pins, wired=()):
        #- a label on every pin but the ones a wire is drawn to
        sh.inst(P + cell + ".sym", name, x, y,
                **{p: same.get(p, p) for p, _ in pins if p not in wired})

    def run(net, rot, *pts, at=0):
        """A wire through pts carrying net, its label on segment at."""
        segs = [(a, b) for a, b in zip(pts, pts[1:]) if a != b]
        for k, ((x1, y1), (x2, y2)) in enumerate(segs):
            if k == at:
                sh.wlab(x1, y1, x2, y2, rot, net)
            else:
                sh.wire(x1, y1, x2, y2)

    sh.text("CK_REF -> PFD -> CP -> LPF -> VCTRL -> ROSC -> DIVN -> CK_FB",
            -1450, -640, 0.4)
    #- The loop drawn as a loop, left to right, its nets as wires. Each
    #- block sits at the height that makes its wire straight: PFD and CP
    #- share UP and DN_N, the oscillator's VCTRL pin is on the charge
    #- pump's, the divider's CK on the oscillator's. The filter hangs
    #- under VCTRL, the control block under the PFD; what the control
    #- block and the bias hand over (KICK, VHI_N, VLO, VBP) stays a label.
    #- Same order of instances as ever, so the netlist does not move
    y = -250
    place("REY_PLL_CTRL", "xctrl", -1150, y + 280, CTRL_PINS)
    place("REY_PLL_PFD", "xpfd", -1150, y, PFD_PINS,
          wired=("UP", "DN_N", "CK_FB"))
    place("REY_PLL_CP", "xcp", -600, y, CP_PINS,
          wired=("UP", "DN_N", "VCTRL", "VLPFZ"))
    place("REY_PLL_LPF", "xlpf", -50, y + 130, LPF_PINS,
          wired=("VCTRL", "VLPFZ"))
    place("REY_PLL_ROSC", "xrosc", 100, y - 140, ROSC_PINS,
          wired=("VCTRL", "CK"))
    place("REY_PLL_DIVN", "xdivn", 650, y - 200, DIVN_PINS,
          wired=("CK", "CK_FB"))
    pin = sh.pin
    run("UP", UP, pin("xpfd", "UP"), pin("xcp", "UP"))
    run("DN_N", DOWN, pin("xpfd", "DN_N"), pin("xcp", "DN_N"))
    #- VCTRL: charge pump to oscillator, the filter's R on a branch down
    (x1, y1), (x2, y2) = pin("xcp", "VCTRL"), pin("xrosc", "VCTRL")
    assert y1 == y2, "VCTRL is drawn straight"
    xt = x1 + 100
    sh.path((x1, y1), (xt, y1), (x2, y2))
    xl, yl = pin("xlpf", "VCTRL")
    run("VCTRL", RIGHT, (xt, y1), (xt, yl), (xl, yl))
    #- VLPFZ: the filter's zero, C1 and the kick, inside that branch
    (x1, y1), (xl, yl) = pin("xcp", "VLPFZ"), pin("xlpf", "VLPFZ")
    run("VLPFZ", LEFT, (x1, y1), (xt - 50, y1), (xt - 50, yl), (xl, yl),
        at=1)
    run("CK", UP, pin("xrosc", "CK"), pin("xdivn", "CK"))
    #- CK_FB: out of the divider and back round under everything
    (x1, y1), (x2, y2) = pin("xdivn", "CK_FB"), pin("xpfd", "CK_FB")
    xr, yb, xw = x1 + 120, y + 450, x2 - 150
    run("CK_FB", RIGHT, (x1, y1), (xr, y1), (xr, yb), (xw, yb), (xw, y2),
        (x2, y2), at=1)
    return sh


def main():
    subs = {}
    for blk in BLOCKS:
        s = columns(blk)
        s.write(outdir)
        subs[s.cell] = s
    s = cp()
    s.write(outdir)
    subs[s.cell] = s
    top(subs).write(outdir)
    cic = os.path.join(os.path.dirname(__file__), "..", "cic")
    write_spi(os.path.join(cic, "pll.spi"))
    ctrl_layout(cic)
    pfd_layout(cic)
    divn_layout(cic)
    lpf_layout(cic)



#- --------------------------------------------------------------------
#- REY_PLL_DIVN's routes, written into cic/pll.json from the netlist
#- --------------------------------------------------------------------
#- Columns B and D are mirrored (alternateGroup) so n-wells face n-wells;
#- there the pins sit on the other side and the offsets differ. Offsets
#- are in routing tracks from each route's default, never coordinates:
#- the supply rings round a digital block, li: width and space in
#- multiples of the rule. The cells' M4 strips carry the current; the
#- rings are where the strips and the top's straps land
RING = (2, 2)
#- rails above and below only: no ring sides, the strips reach both
SIDES = "tb"


def _straps(pat):
    """One M4 strap per column and supply, onto the rail below AND the
    rail above, which are joined by nothing else."""
    return [["M4", net, f"{pat}:{pin}||rail_{s}_{net}", ""]
            for net, pin in (("VSS", "AVSS"), ("VDD_1V8", "AVDD"))
            for s in "bt"]

DTRK, DTRK_M = "track13", "track-22"     # D = QN loop: trunk right of the
                                         # flop's own M3 (x > 8.83 um)
HTRK = "track-13,endoffsetcutlow"        # Q hops: trunk left of the input
HTRK_M = "track6,endoffsetcutlow"        # pins; via low on BFX1.A (li.3)
XOPT = "startLayer=M2,track16"           # crossings from a normal column:
                                         # right of its M5 reset jumpers
XOPT_M = "startLayer=M2,track1"          # ... from a mirrored column
TAP = "track-13,offset_track-9"          # a mid-height tap up the outer
TAP_M = "track6,offset_track7"           # lane, its pin over the lane


def divn_layout(cic):
    """Directed routes for REY_PLL_DIVN, one per connection, generated
    from the subckt in cic/pll.spi:

      - D = QN: from M2 (the flop's own via on QN) out at QN's height,
        down a trunk beyond the flop's own M3, into D
      - RN tied high: a straight M5 jumper from RN onto the flop's own
        VDD strip
      - Q to the stage buffer and the next flop's CK in the column: one
        hop on M2, trunk left of the input pins
      - Q to the next column: on M5, from the stage buffer's (or the
        dummy inverter's) INPUT pin, since a flop's Q lies under its VSS
        strip on M4
      - one supply strap per column to the rings
    """
    import json
    spi = open(os.path.join(cic, 'pll.spi')).read()
    body = spi[spi.index('.subckt REY_PLL_DIVN'):]
    body = body[:body.index('.ends')]
    insts = [l.split() for l in body.split('\n')[1:] if l.startswith('X')]
    dffs = [(t[0], dict(zip(["D", "CK", "RN", "Q", "QN"], t[1:6])))
            for t in insts if t[-1].endswith('DFRNQNX1_CV')]
    ins = {}
    for t in insts:
        if t[-1] in ('REYTR_BFX1_CV', 'REYTR_IVX1_CV'):
            ins.setdefault(t[1], []).append((t[0], 'A'))


    def col(n):
        return n[1]


    def mir(n):
        #- alternateGroup mirrors every other column (B, D) so n-wells
        #- face n-wells; there the pins sit on the other side
        return n[1] in "BD"


    def opt(*xs):
        return ",".join(x for x in xs if x)


    #- one strap per column: "X:AVDD||rail" joins every column's strips
    #- into ONE strap at one x, and leaves the other columns open
    directed = []
    for L in sorted({t[0][1] for t in insts}):
        directed += _straps(f"X{L}\\d+")
    for name, p in dffs:
        #- D = QN: start on M2 where the flop has its own via on QN, out at
        #- QN's height, down a trunk beyond the flop's own M3, into D
        directed.append(["M3", p["QN"], f"{name}:QN-|--{name}:D",
                         opt("startLayer=M2", DTRK_M if mir(name) else DTRK)])
    for name, p in dffs:
        #- RN tied high: from M2 (the flop's own via on RN) up to M5, across
        #- the VSS strip, down onto the flop's own VDD strip
        directed.append(["M5", "VDD_1V8", f"{name}:RN-{name}:AVDD",
                         "startLayer=M2"])
    for name, p in dffs:
        q = p["Q"]
        loc = [f"{i}:{pin}" for i, pin in ins.get(q, []) if col(i) == col(name)]
        nxt = [n for n, pp in dffs if pp["CK"] == q]
        loc += [f"{n}:CK" for n in nxt if col(n) == col(name)]
        if loc:
            directed.append(["M2", q, f"{name}:Q-|--{','.join(loc)}",
                             HTRK_M if mir(name) else HTRK])
        far = [n for n in nxt if col(n) != col(name)]
        if far:
            src = [i for i, pin in ins.get(q, []) if col(i) == col(name)][0]
            #- a crossing from a normal column passes right of that
            #- column's M5 reset jumpers; from a mirrored one it starts
            #- right of them already
            directed.append(["M5", q, f"{src}:A-|--{far[0]}:CK",
                             XOPT_M if mir(name) else XOPT])

    o = json.load(open(os.path.join(cic, 'pll.json')))
    for c in o['cells']:
        if c['name'] != 'REY_PLL_DIVN':
            continue
        c['alternateGroup'] = 1
        c['afterPlace'] = [{"addRouteRings": [
            ["M1", "VSS", SIDES, *RING], ["M1", "VDD_1V8", SIDES, *RING],
            ["M5", "CK", "l", 1, 2]]},
            {"addPowerRings": []}]
        c['beforeRoute'] = {
            "addDirectedRoutes": directed,
            "addRouteConnections": [["^CK$", "XA1$", "left", "M4", ""]],
            "addConnectivityRoutes": []}
        c['afterRoute'] = {"addPortOnRects": [
            [t[2], "M1", t[0] + ":Y"] for t in insts if t[-1] == 'REYTR_BFX1_CV']
            #- CK_FB leaves upwards from its tap buffer's input
            + [["CK_FB", "M1", "%s:%s" % ins["CK_FB"][0]]]}
        #- CK_FB to the top edge for the PFD: straight up on M5 from the
        #- tap buffer's input. Where the net goes on to the next column,
        #- that crossing already stacks it up to M5 there (no second cut
        #- on the pin); the last stage's has only the hop on M2. The
        #- pin on the edge is one wire across, not the input's 0.9 um:
        #- the tap beside it rises on M5 too, from the top level
        #- The taps leave upwards too, on M3: a buffer's Y lies under
        #- its VSS strip on M4. The buffer at the top of a column goes
        #- straight off its pin; the one at mid height takes the outer
        #- lane, which the hops use on M2 only, and its pin stands over
        #- that lane, clear of the other tap's
        fb = [n for n, pp in dffs if pp["Q"] == "CK_FB"][0]
        crosses = any(pp["CK"] == "CK_FB" and col(n) != col(fb)
                      for n, pp in dffs)
        edge = [["M5", "CK_FB", "top", "||",
                 opt("nostartcut" if crosses else "startLayer=M2",
                     "narrowpin")]]
        bufs = [t for t in insts if t[-1] == 'REYTR_BFX1_CV']
        for t in bufs:
            top = t[0] == max((b[0] for b in bufs if col(b[0]) == col(t[0])),
                              key=lambda n: int(n[2:]))
            if top:
                o_ = ""
            else:
                o_ = TAP_M if mir(t[0]) else TAP
            edge.append(["M3", t[2], "top", "-|--", o_])
        c['afterPaint'] = {"resetOrigin": 1, "addPortOnEdges": edge}
    json.dump(o, open(os.path.join(cic, 'pll.json'), 'w'), indent=4)
    log.info(f"pll.json: REY_PLL_DIVN, {len(directed)} directed routes")



#- --------------------------------------------------------------------
#- REY_PLL_CTRL's supplies and ports
#- --------------------------------------------------------------------
#- The signal routes are the connectivity routes already in pll.json:
#- every net is a hop between neighbouring cells.
def ctrl_layout(cic):
    import json
    o = json.load(open(os.path.join(cic, 'pll.json')))
    for c in o['cells']:
        if c['name'] != 'REY_PLL_CTRL':
            continue
        c['afterPlace'] = [{"addRouteRings": [
            ["M1", "VSS", SIDES, *RING], ["M1", "VDD_1V8", SIDES, *RING]]},
            {"addPowerRings": []}]
        c['beforeRoute']['addDirectedRoutes'] = _straps("XA\\d+")
        c['afterRoute'] = {"addPortOnRects": [
            ["OLH", "M1", "XA9:B"], ["OLL", "M1", "XA10:B"]]}
        #- PWRUP_1V8 out to the left, towards the PFD; the three outputs
        #- to the right, towards the pump. OLH and OLL go to pads: up on
        #- M5, which nothing else in the block uses, right of the input
        #- pins. OLL's cell is the upper one and takes the near lane,
        #- OLH's stub passes below where that lane starts; its edge pin
        #- stands over its own lane, clear of OLL's
        c['afterPaint'] = {"resetOrigin": 1, "addPortOnEdges": [
            ["M4", "PWRUP_1V8", "left", "--|-", "nostartcut"],
            ["M5", "OLL", "top", "-|--", ""],
            ["M5", "OLH", "top", "-|--", "track4,offset_track7"],
            ["M3", "KICK", "right", "-|--", ""],
            ["M3", "VHI_N", "right", "-|--", ""],
            ["M3", "VLO", "right", "-|--", ""]]}
    json.dump(o, open(os.path.join(cic, 'pll.json'), 'w'), indent=4)
    log.info("pll.json: REY_PLL_CTRL")


#- --------------------------------------------------------------------
#- REY_PLL_PFD's routes
#- --------------------------------------------------------------------
#- Column B is mirrored (alternateGroup): the flops' D pins face each
#- other across the seam, the input pins stand along the block's two
#- outer edges. A rey_tr cell leaves three lanes for a trunk:
#-
#-   outer   between the cell's edge and its input pins, M2 and M3:
#-           from an OUTPUT to inputs (track-13, mirrored track6)
#-   middle  between the input pins and the outputs, M2 and M3: from
#-           an INPUT, no offset; its stubs cross no other lane
#-   edge    left of the outer lane, M4 and M5: input to input, since
#-           an output lies under its VSS strip and stops at M3
#-
#- An outer route's stub from its output crosses the middle lane, so
#- the two never share a layer where they overlap. Across the columns
#- a net goes on M5, straight, between input pins at one height.
PO, PO_M = "track-13", "track6"          # outer lane


def pfd_layout(cic):
    """Directed routes for REY_PLL_PFD, replacing the ten signal rings
    the block had: every net is a hop in its column or one bar across."""
    import json
    directed = []
    for L in "AB":
        directed += _straps(f"X{L}\\d+")
    directed += [
        #- A, the UP half. RN from the latch: up the middle lane on M2,
        #- off the flop's own via on RN
        ["M2", "RN_U", "XA1:RN-|--XA2:Y", "startLayer=M2"],
        ["M3", "UP", "XA1:Q-|--XA3:B", PO],
        ["M2", "HU", "XA4:Y-|--XA2:A,XA5:A", PO],
        ["M3", "RST", "XA3:Y-|--XA4:A", PO],
        ["M3", "HAU", "XA5:Y-|--XA4:B", PO],
        ["M4", "CK_REF", "XA1:CK|-XA5:B", "track1"],
        #- B, the DN half, mirrored. PWRUP_N overlaps DN and HD, so it
        #- takes the middle lane, on M3 over RN_D's M2
        ["M2", "RN_D", "XB1:RN--|-XB2:Y", "startLayer=M2"],
        ["M3", "DN", "XB1:Q-|--XB3:A", PO_M],
        ["M2", "HD", "XB5:Y-|--XB2:A,XB6:A", PO_M],
        ["M3", "HAD", "XB6:Y-|--XB5:A", PO_M],
        ["M3", "PWRUP_N", "XB2:B--|-XB4:Y", ""],
        ["M4", "CK_FB", "XB1:CK-|XB6:B", "track1"],
        #- across. The end a hop already stands on starts from the
        #- hop's layer: one stack on a pin, not two
        ["M5", "PWRUP_N", "XA2:B-XB2:B", "stopLayer=M3"],
        ["M5", "DN", "XA3:A-XB3:A", "stopLayer=M3"],
        ["M5", "RST", "XA4:A-XB5:B", "startLayer=M3"],
        #- PWRUP_1V8: the two D pins across the seam on M4, then from
        #- the inverter down B's edge lane on M5, over the flop to D
        ["M4", "PWRUP_1V8", "XA1:D-XB1:D", ""],
        ["M5", "PWRUP_1V8", "XB4:A-|--XB1:D", "track0,stopLayer=M4"],
    ]

    o = json.load(open(os.path.join(cic, 'pll.json')))
    for c in o['cells']:
        if c['name'] != 'REY_PLL_PFD':
            continue
        c['alternateGroup'] = 1
        c['afterPlace'] = [{"addRouteRings": [
            ["M1", "VSS", SIDES, *RING], ["M1", "VDD_1V8", SIDES, *RING]]},
            {"addPowerRings": []}]
        c['beforeRoute'] = {
            "addDirectedRoutes": directed,
            "addConnectivityRoutes": []}
        #- the pin each port leaves from
        c['afterRoute'] = {"addPortOnRects": [
            ["UP", "M1", "XA1:Q"], ["DN_N", "M1", "XB3:Y"],
            ["CK_REF", "M1", "XA5:B"], ["CK_FB", "M1", "XB6:B"],
            ["PWRUP_1V8", "M1", "XB4:A"]]}
        #- every port on the top edge: the block stands in the top row,
        #- its neighbours and the pads are reached from above. Outputs up
        #- the lane between the cells' supply strips on M3 (free above
        #- the flops); the clocks straight off the topmost pin of the
        #- net, on the M4 it already has; PWRUP_1V8 on up B's edge lane,
        #- where its M5 already runs down to the flops
        c['afterPaint'] = {"resetOrigin": 1, "addPortOnEdges": [
            ["M3", "UP", "top", "-|--", "nostartcut"],
            ["M3", "DN_N", "top", "--|-", ""],
            ["M4", "CK_REF", "top", "||", "nostartcut"],
            ["M4", "CK_FB", "top", "||", "nostartcut"],
            ["M5", "PWRUP_1V8", "top", "-|--", "nostartcut"]]}
    json.dump(o, open(os.path.join(cic, 'pll.json'), 'w'), indent=4)
    log.info(f"pll.json: REY_PLL_PFD, {len(directed)} directed routes")



#- --------------------------------------------------------------------
#- REY_PLL_LPF's routes
#- --------------------------------------------------------------------
#- The MiMs cover each RCU on M4/M5 (met3/met4): unrelated met3 must
#- keep 1.34 um from a MiM, via2/via3 keep clear of it too. So the
#- resistor chain stays on M2 (hops in a column) and M3 (column to
#- column), VCTRL and VLPFZ leave sideways on M3 and climb to M5 only on
#- their bars outside the cells; the top plates join along the cells'
#- bottom margins on M5, the bottom plates (VDD) by a strap per column.
LTRK = "track1"          # chain hops: trunk right of the resistor pins


def lpf_layout(cic):
    import json
    spi = open(os.path.join(cic, "pll.spi")).read()
    body = spi[spi.index(".subckt REY_PLL_LPF"):]
    body = body[:body.index(".ends")]
    ports = ["P0", "N0", "P1", "N1", "P2", "N2", "P3", "N3", "BR", "A", "B"]
    cells = [(t[0], dict(zip(ports, t[1:12])))
             for t in (l.split() for l in body.split("\n")[1:])
             if t and t[0].startswith("X")]
    directed = []
    for L in sorted({n[1] for n, _ in cells}):
        directed += [["M4", "VDD_1V8", f"X{L}\\d+:A||rail_t_VDD_1V8", ""],
                     ["M2", "VSS", f"X{L}\\d+:BR||rail_t_VSS", ""]]
    #- the chain: N<k> to the next resistor's P, in the cell or the next
    for idx, (name, p) in enumerate(cells):
        for k in range(4):
            net = p[f"N{k}"]
            if k < 3:
                directed.append(["M2", net, f"{name}:N{k}-|--{name}:P{k+1}",
                                 LTRK])
            elif idx + 1 < len(cells):
                nxt = cells[idx + 1][0]
                lay = "M2" if nxt[1] == name[1] else "M3"
                directed.append([lay, net, f"{name}:N3-|--{nxt}:P0", LTRK])
    #- top plates: VLPFZ along each row's bottom margin, straight on M5
    rows = {}
    for name, p in cells:
        rows.setdefault(name[2:], []).append((name, p["B"]))
    for _, row in sorted(rows.items()):
        vl = [n for n, b in row if b == "VLPFZ"]
        if len(vl) > 1:
            directed.append(["M5", "VLPFZ", f"{vl[0]}:B-{vl[-1]}:B", ""])
    first, last = cells[0][0], cells[-1][0]
    rightmost = [n for n, _ in cells if n[1] == last[1]]
    #- to the bars by name: a connection by net and instance would take
    #- every VCTRL pin on XA0, the resistor end AND the plate, and drop
    #- an M1-M5 stack inside the MiM
    directed += [["M3", "VCTRL", f"{first}:P0-rail_l_VCTRL", ""],     # R0
                 ["M5", "VCTRL", f"{first}:B-rail_l_VCTRL", ""],      # C2
                 ["M3", "VLPFZ", f"{last}:N3-rail_r_VLPFZ", ""]]      # R32
    directed += [["M5", "VLPFZ", f"{n}:B-rail_r_VLPFZ", ""]
                 for n in rightmost]
    conn = []
    o = json.load(open(os.path.join(cic, "pll.json")))
    for c in o["cells"]:
        if c["name"] != "REY_PLL_LPF":
            continue
        c.pop("alternateGroup", None)
        #- supply rails on M2: on li they come too close to the RCUs'
        #- own li at the cell edge (BR sticks out of the cell's box).
        #- Both above the cells only, where the top's straps reach them:
        #- ring sides would cost the row 7 um
        c["afterPlace"] = [{"addRouteRings": [
            ["M2", "VSS", "t", 4, 2], ["M2", "VDD_1V8", "t", 4, 2],
            ["M5", "VCTRL", "l", 1, 2], ["M5", "VLPFZ", "r", 1, 2]]},
            {"addPowerRings": []}]
        c["beforeRoute"] = {"addDirectedRoutes": directed,
                            "addRouteConnections": conn,
                            "addConnectivityRoutes": []}
        c["afterPaint"] = {"resetOrigin": 1}
    json.dump(o, open(os.path.join(cic, "pll.json"), "w"), indent=4)
    log.info(f"pll.json: REY_PLL_LPF, {len(directed)} directed routes")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
