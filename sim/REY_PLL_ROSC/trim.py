#!/usr/bin/env python3
"""Summarize the TRIM x VCTRL sweep in tran.spi.

Usage: python3 trim.py [target_MHz] output_tran/tran_*.log

For each corner, prints the ring frequency at VCTRL=0 (fmax) and the
highest VCTRL (fmin) per trim code, and which codes contain the target
frequency inside the VCTRL range.
"""
import re
import sys
import os

args = sys.argv[1:]
target = 512.0
if args and re.match(r"^[0-9.]+$", args[0]):
    target = float(args.pop(0))

rx = re.compile(r"^(trimcode|vctrl|tpd|tck|vbp)\s+=\s+(\S+)")

rows = []
for f in sorted(args):
    corner = os.path.basename(f).replace(".log", "").replace("tran_", "")
    res = {}
    code = vctrl = None
    with open(f) as fi:
        for line in fi:
            m = rx.match(line)
            if not m:
                continue
            k, v = m.group(1), float(m.group(2))
            if k == "trimcode":
                code = int(v)
            elif k == "vctrl":
                vctrl = v
            elif k == "tpd":
                res.setdefault(code, {})[vctrl] = 10 / v / 1e6
    ok = []
    cells = []
    for c in range(8):
        d = res.get(c, {})
        if not d:
            cells.append("     ---    ")
            continue
        fmax = d.get(min(d), 0)
        fmin = d.get(max(d), 0)
        cells.append(f"{fmin:5.0f}-{fmax:<5.0f} ")
        if fmin <= target <= fmax:
            ok.append(str(c))
    rows.append((corner, cells, ok))

print(f"Ring frequency [MHz], fmin(VCTRL=max)-fmax(VCTRL=0) per TRIM code, target {target:.0f} MHz")
print(f"{'corner':24s}" + "".join(f"  code {c}    " for c in range(8)) + " codes hitting target")
for corner, cells, ok in rows:
    print(f"{corner:24s}" + " ".join(cells) + " " + (",".join(ok) if ok else "NONE"))
