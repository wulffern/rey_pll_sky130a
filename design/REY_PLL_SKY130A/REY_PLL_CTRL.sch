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
T {KICK: a pulse when PWRUP_1V8 rises. KD4 is PWRUP_1V8 delayed by five inverters, so NOR(PWRUP_N, KD4) is high between the edge and KD4} -1450 -640 0 0 0.3 0.3 {}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1300 -500 0 0 {name=xi0}
C {devices/lab_pin.sym} -1300 -500 0 0 {name=l1 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1260 -540 3 0 {name=l2 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 -460 1 0 {name=l3 sig_type=std_logic lab=VSS}
N -1220 -500 -1170 -500 {}
N -1170 -500 -1120 -500 {}
C {devices/lab_pin.sym} -1170 -500 3 0 {name=l4 sig_type=std_logic lab=PWRUP_N}
C {REY_TR_SKY130A/REYTR_IVX1_CV.sym} -1100 -500 0 0 {name=xkd[4:0]}
C {devices/lab_pin.sym} -1100 -500 0 0 {name=l5 sig_type=std_logic lab=KD3,KD2,KD1,KD0,PWRUP_N}
C {devices/lab_pin.sym} -1020 -500 2 0 {name=l6 sig_type=std_logic lab=KD4,KD3,KD2,KD1,KD0}
C {devices/lab_pin.sym} -1060 -540 3 0 {name=l7 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1060 -460 1 0 {name=l8 sig_type=std_logic lab=VSS}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -850 -490 0 0 {name=xk}
C {devices/lab_pin.sym} -850 -510 0 0 {name=l9 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -850 -490 0 0 {name=l10 sig_type=std_logic lab=KD4}
C {devices/lab_pin.sym} -760 -500 2 0 {name=l11 sig_type=std_logic lab=KICK}
C {devices/lab_pin.sym} -810 -540 3 0 {name=l12 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -810 -460 1 0 {name=l13 sig_type=std_logic lab=VSS}
T {Open loop, for the per-die trim: OLH parks VCTRL at VDD_1V8 (slowest), OLL at VSS (fastest). Powered down is OLH} -1450 -300 0 0 0.3 0.3 {}
C {REY_TR_SKY130A/REYTR_NRX1_CV.sym} -1300 -150 0 0 {name=xo0}
C {devices/lab_pin.sym} -1300 -170 0 0 {name=l14 sig_type=std_logic lab=PWRUP_N}
C {devices/lab_pin.sym} -1300 -150 0 0 {name=l15 sig_type=std_logic lab=OLH}
C {devices/lab_pin.sym} -1260 -200 3 0 {name=l16 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1260 -120 1 0 {name=l17 sig_type=std_logic lab=VSS}
N -1210 -160 -1150 -160 {}
N -1150 -160 -1090 -160 {}
C {devices/lab_pin.sym} -1150 -160 3 0 {name=l18 sig_type=std_logic lab=VHI_N}
C {REY_TR_SKY130A/REYTR_ANX1_CV.sym} -1090 -140 0 0 {name=xo1}
C {devices/lab_pin.sym} -1090 -140 0 0 {name=l19 sig_type=std_logic lab=OLL}
C {devices/lab_pin.sym} -1000 -150 2 0 {name=l20 sig_type=std_logic lab=VLO}
C {devices/lab_pin.sym} -1050 -190 3 0 {name=l21 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1050 -110 1 0 {name=l22 sig_type=std_logic lab=VSS}
T {VHI_N = PWRUP and not OLH. VLO = VHI_N and OLL, so OLH wins} -1450 -60 0 0 0.3 0.3 {}
C {REY_TR_SKY130A/REYTR_TAPCELLB_CV.sym} -600 -150 0 0 {name=xtap}
C {devices/lab_pin.sym} -600 -170 3 0 {name=l23 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -600 -130 1 0 {name=l24 sig_type=std_logic lab=VSS}
