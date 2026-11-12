#!/usr/bin/env python3
"""tt_um_rey_pll_wulffern, the Tiny Tapeout wrapper: layout and schematic.

    python3 py/gen_tt_um.py design/REY_PLL_SKY130A

Both views come from the tables below (PINS, ROUTES, TIED), so they
cannot disagree. The recipe is lelo_temp's gen_tt_um.py: the port row is
read from the tile's DEF, the two power rails stand at the west edge,
the unused outputs are tied low through a res_generic_m4 each (which
keeps them and VGND separate nets for LVS), and every input that is used
has an antenna diode.

What is this tile's own:

    the core    REY_PLL mirrored in x, which puts its top edge risers in
                the order of the pads: CK_REF under clk, the controls
                under ui_in, the divider taps under uo_out
    the band    3.58 um between the core's top and the pads: five met3
                tracks, the risers carried up to them and the drops to
                the pads on met4
    the power   the core's rings are on locali only, and after the
                mirror neither stands under its rail: each rail has a
                met1..met4 pad under it and a met1 bridge to its ring

Where a riser, a pad or a ring stands is read from REY_PLL.mag and the
DEF. Units are magic internal at magscale 1 2: 5 nm, 200 to the um.
"""
import os
import re
import sys

from cicpy.eda.schgen import Sheet

LIB = "REY_PLL_SKY130A"
CORE = "REY_PLL"
CELL = "tt_um_rey_pll_wulffern"
DIODE = "sky130_fd_pr__diode_pw2nd_05v5_lc"

#- the ports, in the schematic's order. Magic writes the extracted
#- subcircuit's ports by port number and netgen resolves a symmetric
#- orbit (the identical tie resistors) by position, so the layout's port
#- numbers follow this list
PINS = [("uio_oe[7:0]", "out"), ("VDPWR", "in"), ("VGND", "in"),
        ("ui_in[7:0]", "in"), ("uio_in[7:0]", "in"), ("ena", "in"),
        ("rst_n", "in"), ("clk", "in"), ("uo_out[7:0]", "out"),
        ("uio_out[7:0]", "out")]

#- core port, pad, track (0 is the lowest; None: the riser stands under
#- its pad and goes straight up). A riser stops at its track and a drop
#- starts at its own, so of two that stand side by side the riser has
#- the lower track:
#-   OLL's riser is under ui_in[2]'s drop, CKO1's beside uo_out[3]'s
#-   TRIM0 and TRIM2 rise beside pads that are not theirs: not track 4,
#-   whose stacks reach the pad row
#-   CKO2 and CKO3 rise under the tie bus: track 2 or lower
ROUTES = [("CK_REF", "clk", 0),
          ("PWRUP_1V8", "ui_in[0]", None),
          ("TRIM0", "ui_in[1]", 2),
          ("TRIM1", "ui_in[2]", 4),
          ("TRIM2", "ui_in[3]", 3),
          ("OLH", "ui_in[4]", 1),
          ("OLL", "ui_in[5]", 0),
          ("CKO0", "uo_out[0]", 3),
          ("CKO1", "uo_out[1]", 0),
          ("CKO2", "uo_out[2]", 1),
          ("CKO3", "uo_out[3]", 2)]

#- outputs nothing drives, tied to VGND. They are the pads west of
#- uo_out[3], so one bus reaches them all
TIED = ["uio_oe[7:0]", "uio_out[7:0]", "uo_out[7:4]"]

TOP = 22304               # the tile is 161 x 111.52 um
WIDTH = 32200
PADY0 = TOP - 200         # the pads are 0.3 x 1 um, at the top edge
#- the core's left edge. The rails take the first 4.4 um; here the
#- risers also stand clear of every pad that is not theirs
DX = 532
PAD = 55                  # half a via stack's metal pad
PITCH = 148               # of the tracks: a pad clears the next wire
YD = PADY0 - 384          # the diodes' centres: 1.92 um under the pads
RAILS = {"VDPWR": (0, 400), "VGND": (480, 880)}
SUPPLY = {"VDPWR": "VDD_1V8", "VGND": "VSS"}
#- where each rail's pad stands, as a share of the core's height: clear
#- of the oscillator's VDD_1V8 straps, which are met1 at 43 %
POWER_AT = {"VDPWR": 0.7, "VGND": 0.2}
POWER_H = 500

METALS = ["locali", "metal1", "metal2", "metal3", "metal4"]
CUTS = ["viali", "via1", "via2", "via3"]
ORDER = ["locali", "viali", "metal1", "via1", "metal2", "via2", "metal3",
         "via3", "metal4", "rmetal4"]


def bits(name):
    """uio_oe[7:0] -> uio_oe[7] .. uio_oe[0]"""
    m = re.match(r"(\w+)\[(\d+):(\d+)\]$", name)
    if not m:
        return [name]
    hi, lo = int(m.group(2)), int(m.group(3))
    return [f"{m.group(1)}[{i}]" for i in range(hi, lo - 1, -1)]


def track(k):
    """The centre of track k: the top one's stacks end at the pads."""
    return PADY0 - PAD - (4 - k) * PITCH


def read_def(path):
    """The signal pads of the tile: name -> (x centre, direction)."""
    pads = {}
    for m in re.finditer(r"-\s+(\S+)\s+\+ NET \S+ \+ DIRECTION (\w+).*?"
                         r"PLACED \( (\d+) (\d+) \)", open(path).read(),
                         re.S):
        pads[m.group(1)] = (int(m.group(3)) // 5, m.group(2).lower())
    assert len(pads) == 43, f"the DEF gave {len(pads)} pins"
    return pads


def read_core(path):
    """The core's ports, name -> (layer, x1, y1, x2, y2), and its size."""
    txt = open(path).read()
    ports = {}
    for m in re.finditer(r"^flabel (\S+) s (\d+) (\d+) (\d+) (\d+) .* (\S+)$",
                         txt, re.M):
        ports[m.group(6)] = (m.group(1),) + tuple(int(v) for v in
                                                  m.group(2, 3, 4, 5))
    w, h = re.search(r"FIXED_BBOX 0 0 (\d+) (\d+)", txt).groups()
    return ports, int(w), int(h)


class Layout:
    def __init__(self):
        self.layers = {k: [] for k in ORDER}
        self.uses = []
        self.labels = []

    def rect(self, layer, x1, y1, x2, y2):
        assert x2 > x1 and y2 > y1, (layer, x1, y1, x2, y2)
        self.layers[layer].append((x1, y1, x2, y2))

    def stack(self, x, y, top, bot):
        """A via stack centred on (x, y): 0.55 um pads, and 0.35 um of
        contact paint, which magic takes as the cut and its enclosure."""
        hi, lo = METALS.index(top), METALS.index(bot)
        for i in range(lo, hi + 1):
            self.rect(METALS[i], x - PAD, y - PAD, x + PAD, y + PAD)
        for i in range(lo, hi):
            self.rect(CUTS[i], x - 35, y - 35, x + 35, y + 35)

    def use(self, cell, inst, t, box):
        self.uses.append((cell, inst, t, box))

    def port(self, layer, r, name, num, kind, size=480, rot=90):
        self.labels.append(
            f"flabel {layer} s {r[0]} {r[1]} {r[2]} {r[3]} 0 FreeSans "
            f"{size} {rot} 0 0 {name}\nport {num} nsew {kind}")

    def write(self, path):
        with open(path, "w") as f:
            f.write("magic\ntech sky130A\nmagscale 1 2\ntimestamp 1\n")
            for lay in ORDER:
                if self.layers[lay]:
                    f.write(f"<< {lay} >>\n")
                for r in self.layers[lay]:
                    f.write("rect %d %d %d %d\n" % r)
            for cell, inst, t, box in self.uses:
                f.write(f"use {cell}  {inst}\n")
                f.write("transform %d %d %d %d %d %d\n" % t)
                f.write("box %d %d %d %d\n" % box)
            f.write("<< labels >>\n")
            for lab in self.labels:
                f.write(lab + "\n")
            f.write("<< properties >>\n")
            f.write(f"string FIXED_BBOX 0 0 {WIDTH} {TOP}\n<< end >>\n")


def layout(outdir):
    pads = read_def(os.path.join(outdir, "tt_block_1x1_pg.def"))
    ports, w, h = read_core(os.path.join(outdir, CORE + ".mag"))
    num = {n: i for i, n in enumerate(b for p, _ in PINS for b in bits(p))}
    lay = Layout()

    def mirror(r):
        """A rectangle of the core, in the tile."""
        return (DX + w - r[2], r[1], DX + w - r[0], r[3])

    #- the tile's ports
    for name, (xc, direction) in pads.items():
        r = (xc - 30, PADY0, xc + 30, TOP)
        lay.rect("metal4", *r)
        lay.port("metal4", r, name, num[name], f"signal {direction}")
    for name, (x1, x2) in RAILS.items():
        r = (x1, 0, x2, TOP)
        lay.rect("metal4", *r)
        kind = "power" if name == "VDPWR" else "ground"
        lay.port("metal4", r, name, num[name], f"{kind} bidirectional",
                 size=800, rot=0)

    #- the core
    assert DX + w <= WIDTH and track(0) - PAD >= h + 14, "the core is too big"
    lay.use(CORE, CORE + "_0", (-1, 0, DX + w, 0, 1, 0), (0, 0, w, h))

    #- the rails onto the rings: a pad under the rail, met1 from it to
    #- the ring's column, and contacts down to the ring there
    for name, (x1, x2) in RAILS.items():
        layer, *ring = ports[SUPPLY[name]]
        rx1, _, rx2, _ = mirror(ring)
        assert layer == "locali" and rx1 > x1 + 30
        y1 = int(POWER_AT[name] * h) // 2 * 2
        y2 = y1 + POWER_H
        for m in METALS[1:]:
            lay.rect(m, x1 + 30, y1, x2 - 30, y2)
        for c in CUTS[1:]:
            lay.rect(c, x1 + 50, y1 + 20, x2 - 50, y2 - 20)
        lay.rect("metal1", x1 + 30, y1, rx2, y2)
        lay.rect("locali", rx1, y1, rx2, y2)
        #- met1 is 0.06 um over a contact
        lay.rect("viali", rx1 + 12, y1 + 12, rx2 - 12, y2 - 12)

    #- the signals
    diodes = []
    for port, pad, k in ROUTES:
        layer, *riser = ports[port]
        x1, y1, x2, y2 = mirror(riser)
        assert layer == "metal4" and y2 == h, f"{port} is not a top riser"
        xr = (x1 + x2) // 2
        xp, direction = pads[pad]
        if k is None:
            #- the riser at its own width, up into its pad
            assert x1 <= xp - 30 and xp + 30 <= x2, f"{port} misses {pad}"
            lay.rect("metal4", x1, y1, x2, PADY0)
            xd, yt = xr, YD
        else:
            #- riser, met3 along the track, drop
            yt = track(k)
            lay.rect("metal4", x1, y1, x2, yt + PAD)
            lay.stack(xr, yt, "metal4", "metal3")
            lay.rect("metal3", min(xr, xp), yt - 30, max(xr, xp), yt + 30)
            lay.rect("metal4", xp - 30, yt, xp + 30, PADY0)
            xd = xp
        if direction != "input":
            if k is not None:
                lay.stack(xp, yt, "metal4", "metal3")
            continue
        #- an input: the stack goes on down to met1, and met1 to the
        #- diode, which stands under the pad (its anode is the
        #- substrate, so there is nothing else to connect)
        lay.stack(xd, yt, "metal4", "metal1")
        #- at the pad's width: a narrower one leaves a notch between
        #- the pad and the diode's own met1
        if yt != YD:
            lay.rect("metal1", xd - PAD, min(yt, YD), xd + PAD, max(yt, YD))
        lay.use(DIODE, f"ant_{len(diodes)}", (1, 0, xd, 0, 1, YD),
                (-183, -183, 183, 183))
        diodes.append(pad)

    #- the tie resistors: the body is the 0.3 um right under the pad,
    #- so it extracts as exactly W 0.3 L 0.3, and the bus takes the
    #- other ends to the VGND rail
    xs = [pads[b][0] for t in TIED for b in bits(t)]
    for xc in xs:
        lay.rect("rmetal4", xc - 30, PADY0 - 60, xc + 30, PADY0)
        lay.rect("metal4", xc - 30, PADY0 - 180, xc + 30, PADY0 - 60)
    lay.rect("metal4", RAILS["VGND"][0], PADY0 - 180, max(xs) + 30,
             PADY0 - 120)

    lay.write(os.path.join(outdir, CELL + ".mag"))
    return diodes


def schematic(outdir, diodes):
    xschem = os.path.join(os.environ["PDK_ROOT"], "sky130A", "libs.tech",
                          "xschem")
    sh = Sheet(CELL, PINS, search=[os.path.join(outdir, ".."), xschem],
               title=f"{CELL}: REY_PLL in a Tiny Tapeout tile")
    conn = {SUPPLY[rail]: rail for rail in RAILS}
    conn.update({port: pad for port, pad, _ in ROUTES})
    sh.inst(f"{LIB}/{CORE}.sym", "x1", -1000, -400, **conn)
    sh.text("Antenna diodes on the inputs", -1400, 20)
    for i, pad in enumerate(diodes):
        sh.inst("sky130_fd_pr/diode.sym", f"D{i}", -1300 + 220 * i, 150,
                props="model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 "
                      "spiceprefix=X", d0="VGND", d1=pad)
    sh.text("Outputs nothing drives, tied low through a metal resistor "
            "each", -1400, 300)
    for i, name in enumerate(TIED):
        sh.inst("sky130_fd_pr/res_generic_m4.sym",
                f"R{i}[{len(bits(name)) - 1}:0]", -1300 + 300 * i, 520,
                props="W=0.3 L=0.3 model=res_generic_m4 mult=1",
                P=name, M="VGND")
    sh.write(outdir, symbol=False)


def main():
    outdir = sys.argv[1]
    diodes = layout(outdir)
    schematic(outdir, diodes)
    print(f"wrote {CELL}.mag and .sch: {len(ROUTES)} routes, "
          f"{len(diodes)} diodes")


if __name__ == "__main__":
    main()
