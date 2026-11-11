"""REY_PLL: the top, as a cicpy sidecar.

    top:     PFD | CTRL | CP | DIVN | LPF
    bottom:  ROSC

Every block is finished, checked, and publishes the ports the top
reaches on an edge. This level places them and routes only between
them; every path is anchored to a pin, a channel track or a ring, never
a coordinate.

The blocks carry no rings of their own: their supply rails are along
their tops, and the blocks stand 1.6 um apart (the cells' wells and
implants reach 0.4 to 0.75 um past their boxes). The pump stands 2.6 um
from CTRL: both have an n-well at that edge, and n-wells are 1.27 um
apart or one.

Layers between the blocks (cicpy names):

    channel (between the rows)   M3 horizontals, one track per net;
                                 M5 down from the top row, M4 up from
                                 the oscillator
    over the top row             M3 horizontals; M4 and M5 verticals for
                                 the signals, M4 for the supply straps
    supplies                     two rings round the whole, VSS inside
                                 VDD_1V8, on M1; each block's supply
                                 rails strapped to them on M4
    to the top edge              M5 risers, one per pin of the tile: the
                                 wrapper (tt_um_rey_pll_wulffern) takes
                                 each from there to its pad

The core is 156.96 x 106.94 um, for a 161 x 111.52 um tile.
"""
from cicpy.core.path import pin, track, landing, PITCH
from cicpy.sidecar import SidecarCell, Stack

ONE = "1cuts,1vcuts"
#- tracks over the top row, under the rings: CK_FB leaves the divider's
#- top edge there, clear of the tap ports below it and of the supply
#- straps' stacks on the ring above it
OVER = 2


def _block(inst, doc, xspace=0):
    """A stack holding one finished block. The stack is named blk_<inst>,
    since its wrapper subcell is REY_PLL_<STACK> and REY_PLL_<INST> is
    the block itself (cicpy refuses the collision). `xspace` (um) opens
    a gap on its left."""
    return type(f"blk_{inst}", (Stack,),
                dict(__doc__=doc, match=rf'^x{inst}$', group=inst,
                     fill=False, order=[f'x{inst}'], xspace=xspace))


def _b(name):
    return f"xblk_{name}"


def _p(net, start, stop, steps, at=None, options=ONE):
    d = dict(net=net, start=start, stop=stop, options=options, steps=steps)
    if at:
        d["at"] = at
    return d


def _pfd_cp():
    """UP and DN_N, from the PFD's top edge over CTRL into the charge
    pump's top, on M3. The two land at one x in the pump, UP on M5 over
    DN_N on M4, so UP crosses higher and comes down outside DN_N's turn
    (and its M3 run clears DN_N's rise out of the PFD, which is to its
    right)."""
    cp, pfd = _b("cp"), _b("pfd")
    out = []
    for net, up, lay in (("UP", 14, "M5"), ("DN_N", 11, "M4")):
        out.append(_p(net, (pfd, net), (cp, net), [
            ("movey", pin(cp, net, "y") + up * PITCH),
            ("movex", pin(cp, net, "x")),
            ("up", lay), ("movey", pin(cp, net, "y")), ("end",)]))
    return out


def _ctrl_cp():
    """KICK, VLO and VHI_N, from CTRL's right edge into the pump's top.

    They land at one x in the pump on three layers (KICK M5, VLO M4,
    VHI_N M3), so they turn at three heights, the M3 one lowest and the
    M5 one highest: each comes down outside the others' turns. On CTRL's
    side each climbs on M5 in its own lane: KICK from its edge stub, the
    other two in the gap before the pump, a pitch and three pitches out.
    """
    cp, ctrl = _b("cp"), _b("ctrl")
    out = []
    for net, lane, turn, lay in (("KICK", 0, 8, "M5"), ("VHI_N", 1, 4, "M3"),
                                 ("VLO", 3, 6, "M4")):
        steps = []
        if lane:
            steps.append(("movex", pin(ctrl, net, "x2") + lane * PITCH))
        steps += [("up", "M5"),
                  ("movey", pin(cp, net, "y") + turn * PITCH),
                  ("down", "M3"), ("movex", pin(cp, net, "x"))]
        if lay != "M3":
            steps.append(("up", lay))
        steps += [("movey", pin(cp, net, "y")), ("end",)]
        out.append(_p(net, (ctrl, net), (cp, net), steps))
    return out


def _pwrup():
    """PWRUP_1V8, the PFD's top edge to CTRL's left edge, all on M5 (the
    PFD's CK_FB port is M4 under this one): two pitches over the PFD's
    corner (its own M5 reaches the top edge there), down
    the gap between the two blocks, and onto CTRL's M4 stub."""
    ctrl, pfd = _b("ctrl"), _b("pfd")
    return [_p("PWRUP_1V8", (pfd, "PWRUP_1V8"), (ctrl, "PWRUP_1V8"), [
        ("movey", pin(pfd, "PWRUP_1V8", "y") + 2 * PITCH),
        ("movex", pin(ctrl, "PWRUP_1V8", "x1") - PITCH),
        ("movey", pin(ctrl, "PWRUP_1V8", "y")),
        ("down", "M4"), ("end",)])]


def _ck_fb():
    """CK_FB, the divider's top edge to the PFD's: up into the band over
    the row, west on M3 over everything between, and down on M4 onto the
    PFD's port (PWRUP_1V8's riser is M5 over it)."""
    divn, pfd = _b("divn"), _b("pfd")
    return [_p("CK_FB", (divn, "CK_FB"), (pfd, "CK_FB"), [
        ("movey", pin(divn, "CK_FB", "y2") + 2 * PITCH),
        ("down", "M3"),
        ("movex", pin(pfd, "CK_FB", "x")),
        ("up", "M4"), ("movey", pin(pfd, "CK_FB", "y")), ("end",)])]


def _channel():
    """The nets in the channel between the rows, a track each."""
    cp, lpf, rosc, divn = _b("cp"), _b("lpf"), _b("rosc"), _b("divn")

    def down_up(net, src, dst, t, lay_up, dst_y="y"):
        return _p(net, (src, net), (dst, net), [
            ("movey", track("mid", t)), ("down", "M3"),
            ("movex", pin(dst, net, "x")), ("up", lay_up),
            ("movey", pin(dst, net, dst_y)), ("end",)])

    #- VBP's two pins are under a micron apart in x: a jog on the pump's
    #- layer and one via onto the oscillator's port, not two stacks side
    #- by side (nor a via in the jog: its pad and the leg below it leave
    #- a notch)
    vbp = _p("VBP", (cp, "VBP"), (rosc, "VBP"), [
        ("movey", track("mid", 3)),
        ("movex", pin(rosc, "VBP", "x")),
        ("movey", pin(rosc, "VBP", "y")), ("end",)])

    return [down_up("CK", rosc, divn, 1, "M5", "y1"),
            vbp,
            down_up("VCTRL", cp, rosc, 5, "M4"),
            down_up("VCTRL", cp, lpf, 5, "M5", "y1"),
            down_up("VLPFZ", cp, lpf, 7, "M5", "y1")]


#- where each block's two straps leave its rails, in pitches from the
#- rails' left end (VSS, VDD_1V8): clear of the block's own strap stacks
#- and edge ports there, and of the signals over the row
STRAPS = {"pfd": (13, 15), "ctrl": (1, 3), "cp": (1, 4), "divn": (13, 15),
          "lpf": (5, 7)}


def _supplies():
    """Each block's supply rails strapped to the top ring, on M4, from a
    place along the rails where nothing else stands (STRAPS). The pump's
    VSS bar is its bottom one, and its strap crosses the pump. The
    oscillator: VSS straight down at both ends and the middle, VDD_1V8
    out sideways at both ends."""
    out = []
    for blk, ks in STRAPS.items():
        for net, k in zip(("VSS", "VDD_1V8"), ks):
            out.append(_p(net, (_b(blk), net), f"rail_t_{net}", [
                ("movex", pin(_b(blk), net, "x1") + k * PITCH),
                ("up", "M4"), ("movey", landing("y")),
                ("down", "M1"), ("end",)], at="w"))
    for at in ("w", None, "e"):
        out.append(_p("VSS", (_b("rosc"), "VSS"), "rail_b_VSS", [
            ("up", "M2"), ("movey", landing("y")),
            ("down", "M1"), ("end",)], at=at))
    for at, side in (("w", "l"), ("e", "r")):
        out.append(_p("VDD_1V8", (_b("rosc"), "VDD_1V8"),
                      f"rail_{side}_VDD_1V8", [
                          ("up", "M2"), ("movex", landing("x")),
                          ("down", "M1"), ("end",)], at=at))
    return out


class REY_PLL(SidecarCell):
    blk_rosc = _block("rosc", "REY_PLL_ROSC, the oscillator.")
    blk_pfd = _block("pfd", "REY_PLL_PFD.")
    blk_ctrl = _block("ctrl", "REY_PLL_CTRL, power up, kick, open loop.",
                      xspace=1.6)
    #- n-well to n-well: CTRL's stands 0.75 um past its box, the pump's
    #- 0.44 um past its own
    blk_cp = _block("cp", "REY_PLL_CP, the charge pump.", xspace=2.6)
    blk_divn = _block("divn", "REY_PLL_DIVN, the divider and tap buffers.",
                      xspace=1.6)
    blk_lpf = _block("lpf", "REY_PLL_LPF, eight RCU cells.", xspace=1.6)

    #- the rings are laid in beforeRoute, ahead of the paths that land
    #- on them; nothing for the recipe to do
    supplies = []

    #- um between the rows: eight tracks
    channel = 6
    routes = []

    paths = (_pfd_cp() + _ctrl_cp() + _pwrup() + _ck_fb() + _channel()
             + _supplies())

    #- the oscillator's TRIM pins stand in one column; each rises this
    #- many pitches to its left
    TRIM_LANES = {"TRIM0": 5, "TRIM1": 3, "TRIM2": 1}

    def beforeRoute(self, layout):
        """The rings first, round the blocks and the band over the top
        row, so the supply paths can name their sides."""
        layout.updateBoundingRect()
        layout.y2 = int(layout.y2) + OVER * PITCH.resolve("M3")
        layout.addRouteRing("M1", "VSS", "rtbl", widthmult=3, spacemult=2)
        layout.addRouteRing("M1", "VDD_1V8", "rtbl", widthmult=3,
                            spacemult=2)
        super().beforeRoute(layout)

    def afterRoute(self, layout):
        """The tile's pins, carried to the top edge on M5 (the pads'
        layer), each from the port of the block that has it:

          CK_REF, PWRUP_1V8   the PFD's top edge
          OLL, OLH            CTRL's top edge
          CKO<n>              the divider's top edge
          TRIM<n>             the oscillator's pins, through the channel
                              and over the pump's left end, which holds
                              no M5: M3 at the pin's height to the lane,
                              and up there
        """
        super().afterRoute(layout)
        for net, blk in (("CK_REF", "pfd"), ("PWRUP_1V8", "pfd"),
                         ("OLL", "ctrl"), ("OLH", "ctrl")):
            layout.promoteInstancePort(net, rf"^{_b(blk)}$", "top", "M5")
        divn = layout.getInstanceFromInstanceName(_b("divn"))
        for net in sorted(divn.instancePorts):
            if net.startswith("CKO"):
                layout.promoteInstancePort(net, rf"^{_b('divn')}$", "top",
                                           "M5")
        rosc = layout.getInstanceFromInstanceName(_b("rosc"))
        for net, k in self.TRIM_LANES.items():
            x = int(rosc.instancePorts[net].get().centerX())
            layout.promoteInstancePort(
                net, rf"^{_b('rosc')}$", "top", "M5",
                jog=("M3", x - k * PITCH.resolve("M5")))


_C = REY_PLL
REY_PLL.rows = [[_C.blk_rosc],
                [_C.blk_pfd, _C.blk_ctrl, _C.blk_cp, _C.blk_divn, _C.blk_lpf]]
