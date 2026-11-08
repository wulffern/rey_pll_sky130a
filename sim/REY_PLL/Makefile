
all: typical

TB=tran
VIEW=Sch
#VIEW=Lay
CELL=REY_PLL
LIB =REY_PLL_SKY130A
OPT=

include ../../tech/make/sim.make

test:
	${MAKE} typical OPT="Debug"

#- one trim code per process, the middle of the range trim.py found
typical: netlist
	cicsim run --name ${VIEW}_typical ${TB} ${OPT} ${VIEW} Gt C3 Ktt Tt Vt

corners: netlist
	cicsim run --name ${VIEW}_corners --threads 5 ${TB} ${OPT} ${VIEW} Gt "Ktt,Kss,Kff,Ksf,Kfs" "Tl,Th" "Vl,Vh"
