
#- Core makefile provides the following commands:
# -----------------------------------------------------------
# gds: generate gds/<CELL>.gds
# cdl: generate cdl/<CELL>.cdl
# xsch: generate xsch/<CELL>.spice
# lvs: Check cdl/<CELL>.cdl versus ../design/<LIB>/<CELL>.mag
# lpe: Extract parasitics lpe/<CELL>.spi
# drc: Run design rule checks on ../design/<LIB>/<CELL>.mag
# -----------------------------------------------------------

PREFIX=
LIB=REY_PLL_SKY130A
CELL=REY_PLL

#- Provide cells you want to check for the lvsall drcall commands
CELLS = REY_PLL

include ../tech/make/core.make

#- Loop filter unit cells (cic/lpf.json), compiled with cicpy against the
#- rey_atr resistor patterns. Writes design/REY_PLL_SKY130A.cic and the
#- REYPLL_* .mag/.sch/.sym views
cic:
	cd ../design && cicpy compile --I ../cic --I ../../rey_atr_sky130a/cic --prefix REYPLL_ --exclude "(RPPO2|RPPO4|RES2|RES4|11CWALL|RESABUT[RM]|HRPPO2|HRPPO12)$$" --spice --magic --xschem ../cic/lpf.json ../cic/sky130.tech ${LIB}

