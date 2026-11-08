#!/bin/sh
# Lock over process, temperature and supply, each process at the trim
# code trim.py picked from the oscillator sweep (middle of its range)
cicsim run --name Sch_corners --threads 4 tran Sch Gt C3 "Ktt,Kfs" "Tl,Th" "Vl,Vh"
cicsim run --name Sch_corners_ss --threads 4 tran Sch Gt C6 Kss "Tl,Th" "Vl,Vh"
cicsim run --name Sch_corners_ff --threads 4 tran Sch Gt C0 Kff "Tl,Th" "Vl,Vh"
cicsim run --name Sch_corners_sf --threads 4 tran Sch Gt C4 Ksf "Tl,Th" "Vl,Vh"
