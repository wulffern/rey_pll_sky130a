v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_LPF: loop filter on VDD_1V8, eight REYPLL_RCU} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=VCTRL}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=VLPFZ}
T {R: 32 x 15.3 kOhm in series, VCTRL (R0) to VLPFZ (R32). C2: 1 MiM (cell XA0), VCTRL to VDD_1V8. C1: 7 MiM, VLPFZ to VDD_1V8} -1450 -660 0 0 0.3 0.3 {}
T {MiM bottom plates (A) on VDD_1V8, so their parasitic to substrate does not load VCTRL} -1450 -630 0 0 0.3 0.3 {}
T {A: R0..R8} -1360 -500 0 0 0.35 0.35 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} -1300 -420 0 0 {name=XA0}
C {devices/lab_pin.sym} -1320 -420 0 0 {name=l1 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -1320 -400 0 0 {name=l2 sig_type=std_logic lab=R1}
C {devices/lab_pin.sym} -1320 -380 0 0 {name=l3 sig_type=std_logic lab=R1}
C {devices/lab_pin.sym} -1320 -360 0 0 {name=l4 sig_type=std_logic lab=R2}
C {devices/lab_pin.sym} -1320 -340 0 0 {name=l5 sig_type=std_logic lab=R2}
C {devices/lab_pin.sym} -1320 -320 0 0 {name=l6 sig_type=std_logic lab=R3}
C {devices/lab_pin.sym} -1320 -300 0 0 {name=l7 sig_type=std_logic lab=R3}
C {devices/lab_pin.sym} -1320 -280 0 0 {name=l8 sig_type=std_logic lab=R4}
C {devices/lab_pin.sym} -1320 -260 0 0 {name=l9 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1320 -240 0 0 {name=l10 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1320 -220 0 0 {name=l11 sig_type=std_logic lab=VCTRL}
T {XA0} -1180 -426.0 0 0 0.25 0.25 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} -1300 -160 0 0 {name=XA1}
C {devices/lab_pin.sym} -1320 -160 0 0 {name=l12 sig_type=std_logic lab=R4}
C {devices/lab_pin.sym} -1320 -140 0 0 {name=l13 sig_type=std_logic lab=R5}
C {devices/lab_pin.sym} -1320 -120 0 0 {name=l14 sig_type=std_logic lab=R5}
C {devices/lab_pin.sym} -1320 -100 0 0 {name=l15 sig_type=std_logic lab=R6}
C {devices/lab_pin.sym} -1320 -80 0 0 {name=l16 sig_type=std_logic lab=R6}
C {devices/lab_pin.sym} -1320 -60 0 0 {name=l17 sig_type=std_logic lab=R7}
C {devices/lab_pin.sym} -1320 -40 0 0 {name=l18 sig_type=std_logic lab=R7}
C {devices/lab_pin.sym} -1320 -20 0 0 {name=l19 sig_type=std_logic lab=R8}
C {devices/lab_pin.sym} -1320 0 0 0 {name=l20 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1320 20 0 0 {name=l21 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1320 40 0 0 {name=l22 sig_type=std_logic lab=VLPFZ}
T {XA1} -1180 -166.0 0 0 0.25 0.25 {}
T {B: R8..R16} -880 -500 0 0 0.35 0.35 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} -820 -420 0 0 {name=XB0}
C {devices/lab_pin.sym} -840 -420 0 0 {name=l23 sig_type=std_logic lab=R8}
C {devices/lab_pin.sym} -840 -400 0 0 {name=l24 sig_type=std_logic lab=R9}
C {devices/lab_pin.sym} -840 -380 0 0 {name=l25 sig_type=std_logic lab=R9}
C {devices/lab_pin.sym} -840 -360 0 0 {name=l26 sig_type=std_logic lab=R10}
C {devices/lab_pin.sym} -840 -340 0 0 {name=l27 sig_type=std_logic lab=R10}
C {devices/lab_pin.sym} -840 -320 0 0 {name=l28 sig_type=std_logic lab=R11}
C {devices/lab_pin.sym} -840 -300 0 0 {name=l29 sig_type=std_logic lab=R11}
C {devices/lab_pin.sym} -840 -280 0 0 {name=l30 sig_type=std_logic lab=R12}
C {devices/lab_pin.sym} -840 -260 0 0 {name=l31 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -840 -240 0 0 {name=l32 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -840 -220 0 0 {name=l33 sig_type=std_logic lab=VLPFZ}
T {XB0} -700 -426.0 0 0 0.25 0.25 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} -820 -160 0 0 {name=XB1}
C {devices/lab_pin.sym} -840 -160 0 0 {name=l34 sig_type=std_logic lab=R12}
C {devices/lab_pin.sym} -840 -140 0 0 {name=l35 sig_type=std_logic lab=R13}
C {devices/lab_pin.sym} -840 -120 0 0 {name=l36 sig_type=std_logic lab=R13}
C {devices/lab_pin.sym} -840 -100 0 0 {name=l37 sig_type=std_logic lab=R14}
C {devices/lab_pin.sym} -840 -80 0 0 {name=l38 sig_type=std_logic lab=R14}
C {devices/lab_pin.sym} -840 -60 0 0 {name=l39 sig_type=std_logic lab=R15}
C {devices/lab_pin.sym} -840 -40 0 0 {name=l40 sig_type=std_logic lab=R15}
C {devices/lab_pin.sym} -840 -20 0 0 {name=l41 sig_type=std_logic lab=R16}
C {devices/lab_pin.sym} -840 0 0 0 {name=l42 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -840 20 0 0 {name=l43 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -840 40 0 0 {name=l44 sig_type=std_logic lab=VLPFZ}
T {XB1} -700 -166.0 0 0 0.25 0.25 {}
T {C: R16..R24} -400 -500 0 0 0.35 0.35 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} -340 -420 0 0 {name=XC0}
C {devices/lab_pin.sym} -360 -420 0 0 {name=l45 sig_type=std_logic lab=R16}
C {devices/lab_pin.sym} -360 -400 0 0 {name=l46 sig_type=std_logic lab=R17}
C {devices/lab_pin.sym} -360 -380 0 0 {name=l47 sig_type=std_logic lab=R17}
C {devices/lab_pin.sym} -360 -360 0 0 {name=l48 sig_type=std_logic lab=R18}
C {devices/lab_pin.sym} -360 -340 0 0 {name=l49 sig_type=std_logic lab=R18}
C {devices/lab_pin.sym} -360 -320 0 0 {name=l50 sig_type=std_logic lab=R19}
C {devices/lab_pin.sym} -360 -300 0 0 {name=l51 sig_type=std_logic lab=R19}
C {devices/lab_pin.sym} -360 -280 0 0 {name=l52 sig_type=std_logic lab=R20}
C {devices/lab_pin.sym} -360 -260 0 0 {name=l53 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -360 -240 0 0 {name=l54 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -360 -220 0 0 {name=l55 sig_type=std_logic lab=VLPFZ}
T {XC0} -220 -426.0 0 0 0.25 0.25 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} -340 -160 0 0 {name=XC1}
C {devices/lab_pin.sym} -360 -160 0 0 {name=l56 sig_type=std_logic lab=R20}
C {devices/lab_pin.sym} -360 -140 0 0 {name=l57 sig_type=std_logic lab=R21}
C {devices/lab_pin.sym} -360 -120 0 0 {name=l58 sig_type=std_logic lab=R21}
C {devices/lab_pin.sym} -360 -100 0 0 {name=l59 sig_type=std_logic lab=R22}
C {devices/lab_pin.sym} -360 -80 0 0 {name=l60 sig_type=std_logic lab=R22}
C {devices/lab_pin.sym} -360 -60 0 0 {name=l61 sig_type=std_logic lab=R23}
C {devices/lab_pin.sym} -360 -40 0 0 {name=l62 sig_type=std_logic lab=R23}
C {devices/lab_pin.sym} -360 -20 0 0 {name=l63 sig_type=std_logic lab=R24}
C {devices/lab_pin.sym} -360 0 0 0 {name=l64 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -360 20 0 0 {name=l65 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -360 40 0 0 {name=l66 sig_type=std_logic lab=VLPFZ}
T {XC1} -220 -166.0 0 0 0.25 0.25 {}
T {D: R24..R32} 80 -500 0 0 0.35 0.35 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} 140 -420 0 0 {name=XD0}
C {devices/lab_pin.sym} 120 -420 0 0 {name=l67 sig_type=std_logic lab=R24}
C {devices/lab_pin.sym} 120 -400 0 0 {name=l68 sig_type=std_logic lab=R25}
C {devices/lab_pin.sym} 120 -380 0 0 {name=l69 sig_type=std_logic lab=R25}
C {devices/lab_pin.sym} 120 -360 0 0 {name=l70 sig_type=std_logic lab=R26}
C {devices/lab_pin.sym} 120 -340 0 0 {name=l71 sig_type=std_logic lab=R26}
C {devices/lab_pin.sym} 120 -320 0 0 {name=l72 sig_type=std_logic lab=R27}
C {devices/lab_pin.sym} 120 -300 0 0 {name=l73 sig_type=std_logic lab=R27}
C {devices/lab_pin.sym} 120 -280 0 0 {name=l74 sig_type=std_logic lab=R28}
C {devices/lab_pin.sym} 120 -260 0 0 {name=l75 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 120 -240 0 0 {name=l76 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 120 -220 0 0 {name=l77 sig_type=std_logic lab=VLPFZ}
T {XD0} 260 -426.0 0 0 0.25 0.25 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} 140 -160 0 0 {name=XD1}
C {devices/lab_pin.sym} 120 -160 0 0 {name=l78 sig_type=std_logic lab=R28}
C {devices/lab_pin.sym} 120 -140 0 0 {name=l79 sig_type=std_logic lab=R29}
C {devices/lab_pin.sym} 120 -120 0 0 {name=l80 sig_type=std_logic lab=R29}
C {devices/lab_pin.sym} 120 -100 0 0 {name=l81 sig_type=std_logic lab=R30}
C {devices/lab_pin.sym} 120 -80 0 0 {name=l82 sig_type=std_logic lab=R30}
C {devices/lab_pin.sym} 120 -60 0 0 {name=l83 sig_type=std_logic lab=R31}
C {devices/lab_pin.sym} 120 -40 0 0 {name=l84 sig_type=std_logic lab=R31}
C {devices/lab_pin.sym} 120 -20 0 0 {name=l85 sig_type=std_logic lab=VLPFZ}
C {devices/lab_pin.sym} 120 0 0 0 {name=l86 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 120 20 0 0 {name=l87 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 120 40 0 0 {name=l88 sig_type=std_logic lab=VLPFZ}
T {XD1} 260 -166.0 0 0 0.25 0.25 {}
