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
T {UP rises on CK_REF, DN on CK_FB. When both are high RST clears them; the path through the gates is the reset} -1450 -660 0 0 0.3 0.3 {}
T {pulse that keeps the dead zone away} -1450 -630 0 0 0.3 0.3 {}
T {DFRNQNX1 clocks on NAND(CK, RN): released from reset while CK is high it sees a rising edge and sets again. So} -1450 -600 0 0 0.3 0.3 {}
T {each flop's reset is HELD until its own clock is low:} -1450 -570 0 0 0.3 0.3 {}
T {HU = RST or (HU and CK_REF), RN_U = PWRUP and not HU; the same for DN on CK_FB} -1450 -540 0 0 0.3 0.3 {}
T {A: UP flop, UP latch, RST} -1360 -410 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -1300 -280 0 0 {name=XA0}
C {devices/lab_pin.sym} -1300 -300 2 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -260 3 0 {name=l2 sig_type=std_logic lab=VSS}
T {XA0} -1360 -332.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -100 0 0 {name=XA1}
C {devices/lab_pin.sym} -1300 -160 0 0 {name=l3 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1300 -100 0 0 {name=l4 sig_type=std_logic lab=CK_REF}
C {devices/lab_pin.sym} -1270 -70 0 0 {name=l5 sig_type=std_logic lab=RN_U}
C {devices/lab_pin.sym} -1200 -160 2 0 {name=l6 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1200 -100 2 0 {name=l7 sig_type=std_logic lab=UP_N}
C {devices/lab_pin.sym} -1240 -190 2 0 {name=l8 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -70 3 0 {name=l9 sig_type=std_logic lab=VSS}
T {XA1} -1360 -222.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -1300 50 0 0 {name=XA2}
C {devices/lab_pin.sym} -1300 30 0 0 {name=l10 sig_type=std_logic lab=HU}
C {devices/lab_pin.sym} -1300 50 0 0 {name=l11 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1210 40 2 0 {name=l12 sig_type=std_logic lab=RN_U}
C {devices/lab_pin.sym} -1260 0 2 0 {name=l13 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 80 2 0 {name=l14 sig_type=std_logic lab=VSS}
T {XA2} -1360 -32.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1300 200 0 0 {name=XA3}
C {devices/lab_pin.sym} -1300 180 0 0 {name=l15 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -1300 200 0 0 {name=l16 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1210 190 2 0 {name=l17 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -1260 150 2 0 {name=l18 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 230 2 0 {name=l19 sig_type=std_logic lab=VSS}
T {XA3} -1360 118.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ORX1_CV.sym} -1300 350 0 0 {name=XA4}
C {devices/lab_pin.sym} -1300 330 0 0 {name=l20 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -1300 350 0 0 {name=l21 sig_type=std_logic lab=HAU}
C {devices/lab_pin.sym} -1210 340 2 0 {name=l22 sig_type=std_logic lab=HU}
C {devices/lab_pin.sym} -1260 300 2 0 {name=l23 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 380 2 0 {name=l24 sig_type=std_logic lab=VSS}
T {XA4} -1360 268.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1300 500 0 0 {name=XA5}
C {devices/lab_pin.sym} -1300 480 0 0 {name=l25 sig_type=std_logic lab=HU}
C {devices/lab_pin.sym} -1300 500 0 0 {name=l26 sig_type=std_logic lab=CK_REF}
C {devices/lab_pin.sym} -1210 490 2 0 {name=l27 sig_type=std_logic lab=HAU}
C {devices/lab_pin.sym} -1260 450 2 0 {name=l28 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 530 2 0 {name=l29 sig_type=std_logic lab=VSS}
T {XA5} -1360 418.0 0 0 0.25 0.25 {}
T {B: DN flop, DN latch, DN_N, PWRUP_N} -880 -410 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -820 -280 0 0 {name=XB0}
C {devices/lab_pin.sym} -820 -300 2 0 {name=l30 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -820 -260 3 0 {name=l31 sig_type=std_logic lab=VSS}
T {XB0} -880 -332.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -820 -100 0 0 {name=XB1}
C {devices/lab_pin.sym} -820 -160 0 0 {name=l32 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -820 -100 0 0 {name=l33 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -790 -70 0 0 {name=l34 sig_type=std_logic lab=RN_D}
C {devices/lab_pin.sym} -720 -160 2 0 {name=l35 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -720 -100 2 0 {name=l36 sig_type=std_logic lab=DN_Q_N}
C {devices/lab_pin.sym} -760 -190 2 0 {name=l37 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -760 -70 3 0 {name=l38 sig_type=std_logic lab=VSS}
T {XB1} -880 -222.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -820 50 0 0 {name=XB2}
C {devices/lab_pin.sym} -820 30 0 0 {name=l39 sig_type=std_logic lab=HD}
C {devices/lab_pin.sym} -820 50 0 0 {name=l40 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -730 40 2 0 {name=l41 sig_type=std_logic lab=RN_D}
C {devices/lab_pin.sym} -780 0 2 0 {name=l42 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 80 2 0 {name=l43 sig_type=std_logic lab=VSS}
T {XB2} -880 -32.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -820 190 0 0 {name=XB3}
C {devices/lab_pin.sym} -820 190 0 0 {name=l44 sig_type=std_logic lab=DN}
C {devices/lab_pin.sym} -740 190 2 0 {name=l45 sig_type=std_logic lab=DN_N}
C {devices/lab_pin.sym} -780 150 2 0 {name=l46 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 230 2 0 {name=l47 sig_type=std_logic lab=VSS}
T {XB3} -880 118.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -820 340 0 0 {name=XB4}
C {devices/lab_pin.sym} -820 340 0 0 {name=l48 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -740 340 2 0 {name=l49 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -780 300 2 0 {name=l50 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 380 2 0 {name=l51 sig_type=std_logic lab=VSS}
T {XB4} -880 268.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ORX1_CV.sym} -820 500 0 0 {name=XB5}
C {devices/lab_pin.sym} -820 480 0 0 {name=l52 sig_type=std_logic lab=HAD}
C {devices/lab_pin.sym} -820 500 0 0 {name=l53 sig_type=std_logic lab=RST}
C {devices/lab_pin.sym} -730 490 2 0 {name=l54 sig_type=std_logic lab=HD}
C {devices/lab_pin.sym} -780 450 2 0 {name=l55 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 530 2 0 {name=l56 sig_type=std_logic lab=VSS}
T {XB5} -880 418.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -820 650 0 0 {name=XB6}
C {devices/lab_pin.sym} -820 630 0 0 {name=l57 sig_type=std_logic lab=HD}
C {devices/lab_pin.sym} -820 650 0 0 {name=l58 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -730 640 2 0 {name=l59 sig_type=std_logic lab=HAD}
C {devices/lab_pin.sym} -780 600 2 0 {name=l60 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 680 2 0 {name=l61 sig_type=std_logic lab=VSS}
T {XB6} -880 568.0 0 0 0.25 0.25 {}
P 4 5 -1520 -860 -340 -860 -340 740 -1520 740 -1520 -860 {dash=4}
