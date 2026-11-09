"""REY_PLL_ROSC_BIAS: the ring's Vgs/R bias, laid out and routed on its
own. The oscillator places it beside the stages and takes VBP from it.

    top (n-well):  p_diode  p_mirb
    bottom:        r_trim  r_fix  n_sw  n_su  n_bias

The nets that cross between the stacks run in the channel, a track
each. No coordinates here.
"""
from cicpy.sidecar import SidecarCell, Stack


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
        """MN1 and the LVT follower MN2."""
        match = r'^(xmn1|xmn2<\d+>)$'
        order = ['xmn1', r'xmn2<\d+>']

    class n_su(_N):
        """Startup NMOS."""
        match = r'^(xms2<\d+>|xms3)$'
        order = [r'xms2<\d+>', 'xms3']

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

    class r_fix(Stack):
        """The fixed half of R, RT0 at the bottom up to VG."""
        match = r'^(xrf[01]|xrf2<\d+>)$'
        group = "res"
        fill = False
        order = [r'xrf2<\d+>', 'xrf1', 'xrf0']

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    #- a drop is a straight vertical from its pin to the channel, so in
    #- a stack where one net's pin lies under another's the two take
    #- different lanes of the (wide) pins: left, center, right
    channel = 6
    routes = [
        {"net": "VBP", "track": 0},
        {"net": "VG", "track": 1,
         "drops": [[r_fix, "M2", "right"], [n_bias, "M2", "left"],
                   [n_su, "M2", "left"]]},
        {"net": "VX", "track": 2, "drops": [[p_mirb, "M2", "left"]]},
        {"net": "XST", "track": 3, "drops": [[n_su, "M2", "right"]]},
        {"net": "RT0", "track": 4,
         "drops": [[r_trim, "M2", "left"], [r_fix, "M2", "left"],
                   [n_sw, "M2", "right"]]},
        {"net": "RT1", "track": 5,
         "drops": [[r_trim, "M2", "center"], [n_sw, "M2", "left"]]},
        {"net": "RT2", "track": 6,
         "drops": [[r_trim, "M2", "right"], [n_sw, "M2", "center"]]},
    ]


_C = REY_PLL_ROSC_BIAS
REY_PLL_ROSC_BIAS.rows = [
    [_C.r_trim, _C.r_fix, _C.n_sw, _C.n_su, _C.n_bias],
    [_C.p_diode, _C.p_mirb],
]
