v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_DIVN: 10 flop ripple divider, CK/64 to the PFD} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=PWRUP_1V8}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=CK}
C {devices/opin.sym} -760 -740 0 0 {name=p4 lab=CK_FB}
C {devices/opin.sym} -600 -740 0 0 {name=p5 lab=CKO0}
C {devices/opin.sym} -440 -740 0 0 {name=p6 lab=CKO1}
C {devices/opin.sym} -280 -740 0 0 {name=p7 lab=CKO2}
C {devices/opin.sym} -120 -740 0 0 {name=p8 lab=CKO3}
C {devices/opin.sym} 40 -740 0 0 {name=p9 lab=CKO4}
C {devices/opin.sym} 200 -740 0 0 {name=p10 lab=CKO5}
C {devices/opin.sym} 360 -740 0 0 {name=p11 lab=CKO6}
C {devices/opin.sym} 520 -740 0 0 {name=p12 lab=CKO7}
T {Flop k divides the previous one by two: Q<k> is CK/2^(k+1). Q5 is CK_FB} -1450 -640 0 0 0.3 0.3 {}
C {REY_TR_SKY130A/REYTR_DFRNQNX1_CV.sym} -1300 -400 0 0 {name=xdf[9:0]}
C {devices/lab_pin.sym} -1300 -460 0 0 {name=l1 sig_type=std_logic lab=QN9,QN8,QN7,QN6,QN5,QN4,QN3,QN2,QN1,QN0}
C {devices/lab_pin.sym} -1300 -400 0 0 {name=l2 sig_type=std_logic lab=Q8,Q7,Q6,CK_FB,Q4,Q3,Q2,Q1,Q0,CK}
C {devices/lab_pin.sym} -1270 -370 1 0 {name=l3 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1200 -460 2 0 {name=l4 sig_type=std_logic lab=Q9,Q8,Q7,Q6,CK_FB,Q4,Q3,Q2,Q1,Q0}
C {devices/lab_pin.sym} -1200 -400 2 0 {name=l5 sig_type=std_logic lab=QN9,QN8,QN7,QN6,QN5,QN4,QN3,QN2,QN1,QN0}
C {devices/lab_pin.sym} -1240 -490 3 0 {name=l6 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1240 -370 1 0 {name=l7 sig_type=std_logic lab=VSS}
T {Output buffers, one per tap so the pins do not load the chain: CKO<k> = Q<k+2>, CK/8 .. CK/1024} -1000 -540 0 0 0.3 0.3 {}
C {REY_TR_SKY130A/REYTR_BFX1_CV.sym} -900 -400 0 0 {name=xbo[7:0]}
C {devices/lab_pin.sym} -900 -400 0 0 {name=l8 sig_type=std_logic lab=Q9,Q8,Q7,Q6,CK_FB,Q4,Q3,Q2}
C {devices/lab_pin.sym} -820 -400 2 0 {name=l9 sig_type=std_logic lab=CKO7,CKO6,CKO5,CKO4,CKO3,CKO2,CKO1,CKO0}
C {devices/lab_pin.sym} -860 -440 3 0 {name=l10 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -860 -360 1 0 {name=l11 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -600 -400 0 0 {name=xtap[1:0]}
C {devices/lab_pin.sym} -600 -420 3 0 {name=l12 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -600 -380 1 0 {name=l13 sig_type=std_logic lab=VSS}
