"""REY_PLL_ROSC_STAGE: one ring stage, laid out and routed on its own.

The oscillator places seven of these and routes only what runs between
them (the ring nodes, VBP, VCTRL), so a stage is finished here:

    top (n-well):  xmpfb   fixed mirror
                   xmpfa   fixed mirror
                   xmpca   tunable mirror      NC
                   xmpv    VCTRL device        VS
                   xip     inverter PMOS       (drain Y nearest the nmos)
    channel:       A (both gates), Y (both drains)
    bottom:        xin     inverter NMOS

VS and NC stay inside the PMOS column. No coordinates here.
"""
from cicpy.core.path import pin
from cicpy.sidecar import SidecarCell, Stack


class REY_PLL_ROSC_STAGE(SidecarCell):

    class p_st(Stack):
        """The stage's PMOS, inverter at the bottom by the channel."""
        match = r'^(xip|xmpv|xmpca|xmpf[ab])$'
        group = "pmos"
        fill = False
        order = ['xip', 'xmpv', 'xmpca', 'xmpfa', 'xmpfb']
        blocked = [("VDD_1V8", "sources and bulks; the guard carries it")]
        #- VS straight up at the centre of xip's source pin: the search
        #- put its trunk two pitches right, and the two-cut via on xip's
        #- source then came 0.12 um from the cell's gate contact (li.3).
        #- One leg per pair of VS pins, the vias shared where legs meet
        paths = [dict(net="VS", start=(a, "VS"), stop=(b, "VS"),
                      steps=[("movex", pin("xip", "VS", "x")),
                             ("up", "M2"),
                             ("movey", pin(b, "VS", "y")),
                             ("down", "M1"),
                             ("end",)])
                 for a, b in (("xip", "xmpv"), ("xmpv", "xmpfa"),
                              ("xmpfa", "xmpfb"))]
        #- NC at the centre of xmpca's drain, inside xmpv's source too,
        #- clear of the VS trunk (the search does not see declared paths
        #- and put NC on top of it)
        paths += [dict(net="NC", start=("xmpv", "NC"), stop=("xmpca", "NC"),
                       steps=[("movex", pin("xmpca", "NC", "x")),
                              ("up", "M2"),
                              ("movey", pin("xmpca", "NC", "y")),
                              ("down", "M1"),
                              ("end",)])]

    class n_st(Stack):
        """The inverter NMOS."""
        match = r'^xin$'
        group = "nmos"
        fill = False
        order = ['xin']
        blocked = [("VSS", "source and bulk; the guard carries it")]

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    #- A and Y cross between the rows, a track each
    channel = 4
    routes = [{"net": "A", "track": 0}, {"net": "Y", "track": 2, "drops": [[p_st, "M2", "right"]]}]


REY_PLL_ROSC_STAGE.rows = [[REY_PLL_ROSC_STAGE.n_st],
                           [REY_PLL_ROSC_STAGE.p_st]]
