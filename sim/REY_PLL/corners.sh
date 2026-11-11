#!/bin/sh
# Lock over process, temperature and supply, each process at the trim
# code trim.py picked from the oscillator sweep (middle of its range).
#   ./corners.sh        schematic
#   ./corners.sh Lay    extracted (work/lpe/REY_PLL_lpe.spi must exist)
VIEW=${1:-Sch}
cicsim run --name ${VIEW}_corners --threads 4 tran ${VIEW} Gt C3 "Ktt,Kfs" "Tl,Th" "Vl,Vh"
cicsim run --name ${VIEW}_corners_ss --threads 4 tran ${VIEW} Gt C6 Kss "Tl,Th" "Vl,Vh"
cicsim run --name ${VIEW}_corners_ff --threads 4 tran ${VIEW} Gt C0 Kff "Tl,Th" "Vl,Vh"
cicsim run --name ${VIEW}_corners_sf --threads 4 tran ${VIEW} Gt C4 Ksf "Tl,Th" "Vl,Vh"
