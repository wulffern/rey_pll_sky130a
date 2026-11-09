v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_ROSC_BIAS: the Vgs/R bias of the ring, VBP out} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=TRIM0}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=TRIM1}
C {devices/ipin.sym} -760 -740 0 0 {name=p4 lab=TRIM2}
C {devices/opin.sym} -600 -740 0 0 {name=p5 lab=VBP}
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
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} -1450 -100 0 0 {name=xrf0}
C {devices/lab_pin.sym} -1450 -100 0 0 {name=l25 sig_type=std_logic lab=VG}
C {devices/lab_pin.sym} -1410 -80 1 0 {name=l26 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} -1260 -100 0 0 {name=xrf1}
C {devices/lab_pin.sym} -1220 -80 1 0 {name=l27 sig_type=std_logic lab=VSS}
N -1370 -100 -1315 -100 {}
N -1315 -100 -1260 -100 {}
C {devices/lab_pin.sym} -1315 -100 3 0 {name=l28 sig_type=std_logic lab=RFA}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} -1070 -100 0 0 {name=xrf2[1:0]}
C {devices/lab_pin.sym} -1030 -80 1 0 {name=l29 sig_type=std_logic lab=VSS}
N -1180 -100 -1125 -100 {}
N -1125 -100 -1070 -100 {}
C {devices/lab_pin.sym} -1125 -100 3 0 {name=l30 sig_type=std_logic lab=RF}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} -880 -100 0 0 {name=xrt0[1:0]}
C {devices/lab_pin.sym} -840 -80 1 0 {name=l31 sig_type=std_logic lab=VSS}
N -990 -100 -935 -100 {}
N -935 -100 -880 -100 {}
C {devices/lab_pin.sym} -935 -100 3 0 {name=l32 sig_type=std_logic lab=RT0}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} -690 -100 0 0 {name=xrt1}
C {devices/lab_pin.sym} -650 -80 1 0 {name=l33 sig_type=std_logic lab=VSS}
N -800 -100 -745 -100 {}
N -745 -100 -690 -100 {}
C {devices/lab_pin.sym} -745 -100 3 0 {name=l34 sig_type=std_logic lab=RT1}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} -500 -100 0 0 {name=xrt2a}
C {devices/lab_pin.sym} -460 -80 1 0 {name=l35 sig_type=std_logic lab=VSS}
N -610 -100 -555 -100 {}
N -555 -100 -500 -100 {}
C {devices/lab_pin.sym} -555 -100 3 0 {name=l36 sig_type=std_logic lab=RT2}
C {REY_ATR_SKY130A/REYATR_RES_36C2F0.sym} -310 -100 0 0 {name=xrt2b}
C {devices/lab_pin.sym} -230 -100 2 0 {name=l37 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -270 -80 1 0 {name=l38 sig_type=std_logic lab=VSS}
N -420 -100 -365 -100 {}
N -365 -100 -310 -100 {}
C {devices/lab_pin.sym} -365 -100 3 0 {name=l39 sig_type=std_logic lab=RT2B}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -840 20 0 0 {name=xst0}
C {devices/lab_pin.sym} -840 20 0 0 {name=l40 sig_type=std_logic lab=TRIM0}
C {devices/lab_pin.sym} -800 -10 3 0 {name=l41 sig_type=std_logic lab=RT0}
C {devices/lab_pin.sym} -800 50 1 0 {name=l42 sig_type=std_logic lab=RT1}
C {devices/lab_pin.sym} -800 20 2 0 {name=l43 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -650 20 0 0 {name=xst1}
C {devices/lab_pin.sym} -650 20 0 0 {name=l44 sig_type=std_logic lab=TRIM1}
C {devices/lab_pin.sym} -610 -10 3 0 {name=l45 sig_type=std_logic lab=RT1}
C {devices/lab_pin.sym} -610 50 1 0 {name=l46 sig_type=std_logic lab=RT2}
C {devices/lab_pin.sym} -610 20 2 0 {name=l47 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -460 20 0 0 {name=xst2}
C {devices/lab_pin.sym} -460 20 0 0 {name=l48 sig_type=std_logic lab=TRIM2}
C {devices/lab_pin.sym} -420 -10 3 0 {name=l49 sig_type=std_logic lab=RT2}
C {devices/lab_pin.sym} -420 50 1 0 {name=l50 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -420 20 2 0 {name=l51 sig_type=std_logic lab=VSS}
T {38.5k fixed, then 7.7k / 15.4k / 30.8k, each shorted when TRIM<k> is high} -1450 100 0 0 0.3 0.3 {}
