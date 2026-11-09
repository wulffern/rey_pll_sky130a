v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_ROSC: current starved ring oscillator. TRIM sets the bias (coarse), VCTRL steers part of each stage's current (f falls as VCTRL rises)} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=TRIM0}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=TRIM1}
C {devices/ipin.sym} -760 -740 0 0 {name=p4 lab=TRIM2}
C {devices/ipin.sym} -600 -740 0 0 {name=p5 lab=VCTRL}
C {devices/opin.sym} -440 -740 0 0 {name=p6 lab=CK}
C {devices/opin.sym} -280 -740 0 0 {name=p7 lab=VBP}
T {Bias: I = Vgs(MN1) / R, its own cell} -1450 -620 0 0 0.4 0.4 {}
C {REY_PLL_SKY130A/REY_PLL_ROSC_BIAS.sym} -1100 -350 0 0 {name=xbias}
C {devices/lab_pin.sym} -1250 -440 0 0 {name=l52 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1250 -420 0 0 {name=l53 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1250 -400 0 0 {name=l54 sig_type=std_logic lab=TRIM0}
C {devices/lab_pin.sym} -1250 -380 0 0 {name=l55 sig_type=std_logic lab=TRIM1}
C {devices/lab_pin.sym} -1250 -360 0 0 {name=l56 sig_type=std_logic lab=TRIM2}
C {devices/lab_pin.sym} -950 -440 2 0 {name=l57 sig_type=std_logic lab=VBP}
T {Ring: 7 stages of REY_PLL_ROSC_STAGE} 100 -620 0 0 0.4 0.4 {}
C {REY_PLL_SKY130A/REY_PLL_ROSC_STAGE.sym} 400 -350 0 0 {name=xstg[6:0]}
C {devices/lab_pin.sym} 250 -440 0 0 {name=l76 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 250 -420 0 0 {name=l77 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 250 -400 0 0 {name=l78 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 250 -380 0 0 {name=l79 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} 250 -360 0 0 {name=l80 sig_type=std_logic lab=N5,N4,N3,N2,N1,N0,N6}
C {devices/lab_pin.sym} 550 -440 2 0 {name=l81 sig_type=std_logic lab=N6,N5,N4,N3,N2,N1,N0}
T {stage k: N<k-1> -> N<k>} 100 -60 0 0 0.3 0.3 {}
T {Output buffer} 1370 -620 0 0 0.4 0.4 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} 1370 -170 0 0 {name=xo0}
C {devices/lab_pin.sym} 1410 -210 3 0 {name=l82 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1410 -130 1 0 {name=l83 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1370 -170 0 0 {name=l84 sig_type=std_logic lab=N6}
N 1450 -170 1510 -170 {}
N 1510 -170 1570 -170 {}
C {devices/lab_pin.sym} 1510 -170 3 0 {name=l85 sig_type=std_logic lab=CKN}
C {REY_TR_SKY130A/REYTR_IVX4_CV.sym} 1570 -170 0 0 {name=xo1}
C {devices/lab_pin.sym} 1610 -210 3 0 {name=l86 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1610 -130 1 0 {name=l87 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1650 -170 2 0 {name=l88 sig_type=std_logic lab=CK}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} 1790 -170 0 0 {name=xotap}
C {devices/lab_pin.sym} 1790 -190 3 0 {name=l89 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1790 -150 1 0 {name=l90 sig_type=std_logic lab=VSS}
