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
T {Bias: I = Vgs(MN1) / R} -1450 -620 0 0 0.4 0.4 {}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} -1200 -500 0 0 {name=xmpd[3:0]}
C {devices/lab_pin.sym} -1160 -530 3 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1160 -500 2 0 {name=l2 sig_type=std_logic lab=VDD_1V8}
N -1160 -470 -1160 -440 {}
N -1160 -440 -1230 -440 {}
N -1230 -440 -1230 -500 {}
N -1230 -500 -1200 -500 {}
C {devices/lab_pin.sym} -1230 -500 0 0 {name=l3 sig_type=std_logic lab=VBP}
C {REY_ATR_SKY130A/REYATR_LVT_NCH_2C5F0.sym} -1200 -350 0 0 {name=xmn2[3:0]}
C {devices/lab_pin.sym} -1200 -350 0 0 {name=l4 sig_type=std_logic lab=VX}
C {devices/lab_pin.sym} -1160 -320 1 0 {name=l5 sig_type=std_logic lab=VG}
C {devices/lab_pin.sym} -1160 -350 2 0 {name=l6 sig_type=std_logic lab=VSS}
N -1160 -440 -1160 -380 {}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} -950 -500 0 0 {name=xmpb[3:0]}
C {devices/lab_pin.sym} -950 -500 0 0 {name=l7 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -910 -530 3 0 {name=l8 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -910 -500 2 0 {name=l9 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_NCH_2C5F0.sym} -950 -350 0 0 {name=xmn1}
C {devices/lab_pin.sym} -950 -350 0 0 {name=l10 sig_type=std_logic lab=VG}
C {devices/lab_pin.sym} -910 -320 1 0 {name=l11 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -910 -350 2 0 {name=l12 sig_type=std_logic lab=VSS}
N -910 -470 -910 -425 {}
N -910 -425 -910 -380 {}
C {devices/lab_pin.sym} -910 -425 2 0 {name=l13 sig_type=std_logic lab=VX}
T {MPB mirrors the diode current into MN1. MN2 (LVT) follows VX down to VG, so R carries Vgs(MN1)/R} -1450 -280 0 0 0.3 0.3 {}
T {Startup} -700 -620 0 0 0.4 0.4 {}
C {REY_ATR_SKY130A/REYATR_PCH_2C5F0.sym} -650 -500 0 0 {name=xms1}
C {devices/lab_pin.sym} -650 -500 0 0 {name=l14 sig_type=std_logic lab=VG}
C {devices/lab_pin.sym} -610 -530 3 0 {name=l15 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -610 -500 2 0 {name=l16 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -650 -350 0 0 {name=xms2[1:0]}
C {devices/lab_pin.sym} -650 -350 0 0 {name=l17 sig_type=std_logic lab=VG}
C {devices/lab_pin.sym} -610 -320 1 0 {name=l18 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -610 -350 2 0 {name=l19 sig_type=std_logic lab=VSS}
N -610 -470 -610 -425 {}
N -610 -425 -610 -380 {}
C {devices/lab_pin.sym} -610 -425 2 0 {name=l20 sig_type=std_logic lab=XST}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -390 -350 0 0 {name=xms3}
C {devices/lab_pin.sym} -390 -350 0 0 {name=l21 sig_type=std_logic lab=XST}
C {devices/lab_pin.sym} -350 -380 3 0 {name=l22 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -350 -320 1 0 {name=l23 sig_type=std_logic lab=VG}
C {devices/lab_pin.sym} -350 -350 2 0 {name=l24 sig_type=std_logic lab=VSS}
T {While VG is low, XST is high and MS3 pulls VBP down into VG, through R, until MN1 turns on} -700 -280 0 0 0.3 0.3 {}
T {Trim resistor: VG to VSS} -1450 -200 0 0 0.4 0.4 {}
C {REY_ATR_SKY130A/REYATR_RPPO4.sym} -1450 -100 0 0 {name=xrf0}
C {devices/lab_pin.sym} -1450 -100 0 0 {name=l25 sig_type=std_logic lab=VG}
C {devices/lab_pin.sym} -1410 -80 1 0 {name=l26 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_RPPO2.sym} -1250 -100 0 0 {name=xrf1[1:0]}
C {devices/lab_pin.sym} -1210 -80 1 0 {name=l27 sig_type=std_logic lab=VSS}
N -1370 -100 -1310 -100 {}
N -1310 -100 -1250 -100 {}
C {devices/lab_pin.sym} -1310 -100 3 0 {name=l28 sig_type=std_logic lab=RF}
C {REY_ATR_SKY130A/REYATR_RPPO2.sym} -1050 -100 0 0 {name=xrt0[1:0]}
C {devices/lab_pin.sym} -1010 -80 1 0 {name=l29 sig_type=std_logic lab=VSS}
N -1170 -100 -1110 -100 {}
N -1110 -100 -1050 -100 {}
C {devices/lab_pin.sym} -1110 -100 3 0 {name=l30 sig_type=std_logic lab=RT0}
C {REY_ATR_SKY130A/REYATR_RPPO2.sym} -850 -100 0 0 {name=xrt1}
C {devices/lab_pin.sym} -810 -80 1 0 {name=l31 sig_type=std_logic lab=VSS}
N -970 -100 -910 -100 {}
N -910 -100 -850 -100 {}
C {devices/lab_pin.sym} -910 -100 3 0 {name=l32 sig_type=std_logic lab=RT1}
C {REY_ATR_SKY130A/REYATR_RPPO4.sym} -650 -100 0 0 {name=xrt2}
C {devices/lab_pin.sym} -570 -100 2 0 {name=l33 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -610 -80 1 0 {name=l34 sig_type=std_logic lab=VSS}
N -770 -100 -710 -100 {}
N -710 -100 -650 -100 {}
C {devices/lab_pin.sym} -710 -100 3 0 {name=l35 sig_type=std_logic lab=RT2}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -1030 20 0 0 {name=xst0}
C {devices/lab_pin.sym} -1030 20 0 0 {name=l36 sig_type=std_logic lab=TRIM0}
C {devices/lab_pin.sym} -990 -10 3 0 {name=l37 sig_type=std_logic lab=RT0}
C {devices/lab_pin.sym} -990 50 1 0 {name=l38 sig_type=std_logic lab=RT1}
C {devices/lab_pin.sym} -990 20 2 0 {name=l39 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -830 20 0 0 {name=xst1}
C {devices/lab_pin.sym} -830 20 0 0 {name=l40 sig_type=std_logic lab=TRIM1}
C {devices/lab_pin.sym} -790 -10 3 0 {name=l41 sig_type=std_logic lab=RT1}
C {devices/lab_pin.sym} -790 50 1 0 {name=l42 sig_type=std_logic lab=RT2}
C {devices/lab_pin.sym} -790 20 2 0 {name=l43 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -630 20 0 0 {name=xst2}
C {devices/lab_pin.sym} -630 20 0 0 {name=l44 sig_type=std_logic lab=TRIM2}
C {devices/lab_pin.sym} -590 -10 3 0 {name=l45 sig_type=std_logic lab=RT2}
C {devices/lab_pin.sym} -590 50 1 0 {name=l46 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -590 20 2 0 {name=l47 sig_type=std_logic lab=VSS}
T {38.5k fixed, then 7.7k / 15.4k / 30.8k, each shorted when TRIM<k> is high} -1450 100 0 0 0.3 0.3 {}
T {Ring: 7 stages, one drawn, the rest by the bus} 100 -620 0 0 0.4 0.4 {}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} 200 -490 0 0 {name=xmpca[6:0]}
C {devices/lab_pin.sym} 200 -490 0 0 {name=l48 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 240 -520 3 0 {name=l49 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 240 -490 2 0 {name=l50 sig_type=std_logic lab=VDD_1V8}
N 240 -460 240 -435 {}
N 240 -435 240 -410 {}
C {devices/lab_pin.sym} 240 -435 0 0 {name=l51 sig_type=std_logic lab=NC6,NC5,NC4,NC3,NC2,NC1,NC0}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_4C5F0.sym} 200 -380 0 0 {name=xmpv[6:0]}
C {devices/lab_pin.sym} 200 -380 0 0 {name=l52 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} 240 -380 2 0 {name=l53 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} 500 -380 0 0 {name=xmpfa[6:0]}
C {devices/lab_pin.sym} 500 -380 0 0 {name=l54 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 540 -410 3 0 {name=l55 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 540 -380 2 0 {name=l56 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} 760 -380 0 0 {name=xmpfb[6:0]}
C {devices/lab_pin.sym} 760 -380 0 0 {name=l57 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 800 -410 3 0 {name=l58 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 800 -380 2 0 {name=l59 sig_type=std_logic lab=VDD_1V8}
N 240 -350 240 -300 {}
N 540 -350 540 -300 {}
N 800 -350 800 -300 {}
N 240 -300 800 -300 {}
C {devices/lab_pin.sym} 800 -300 2 0 {name=l60 sig_type=std_logic lab=VS6,VS5,VS4,VS3,VS2,VS1,VS0}
C {REY_ATR_SKY130A/REYATR_PCH_2C1F2.sym} 200 -230 0 0 {name=xip[6:0]}
C {devices/lab_pin.sym} 240 -230 2 0 {name=l61 sig_type=std_logic lab=VDD_1V8}
N 240 -300 240 -260 {}
C {REY_ATR_SKY130A/REYATR_NCH_2C1F2.sym} 200 -110 0 0 {name=xin[6:0]}
C {devices/lab_pin.sym} 240 -80 1 0 {name=l62 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 240 -110 2 0 {name=l63 sig_type=std_logic lab=VSS}
N 240 -200 240 -170 {}
N 240 -170 240 -140 {}
N 240 -170 340 -170 {}
C {devices/lab_pin.sym} 340 -170 2 0 {name=l64 sig_type=std_logic lab=N6,N5,N4,N3,N2,N1,N0}
N 200 -230 160 -230 {}
N 160 -230 160 -170 {}
N 160 -170 160 -110 {}
N 160 -110 200 -110 {}
C {devices/lab_pin.sym} 160 -170 0 0 {name=l65 sig_type=std_logic lab=N5,N4,N3,N2,N1,N0,N6}
T {stage k: N<k-1> -> N<k>, stage 0 takes the last node} 100 -60 0 0 0.3 0.3 {}
T {fixed mirror: sets f_min; tunable mirror through the VCTRL device: the rest} 100 -30 0 0 0.3 0.3 {}
T {Output buffer} 1370 -620 0 0 0.4 0.4 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} 1370 -170 0 0 {name=xo0}
C {devices/lab_pin.sym} 1410 -210 3 0 {name=l66 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1410 -130 1 0 {name=l67 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1370 -170 0 0 {name=l68 sig_type=std_logic lab=N6}
N 1450 -170 1510 -170 {}
N 1510 -170 1570 -170 {}
C {devices/lab_pin.sym} 1510 -170 3 0 {name=l69 sig_type=std_logic lab=CKN}
C {REY_TR_SKY130A/REYTR_IVX4_CV.sym} 1570 -170 0 0 {name=xo1}
C {devices/lab_pin.sym} 1610 -210 3 0 {name=l70 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 1610 -130 1 0 {name=l71 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1650 -170 2 0 {name=l72 sig_type=std_logic lab=CK}
