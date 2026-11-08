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
T {R: 32 x 15.3 kOhm in series, VCTRL to VLPFZ (490 kOhm). C1: 7 MiM, VLPFZ to VDD_1V8. C2: 1 MiM, VCTRL to VDD_1V8} -1450 -640 0 0 0.3 0.3 {}
T {MiM bottom plates (A) on VDD_1V8, so their parasitic to substrate does not load VCTRL} -1450 -610 0 0 0.3 0.3 {}
C {REY_PLL_SKY130A/REYPLL_RCU.sym} -1000 -450 0 0 {name=xrc[7:0]}
C {devices/lab_pin.sym} -1020 -290 0 0 {name=l1 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1020 -270 0 0 {name=l2 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1020 -450 0 0 {name=l3 sig_type=std_logic lab=R28,R24,R20,R16,R12,R8,R4,VCTRL}
C {devices/lab_pin.sym} -1020 -430 0 0 {name=l4 sig_type=std_logic lab=R29,R25,R21,R17,R13,R9,R5,R1}
C {devices/lab_pin.sym} -1020 -410 0 0 {name=l5 sig_type=std_logic lab=R29,R25,R21,R17,R13,R9,R5,R1}
C {devices/lab_pin.sym} -1020 -390 0 0 {name=l6 sig_type=std_logic lab=R30,R26,R22,R18,R14,R10,R6,R2}
C {devices/lab_pin.sym} -1020 -370 0 0 {name=l7 sig_type=std_logic lab=R30,R26,R22,R18,R14,R10,R6,R2}
C {devices/lab_pin.sym} -1020 -350 0 0 {name=l8 sig_type=std_logic lab=R31,R27,R23,R19,R15,R11,R7,R3}
C {devices/lab_pin.sym} -1020 -330 0 0 {name=l9 sig_type=std_logic lab=R31,R27,R23,R19,R15,R11,R7,R3}
C {devices/lab_pin.sym} -1020 -310 0 0 {name=l10 sig_type=std_logic lab=VLPFZ,R28,R24,R20,R16,R12,R8,R4}
C {devices/lab_pin.sym} -1020 -250 0 0 {name=l11 sig_type=std_logic lab=VCTRL,VLPFZ,VLPFZ,VLPFZ,VLPFZ,VLPFZ,VLPFZ,VLPFZ}
T {cell i holds resistors 4i..4i+3 of the chain, R0 = VCTRL, R32 = VLPFZ; cell 7's MiM is C2} -1450 -150 0 0 0.3 0.3 {}
