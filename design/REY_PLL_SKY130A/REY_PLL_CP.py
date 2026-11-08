"""REY_PLL_CP: the layout, as a cicpy sidecar.

Two rows, NMOS under PMOS, as in REY_PLL_ROSC:

    top (n-well):  the source mirror and DN switch, the reference
                   mirror into VBN, the VCTRL park high
    bottom:        the UP switch and sink mirror, the VBN diode, the
                   park low and the kick

No coordinates here.
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


class REY_PLL_CP(SidecarCell):

    class p_src(_P):
        """xmpu (Icp source) under xmpd (DN switch)."""
        match = r'^xmp[ud]$'
        order = ['xmpd', 'xmpu']

    class p_ref(_P):
        """xmpn, the PMOS copy into VBN, and xmph, VCTRL park high."""
        match = r'^xmp[nh]$'
        order = ['xmpn', 'xmph']

    class n_sink(_N):
        """xmns (sink) under xmnu (UP switch), and the VBN diode."""
        match = r'^xmn[usd]$'
        order = ['xmns', 'xmnu', 'xmnd']

    class n_park(_N):
        """xmnl, VCTRL park low, and xmnk, the kick on VLPFZ."""
        match = r'^xmn[lk]$'
        order = ['xmnl', 'xmnk']

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    #- the nets that cross between the rows, one channel track each
    channel = 6
    routes = [
        #- VCTRL's drop in p_src comes from the right: on the left it ran
        #- into the stack's own VPS (source to switch) wire
        {"net": "VCTRL", "track": 0,
         "drops": [[n_sink, "M2", "left"], [n_park, "M2", "left"],
                   [p_src, "M2", "right"], [p_ref, "M2", "left"]]},
        {"net": "VBN", "track": 2},
        {"net": "VBP", "track": 4},
    ]


REY_PLL_CP.rows = [[REY_PLL_CP.n_sink, REY_PLL_CP.n_park],
                   [REY_PLL_CP.p_src, REY_PLL_CP.p_ref]]
