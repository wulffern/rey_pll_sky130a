v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL: 512 MHz from 8 MHz, current starved ring oscillator} -1450 -820 0 0 0.5 0.5 {}
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
C {devices/opin.sym} 840 -740 0 0 {name=p14 lab=CKO4}
C {devices/opin.sym} 1000 -740 0 0 {name=p15 lab=CKO5}
C {devices/opin.sym} 1160 -740 0 0 {name=p16 lab=CKO6}
C {devices/opin.sym} 1320 -740 0 0 {name=p17 lab=CKO7}
T {CK_REF -> PFD -> CP -> LPF -> VCTRL -> ROSC -> DIVN -> CK_FB} -1450 -640 0 0 0.4 0.4 {}
C {REY_PLL_SKY130A/REY_PLL_CTRL.sym} -1200 -150 0 0 {name=xctrl}
C {devices/lab_pin.sym} -1350 -240 0 0 {name=l1 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1350 -220 0 0 {name=l2 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1350 -200 0 0 {name=l3 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1350 -180 0 0 {name=l4 sig_type=std_logic lab=OLH}
C {devices/lab_pin.sym} -1350 -160 0 0 {name=l5 sig_type=std_logic lab=OLL}
C {devices/lab_pin.sym} -1050 -240 2 0 {name=l6 sig_type=std_logic lab=KICK}
C {devices/lab_pin.sym} -1050 -220 2 0 {name=l7 sig_type=std_logic lab=VHI_N}
C {devices/lab_pin.sym} -1050 -200 2 0 {name=l8 sig_type=std_logic lab=VLO}
C {REY_PLL_SKY130A/REY_PLL_PFD.sym} -1200 -450 0 0 {name=xpfd}
C {devices/lab_pin.sym} -1350 -540 0 0 {name=l9 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1350 -520 0 0 {name=l10 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1350 -500 0 0 {name=l11 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -1350 -480 0 0 {name=l12 sig_type=std_logic lab=CK_REF}
C {devices/lab_pin.sym} -1350 -460 0 0 {name=l13 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -1050 -540 2 0 {name=l14 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1050 -520 2 0 {name=l15 sig_type=std_logic lab=DN_N}
C {REY_PLL_SKY130A/REY_PLL_CP.sym} -800 -450 0 0 {name=xcp}
C {devices/lab_pin.sym} -950 -600 0 0 {name=l16 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -950 -580 0 0 {name=l17 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -950 -560 0 0 {name=l18 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -950 -540 0 0 {name=l19 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -950 -520 0 0 {name=l20 sig_type=std_logic lab=DN_N}
C {devices/lab_pin.sym} -950 -500 0 0 {name=l21 sig_type=std_logic lab=VHI_N}
C {devices/lab_pin.sym} -950 -480 0 0 {name=l22 sig_type=std_logic lab=VLO}
C {devices/lab_pin.sym} -950 -460 0 0 {name=l23 sig_type=std_logic lab=KICK}
C {devices/lab_pin.sym} -650 -600 2 0 {name=l24 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -650 -580 2 0 {name=l25 sig_type=std_logic lab=VLPFZ}
C {REY_PLL_SKY130A/REY_PLL_LPF.sym} -800 -150 0 0 {name=xlpf}
C {devices/lab_pin.sym} -950 -220 0 0 {name=l26 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -950 -200 0 0 {name=l27 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -950 -180 0 0 {name=l28 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -950 -160 0 0 {name=l29 sig_type=std_logic lab=VLPFZ}
C {REY_PLL_SKY130A/REY_PLL_ROSC.sym} -400 -450 0 0 {name=xrosc}
C {devices/lab_pin.sym} -550 -560 0 0 {name=l30 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -550 -540 0 0 {name=l31 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -550 -520 0 0 {name=l32 sig_type=std_logic lab=TRIM0}
C {devices/lab_pin.sym} -550 -500 0 0 {name=l33 sig_type=std_logic lab=TRIM1}
C {devices/lab_pin.sym} -550 -480 0 0 {name=l34 sig_type=std_logic lab=TRIM2}
C {devices/lab_pin.sym} -550 -460 0 0 {name=l35 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -250 -560 2 0 {name=l36 sig_type=std_logic lab=CK}
C {devices/lab_pin.sym} -250 -540 2 0 {name=l37 sig_type=std_logic lab=VBP}
C {REY_PLL_SKY130A/REY_PLL_DIVN.sym} -400 -100 0 0 {name=xdivn}
C {devices/lab_pin.sym} -550 -270 0 0 {name=l38 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -550 -250 0 0 {name=l39 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -550 -230 0 0 {name=l40 sig_type=std_logic lab=PWRUP_1V8}
C {devices/lab_pin.sym} -550 -210 0 0 {name=l41 sig_type=std_logic lab=CK}
C {devices/lab_pin.sym} -250 -270 2 0 {name=l42 sig_type=std_logic lab=CK_FB}
C {devices/lab_pin.sym} -250 -250 2 0 {name=l43 sig_type=std_logic lab=CKO0}
C {devices/lab_pin.sym} -250 -230 2 0 {name=l44 sig_type=std_logic lab=CKO1}
C {devices/lab_pin.sym} -250 -210 2 0 {name=l45 sig_type=std_logic lab=CKO2}
C {devices/lab_pin.sym} -250 -190 2 0 {name=l46 sig_type=std_logic lab=CKO3}
C {devices/lab_pin.sym} -250 -170 2 0 {name=l47 sig_type=std_logic lab=CKO4}
C {devices/lab_pin.sym} -250 -150 2 0 {name=l48 sig_type=std_logic lab=CKO5}
C {devices/lab_pin.sym} -250 -130 2 0 {name=l49 sig_type=std_logic lab=CKO6}
C {devices/lab_pin.sym} -250 -110 2 0 {name=l50 sig_type=std_logic lab=CKO7}
