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

from cicpy.eda.schgen import Sheet, bus, nets, box_symbol, UP, RIGHT

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
#- REY_PLL_CTRL
#- --------------------------------------------------------------------
CTRL_PINS = [(VDD, "in"), (VSS, "in"), ("PWRUP_1V8", "in"), ("OLH", "in"),
             ("OLL", "in"), ("KICK", "out"), ("VHI_N", "out"),
             ("VLO", "out")]


def ctrl():
    sh = sheet("REY_PLL_CTRL", CTRL_PINS,
               "REY_PLL_CTRL: power up, start-up kick and open loop modes")
    sh.text("KICK: a pulse when PWRUP_1V8 rises. KD4 is PWRUP_1V8 "
            "delayed by five inverters, so NOR(PWRUP_N, KD4) is high "
            "between the edge and KD4", -1450, -640, 0.3)
    sh.inst(T + "REYTR_IVX1_CV.sym", "xi0", -1300, -500, A="PWRUP_1V8",
            **SUP)
    x, y = sh.pin("xi0", "Y")
    sh.wlab(x, y, x + 100, y, UP, "PWRUP_N")
    #- the delay line, drawn once as a bus
    sh.inst(T + "REYTR_IVX1_CV.sym", bus("xkd", 5), -1100, -500,
            A=nets("KD", range(3, -1, -1)) + ",PWRUP_N",
            Y=nets("KD", range(4, -1, -1)), **SUP)
    sh.inst(T + "REYTR_NRX1_CV.sym", "xk", -850, -490, A="PWRUP_N",
            B="KD4", Y="KICK", **SUP)

    sh.text("Open loop, for the per-die trim: OLH parks VCTRL at VDD_1V8 "
            "(slowest), OLL at VSS (fastest). Powered down is OLH",
            -1450, -300, 0.3)
    sh.inst(T + "REYTR_NRX1_CV.sym", "xo0", -1300, -150, A="PWRUP_N",
            B="OLH", **SUP)
    x, y = sh.pin("xo0", "Y")
    sh.wlab(x, y, x + 120, y, UP, "VHI_N")
    sh.inst(T + "REYTR_ANX1_CV.sym", "xo1", x + 120, y + 20,
            B="OLL", Y="VLO", **SUP)
    sh.text("VHI_N = PWRUP and not OLH. VLO = VHI_N and OLL, so OLH "
            "wins", -1450, -60, 0.3)
    sh.inst(T + "REYTR_TAPCELLB_CV.sym", "xtap", -600, -150, **SUP)
    return sh


#- --------------------------------------------------------------------
#- REY_PLL_PFD
#- --------------------------------------------------------------------
PFD_PINS = [(VDD, "in"), (VSS, "in"), ("PWRUP_1V8", "in"), ("CK_REF", "in"),
            ("CK_FB", "in"), ("UP", "out"), ("DN_N", "out")]


def pfd():
    sh = sheet("REY_PLL_PFD", PFD_PINS,
               "REY_PLL_PFD: tri-state phase frequency detector")
    sh.text("UP rises on CK_REF, DN on CK_FB. When both are high RST "
            "clears them; the path through the gates is the reset pulse "
            "that keeps the dead zone away", -1450, -640, 0.3)
    sh.text("DFRNQNX1 clocks on NAND(CK, RN): released from reset while "
            "CK is high it sees a rising edge and sets again. So each "
            "flop's reset is HELD until its own clock is low:", -1450,
            -610, 0.3)
    sh.text("HU = RST or (HU and CK_REF), RN_U = PWRUP and not HU; the "
            "same for DN on CK_FB", -1450, -580, 0.3)
    sh.inst(T + "REYTR_DFRNQNX1_CV.sym", "xdu", -1300, -380, D=VDD,
            CK="CK_REF", RN="RN_U", Q="UP", QN="UP_N", **SUP)
    sh.inst(T + "REYTR_DFRNQNX1_CV.sym", "xdd", -1300, -150, D=VDD,
            CK="CK_FB", RN="RN_D", Q="DN", QN="DN_N", **SUP)
    #- RST = UP and DN
    sh.inst(T + "REYTR_ANX1_CV.sym", "xr0", -1050, -250, A="UP", B="DN",
            Y="RST", **SUP)
    sh.inst(T + "REYTR_IVX1_CV.sym", "xr1", -1050, -100, A="PWRUP_1V8",
            Y="PWRUP_N", **SUP)
    #- the two hold latches, drawn the same way, UP above DN
    for side, ck, yy in (("U", "CK_REF", -400), ("D", "CK_FB", -170)):
        x = -800
        sh.inst(T + "REYTR_ANX1_CV.sym", f"xh{side.lower()}a", x, yy,
                A=f"H{side}", B=ck, **SUP)
        x1, y1 = sh.pin(f"xh{side.lower()}a", "Y")
        sh.inst(T + "REYTR_ORX1_CV.sym", f"xh{side.lower()}o", x1 + 80,
                y1 + 20, A=None, B="RST", **SUP)
        sh.wlab(x1, y1, x1 + 80, y1, UP, f"HA{side}")
        x2, y2 = sh.pin(f"xh{side.lower()}o", "Y")
        sh.inst(T + "REYTR_NRX1_CV.sym", f"xh{side.lower()}n", x2 + 80,
                y2 + 20, B="PWRUP_N", Y=f"RN_{side}", **SUP)
        sh.wlab(x2, y2, x2 + 80, y2, UP, f"H{side}")
    #- one tap per layout column, UP side and DN side
    sh.inst(T + "REYTR_TAPCELLB_CV.sym", bus("xtap", 2), -250, -250, **SUP)
    return sh


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
#- REY_PLL_LPF
#- --------------------------------------------------------------------
LPF_PINS = [(VDD, "in"), (VSS, "in"), ("VCTRL", "in"), ("VLPFZ", "in")]


def lpf():
    sh = sheet("REY_PLL_LPF", LPF_PINS,
               "REY_PLL_LPF: loop filter on VDD_1V8, eight REYPLL_RCU")
    sh.text(f"R: {4*NRCU} x 15.3 kOhm in series, VCTRL to VLPFZ "
            f"({4*NRCU*15.3:.0f} kOhm). C1: {NC1} MiM, VLPFZ to VDD_1V8. "
            f"C2: {NRCU - NC1} MiM, VCTRL to VDD_1V8", -1450, -640, 0.3)
    sh.text("MiM bottom plates (A) on VDD_1V8, so their parasitic to "
            "substrate does not load VCTRL", -1450, -610, 0.3)
    idx = range(NRCU - 1, -1, -1)

    def r(j):
        return {0: "VCTRL", 4*NRCU: "VLPFZ"}.get(j, f"R{j}")

    conn = {}
    for k in range(4):
        conn[f"P{k}"] = ",".join(r(4*i + k) for i in idx)
        conn[f"N{k}"] = ",".join(r(4*i + k + 1) for i in idx)
    conn["B"] = ",".join("VLPFZ" if i < NC1 else "VCTRL" for i in idx)
    sh.inst(P + "REYPLL_RCU.sym", bus("xrc", NRCU), -1000, -450, BR=VSS,
            A=VDD, **conn)
    sh.text("cell i holds resistors 4i..4i+3 of the chain, R0 = VCTRL, "
            f"R{4*NRCU} = VLPFZ; cell {NRCU-1}'s MiM is C2", -1450, -150,
            0.3)
    return sh


#- --------------------------------------------------------------------
#- REY_PLL_DIVN
#- --------------------------------------------------------------------
DIVN_PINS = ([(VDD, "in"), (VSS, "in"), ("PWRUP_1V8", "in"), ("CK", "in"),
              ("CK_FB", "out")]
             + [(f"CKO{k}", "out") for k in range(len(TAPS))])


def divn():
    sh = sheet("REY_PLL_DIVN", DIVN_PINS,
               f"REY_PLL_DIVN: {NDIV} flop ripple divider, CK/{2**NFB} "
               f"to the PFD")
    sh.text("Flop k divides the previous one by two: Q<k> is "
            "CK/2^(k+1). Q5 is CK_FB", -1450, -640, 0.3)
    idx = list(range(NDIV - 1, -1, -1))

    def q(i):
        return "CK_FB" if i == NFB - 1 else f"Q{i}"

    sh.inst(T + "REYTR_DFRNQNX1_CV.sym", bus("xdf", NDIV), -1300, -400,
            D=nets("QN", idx), CK=",".join(q(i - 1) if i else "CK"
                                            for i in idx),
            RN="PWRUP_1V8", Q=",".join(q(i) for i in idx),
            QN=nets("QN", idx), **SUP)
    sh.text("Output buffers, one per tap so the pins do not load the "
            "chain: CKO<k> = Q<k+2>, CK/8 .. CK/1024", -1000, -540, 0.3)
    tap = list(TAPS)[::-1]
    sh.inst(T + "REYTR_BFX1_CV.sym", bus("xbo", len(TAPS)), -900, -400,
            A=",".join(q(i) for i in tap),
            Y=nets("CKO", range(len(TAPS) - 1, -1, -1)), **SUP)
    #- one tap per layout column
    sh.inst(T + "REYTR_TAPCELLB_CV.sym", bus("xtap", 2), -600, -400,
            **SUP)
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
    for f in (ctrl, pfd, cp, lpf, divn):
        s = f()
        s.write(outdir)
        subs[s.cell] = s
    top(subs).write(outdir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
