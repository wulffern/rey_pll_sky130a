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
        """xmpu (Icp source) by the channel, xmpd (DN switch) over it:
        VBP's drop reaches xmpu's gate without passing xmpd's (DN_N),
        whose riser then leaves the top past nothing."""
        match = r'^xmp[ud]$'
        order = ['xmpu', 'xmpd']

    class p_ref(_P):
        """xmpn, the PMOS copy into VBN, and xmph, VCTRL park high."""
        match = r'^xmp[nh]$'
        order = ['xmpn', 'xmph']

    class n_sink(_N):
        """xmnu (UP switch) at the bottom, xmns (sink) over it, the VBN
        diode on top by the channel. Nothing passes UP's gate tab: with
        xmnu between the two VBN gates their wire did, and with xmnu on
        top VBN's drop did, closer than UP's own via could stand."""
        match = r'^xmn[usd]$'
        order = ['xmnu', 'xmns', 'xmnd']

    class n_park(_N):
        """xmnk, the kick on VLPFZ, under xmnl, VCTRL park low by the
        channel: VCTRL's drop is short, and VLPFZ's riser leaves the
        bottom past nothing."""
        match = r'^xmn[lk]$'
        order = ['xmnk', 'xmnl']

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

    def afterRoute(self, layout):
        """The ports the top reaches, carried to an edge.

        The control inputs come from above (the PFD and CTRL sit over
        this block's top), the loop filter nets leave below to the
        channel under the top row. Pins that share a column share an x,
        so each riser has its own layer:

          x of UP / DN_N         UP M5 (lower pin), DN_N M4
          x of KICK / VLO / VHI_N  KICK M5, VLO M4, VHI_N M3 (low to high)
          down                   VLPFZ M5, VCTRL M5 from its bar's centre
                                 (n_sink's drop is at its end), VBP M5
                                 from its bar's centre (the end
                                 is under UP's riser)
        """
        super().afterRoute(layout)
        for net, inst, side, lay in (
                ("UP", "xn_sink", "top", "M5"),
                ("DN_N", "xp_src", "top", "M4"),
                ("KICK", "xn_park", "top", "M5"),
                ("VLO", "xn_park", "top", "M4"),
                ("VHI_N", "xp_ref", "top", "M3"),
                ("VLPFZ", "xn_park", "bottom", "M5")):
            layout.promoteInstancePort(net, rf"^{inst}$", side, lay)
        layout.promoteRailPort("VCTRL", "bottom", "M5", center=True)
        layout.promoteRailPort("VBP", "bottom", "M5", center=True)


REY_PLL_CP.rows = [[REY_PLL_CP.n_sink, REY_PLL_CP.n_park],
                   [REY_PLL_CP.p_src, REY_PLL_CP.p_ref]]
