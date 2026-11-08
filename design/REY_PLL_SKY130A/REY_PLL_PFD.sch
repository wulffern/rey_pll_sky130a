v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_PFD: tri-state phase frequency detector} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=PWRUP_1V8}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=CK_REF}
C {devices/ipin.sym} -760 -740 0 0 {name=p4 lab=CK_FB}
C {devices/opin.sym} -600 -740 0 0 {name=p5 lab=UP}
C {devices/opin.sym} -440 -740 0 0 {name=p6 lab=DN_N}
T {UP rises on CK_REF, DN on CK_FB. When both are high RST clears them; the path through the gates is the reset pulse that keeps the dead zone away} -1450 -660 0 0 0.3 0.3 {}
T {DFRNQNX1 clocks on NAND(CK, RN): released from reset while CK is high it sees a rising edge and sets again. So each flop's reset is HELD until its own clock is low:} -1450 -630 0 0 0.3 0.3 {}
T {HU = RST or (HU and CK_REF), RN_U = PWRUP and not HU; the same for DN on CK_FB} -1450 -600 0 0 0.3 0.3 {}
T {A: UP flop, RST, UP latch, PWRUP_N, DN flop, DN latch} -1360 -470 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -1300 -370 0 0 {name=XA0}
C {devices/lab_pin.sym} -1300 -390 3 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -350 1 0 {name=l2 sig_type=std_logic lab=VSS}
T {XA0} -1180 -376.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -200 0 0 {name=XA1}
C {devices/lab_pin.sym} -1300 -260 0 0 {name=l3 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1300 -200 0 0 {name=l4 sig_type=std_logic lab=CK_REF}
C {devices/lab_pin.sym} -1270 -170 1 0 {name=l5 sig_type=std_logic lab=RN_U}
C {devices/lab_pin.sym} -1200 -260 2 0 {name=l6 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1200 -200 2 0 {name=l7 sig_type=std_logic lab=UP_N}
C {devices/lab_pin.sym} -1240 -290 3 0 {name=l8 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -170 1 0 {name=l9 sig_type=std_logic lab=VSS}
T {XA1} -1180 -206.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1300 -60 0 0 {name=XA2}
C {devices/lab_pin.sym} -1300 -80 0 0 {name=l10 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1300 -60 0 0 {name=l11 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -1210 -70 2 0 {name=l12 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -1260 -110 3 0 {name=l13 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 -30 1 0 {name=l14 sig_type=std_logic lab=VSS}
T {XA2} -1180 -66.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -1300 80 0 0 {name=XA3}
C {devices/lab_pin.sym} -1300 60 0 0 {name=l15 sig_type=std_logic lab=HU}
C {devices/lab_pin.sym} -1300 80 0 0 {name=l16 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1210 70 2 0 {name=l17 sig_type=std_logic lab=RN_U}
C {devices/lab_pin.sym} -1260 30 3 0 {name=l18 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 110 1 0 {name=l19 sig_type=std_logic lab=VSS}
T {XA3} -1180 74.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ORX1_CV.sym} -1300 220 0 0 {name=XA4}
C {devices/lab_pin.sym} -1300 200 0 0 {name=l20 sig_type=std_logic lab=HAU}
C {devices/lab_pin.sym} -1300 220 0 0 {name=l21 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -1210 210 2 0 {name=l22 sig_type=std_logic lab=HU}
C {devices/lab_pin.sym} -1260 170 3 0 {name=l23 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 250 1 0 {name=l24 sig_type=std_logic lab=VSS}
T {XA4} -1180 214.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1300 360 0 0 {name=XA5}
C {devices/lab_pin.sym} -1300 340 0 0 {name=l25 sig_type=std_logic lab=HU}
C {devices/lab_pin.sym} -1300 360 0 0 {name=l26 sig_type=std_logic lab=CK_REF}
C {devices/lab_pin.sym} -1210 350 2 0 {name=l27 sig_type=std_logic lab=HAU}
C {devices/lab_pin.sym} -1260 310 3 0 {name=l28 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 390 1 0 {name=l29 sig_type=std_logic lab=VSS}
T {XA5} -1180 354.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 490 0 0 {name=XA6}
C {devices/lab_pin.sym} -1300 490 0 0 {name=l30 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1220 490 2 0 {name=l31 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1260 450 3 0 {name=l32 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 530 1 0 {name=l33 sig_type=std_logic lab=VSS}
T {XA6} -1180 484.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 680 0 0 {name=XA7}
C {devices/lab_pin.sym} -1300 620 0 0 {name=l34 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1300 680 0 0 {name=l35 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -1270 710 1 0 {name=l36 sig_type=std_logic lab=RN_D}
C {devices/lab_pin.sym} -1200 620 2 0 {name=l37 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -1200 680 2 0 {name=l38 sig_type=std_logic lab=DN_Q_N}
C {devices/lab_pin.sym} -1240 590 3 0 {name=l39 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 710 1 0 {name=l40 sig_type=std_logic lab=VSS}
T {XA7} -1180 674.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -1300 820 0 0 {name=XA8}
C {devices/lab_pin.sym} -1300 800 0 0 {name=l41 sig_type=std_logic lab=HD}
C {devices/lab_pin.sym} -1300 820 0 0 {name=l42 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1210 810 2 0 {name=l43 sig_type=std_logic lab=RN_D}
C {devices/lab_pin.sym} -1260 770 3 0 {name=l44 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 850 1 0 {name=l45 sig_type=std_logic lab=VSS}
T {XA8} -1180 814.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ORX1_CV.sym} -1300 960 0 0 {name=XA9}
C {devices/lab_pin.sym} -1300 940 0 0 {name=l46 sig_type=std_logic lab=HAD}
C {devices/lab_pin.sym} -1300 960 0 0 {name=l47 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -1210 950 2 0 {name=l48 sig_type=std_logic lab=HD}
C {devices/lab_pin.sym} -1260 910 3 0 {name=l49 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 990 1 0 {name=l50 sig_type=std_logic lab=VSS}
T {XA9} -1180 954.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1300 1100 0 0 {name=XA10}
C {devices/lab_pin.sym} -1300 1080 0 0 {name=l51 sig_type=std_logic lab=HD}
C {devices/lab_pin.sym} -1300 1100 0 0 {name=l52 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -1210 1090 2 0 {name=l53 sig_type=std_logic lab=HAD}
C {devices/lab_pin.sym} -1260 1050 3 0 {name=l54 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 1130 1 0 {name=l55 sig_type=std_logic lab=VSS}
T {XA10} -1180 1094.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 1230 0 0 {name=XA11}
C {devices/lab_pin.sym} -1300 1230 0 0 {name=l56 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -1220 1230 2 0 {name=l57 sig_type=std_logic lab=DN_N}
C {devices/lab_pin.sym} -1260 1190 3 0 {name=l58 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 1270 1 0 {name=l59 sig_type=std_logic lab=VSS}
T {XA11} -1180 1224.0 0 0 0.25 0.25 {}
