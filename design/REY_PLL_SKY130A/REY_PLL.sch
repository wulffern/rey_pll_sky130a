v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL: 128 MHz from 8 MHz, current starved ring oscillator} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=PWRUP_1V8}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=CK_REF}
C {devices/ipin.sym} -760 -740 0 0 {name=p4 lab=TRIM0}
C {devices/ipin.sym} -600 -740 0 0 {name=p5 lab=TRIM1}
C {devices/ipin.sym} -440 -740 0 0 {name=p6 lab=TRIM2}
C {devices/ipin.sym} -280 -740 0 0 {name=p7 lab=OLH}
C {devices/ipin.sym} -120 -740 0 0 {name=p8 lab=OLL}
C {devices/opin.sym} 40 -740 0 0 {name=p9 lab=CK}
C {devices/opin.sym} 200 -740 0 0 {name=p10 lab=CKO0}
C {devices/opin.sym} 360 -740 0 0 {name=p11 lab=CKO1}
C {devices/opin.sym} 520 -740 0 0 {name=p12 lab=CKO2}
C {devices/opin.sym} 680 -740 0 0 {name=p13 lab=CKO3}
T {CK_REF -> PFD -> CP -> LPF -> VCTRL -> ROSC -> DIVN -> CK_FB} -1450 -640 0 0 0.4 0.4 {}
C {REY_PLL_SKY130A/REY_PLL_CTRL.sym} -1150 30 0 0 {name=xctrl}
C {devices/lab_pin.sym} -1300 -60 0 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -40 0 0 {name=l2 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1300 -20 0 0 {name=l3 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1300 0 0 0 {name=l4 sig_type=std_logic lab=OLH}
C {devices/lab_pin.sym} -1300 20 0 0 {name=l5 sig_type=std_logic lab=OLL}
C {devices/lab_pin.sym} -1000 -60 2 0 {name=l6 sig_type=std_logic lab=KICK}
C {devices/lab_pin.sym} -1000 -40 2 0 {name=l7 sig_type=std_logic lab=VHI_N}
C {devices/lab_pin.sym} -1000 -20 2 0 {name=l8 sig_type=std_logic lab=VLO}
C {REY_PLL_SKY130A/REY_PLL_PFD.sym} -1150 -250 0 0 {name=xpfd}
C {devices/lab_pin.sym} -1300 -340 0 0 {name=l9 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1300 -320 0 0 {name=l10 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1300 -300 0 0 {name=l11 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1300 -280 0 0 {name=l12 sig_type=std_logic lab=CK_REF}
C {REY_PLL_SKY130A/REY_PLL_CP.sym} -600 -250 0 0 {name=xcp}
C {devices/lab_pin.sym} -750 -400 0 0 {name=l13 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -750 -380 0 0 {name=l14 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -750 -360 0 0 {name=l15 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -750 -300 0 0 {name=l16 sig_type=std_logic lab=VHI_N}
C {devices/lab_pin.sym} -750 -280 0 0 {name=l17 sig_type=std_logic lab=VLO}
C {devices/lab_pin.sym} -750 -260 0 0 {name=l18 sig_type=std_logic lab=KICK}
C {REY_PLL_SKY130A/REY_PLL_LPF.sym} -50 -120 0 0 {name=xlpf}
C {devices/lab_pin.sym} -200 -190 0 0 {name=l19 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -200 -170 0 0 {name=l20 sig_type=std_logic lab=VSS}
C {REY_PLL_SKY130A/REY_PLL_ROSC.sym} 100 -390 0 0 {name=xrosc}
C {devices/lab_pin.sym} -50 -500 0 0 {name=l21 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -50 -480 0 0 {name=l22 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -50 -460 0 0 {name=l23 sig_type=std_logic lab=TRIM0}
C {devices/lab_pin.sym} -50 -440 0 0 {name=l24 sig_type=std_logic lab=TRIM1}
C {devices/lab_pin.sym} -50 -420 0 0 {name=l25 sig_type=std_logic lab=TRIM2}
C {devices/lab_pin.sym} 250 -480 2 0 {name=l26 sig_type=std_logic lab=VBP}
C {REY_PLL_SKY130A/REY_PLL_DIVN.sym} 650 -450 0 0 {name=xdivn}
C {devices/lab_pin.sym} 500 -540 0 0 {name=l27 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 500 -520 0 0 {name=l28 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 800 -520 2 0 {name=l29 sig_type=std_logic lab=CKO0}
C {devices/lab_pin.sym} 800 -500 2 0 {name=l30 sig_type=std_logic lab=CKO1}
C {devices/lab_pin.sym} 800 -480 2 0 {name=l31 sig_type=std_logic lab=CKO2}
C {devices/lab_pin.sym} 800 -460 2 0 {name=l32 sig_type=std_logic lab=CKO3}
N -1000 -340 -875 -340 {}
N -875 -340 -750 -340 {}
C {devices/lab_pin.sym} -875 -340 1 0 {name=l33 sig_type=std_logic lab=UP}
N -1000 -320 -875 -320 {}
N -875 -320 -750 -320 {}
C {devices/lab_pin.sym} -875 -320 3 0 {name=l34 sig_type=std_logic lab=DN_N}
N -450 -400 -350 -400 {}
N -350 -400 -50 -400 {}
N -350 -400 -350 -275 {}
N -350 -275 -350 -150 {}
C {devices/lab_pin.sym} -350 -275 2 0 {name=l35 sig_type=std_logic lab=VCTRL}
N -350 -150 -200 -150 {}
N -450 -380 -400 -380 {}
N -400 -380 -400 -255 {}
N -400 -255 -400 -130 {}
C {devices/lab_pin.sym} -400 -255 0 0 {name=l36 sig_type=std_logic lab=VLPFZ}
N -400 -130 -200 -130 {}
N 250 -500 375 -500 {}
N 375 -500 500 -500 {}
C {devices/lab_pin.sym} 375 -500 1 0 {name=l37 sig_type=std_logic lab=CK}
N 800 -540 920 -540 {}
N 920 -540 920 -170 {}
N 920 -170 920 200 {}
C {devices/lab_pin.sym} 920 -170 2 0 {name=l38 sig_type=std_logic lab=CK_FB}
N 920 200 -1450 200 {}
N -1450 200 -1450 -260 {}
N -1450 -260 -1300 -260 {}
P 4 5 -1520 -860 1030 -860 1030 240 -1520 240 -1520 -860 {dash=4}
