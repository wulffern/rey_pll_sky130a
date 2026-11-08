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
T {UP rises on CK_REF, DN on CK_FB. When both are high RST clears them; the path through the gates is the reset pulse that keeps the dead zone away} -1450 -640 0 0 0.3 0.3 {}
T {DFRNQNX1 clocks on NAND(CK, RN): released from reset while CK is high it sees a rising edge and sets again. So each flop's reset is HELD until its own clock is low:} -1450 -610 0 0 0.3 0.3 {}
T {HU = RST or (HU and CK_REF), RN_U = PWRUP and not HU; the same for DN on CK_FB} -1450 -580 0 0 0.3 0.3 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -380 0 0 {name=xdu}
C {devices/lab_pin.sym} -1300 -440 0 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -380 0 0 {name=l2 sig_type=std_logic lab=CK_REF}
C {devices/lab_pin.sym} -1270 -350 1 0 {name=l3 sig_type=std_logic lab=RN_U}
C {devices/lab_pin.sym} -1200 -440 2 0 {name=l4 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1200 -380 2 0 {name=l5 sig_type=std_logic lab=UP_N}
C {devices/lab_pin.sym} -1240 -470 3 0 {name=l6 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -350 1 0 {name=l7 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -150 0 0 {name=xdd}
C {devices/lab_pin.sym} -1300 -210 0 0 {name=l8 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -150 0 0 {name=l9 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -1270 -120 1 0 {name=l10 sig_type=std_logic lab=RN_D}
C {devices/lab_pin.sym} -1200 -210 2 0 {name=l11 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -1200 -150 2 0 {name=l12 sig_type=std_logic lab=DN_N}
C {devices/lab_pin.sym} -1240 -240 3 0 {name=l13 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -120 1 0 {name=l14 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1050 -250 0 0 {name=xr0}
C {devices/lab_pin.sym} -1050 -270 0 0 {name=l15 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1050 -250 0 0 {name=l16 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -960 -260 2 0 {name=l17 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -1010 -300 3 0 {name=l18 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1010 -220 1 0 {name=l19 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1050 -100 0 0 {name=xr1}
C {devices/lab_pin.sym} -1050 -100 0 0 {name=l20 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -970 -100 2 0 {name=l21 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1010 -140 3 0 {name=l22 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1010 -60 1 0 {name=l23 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -800 -400 0 0 {name=xhua}
C {devices/lab_pin.sym} -800 -420 0 0 {name=l24 sig_type=std_logic lab=HU}
C {devices/lab_pin.sym} -800 -400 0 0 {name=l25 sig_type=std_logic lab=CK_REF}
C {devices/lab_pin.sym} -760 -450 3 0 {name=l26 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -760 -370 1 0 {name=l27 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_ORX1_CV.sym} -630 -390 0 0 {name=xhuo}
C {devices/lab_pin.sym} -630 -390 0 0 {name=l28 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -590 -440 3 0 {name=l29 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -590 -360 1 0 {name=l30 sig_type=std_logic lab=VSS}
N -710 -410 -670 -410 {}
N -670 -410 -630 -410 {}
C {devices/lab_pin.sym} -670 -410 3 0 {name=l31 sig_type=std_logic lab=HAU}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -460 -380 0 0 {name=xhun}
C {devices/lab_pin.sym} -460 -380 0 0 {name=l32 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -370 -390 2 0 {name=l33 sig_type=std_logic lab=RN_U}
C {devices/lab_pin.sym} -420 -430 3 0 {name=l34 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -420 -350 1 0 {name=l35 sig_type=std_logic lab=VSS}
N -540 -400 -500 -400 {}
N -500 -400 -460 -400 {}
C {devices/lab_pin.sym} -500 -400 3 0 {name=l36 sig_type=std_logic lab=HU}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -800 -170 0 0 {name=xhda}
C {devices/lab_pin.sym} -800 -190 0 0 {name=l37 sig_type=std_logic lab=HD}
C {devices/lab_pin.sym} -800 -170 0 0 {name=l38 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -760 -220 3 0 {name=l39 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -760 -140 1 0 {name=l40 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_ORX1_CV.sym} -630 -160 0 0 {name=xhdo}
C {devices/lab_pin.sym} -630 -160 0 0 {name=l41 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -590 -210 3 0 {name=l42 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -590 -130 1 0 {name=l43 sig_type=std_logic lab=VSS}
N -710 -180 -670 -180 {}
N -670 -180 -630 -180 {}
C {devices/lab_pin.sym} -670 -180 3 0 {name=l44 sig_type=std_logic lab=HAD}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -460 -150 0 0 {name=xhdn}
C {devices/lab_pin.sym} -460 -150 0 0 {name=l45 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -370 -160 2 0 {name=l46 sig_type=std_logic lab=RN_D}
C {devices/lab_pin.sym} -420 -200 3 0 {name=l47 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -420 -120 1 0 {name=l48 sig_type=std_logic lab=VSS}
N -540 -170 -500 -170 {}
N -500 -170 -460 -170 {}
C {devices/lab_pin.sym} -500 -170 3 0 {name=l49 sig_type=std_logic lab=HD}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -250 -250 0 0 {name=xtap[1:0]}
C {devices/lab_pin.sym} -250 -270 3 0 {name=l50 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -250 -230 1 0 {name=l51 sig_type=std_logic lab=VSS}
