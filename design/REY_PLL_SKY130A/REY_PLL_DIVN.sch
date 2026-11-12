v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_DIVN: 6 flop ripple divider, CK/16 to the PFD} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=CK}
C {devices/opin.sym} -920 -740 0 0 {name=p3 lab=CK_FB}
C {devices/opin.sym} -760 -740 0 0 {name=p4 lab=CKO0}
C {devices/opin.sym} -600 -740 0 0 {name=p5 lab=CKO1}
C {devices/opin.sym} -440 -740 0 0 {name=p6 lab=CKO2}
C {devices/opin.sym} -280 -740 0 0 {name=p7 lab=CKO3}
T {Flop k divides the previous one by two: Q<k> is CK/2^(k+1), D = QN<k>. Q3 is CK_FB. No reset: a ripple divider} -1450 -660 0 0 0.3 0.3 {}
T {runs from any state} -1450 -630 0 0 0.3 0.3 {}
T {Each tap has its buffer over its flop, so the pins do not load the chain: CKO<t> = Q<t+2>, CK/8 .. CK/64} -1450 -600 0 0 0.3 0.3 {}
T {A: stages 0 and 1} -1360 -470 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -1300 -340 0 0 {name=XA0}
C {devices/lab_pin.sym} -1300 -360 2 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -320 3 0 {name=l2 sig_type=std_logic lab=VSS}
T {XA0} -1360 -392.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -160 0 0 {name=XA1}
C {devices/lab_pin.sym} -1300 -220 0 0 {name=l3 sig_type=std_logic lab=QN0}
C {devices/lab_pin.sym} -1300 -160 0 0 {name=l4 sig_type=std_logic lab=CK}
C {devices/lab_pin.sym} -1270 -130 0 0 {name=l5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1200 -220 2 0 {name=l6 sig_type=std_logic lab=Q0}
C {devices/lab_pin.sym} -1200 -160 2 0 {name=l7 sig_type=std_logic lab=QN0}
C {devices/lab_pin.sym} -1240 -250 2 0 {name=l8 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -130 3 0 {name=l9 sig_type=std_logic lab=VSS}
T {XA1} -1360 -282.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 30 0 0 {name=XA2}
C {devices/lab_pin.sym} -1300 -30 0 0 {name=l10 sig_type=std_logic lab=QN1}
C {devices/lab_pin.sym} -1300 30 0 0 {name=l11 sig_type=std_logic lab=Q0}
C {devices/lab_pin.sym} -1270 60 0 0 {name=l12 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1200 -30 2 0 {name=l13 sig_type=std_logic lab=Q1}
C {devices/lab_pin.sym} -1200 30 2 0 {name=l14 sig_type=std_logic lab=QN1}
C {devices/lab_pin.sym} -1240 -60 2 0 {name=l15 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 60 3 0 {name=l16 sig_type=std_logic lab=VSS}
T {XA2} -1360 -92.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 170 0 0 {name=XA3}
C {devices/lab_pin.sym} -1300 170 0 0 {name=l17 sig_type=std_logic lab=Q1}
C {devices/lab_pin.sym} -1220 170 2 0 {name=l18 sig_type=std_logic lab=Q1X}
C {devices/lab_pin.sym} -1260 130 2 0 {name=l19 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 210 2 0 {name=l20 sig_type=std_logic lab=VSS}
T {XA3} -1360 98.0 0 0 0.25 0.25 {}
T {B: stages 2 and 3} -880 -470 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -820 -340 0 0 {name=XB0}
C {devices/lab_pin.sym} -820 -360 2 0 {name=l21 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -820 -320 3 0 {name=l22 sig_type=std_logic lab=VSS}
T {XB0} -880 -392.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -820 -160 0 0 {name=XB1}
C {devices/lab_pin.sym} -820 -220 0 0 {name=l23 sig_type=std_logic lab=QN2}
C {devices/lab_pin.sym} -820 -160 0 0 {name=l24 sig_type=std_logic lab=Q1}
C {devices/lab_pin.sym} -790 -130 0 0 {name=l25 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -720 -220 2 0 {name=l26 sig_type=std_logic lab=Q2}
C {devices/lab_pin.sym} -720 -160 2 0 {name=l27 sig_type=std_logic lab=QN2}
C {devices/lab_pin.sym} -760 -250 2 0 {name=l28 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -760 -130 3 0 {name=l29 sig_type=std_logic lab=VSS}
T {XB1} -880 -282.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -820 -20 0 0 {name=XB2}
C {devices/lab_pin.sym} -820 -20 0 0 {name=l30 sig_type=std_logic lab=Q2}
C {devices/lab_pin.sym} -740 -20 2 0 {name=l31 sig_type=std_logic lab=CKO0}
C {devices/lab_pin.sym} -780 -60 2 0 {name=l32 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 20 2 0 {name=l33 sig_type=std_logic lab=VSS}
T {XB2} -880 -92.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -820 180 0 0 {name=XB3}
C {devices/lab_pin.sym} -820 120 0 0 {name=l34 sig_type=std_logic lab=QN3}
C {devices/lab_pin.sym} -820 180 0 0 {name=l35 sig_type=std_logic lab=Q2}
C {devices/lab_pin.sym} -790 210 0 0 {name=l36 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -720 120 2 0 {name=l37 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -720 180 2 0 {name=l38 sig_type=std_logic lab=QN3}
C {devices/lab_pin.sym} -760 90 2 0 {name=l39 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -760 210 3 0 {name=l40 sig_type=std_logic lab=VSS}
T {XB3} -880 58.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -820 320 0 0 {name=XB4}
C {devices/lab_pin.sym} -820 320 0 0 {name=l41 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -740 320 2 0 {name=l42 sig_type=std_logic lab=CKO1}
C {devices/lab_pin.sym} -780 280 2 0 {name=l43 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 360 2 0 {name=l44 sig_type=std_logic lab=VSS}
T {XB4} -880 248.0 0 0 0.25 0.25 {}
T {C: stages 4 and 5} -400 -470 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -340 -340 0 0 {name=XC0}
C {devices/lab_pin.sym} -340 -360 2 0 {name=l45 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -340 -320 3 0 {name=l46 sig_type=std_logic lab=VSS}
T {XC0} -400 -392.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -340 -160 0 0 {name=XC1}
C {devices/lab_pin.sym} -340 -220 0 0 {name=l47 sig_type=std_logic lab=QN4}
C {devices/lab_pin.sym} -340 -160 0 0 {name=l48 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -310 -130 0 0 {name=l49 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -240 -220 2 0 {name=l50 sig_type=std_logic lab=Q4}
C {devices/lab_pin.sym} -240 -160 2 0 {name=l51 sig_type=std_logic lab=QN4}
C {devices/lab_pin.sym} -280 -250 2 0 {name=l52 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -280 -130 3 0 {name=l53 sig_type=std_logic lab=VSS}
T {XC1} -400 -282.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -340 -20 0 0 {name=XC2}
C {devices/lab_pin.sym} -340 -20 0 0 {name=l54 sig_type=std_logic lab=Q4}
C {devices/lab_pin.sym} -260 -20 2 0 {name=l55 sig_type=std_logic lab=CKO2}
C {devices/lab_pin.sym} -300 -60 2 0 {name=l56 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -300 20 2 0 {name=l57 sig_type=std_logic lab=VSS}
T {XC2} -400 -92.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -340 180 0 0 {name=XC3}
C {devices/lab_pin.sym} -340 120 0 0 {name=l58 sig_type=std_logic lab=QN5}
C {devices/lab_pin.sym} -340 180 0 0 {name=l59 sig_type=std_logic lab=Q4}
C {devices/lab_pin.sym} -310 210 0 0 {name=l60 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -240 120 2 0 {name=l61 sig_type=std_logic lab=Q5}
C {devices/lab_pin.sym} -240 180 2 0 {name=l62 sig_type=std_logic lab=QN5}
C {devices/lab_pin.sym} -280 90 2 0 {name=l63 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -280 210 3 0 {name=l64 sig_type=std_logic lab=VSS}
T {XC3} -400 58.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -340 320 0 0 {name=XC4}
C {devices/lab_pin.sym} -340 320 0 0 {name=l65 sig_type=std_logic lab=Q5}
C {devices/lab_pin.sym} -260 320 2 0 {name=l66 sig_type=std_logic lab=CKO3}
C {devices/lab_pin.sym} -300 280 2 0 {name=l67 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -300 360 2 0 {name=l68 sig_type=std_logic lab=VSS}
T {XC4} -400 248.0 0 0 0.25 0.25 {}
P 4 5 -1520 -860 -150 -860 -150 420 -1520 420 -1520 -860 {dash=4}
