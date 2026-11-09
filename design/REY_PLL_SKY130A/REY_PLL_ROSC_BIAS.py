"""REY_PLL_ROSC_BIAS: the ring's Vgs/R bias, laid out and routed on its
own. The oscillator places it beside the stages and takes VBP from it.

    top (n-well):  p_diode  p_mirb
    bottom:        r_trim  r_fix  n_sw  n_su  n_bias

The nets that cross between the stacks run in the channel, a track
each. No coordinates here.
"""
from cicpy.core.path import pin, PITCH
from cicpy.sidecar import SidecarCell, Stack


def _n_bias_paths():
    """The n_bias stack's three nets, see REY_PLL_ROSC_BIAS.n_bias."""
    m2 = [f"xmn2<{k}>" for k in range(4)]
    g = pin("xmn1", "VG", "x") + 3 * PITCH
    #- vias: flat (2x1) on the wide, low source and drain pins; a single
    #- cut where a leg touches a gate (narrow) or MN1's drain (VX's
    #- tall via there stood into the gate's li)
    flat, one = "2cuts,1vcuts", "1cuts,1vcuts"
    vbp = [dict(net="VBP", start=(a, "VBP"), stop=(b, "VBP"), options=flat,
                steps=[("up", "M2"), ("movey", pin(b, "VBP", "y")),
                       ("down", "M1"), ("end",)])
           for a, b in zip(m2, m2[1:])]
    vx = [dict(net="VX", start=("xmn1", "VX"), stop=(m2[0], "VX"),
               options=one,
               steps=[("up", "M4"), ("movex", pin(m2[0], "VX", "x")),
                      ("movey", pin(m2[0], "VX", "y")),
                      ("down", "M1"), ("end",)])]
    vx += [dict(net="VX", start=(a, "VX"), stop=(b, "VX"), options=one,
                steps=[("up", "M4"), ("movey", pin(b, "VX", "y")),
                       ("down", "M1"), ("end",)])
           for a, b in zip(m2, m2[1:])]
    #- VG lands at the source centre with ONE cut, which clears VBP's
    #- trunk over the drains (a flat via there came 0.05 um from it),
    #- and the next leg starts on the same via
    vg = [dict(net="VG", start=(a, "VG"), stop=(b, "VG"), options=one,
               steps=[("up", "M3"), ("movex", g),
                      ("movey", pin(b, "VG", "y")),
                      ("movex", pin(b, "VG", "x")),
                      ("down", "M1"), ("end",)])
          for a, b in zip(["xmn1"] + m2, m2)]
    return vbp + vx + vg


def _r_trim_paths():
    """The trim ladder's nets inside r_trim. Both pins of every unit
    are on the left at the same x, and each net spans another's pin
    row, so two M2 lanes alternate: RT2B and RT1 left, RT2 and RT0
    right, a pitch and a half either side of the pins' centre. One cut
    per pin."""
    legs = [("RT2B", "xrt2b", "xrt2a", -1.5), ("RT2", "xrt2a", "xrt1", 1.5),
            ("RT1", "xrt1", "xrt0<0>", -1.5),
            ("RT1", "xrt0<0>", "xrt0<1>", -1.5),
            ("RT0", "xrt0<0>", "xrt0<1>", 1.5)]
    return [dict(net=n, start=(a, n), stop=(b, n), options="1cuts,1vcuts",
                 steps=[("movex", pin(a, n, "x") + d * PITCH),
                        ("up", "M2"), ("movey", pin(b, n, "y")),
                        ("down", "M1"), ("end",)])
            for n, a, b, d in legs]


def _n_su_paths():
    """The startup stack's two nets. Each MS2's drain (XST) lies right
    under its gate (VG), as in n_bias, so they take different layers:
      XST  M2, up the right part of the drains, over into MS3's gate
      VG   M4, up the gate column, over into MS3's source
    """
    one = "1cuts,1vcuts"
    x = pin("xms2<0>", "XST", "x") + 1.2 * PITCH
    xst = [dict(net="XST", start=("xms2<0>", "XST"), stop=("xms2<1>", "XST"),
                options=one,
                steps=[("movex", x), ("up", "M2"),
                       ("movey", pin("xms2<1>", "XST", "y")),
                       ("down", "M1"), ("end",)]),
           dict(net="XST", start=("xms2<1>", "XST"), stop=("xms3", "XST"),
                options=one,
                steps=[("movex", x), ("up", "M2"),
                       ("movey", pin("xms3", "XST", "y")),
                       ("movex", pin("xms3", "XST", "x")),
                       ("down", "M1"), ("end",)])]
    vg = [dict(net="VG", start=("xms2<0>", "VG"), stop=("xms2<1>", "VG"),
               options=one,
               steps=[("up", "M4"), ("movey", pin("xms2<1>", "VG", "y")),
                      ("down", "M1"), ("end",)]),
          dict(net="VG", start=("xms2<1>", "VG"), stop=("xms3", "VG"),
               options=one,
               steps=[("up", "M4"), ("movey", pin("xms3", "VG", "y")),
                      #- land on the source's left, under the lane VG's
                      #- channel drop takes there (it then lands on this
                      #- via instead of placing its own beside it)
                      ("movex", pin("xms3", "VG", "x") - 1.6 * PITCH),
                      ("down", "M1"), ("end",)])]
    return xst + vg


def _r_fix_paths():
    """The fixed half of R inside r_fix, the same two lanes as r_trim:
    RF (both xrf2 P pins up to xrf1's N) on the right, RT0 and RFA on
    the left."""
    legs = [("RT0", "xrf2<0>", "xrf2<1>", -1.5),
            ("RF", "xrf2<0>", "xrf2<1>", 1.5), ("RF", "xrf2<1>", "xrf1", 1.5),
            ("RFA", "xrf1", "xrf0", -1.5)]
    return [dict(net=n, start=(a, n), stop=(b, n), options="1cuts,1vcuts",
                 steps=[("movex", pin(a, n, "x") + d * PITCH),
                        ("up", "M2"), ("movey", pin(b, n, "y")),
                        ("down", "M1"), ("end",)])
            for n, a, b, d in legs]


class _P(Stack):
    group = "pmos"
    fill = False
    blocked = [("VDD_1V8", "sources and bulks; the guard carries it")]


class _N(Stack):
    group = "nmos"
    fill = False
    blocked = [("VSS", "sources and bulks; the guard carries it")]


class REY_PLL_ROSC_BIAS(SidecarCell):

    class p_diode(_P):
        """The PMOS diode on VBP, four units."""
        match = r'^xmpd<\d+>$'
        order = [r'xmpd<\d+>']

    class p_mirb(_P):
        """The mirror into MN1 (VX), and the startup PMOS on top."""
        match = r'^(xmpb<\d+>|xms1)$'
        order = [r'xmpb<\d+>', 'xms1']

    class n_bias(_N):
        """MN1 and the LVT follower MN2.

        Three nets cross in one column (MN1's drain VX sits right under
        its gate VG), so each gets a layer and a lane, as paths anchored
        to the pins; the search shorted VG to VX here:
          VBP  M2, straight up the MN2 drains
          VX   M4, from MN1's drain over to the gate column and up it
          VG   M3, out to a trunk three pitches right of the gates and
               left into each MN2 source
        """
        match = r'^(xmn1|xmn2<\d+>)$'
        order = ['xmn1', r'xmn2<\d+>']
        paths = _n_bias_paths()

    class n_su(_N):
        """Startup NMOS."""
        match = r'^(xms2<\d+>|xms3)$'
        order = [r'xms2<\d+>', 'xms3']
        paths = _n_su_paths()

    class n_sw(_N):
        """The trim switches, bit 2 (nearest VSS) at the bottom."""
        match = r'^xst\d$'
        order = ['xst2', 'xst1', 'xst0']

    class r_trim(Stack):
        """The switched half of R, VSS at the bottom up to RT0."""
        match = r'^(xrt0<\d+>|xrt1|xrt2[ab])$'
        group = "res"
        fill = False
        order = ['xrt2b', 'xrt2a', 'xrt1', r'xrt0<\d+>']
        paths = _r_trim_paths()

    class r_fix(Stack):
        """The fixed half of R, RT0 at the bottom up to VG."""
        match = r'^(xrf[01]|xrf2<\d+>)$'
        group = "res"
        fill = False
        order = [r'xrf2<\d+>', 'xrf1', 'xrf0']
        paths = _r_fix_paths()

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    #- the nets that cross between the stacks; the drops find their own
    #- free lane on each pin (addRailConnection). Tracks two lanes
    #- apart: a rail via's pad is taller than the bar and comes within
    #- the space of the next lane's bar
    channel = 9
    #- VG in n_su climbs from MS3's source past its drain (VBP): left of
    #- the drain, which starts 0.64 um right of the source
    routes = [{"net": "VG", "track": 0,
               "drops": [[n_su, "M2", "left", "nopin"]]},
              {"net": "VX", "track": 2}]
    #- VBP in n_su on the left of the drain, clear of
    #- XST's trunk
    #- there; XST from p_mirb down on M4, past that stack's own M2/M3
    routes += [{"net": "VBP", "track": 4, "drops": [[n_su, "M2", "left"]]},
               {"net": "XST", "track": 6, "drops": [[p_mirb, "M4", "center"]]}]
    #- RT0's drop in r_fix and RT2's in r_trim climb past both of the
    #- stack's M2 lanes and the other tracks' M3 bars: on M4
    routes += [{"net": "RT0", "track": 8, "drops": [[r_fix, "M4", "center"]]},
               {"net": "RT1", "track": 10}]
    #- RT2's drop in r_trim climbs past both of the stack's M2 lanes
    routes += [{"net": "RT2", "track": 12, "drops": [[r_trim, "M4", "center"]]}]


_C = REY_PLL_ROSC_BIAS
REY_PLL_ROSC_BIAS.rows = [
    [_C.r_trim, _C.r_fix, _C.n_sw, _C.n_su, _C.n_bias],
    [_C.p_diode, _C.p_mirb],
]
