"""REY_PLL: the top, as a cicpy sidecar, for one Tiny Tapeout tile
(161 x 111.52 um, tt_block_1x1_pg.def).

    top:     DIVN | PFD | CTRL | CP
    bottom:  ROSC | LPF

The loop runs left to right along the seam: CK_REF into the PFD, UP/DN
to the CP, VCTRL/VLPFZ down to the LPF and across to the ROSC, CK up to
the DIVN, CK_FB back to the PFD. Placement only so far; no coordinates.
"""
from cicpy.sidecar import SidecarCell, Stack


def _block(inst, doc):
    """A stack holding one finished block. The stack is named blk_<inst>,
    since its wrapper subcell is REY_PLL_<STACK> and REY_PLL_<INST> is
    the block itself (cicpy refuses the collision)."""
    return type(f"blk_{inst}", (Stack,),
                dict(__doc__=doc, match=rf'^x{inst}$', group=inst,
                     fill=False, order=[f'x{inst}']))


class REY_PLL(SidecarCell):
    blk_rosc = _block("rosc", "REY_PLL_ROSC, the oscillator.")
    blk_lpf = _block("lpf", "REY_PLL_LPF, eight RCU cells.")
    blk_divn = _block("divn", "REY_PLL_DIVN, the divider and tap buffers.")
    blk_pfd = _block("pfd", "REY_PLL_PFD.")
    blk_ctrl = _block("ctrl", "REY_PLL_CTRL, power up, kick, open loop.")
    blk_cp = _block("cp", "REY_PLL_CP, the charge pump.")

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    channel = 4
    routes = []


_C = REY_PLL
REY_PLL.rows = [[_C.blk_rosc, _C.blk_lpf], [_C.blk_divn, _C.blk_pfd, _C.blk_ctrl, _C.blk_cp]]
