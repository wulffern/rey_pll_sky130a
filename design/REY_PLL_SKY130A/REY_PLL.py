"""REY_PLL: the top, as a cicpy sidecar.

    top:     DIVN | PFD | CTRL | CP | LPF
    bottom:  ROSC

Every block is finished, checked, and publishes the ports the top
reaches on an edge. This level places them and routes only between
them; every path is anchored to a pin, a channel track or a ring, never
a coordinate.

Layers between the blocks (cicpy names):

    channel (between the rows)   M3 horizontals, one track per net;
                                 M5 down from the top row, M4 up from
                                 the oscillator
    over the top row             M3 horizontals; M5 verticals for the
                                 signals, M4 for the supply straps
    supplies                     two rings round the whole, VSS inside
                                 VDD_1V8, on M1; each block's supply
                                 rails strapped to them on M4

The tile budget (161 x 111.52 um) is not met yet: this is the assembly
checked whole, and the size comes next.
"""
from cicpy.core.path import pin, track, landing, PITCH
from cicpy.sidecar import SidecarCell, Stack

ONE = "1cuts,1vcuts"
#- tracks over the top row, under the rings: CK_FB crosses the PFD there
OVER = 6


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
    """UP and DN_N, from the PFD's rails over CTRL into the charge pump's
    top. The two land at one x in the pump, UP on M5 over DN_N on M4, so
    UP crosses higher and comes down outside DN_N's turn."""
    cp, pfd = _b("cp"), _b("pfd")
    out = []
    for net, up, lay in (("UP", 14, "M5"), ("DN_N", 11, "M4")):
        out.append(_p(net, (pfd, net), (cp, net), [
            ("movey", pin(cp, net, "y") + up * PITCH),
            ("down", "M3"), ("movex", pin(cp, net, "x")),
            ("up", lay), ("movey", pin(cp, net, "y")), ("end",)]))
    return out


def _ctrl_cp():
    """KICK, VLO and VHI_N, from CTRL's right edge into the pump's top.

    They land at one x in the pump on three layers (KICK M5, VLO M4,
    VHI_N M3), so they turn at three heights, the M3 one lowest and the
    M5 one highest: each comes down outside the others' turns. On CTRL's
    side each climbs on M5 from its own edge stub, two pitches apart.
    """
    cp, ctrl = _b("cp"), _b("ctrl")
    out = []
    for net, left, turn, lay in (("KICK", 0, 8, "M5"), ("VLO", 2, 6, "M4"),
                                 ("VHI_N", 4, 4, "M3")):
        steps = []
        if left:
            steps.append(("movex", pin(ctrl, net, "x") - left * PITCH))
        steps += [("up", "M5"),
                  ("movey", pin(cp, net, "y") + turn * PITCH),
                  ("down", "M3"), ("movex", pin(cp, net, "x"))]
        if lay != "M3":
            steps.append(("up", lay))
        steps += [("movey", pin(cp, net, "y")), ("end",)]
        out.append(_p(net, (ctrl, net), (cp, net), steps))
    return out


def _pwrup():
    """PWRUP_1V8, CTRL's left edge to the PFD's ring, on M4 under the
    PFD's rails, up its own rail to above the ring sides below it."""
    ctrl, pfd = _b("ctrl"), _b("pfd")
    return [_p("PWRUP_1V8", (ctrl, "PWRUP_1V8"), (pfd, "PWRUP_1V8"), [
        ("movex", pin(pfd, "PWRUP_1V8", "x")),
        ("movey", pin(pfd, "PWRUP_1V8", "y")),
        ("up", "M5"), ("end",)])]


def _ck_fb():
    """CK_FB, the divider's top edge to the PFD's ring, over the PFD
    (its sides are full of the core's connections) and down onto the
    ring's top side, two pitches in from its corner."""
    divn, pfd = _b("divn"), _b("pfd")
    return [_p("CK_FB", (divn, "CK_FB"), (pfd, "CK_FB"), [
        ("movey", pin(pfd, "DN_N", "y2") + 2 * PITCH),
        ("down", "M3"),
        ("movex", pin(pfd, "CK_FB", "x") - 2 * PITCH),
        ("up", "M4"), ("movey", pin(pfd, "CK_FB", "y2")),
        ("up", "M5"), ("end",)])]


def _channel():
    """The nets in the channel between the rows, a track each."""
    cp, lpf, rosc, divn = _b("cp"), _b("lpf"), _b("rosc"), _b("divn")

    def down_up(net, src, dst, t, lay_up, dst_y="y"):
        return _p(net, (src, net), (dst, net), [
            ("movey", track("mid", t)), ("down", "M3"),
            ("movex", pin(dst, net, "x")), ("up", lay_up),
            ("movey", pin(dst, net, dst_y)), ("end",)])

    return [down_up("CK", rosc, divn, 1, "M5", "y1"),
            down_up("VBP", cp, rosc, 3, "M4"),
            down_up("VCTRL", cp, rosc, 5, "M4"),
            down_up("VCTRL", cp, lpf, 5, "M5", "y1"),
            down_up("VLPFZ", cp, lpf, 7, "M5", "y1")]


def _supplies():
    """Each block's supply rails strapped to the rings, on M4, away from
    where the signals turn: at the rails themselves for DIVN, PFD and
    LPF; along CTRL's own ring to its left half (its right edge is where
    KICK, VLO and VHI_N climb); at the left end of the pump's bars (its
    top carries the signal pins). The oscillator: VSS straight down at
    both ends and the middle, VDD_1V8 out sideways at both ends."""
    out = []
    for blk, shift in (("divn", None), ("pfd", None), ("lpf", None),
                       ("ctrl", 20)):
        for net in ("VDD_1V8", "VSS"):
            steps = []
            if shift:
                steps.append(("movex", pin(_b(blk), net, "x")
                              - shift * PITCH))
            steps += [("up", "M4"), ("movey", landing("y")),
                      ("down", "M1"), ("end",)]
            out.append(_p(net, (_b(blk), net), f"rail_t_{net}", steps,
                          at="n"))
    for net, k in (("VDD_1V8", 4), ("VSS", 1)):
        out.append(_p(net, (_b("cp"), net), f"rail_t_{net}", [
            ("movex", pin(_b("cp"), net, "x1") + k * PITCH),
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
    blk_lpf = _block("lpf", "REY_PLL_LPF, eight RCU cells.")
    blk_divn = _block("divn", "REY_PLL_DIVN, the divider and tap buffers.")
    blk_pfd = _block("pfd", "REY_PLL_PFD.")
    blk_ctrl = _block("ctrl", "REY_PLL_CTRL, power up, kick, open loop.")
    #- the pump's guard (VSS) reaches its box edge, and CTRL's outer
    #- ring there is VDD_1V8 li: abutted, the two shorted the supplies
    blk_cp = _block("cp", "REY_PLL_CP, the charge pump.", xspace=1.6)

    #- the rings are laid in beforeRoute, ahead of the paths that land
    #- on them; nothing for the recipe to do
    supplies = []

    #- um between the rows: eight tracks
    channel = 6
    routes = []

    paths = (_pfd_cp() + _ctrl_cp() + _pwrup() + _ck_fb() + _channel()
             + _supplies())

    def beforeRoute(self, layout):
        """The rings first, round the blocks and the band over the top
        row, so the supply paths can name their sides."""
        layout.updateBoundingRect()
        layout.y2 = int(layout.y2) + OVER * PITCH.resolve("M3")
        layout.addRouteRing("M1", "VSS", "rtbl", widthmult=3, spacemult=2)
        layout.addRouteRing("M1", "VDD_1V8", "rtbl", widthmult=3,
                            spacemult=2)
        super().beforeRoute(layout)


_C = REY_PLL
REY_PLL.rows = [[_C.blk_rosc],
                [_C.blk_divn, _C.blk_pfd, _C.blk_ctrl, _C.blk_cp, _C.blk_lpf]]
