v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_CP: charge pump, UP sinks and DN sources (negative Kvco)} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=VBP}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=UP}
C {devices/ipin.sym} -760 -740 0 0 {name=p4 lab=DN_N}
C {devices/ipin.sym} -600 -740 0 0 {name=p5 lab=VHI_N}
C {devices/ipin.sym} -440 -740 0 0 {name=p6 lab=VLO}
C {devices/ipin.sym} -280 -740 0 0 {name=p7 lab=KICK}
C {devices/opin.sym} -120 -740 0 0 {name=p8 lab=VCTRL}
C {devices/opin.sym} 40 -740 0 0 {name=p9 lab=VLPFZ}
T {Icp from the oscillator bias: one LVT_PCH_4C5F0 on VBP, about 1.1 to 2.8 uA over the trim codes} -1450 -640 0 0 0.3 0.3 {}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_4C5F0.sym} -1200 -500 0 0 {name=xmpu}
C {devices/lab_pin.sym} -1200 -500 0 0 {name=l1 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -1160 -530 1 0 {name=l2 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1160 -500 2 0 {name=l3 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_PCH_2C1F2.sym} -1200 -380 0 0 {name=xmpd}
C {devices/lab_pin.sym} -1200 -380 0 0 {name=l4 sig_type=std_logic lab=DN_N}
C {devices/lab_pin.sym} -1160 -380 2 0 {name=l5 sig_type=std_logic lab=VDD_1V8}
N -1160 -470 -1160 -440 {}
N -1160 -440 -1160 -410 {}
C {devices/lab_pin.sym} -1160 -440 2 0 {name=l6 sig_type=std_logic lab=VPS}
C {REY_ATR_SKY130A/REYATR_NCH_2C1F2.sym} -1200 -230 0 0 {name=xmnu}
C {devices/lab_pin.sym} -1200 -230 0 0 {name=l7 sig_type=std_logic lab=UP}
C {devices/lab_pin.sym} -1160 -230 2 0 {name=l8 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_4C5F0.sym} -1200 -110 0 0 {name=xmns}
C {devices/lab_pin.sym} -1200 -110 0 0 {name=l9 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} -1160 -80 3 0 {name=l10 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1160 -110 2 0 {name=l11 sig_type=std_logic lab=VSS}
N -1160 -200 -1160 -170 {}
N -1160 -170 -1160 -140 {}
C {devices/lab_pin.sym} -1160 -170 2 0 {name=l12 sig_type=std_logic lab=VNS}
N -1160 -350 -1160 -305 {}
N -1160 -260 -1160 -305 {}
N -1160 -305 -1040 -305 {}
C {devices/lab_pin.sym} -1040 -305 2 0 {name=l13 sig_type=std_logic lab=VCTRL}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_4C5F0.sym} -850 -500 0 0 {name=xmpn}
C {devices/lab_pin.sym} -850 -500 0 0 {name=l14 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -810 -530 1 0 {name=l15 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -810 -500 2 0 {name=l16 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_NCH_4C5F0.sym} -850 -110 0 0 {name=xmnd}
C {devices/lab_pin.sym} -850 -110 0 0 {name=l17 sig_type=std_logic lab=VBN}
C {devices/lab_pin.sym} -810 -80 3 0 {name=l18 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -810 -110 2 0 {name=l19 sig_type=std_logic lab=VSS}
N -810 -470 -810 -305 {}
N -810 -305 -810 -140 {}
C {devices/lab_pin.sym} -810 -305 2 0 {name=l20 sig_type=std_logic lab=VBN}
T {Parking and kick} -550 -640 0 0 0.4 0.4 {}
C {REY_ATR_SKY130A/REYATR_PCH_4C1F2.sym} -500 -500 0 0 {name=xmph}
C {devices/lab_pin.sym} -500 -500 0 0 {name=l21 sig_type=std_logic lab=VHI_N}
C {devices/lab_pin.sym} -460 -530 1 0 {name=l22 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -460 -470 3 0 {name=l23 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -460 -500 2 0 {name=l24 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -500 -300 0 0 {name=xmnl}
C {devices/lab_pin.sym} -500 -300 0 0 {name=l25 sig_type=std_logic lab=VLO}
C {devices/lab_pin.sym} -460 -330 1 0 {name=l26 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -460 -270 3 0 {name=l27 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -460 -300 2 0 {name=l28 sig_type=std_logic lab=VSS}
C {REY_ATR_SKY130A/REYATR_NCH_4C1F2.sym} -500 -110 0 0 {name=xmnk}
C {devices/lab_pin.sym} -500 -110 0 0 {name=l29 sig_type=std_logic lab=KICK}
C {devices/lab_pin.sym} -460 -140 1 0 {name=l30 sig_type=std_logic lab=VLPFZ}
C {devices/lab_pin.sym} -460 -80 3 0 {name=l31 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -460 -110 2 0 {name=l32 sig_type=std_logic lab=VSS}
T {VHI_N low: VCTRL to VDD_1V8 (powered down, or OLH)} -550 -20 0 0 0.3 0.3 {}
T {VLO high: VCTRL to VSS (OLL). KICK pulls C1 down at power up} -550 10 0 0 0.3 0.3 {}
P 4 5 -1520 -860 150 -860 150 70 -1520 70 -1520 -860 {dash=4}
