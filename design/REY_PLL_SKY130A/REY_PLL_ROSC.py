"""REY_PLL_ROSC: the oscillator, assembled from finished blocks.

Every block is laid out, routed and checked on its own first:

    REY_PLL_ROSC_STAGE   one ring stage (inverter, VCTRL device, mirrors)
    REY_PLL_ROSC_BIAS    the Vgs/R bias, VBP out, trim switches
    dig                  the output buffer, rey_tr cells xo0/xo1/xotap

so this level places them in one row and routes only what runs between
them: the ring nodes N0..N6, VBP from the bias, VCTRL, and N6 into the
buffer.

    bias | dig | stg0 stg6 stg1 stg5 stg2 stg4 stg3

The stages are INTERLEAVED, so no ring hop is longer than two stages
(the closing N6 -> N0 included) and every node sees about the same
wire. Layers between the blocks (cicpy names):

    M4  verticals, from a stage's A/Y port down to the hop lanes
    M5  the hop lanes, under the ports over the nmos half; VBP and
        VCTRL across the stages at their pins' own height

Nothing in a stage uses M4 or M5. No coordinates here: every lane is a
pin's own coordinate, or a whole number of pitches from one.
"""
from cicpy.core.path import pin, PITCH
from cicpy.sidecar import SidecarCell, Stack

NSTAGE = 7
#- left to right; neighbours in the ring are at most two apart
ORDER = [0, 6, 1, 5, 2, 4, 3]
#- the hop lane each ring node takes, chosen so hops whose x ranges
#- overlap sit on different lanes (N0, N1, N2 step right; N3..N6 back)
LANE = {0: 0, 1: 1, 2: 0, 3: 2, 4: 3, 5: 2, 6: 3}
ONE = "1cuts,1vcuts"


def _stg(k):
    return f"xblk_stg{k}"


def _block(name, match, order, doc, xspace=0):
    """A stack holding finished cells. Named blk_<name> so its wrapper
    REY_PLL_ROSC_BLK_<NAME> cannot collide with the block itself.
    `xspace` (um) opens a gap on its left."""
    return type(f"blk_{name}", (Stack,),
                dict(__doc__=doc, match=match, group=name, fill=False,
                     order=order, xspace=xspace))


def _lane(src, net, lane):
    """A hop lane, under the source's output port: five pitches below
    it to clear the A port, then two pitches per lane."""
    return pin(src, net, "y") - (5 + 2 * lane) * PITCH


def _hop(net, src, dst, lane, land="M3"):
    """Node `net` from the Y port of `src` to the A port of `dst`:
    down M4 to the lane, along it on M5, back up M4 into the port."""
    return dict(net=net, start=(src, net), stop=(dst, net), options=ONE,
                steps=[("up", "M4"), ("movey", _lane(src, net, lane)),
                       ("up", "M5"), ("movex", pin(dst, net, "x")),
                       ("down", "M4"), ("movey", pin(dst, net, "y")),
                       ("down", land), ("end",)])


def _ring_paths():
    out = []
    for k in range(NSTAGE):
        n = f"N{k}"
        out.append(_hop(n, _stg(k), _stg((k + 1) % NSTAGE), LANE[k]))
    #- N6 also into the buffer, on N6's lane, landing on the cell's pin
    out.append(_hop("N6", _stg(6), "xblk_dig", LANE[6], land="M1"))
    return out


def _bias_paths():
    """VBP and VCTRL across the stages, M5 at the pins' own height; the
    stage pins are M1, deep in the pmos column, so each end is a stack.
    VBP comes in from the bias's own bar, from its east end."""
    stg = [_stg(k) for k in ORDER]
    out = []
    for net in ("VBP", "VCTRL"):
        out += [dict(net=net, start=(a, net), stop=(b, net), options=ONE,
                     steps=[("up", "M5"), ("movex", pin(b, net, "x")),
                            ("down", "M1"), ("end",)])
                for a, b in zip(stg, stg[1:])]
    out.append(dict(net="VBP", start=("xblk_bias", "VBP"),
                    stop=(stg[0], "VBP"), at="e", options=ONE,
                    steps=[("movex", pin(stg[0], "VBP", "x")),
                           ("up", "M4"), ("movey", pin(stg[0], "VBP", "y")),
                           ("down", "M1"), ("end",)]))
    return out


class REY_PLL_ROSC(SidecarCell):

    blk_bias = _block("bias", r'^xbias$', ['xbias'],
                      "REY_PLL_ROSC_BIAS, finished.")
    blk_dig = _block("dig", r'^(xo0|xo1|xotap)$', ['xotap', 'xo0', 'xo1'],
                     "The output buffer on its tap cell.",
                     #- as stage 0's gap: the buffer stands 0.75 um past
                     #- its box, the bias's pmos guard 0.4 past its own
                     xspace=1.6)

    supplies = [
        {"net": "VDD_1V8", "ring": "t", "strap": "top", "pin_strap": True},
        {"net": "VSS", "ring": "b", "strap": "bottom", "pin_strap": True},
    ]

    paths = _ring_paths() + _bias_paths()
    routes = []


_C = REY_PLL_ROSC
for _k in range(NSTAGE):
    setattr(_C, f"blk_stg{_k}", _block(
        f"stg{_k}", rf'^xstg<{_k}>$', [f'xstg<{_k}>'],
        f"Ring stage {_k}, REY_PLL_ROSC_STAGE.",
        #- the rey_tr buffer's cells stand 0.75 um past their box (li,
        #- nwell) and a stage's guard 0.44 um past its own; 1 um shorted
        #- the buffer's supply into the guard and overlapped the wells
        xspace=1.6 if _k == ORDER[0] else 0))
REY_PLL_ROSC.rows = [[_C.blk_bias, _C.blk_dig]
                     + [getattr(_C, f"blk_stg{k}") for k in ORDER]]
