v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_DIVN: 10 flop ripple divider, CK/64 to the PFD} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=CK}
C {devices/opin.sym} -920 -740 0 0 {name=p3 lab=CK_FB}
C {devices/opin.sym} -760 -740 0 0 {name=p4 lab=CKO0}
C {devices/opin.sym} -600 -740 0 0 {name=p5 lab=CKO1}
C {devices/opin.sym} -440 -740 0 0 {name=p6 lab=CKO2}
C {devices/opin.sym} -280 -740 0 0 {name=p7 lab=CKO3}
C {devices/opin.sym} -120 -740 0 0 {name=p8 lab=CKO4}
C {devices/opin.sym} 40 -740 0 0 {name=p9 lab=CKO5}
C {devices/opin.sym} 200 -740 0 0 {name=p10 lab=CKO6}
C {devices/opin.sym} 360 -740 0 0 {name=p11 lab=CKO7}
T {Flop k divides the previous one by two: Q<k> is CK/2^(k+1), D = QN<k>. Q5 is CK_FB. No reset: a ripple divider runs from any state} -1450 -660 0 0 0.3 0.3 {}
T {Each tap has its buffer over its flop, so the pins do not load the chain: CKO<t> = Q<t+2>, CK/8 .. CK/1024} -1450 -630 0 0 0.3 0.3 {}
T {A: stages 0 and 1} -1360 -500 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -1300 -400 0 0 {name=XA0}
C {devices/lab_pin.sym} -1300 -420 3 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -380 1 0 {name=l2 sig_type=std_logic lab=VSS}
T {XA0} -1180 -406.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -230 0 0 {name=XA1}
C {devices/lab_pin.sym} -1300 -290 0 0 {name=l3 sig_type=std_logic lab=QN0}
C {devices/lab_pin.sym} -1300 -230 0 0 {name=l4 sig_type=std_logic lab=CK}
C {devices/lab_pin.sym} -1270 -200 1 0 {name=l5 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1200 -290 2 0 {name=l6 sig_type=std_logic lab=Q0}
C {devices/lab_pin.sym} -1200 -230 2 0 {name=l7 sig_type=std_logic lab=QN0}
C {devices/lab_pin.sym} -1240 -320 3 0 {name=l8 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -200 1 0 {name=l9 sig_type=std_logic lab=VSS}
T {XA1} -1180 -236.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -50 0 0 {name=XA2}
C {devices/lab_pin.sym} -1300 -110 0 0 {name=l10 sig_type=std_logic lab=QN1}
C {devices/lab_pin.sym} -1300 -50 0 0 {name=l11 sig_type=std_logic lab=Q0}
C {devices/lab_pin.sym} -1270 -20 1 0 {name=l12 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1200 -110 2 0 {name=l13 sig_type=std_logic lab=Q1}
C {devices/lab_pin.sym} -1200 -50 2 0 {name=l14 sig_type=std_logic lab=QN1}
C {devices/lab_pin.sym} -1240 -140 3 0 {name=l15 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -20 1 0 {name=l16 sig_type=std_logic lab=VSS}
T {XA2} -1180 -56.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 80 0 0 {name=XA3}
C {devices/lab_pin.sym} -1300 80 0 0 {name=l17 sig_type=std_logic lab=Q1}
C {devices/lab_pin.sym} -1220 80 2 0 {name=l18 sig_type=std_logic lab=Q1X}
C {devices/lab_pin.sym} -1260 40 3 0 {name=l19 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 120 1 0 {name=l20 sig_type=std_logic lab=VSS}
T {XA3} -1180 74.0 0 0 0.25 0.25 {}
T {B: stages 2 and 3} -880 -500 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -820 -400 0 0 {name=XB0}
C {devices/lab_pin.sym} -820 -420 3 0 {name=l21 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -820 -380 1 0 {name=l22 sig_type=std_logic lab=VSS}
T {XB0} -700 -406.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -820 -230 0 0 {name=XB1}
C {devices/lab_pin.sym} -820 -290 0 0 {name=l23 sig_type=std_logic lab=QN2}
C {devices/lab_pin.sym} -820 -230 0 0 {name=l24 sig_type=std_logic lab=Q1}
C {devices/lab_pin.sym} -790 -200 1 0 {name=l25 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -720 -290 2 0 {name=l26 sig_type=std_logic lab=Q2}
C {devices/lab_pin.sym} -720 -230 2 0 {name=l27 sig_type=std_logic lab=QN2}
C {devices/lab_pin.sym} -760 -320 3 0 {name=l28 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -760 -200 1 0 {name=l29 sig_type=std_logic lab=VSS}
T {XB1} -700 -236.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -820 -100 0 0 {name=XB2}
C {devices/lab_pin.sym} -820 -100 0 0 {name=l30 sig_type=std_logic lab=Q2}
C {devices/lab_pin.sym} -740 -100 2 0 {name=l31 sig_type=std_logic lab=CKO0}
C {devices/lab_pin.sym} -780 -140 3 0 {name=l32 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 -60 1 0 {name=l33 sig_type=std_logic lab=VSS}
T {XB2} -700 -106.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -820 90 0 0 {name=XB3}
C {devices/lab_pin.sym} -820 30 0 0 {name=l34 sig_type=std_logic lab=QN3}
C {devices/lab_pin.sym} -820 90 0 0 {name=l35 sig_type=std_logic lab=Q2}
C {devices/lab_pin.sym} -790 120 1 0 {name=l36 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -720 30 2 0 {name=l37 sig_type=std_logic lab=Q3}
C {devices/lab_pin.sym} -720 90 2 0 {name=l38 sig_type=std_logic lab=QN3}
C {devices/lab_pin.sym} -760 0 3 0 {name=l39 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -760 120 1 0 {name=l40 sig_type=std_logic lab=VSS}
T {XB3} -700 84.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -820 220 0 0 {name=XB4}
C {devices/lab_pin.sym} -820 220 0 0 {name=l41 sig_type=std_logic lab=Q3}
C {devices/lab_pin.sym} -740 220 2 0 {name=l42 sig_type=std_logic lab=CKO1}
C {devices/lab_pin.sym} -780 180 3 0 {name=l43 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -780 260 1 0 {name=l44 sig_type=std_logic lab=VSS}
T {XB4} -700 214.0 0 0 0.25 0.25 {}
T {C: stages 4 and 5} -400 -500 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -340 -400 0 0 {name=XC0}
C {devices/lab_pin.sym} -340 -420 3 0 {name=l45 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -340 -380 1 0 {name=l46 sig_type=std_logic lab=VSS}
T {XC0} -220 -406.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -340 -230 0 0 {name=XC1}
C {devices/lab_pin.sym} -340 -290 0 0 {name=l47 sig_type=std_logic lab=QN4}
C {devices/lab_pin.sym} -340 -230 0 0 {name=l48 sig_type=std_logic lab=Q3}
C {devices/lab_pin.sym} -310 -200 1 0 {name=l49 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -240 -290 2 0 {name=l50 sig_type=std_logic lab=Q4}
C {devices/lab_pin.sym} -240 -230 2 0 {name=l51 sig_type=std_logic lab=QN4}
C {devices/lab_pin.sym} -280 -320 3 0 {name=l52 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -280 -200 1 0 {name=l53 sig_type=std_logic lab=VSS}
T {XC1} -220 -236.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -340 -100 0 0 {name=XC2}
C {devices/lab_pin.sym} -340 -100 0 0 {name=l54 sig_type=std_logic lab=Q4}
C {devices/lab_pin.sym} -260 -100 2 0 {name=l55 sig_type=std_logic lab=CKO2}
C {devices/lab_pin.sym} -300 -140 3 0 {name=l56 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -300 -60 1 0 {name=l57 sig_type=std_logic lab=VSS}
T {XC2} -220 -106.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -340 90 0 0 {name=XC3}
C {devices/lab_pin.sym} -340 30 0 0 {name=l58 sig_type=std_logic lab=QN5}
C {devices/lab_pin.sym} -340 90 0 0 {name=l59 sig_type=std_logic lab=Q4}
C {devices/lab_pin.sym} -310 120 1 0 {name=l60 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -240 30 2 0 {name=l61 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -240 90 2 0 {name=l62 sig_type=std_logic lab=QN5}
C {devices/lab_pin.sym} -280 0 3 0 {name=l63 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -280 120 1 0 {name=l64 sig_type=std_logic lab=VSS}
T {XC3} -220 84.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -340 220 0 0 {name=XC4}
C {devices/lab_pin.sym} -340 220 0 0 {name=l65 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -260 220 2 0 {name=l66 sig_type=std_logic lab=CKO3}
C {devices/lab_pin.sym} -300 180 3 0 {name=l67 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -300 260 1 0 {name=l68 sig_type=std_logic lab=VSS}
T {XC4} -220 214.0 0 0 0.25 0.25 {}
T {D: stages 6 and 7} 80 -500 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} 140 -400 0 0 {name=XD0}
C {devices/lab_pin.sym} 140 -420 3 0 {name=l69 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 140 -380 1 0 {name=l70 sig_type=std_logic lab=VSS}
T {XD0} 260 -406.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} 140 -230 0 0 {name=XD1}
C {devices/lab_pin.sym} 140 -290 0 0 {name=l71 sig_type=std_logic lab=QN6}
C {devices/lab_pin.sym} 140 -230 0 0 {name=l72 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} 170 -200 1 0 {name=l73 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 240 -290 2 0 {name=l74 sig_type=std_logic lab=Q6}
C {devices/lab_pin.sym} 240 -230 2 0 {name=l75 sig_type=std_logic lab=QN6}
C {devices/lab_pin.sym} 200 -320 3 0 {name=l76 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 200 -200 1 0 {name=l77 sig_type=std_logic lab=VSS}
T {XD1} 260 -236.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} 140 -100 0 0 {name=XD2}
C {devices/lab_pin.sym} 140 -100 0 0 {name=l78 sig_type=std_logic lab=Q6}
C {devices/lab_pin.sym} 220 -100 2 0 {name=l79 sig_type=std_logic lab=CKO4}
C {devices/lab_pin.sym} 180 -140 3 0 {name=l80 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 180 -60 1 0 {name=l81 sig_type=std_logic lab=VSS}
T {XD2} 260 -106.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} 140 90 0 0 {name=XD3}
C {devices/lab_pin.sym} 140 30 0 0 {name=l82 sig_type=std_logic lab=QN7}
C {devices/lab_pin.sym} 140 90 0 0 {name=l83 sig_type=std_logic lab=Q6}
C {devices/lab_pin.sym} 170 120 1 0 {name=l84 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 240 30 2 0 {name=l85 sig_type=std_logic lab=Q7}
C {devices/lab_pin.sym} 240 90 2 0 {name=l86 sig_type=std_logic lab=QN7}
C {devices/lab_pin.sym} 200 0 3 0 {name=l87 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 200 120 1 0 {name=l88 sig_type=std_logic lab=VSS}
T {XD3} 260 84.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} 140 220 0 0 {name=XD4}
C {devices/lab_pin.sym} 140 220 0 0 {name=l89 sig_type=std_logic lab=Q7}
C {devices/lab_pin.sym} 220 220 2 0 {name=l90 sig_type=std_logic lab=CKO5}
C {devices/lab_pin.sym} 180 180 3 0 {name=l91 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 180 260 1 0 {name=l92 sig_type=std_logic lab=VSS}
T {XD4} 260 214.0 0 0 0.25 0.25 {}
T {E: stages 8 and 9} 560 -500 0 0 0.35 0.35 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} 620 -400 0 0 {name=XE0}
C {devices/lab_pin.sym} 620 -420 3 0 {name=l93 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 620 -380 1 0 {name=l94 sig_type=std_logic lab=VSS}
T {XE0} 740 -406.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} 620 -230 0 0 {name=XE1}
C {devices/lab_pin.sym} 620 -290 0 0 {name=l95 sig_type=std_logic lab=QN8}
C {devices/lab_pin.sym} 620 -230 0 0 {name=l96 sig_type=std_logic lab=Q7}
C {devices/lab_pin.sym} 650 -200 1 0 {name=l97 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 720 -290 2 0 {name=l98 sig_type=std_logic lab=Q8}
C {devices/lab_pin.sym} 720 -230 2 0 {name=l99 sig_type=std_logic lab=QN8}
C {devices/lab_pin.sym} 680 -320 3 0 {name=l100 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 680 -200 1 0 {name=l101 sig_type=std_logic lab=VSS}
T {XE1} 740 -236.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} 620 -100 0 0 {name=XE2}
C {devices/lab_pin.sym} 620 -100 0 0 {name=l102 sig_type=std_logic lab=Q8}
C {devices/lab_pin.sym} 700 -100 2 0 {name=l103 sig_type=std_logic lab=CKO6}
C {devices/lab_pin.sym} 660 -140 3 0 {name=l104 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 660 -60 1 0 {name=l105 sig_type=std_logic lab=VSS}
T {XE2} 740 -106.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} 620 90 0 0 {name=XE3}
C {devices/lab_pin.sym} 620 30 0 0 {name=l106 sig_type=std_logic lab=QN9}
C {devices/lab_pin.sym} 620 90 0 0 {name=l107 sig_type=std_logic lab=Q8}
C {devices/lab_pin.sym} 650 120 1 0 {name=l108 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 720 30 2 0 {name=l109 sig_type=std_logic lab=Q9}
C {devices/lab_pin.sym} 720 90 2 0 {name=l110 sig_type=std_logic lab=QN9}
C {devices/lab_pin.sym} 680 0 3 0 {name=l111 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 680 120 1 0 {name=l112 sig_type=std_logic lab=VSS}
T {XE3} 740 84.0 0 0 0.25 0.25 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} 620 220 0 0 {name=XE4}
C {devices/lab_pin.sym} 620 220 0 0 {name=l113 sig_type=std_logic lab=Q9}
C {devices/lab_pin.sym} 700 220 2 0 {name=l114 sig_type=std_logic lab=CKO7}
C {devices/lab_pin.sym} 660 180 3 0 {name=l115 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 660 260 1 0 {name=l116 sig_type=std_logic lab=VSS}
T {XE4} 740 214.0 0 0 0.25 0.25 {}
