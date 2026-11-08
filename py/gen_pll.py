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
  REY_PLL_DIVN  ten flop ripple divider, CK/64 is the feedback, eight
                buffered taps CK/8..CK/1024 for the pins
  REY_PLL       the top

The schematics are written with cicpy.eda.schgen; the oscillator comes
from py/gen_rosc.py.
"""
import logging
import os
import sys

from cicpy.eda.schgen import Sheet, box_symbol, RIGHT

A = "REY_ATR_SKY130A/"
T = "REY_TR_SKY130A/"
P = "REY_PLL_SKY130A/"
VDD, VSS = "VDD_1V8", "VSS"
SUP = dict(AVDD=VDD, AVSS=VSS)

NDIV = 10                 # flops in the divider
NFB = 6                   # feedback after this many: CK/64
TAPS = range(2, 10)       # Q2 (CK/8) .. Q9 (CK/1024)
NRCU = 8                  # loop filter unit cells
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
        ("A: UP side", [
            tap("XA0"),
            g("XA1", "DFRNQNX1", D=VDD, CK="CK_REF", RN="RN_U", Q="UP",
              QN="UP_N"),
            g("XA2", "ANX1", A="HU", B="CK_REF", Y="HAU"),
            g("XA3", "ORX1", A="HAU", B="RST", Y="HU"),
            g("XA4", "NRX1", A="HU", B="PWRUP_N", Y="RN_U"),
            g("XA5", "ANX1", A="UP", B="DN", Y="RST")]),
        ("B: DN side", [
            tap("XB0"),
            g("XB1", "DFRNQNX1", D=VDD, CK="CK_FB", RN="RN_D", Q="DN",
              QN="DN_N"),
            g("XB2", "ANX1", A="HD", B="CK_FB", Y="HAD"),
            g("XB3", "ORX1", A="HAD", B="RST", Y="HD"),
            g("XB4", "NRX1", A="HD", B="PWRUP_N", Y="RN_D"),
            g("XB5", "IVX1", A="PWRUP_1V8", Y="PWRUP_N")])])

#- REY_PLL_DIVN ---------------------------------------------------------
DIVN_PINS = ([(VDD, "in"), (VSS, "in"), ("PWRUP_1V8", "in"), ("CK", "in"),
              ("CK_FB", "out")]
             + [(f"CKO{k}", "out") for k in range(len(TAPS))])


def _q(i):
    return "CK" if i < 0 else ("CK_FB" if i == NFB - 1 else f"Q{i}")


def _divn_columns():
    cols = []
    for c in range(NDIV // 2):
        L = "ABCDE"[c]
        insts = [tap(f"X{L}0")]
        for j in range(2):
            k = 2*c + j
            insts.append(g(f"X{L}{j+1}", "DFRNQNX1", D=f"QN{k}", CK=_q(k - 1),
                           RN="PWRUP_1V8", Q=_q(k), QN=f"QN{k}"))
        cols.append((f"{L}: flops {2*c} and {2*c+1}", insts))
    cols.append(("F: tap buffers", [tap("XF0")] + [
        g(f"XF{t+1}", "BFX1", A=_q(k), Y=f"CKO{t}")
        for t, k in enumerate(TAPS)]))
    return cols


DIVN = dict(
    cell="REY_PLL_DIVN", pins=DIVN_PINS,
    title=f"REY_PLL_DIVN: {NDIV} flop ripple divider, CK/{2**NFB} to the PFD",
    notes=["Flop k divides the previous one by two: Q<k> is CK/2^(k+1), "
           f"D = QN<k>. Q{NFB-1} is CK_FB",
           "Column F: one buffer per tap so the pins do not load the "
           "chain, CKO<t> = Q<t+2>, CK/8 .. CK/1024"],
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
            conn.update(BR=VSS, A=VDD,
                        B="VLPFZ" if i < NC1 else "VCTRL")
            insts.append((f"X{L}{j}", "REYPLL_RCU", conn))
        cols.append((f"{L}: R{8*c}..R{8*c+8}", insts))
    return cols


LPF = dict(
    cell="REY_PLL_LPF", pins=LPF_PINS,
    title="REY_PLL_LPF: loop filter on VDD_1V8, eight REYPLL_RCU",
    notes=[f"R: {4*NRCU} x 15.3 kOhm in series, VCTRL (R0) to VLPFZ "
           f"(R{4*NRCU}). C1: {NC1} MiM, VLPFZ to VDD_1V8. C2: "
           f"{NRCU - NC1} MiM, VCTRL to VDD_1V8",
           "MiM bottom plates (A) on VDD_1V8, so their parasitic to "
           "substrate does not load VCTRL"],
    columns=_lpf_columns())

BLOCKS = [CTRL, PFD, DIVN, LPF]


def columns(blk):
    """The xschem view: each layout column drawn as a column."""
    sh = sheet(blk["cell"], blk["pins"], blk["title"])
    for k, n in enumerate(blk["notes"]):
        sh.text(n, -1450, -660 + 30*k, 0.3)
    y0 = -560 + 30*len(blk["notes"])
    for c, (label, insts) in enumerate(blk["columns"]):
        x = -1300 + 480*c
        sh.text(label, x - 60, y0, 0.35)
        y = y0 + 80
        for name, cell, conn in insts:
            ref = LIBS.get(cell, T) + cell + ".sym"
            sym = sh.symbol(ref)
            ys = [p[1] for p in sym.pins.values()]
            y -= min(ys)
            pins = dict(conn)
            for p in ("AVDD", "AVSS"):
                if p in sym.pins:
                    pins[p] = VDD if p == "AVDD" else VSS
            sh.inst(ref, name, x, y, **pins)
            sh.text(name, x + 120, y - 6, 0.25)
            y += max(ys) + 60
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
    sh.text("VHI_N low: VCTRL to VDD_1V8 (powered down, or OLH). VLO "
            "high: VCTRL to VSS (OLL). KICK pulls C1 down at power up",
            -550, -20, 0.3)
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
               "REY_PLL: 512 MHz from 8 MHz, current starved ring "
               "oscillator")
    for name, s in subs.items():
        sh.add_local(P + name + ".sym", s)
    sh.local[P + "REY_PLL_ROSC.sym"] = box_symbol(ROSC_PINS)
    same = {p: p for p, _ in TOP_PINS}

    def place(cell, name, x, y, pins, **ren):
        conn = {p: ren.get(p, same.get(p, p)) for p, _ in pins}
        sh.inst(P + cell + ".sym", name, x, y, **conn)

    sh.text("CK_REF -> PFD -> CP -> LPF -> VCTRL -> ROSC -> DIVN -> CK_FB",
            -1450, -640, 0.4)
    place("REY_PLL_CTRL", "xctrl", -1200, -150, CTRL_PINS)
    place("REY_PLL_PFD", "xpfd", -1200, -450, PFD_PINS)
    place("REY_PLL_CP", "xcp", -800, -450, CP_PINS)
    place("REY_PLL_LPF", "xlpf", -800, -150, LPF_PINS)
    place("REY_PLL_ROSC", "xrosc", -400, -450, ROSC_PINS)
    place("REY_PLL_DIVN", "xdivn", -400, -100, DIVN_PINS)
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
    write_spi(os.path.join(os.path.dirname(__file__), "..", "cic",
                           "pll.spi"))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
