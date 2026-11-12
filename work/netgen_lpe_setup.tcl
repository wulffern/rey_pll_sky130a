#---------------------------------------------------------------
# netgen setup for the LVS check at the end of `make lpe`
# (work/Makefile: lpe: NETGENSETUP = netgen_lpe_setup.tcl).
#
# That check compares the flat extracted netlist with the hierarchical
# schematic. With the PDK setup netgen 1.5.305 segfaults in
# remove_group_tags (base/netgen.c; the function is the same in 1.5.328)
# while it series/parallel merges the poly resistors of the oscillator
# bias ladder: flat, the fixed branch is ((r+r)||(r+r)) + r+r + r+r,
# in the schematic it is four two-segment cells.
#
# So: the PDK setup, then no series merging for the high resistance
# poly resistor. Every segment is then matched one to one, which is
# stricter than the PDK setup, not looser. Parallel merging stays.
#---------------------------------------------------------------

source $::env(PDK_ROOT)/sky130A/libs.tech/netgen/sky130A_setup.tcl

set dev sky130_fd_pr__res_high_po
foreach c {circuit1 circuit2} {
    if {[lsearch [cells list -all -$c] $dev] >= 0} {
        property "-$c $dev" series disable
    }
}
