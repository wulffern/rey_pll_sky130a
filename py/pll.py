#!/usr/bin/env python3
"""Charge pump PLL loop model for REY_PLL: DESIGN the loop filter.

Loop:  PFD/CP (Icp) -> Z(s) -> VCO (Kvco) -> 1/N

  Z(s)  = (1 + s R C1) / (s (C1+C2) (1 + s R Cs)),  Cs = C1 C2/(C1+C2)
  L(s)  = Icp/(2 pi) * Kvco * Z(s) / (N s)

Design for a crossover wc and phase margin PM, with the zero and the
extra pole placed symmetric around wc (maximum phase at wc):

  b        = (C1+C2)/C2 = wp/wz = (tan PM + sec PM)^2
  C1 + C2  = Icp Kvco sqrt(b) / (2 pi N wc^2)
  C2       = (C1+C2)/b
  R        = sqrt(b) / (wc C1)

So the capacitance scales with Icp*Kvco/(N wc^2): a smaller Kvco or
a smaller Icp shrinks C, but R scales as 1/C and grows. The sweep at
the bottom prints the area of both, for picking a point that fits a
Tiny Tapeout tile.

The VCO here has NEGATIVE gain (f falls as VCTRL rises); the loop
uses |Kvco| with UP/DN swapped at the charge pump, and the filter is
referenced to VDD_1V8 (VCTRL follows the PMOS sources).

Usage:
  python3 py/pll.py                       # defaults below
  python3 py/pll.py --kvco 235e6 --icp 1e-6 --fref 8e6 --n 32
  python3 py/pll.py --log sim/REY_PLL_ROSC/output_tran/tran_SchGtKttTtVt.log --code 3
"""
import argparse
import re
import numpy as np

#- Area densities, sky130 (assumptions, check against the cells)
MIM_F_PER_UM2 = 2e-15        # cap_mim_m3_1, ~2 fF/um2, can sit over devices
MOS_F_PER_UM2 = 8e-15        # nfet_01v8 gate cap, ~8 fF/um2 in inversion
#- REYATR_HRPPO8: four 15.3k resistors in a 16 x 20.8 um cell
RES_OHM_PER_UM2 = 61.2e3 / (16 * 20.8)

#- One Tiny Tapeout tile, sky130 (check the shuttle's tile size)
TILE_UM2 = 161.0 * 111.52


def design(fref, N, kvco_hz, icp, fc_ratio=20, pm_deg=60):
    """Return the loop filter for crossover fref/fc_ratio and PM."""
    kvco = 2*np.pi*abs(kvco_hz)
    wc = 2*np.pi*fref/fc_ratio
    pm = np.radians(pm_deg)
    sb = np.tan(pm) + 1/np.cos(pm)
    b = sb**2
    ctot = icp*kvco*sb/(2*np.pi*N*wc**2)
    c2 = ctot/b
    c1 = ctot - c2
    r = sb/(wc*c1)
    return dict(fref=fref, N=N, kvco_hz=kvco_hz, icp=icp, fc=wc/(2*np.pi),
                pm_deg=pm_deg, b=b, C1=c1, C2=c2, R=r)


def loopgain(d, f):
    s = 1j*2*np.pi*f
    c1, c2, r = d["C1"], d["C2"], d["R"]
    cs = c1*c2/(c1 + c2)
    z = (1 + s*r*c1)/(s*(c1 + c2)*(1 + s*r*cs))
    return d["icp"]/(2*np.pi)*2*np.pi*abs(d["kvco_hz"])*z/(d["N"]*s)


def check(d):
    """Numerical crossover and phase margin of the designed loop."""
    f = np.logspace(2, 9, 20000)
    L = loopgain(d, f)
    i = np.where(np.abs(L) < 1)[0][0]
    return f[i], 180 + np.degrees(np.angle(L[i]))


def area(d):
    a_c_mim = (d["C1"] + d["C2"])/MIM_F_PER_UM2
    a_c_mos = (d["C1"] + d["C2"])/MOS_F_PER_UM2
    a_r = d["R"]/RES_OHM_PER_UM2
    return a_c_mim, a_c_mos, a_r


def report(d):
    fc, pm = check(d)
    a_mim, a_mos, a_r = area(d)
    print(f"fref={d['fref']/1e6:.3g} MHz  N={d['N']}  fout={d['fref']*d['N']/1e6:.4g} MHz  "
          f"|Kvco|={abs(d['kvco_hz'])/1e6:.3g} MHz/V  Icp={d['icp']*1e6:.3g} uA")
    print(f"  target fc={d['fc']/1e3:.4g} kHz PM={d['pm_deg']}  ->  "
          f"check fc={fc/1e3:.4g} kHz PM={pm:.1f} deg")
    print(f"  C1={d['C1']*1e12:.3g} pF  C2={d['C2']*1e12:.3g} pF  R={d['R']/1e3:.4g} kOhm")
    print(f"  area: C as MiM {a_mim:.0f} um2 (or MOS {a_mos:.0f} um2), "
          f"R {a_r:.0f} um2  = {(a_mos + a_r)/TILE_UM2*100:.0f}% of a tile "
          f"(MOS C), {(a_mim + a_r)/TILE_UM2*100:.0f}% (MiM C, not stacked)")


def kvco_from_log(logfile, code, ftarget):
    """|Kvco| [Hz/V] at ftarget from the TRIM x VCTRL sweep in tran.spi."""
    rx = re.compile(r"^(trimcode|vctrl|tpd)\s+=\s+(\S+)")
    pts = []
    c = v = None
    with open(logfile) as fi:
        for line in fi:
            m = rx.match(line)
            if not m:
                continue
            k, x = m.group(1), float(m.group(2))
            if k == "trimcode":
                c = int(x)
            elif k == "vctrl":
                v = x
            elif k == "tpd" and c == code:
                pts.append((v, 10/x))
    pts.sort()
    for (v0, f0), (v1, f1) in zip(pts, pts[1:]):
        if min(f0, f1) <= ftarget <= max(f0, f1):
            return abs((f1 - f0)/(v1 - v0)), pts
    return None, pts


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fref", type=float, default=8e6)
    ap.add_argument("--n", type=int, default=64)
    ap.add_argument("--kvco", type=float, default=235e6, help="|Kvco| in Hz/V")
    ap.add_argument("--icp", type=float, default=1e-6)
    ap.add_argument("--fc_ratio", type=float, default=20)
    ap.add_argument("--pm", type=float, default=60)
    ap.add_argument("--log", help="tran log of the ROSC sweep, to read Kvco")
    ap.add_argument("--code", type=int, default=3)
    a = ap.parse_args()

    kvco = a.kvco
    if a.log:
        k, pts = kvco_from_log(a.log, a.code, a.fref*a.n)
        print("sweep (VCTRL, f):", ", ".join(f"({v:.2f}, {f/1e6:.0f}M)" for v, f in pts))
        if k is None:
            raise SystemExit(f"code {a.code} does not reach {a.fref*a.n/1e6:.4g} MHz")
        kvco = k
        print(f"|Kvco| at {a.fref*a.n/1e6:.4g} MHz, code {a.code}: {k/1e6:.3g} MHz/V")

    #- the design point
    report(design(a.fref, a.n, kvco, a.icp, a.fc_ratio, a.pm))

    #- sun_pll for reference: Kvco 1.6 GHz/V, Icp 1 uA, N 32
    print("\nsun_pll's numbers through the same procedure:")
    report(design(8e6, 32, 1.6e9, 1e-6, a.fc_ratio, a.pm))

    #- the trade: C ~ Icp*Kvco, R ~ 1/(Icp*Kvco)
    print("\narea vs Icp*|Kvco| (MOS C + HRPPO R), fc = fref/%g, PM %g:" % (a.fc_ratio, a.pm))
    print(f"{'Icp':>8s} {'Kvco':>10s} {'C1 pF':>7s} {'R kOhm':>8s} {'C um2':>7s} {'R um2':>7s} {'tile %':>7s}")
    for icp in (0.25e-6, 0.5e-6, 1e-6, 2e-6, 4e-6):
        for kv in (100e6, 235e6, 500e6):
            d = design(a.fref, a.n, kv, icp, a.fc_ratio, a.pm)
            _, a_mos, a_r = area(d)
            print(f"{icp*1e6:6.2f}uA {kv/1e6:7.0f}M/V {d['C1']*1e12:7.2f} {d['R']/1e3:8.0f} "
                  f"{a_mos:7.0f} {a_r:7.0f} {(a_mos + a_r)/TILE_UM2*100:6.0f}%")
