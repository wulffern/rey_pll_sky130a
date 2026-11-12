
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

#- `make lpe` ends with an LVS of the flat extracted netlist against the
#- hierarchical schematic. With the PDK's netgen setup netgen segfaults
#- there, on the series merging of the oscillator bias ladder's poly
#- resistors. netgen_lpe_setup.tcl is the PDK setup with series merging
#- of res_high_po switched off. For `lpe` only: `lvs` keeps the PDK setup.
lpe: NETGENSETUP = netgen_lpe_setup.tcl

#- sch2mag reads THIS IP's rules (cic/sky130A.tech: the shared
#- tech_sky130A file plus the met3/met4 minimum area, which cicpy needs
#- to size the middle pads of a via stack); the shared file stays as it
#- is. Scoped to `mag`: OPT also reaches checklvs.
mag: OPT += --tech ../cic/sky130A.tech

#- ciccreator cells (cic/ip.json), compiled with cicpy: the loop filter
#- units (lpf.json, against rey_atr's resistor patterns, prefixed REYPLL_)
#- and the digital blocks (pll.json, on the built rey_tr library,
#- unprefixed, LVS'd against their xschem schematics, which the compile
#- leaves alone: meta noSchematic). Writes design/REY_PLL_SKY130A.cic and
#- the .mag/.sch/.sym views. rey_tr's own cells are not rewritten.
CIC_EXCLUDE = (RPPO2|RPPO4|RES2|RES4|11CWALL|RESABUT[RM]|HRPPO2|HRPPO12)$$|^REYTR_
cic:
	cd ../design && cicpy compile --I ../cic --I ../../rey_atr_sky130a/cic --prefix REYPLL_ --exclude "${CIC_EXCLUDE}" --spice --magic --xschem ../cic/ip.json ../cic/sky130.tech ${LIB}
