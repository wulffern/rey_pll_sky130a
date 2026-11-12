v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_CTRL: power up, start-up kick and open loop modes} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=PWRUP_1V8}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=OLH}
C {devices/ipin.sym} -760 -740 0 0 {name=p4 lab=OLL}
C {devices/opin.sym} -600 -740 0 0 {name=p5 lab=KICK}
C {devices/opin.sym} -440 -740 0 0 {name=p6 lab=VHI_N}
C {devices/opin.sym} -280 -740 0 0 {name=p7 lab=VLO}
T {KICK: a pulse when PWRUP_1V8 rises. KD4 is PWRUP_1V8 delayed by five inverters, so NOR(PWRUP_N, KD4) is high} -1450 -660 0 0 0.3 0.3 {}
T {between the edge and KD4. PWRUP_NB is a second PWRUP_N, local to the NORs, so no net runs the length of the} -1450 -630 0 0 0.3 0.3 {}
T {column} -1450 -600 0 0 0.3 0.3 {}
T {Open loop, for the per-die trim: VHI_N = PWRUP and not OLH parks VCTRL at VDD_1V8 (slowest), VLO = VHI_N and} -1450 -570 0 0 0.3 0.3 {}
T {OLL at VSS (fastest). Powered down is OLH} -1450 -540 0 0 0.3 0.3 {}
T {A: power up, kick, open loop} -1360 -410 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -1300 -280 0 0 {name=XA0}
C {devices/lab_pin.sym} -1300 -300 2 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -260 3 0 {name=l2 sig_type=std_logic lab=VSS}
T {XA0} -1360 -332.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 -150 0 0 {name=XA1}
C {devices/lab_pin.sym} -1300 -150 0 0 {name=l3 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1220 -150 2 0 {name=l4 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1260 -190 2 0 {name=l5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 -110 2 0 {name=l6 sig_type=std_logic lab=VSS}
T {XA1} -1360 -222.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 0 0 0 {name=XA2}
C {devices/lab_pin.sym} -1300 0 0 0 {name=l7 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1220 0 2 0 {name=l8 sig_type=std_logic lab=KD0}
C {devices/lab_pin.sym} -1260 -40 2 0 {name=l9 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 40 2 0 {name=l10 sig_type=std_logic lab=VSS}
T {XA2} -1360 -72.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 150 0 0 {name=XA3}
C {devices/lab_pin.sym} -1300 150 0 0 {name=l11 sig_type=std_logic lab=KD0}
C {devices/lab_pin.sym} -1220 150 2 0 {name=l12 sig_type=std_logic lab=KD1}
C {devices/lab_pin.sym} -1260 110 2 0 {name=l13 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 190 2 0 {name=l14 sig_type=std_logic lab=VSS}
T {XA3} -1360 78.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 300 0 0 {name=XA4}
C {devices/lab_pin.sym} -1300 300 0 0 {name=l15 sig_type=std_logic lab=KD1}
C {devices/lab_pin.sym} -1220 300 2 0 {name=l16 sig_type=std_logic lab=KD2}
C {devices/lab_pin.sym} -1260 260 2 0 {name=l17 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 340 2 0 {name=l18 sig_type=std_logic lab=VSS}
T {XA4} -1360 228.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 450 0 0 {name=XA5}
C {devices/lab_pin.sym} -1300 450 0 0 {name=l19 sig_type=std_logic lab=KD2}
C {devices/lab_pin.sym} -1220 450 2 0 {name=l20 sig_type=std_logic lab=KD3}
C {devices/lab_pin.sym} -1260 410 2 0 {name=l21 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 490 2 0 {name=l22 sig_type=std_logic lab=VSS}
T {XA5} -1360 378.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 600 0 0 {name=XA6}
C {devices/lab_pin.sym} -1300 600 0 0 {name=l23 sig_type=std_logic lab=KD3}
C {devices/lab_pin.sym} -1220 600 2 0 {name=l24 sig_type=std_logic lab=KD4}
C {devices/lab_pin.sym} -1260 560 2 0 {name=l25 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 640 2 0 {name=l26 sig_type=std_logic lab=VSS}
T {XA6} -1360 528.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 750 0 0 {name=XA7}
C {devices/lab_pin.sym} -1300 750 0 0 {name=l27 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1220 750 2 0 {name=l28 sig_type=std_logic lab=PWRUP_NB}
C {devices/lab_pin.sym} -1260 710 2 0 {name=l29 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 790 2 0 {name=l30 sig_type=std_logic lab=VSS}
T {XA7} -1360 678.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -1300 910 0 0 {name=XA8}
C {devices/lab_pin.sym} -1300 890 0 0 {name=l31 sig_type=std_logic lab=PWRUP_NB}
C {devices/lab_pin.sym} -1300 910 0 0 {name=l32 sig_type=std_logic lab=KD4}
C {devices/lab_pin.sym} -1210 900 2 0 {name=l33 sig_type=std_logic lab=KICK}
C {devices/lab_pin.sym} -1260 860 2 0 {name=l34 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 940 2 0 {name=l35 sig_type=std_logic lab=VSS}
T {XA8} -1360 828.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -1300 1060 0 0 {name=XA9}
C {devices/lab_pin.sym} -1300 1040 0 0 {name=l36 sig_type=std_logic lab=PWRUP_NB}
C {devices/lab_pin.sym} -1300 1060 0 0 {name=l37 sig_type=std_logic lab=OLH}
C {devices/lab_pin.sym} -1210 1050 2 0 {name=l38 sig_type=std_logic lab=VHI_N}
C {devices/lab_pin.sym} -1260 1010 2 0 {name=l39 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 1090 2 0 {name=l40 sig_type=std_logic lab=VSS}
T {XA9} -1360 978.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1300 1210 0 0 {name=XA10}
C {devices/lab_pin.sym} -1300 1190 0 0 {name=l41 sig_type=std_logic lab=VHI_N}
C {devices/lab_pin.sym} -1300 1210 0 0 {name=l42 sig_type=std_logic lab=OLL}
C {devices/lab_pin.sym} -1210 1200 2 0 {name=l43 sig_type=std_logic lab=VLO}
C {devices/lab_pin.sym} -1260 1160 2 0 {name=l44 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 1240 2 0 {name=l45 sig_type=std_logic lab=VSS}
T {XA10} -1360 1128.0 0 0 0.25 0.25 {}
P 4 5 -1520 -860 -190 -860 -190 1300 -1520 1300 -1520 -860 {dash=4}
