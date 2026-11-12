v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {REY_PLL_ROSC_STAGE: one ring stage, a starved inverter A -> Y} -1450 -820 0 0 0.5 0.5 {}
C {devices/ipin.sym} -1400 -740 0 0 {name=p0 lab=VDD_1V8}
C {devices/ipin.sym} -1240 -740 0 0 {name=p1 lab=VSS}
C {devices/ipin.sym} -1080 -740 0 0 {name=p2 lab=VBP}
C {devices/ipin.sym} -920 -740 0 0 {name=p3 lab=VCTRL}
C {devices/ipin.sym} -760 -740 0 0 {name=p4 lab=A}
C {devices/opin.sym} -600 -740 0 0 {name=p5 lab=Y}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} -1200 -490 0 0 {name=xmpca}
C {devices/lab_pin.sym} -1200 -490 0 0 {name=l58 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -1160 -520 1 0 {name=l59 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -1160 -490 2 0 {name=l60 sig_type=std_logic lab=VDD_1V8}
N -1160 -460 -1160 -435 {}
N -1160 -435 -1160 -410 {}
C {devices/lab_pin.sym} -1160 -435 0 0 {name=l61 sig_type=std_logic lab=NC}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_4C5F0.sym} -1200 -380 0 0 {name=xmpv}
C {devices/lab_pin.sym} -1200 -380 0 0 {name=l62 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} -1160 -380 2 0 {name=l63 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} -900 -380 0 0 {name=xmpfa}
C {devices/lab_pin.sym} -900 -380 0 0 {name=l64 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -860 -410 1 0 {name=l65 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -860 -380 2 0 {name=l66 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} -640 -380 0 0 {name=xmpfb}
C {devices/lab_pin.sym} -640 -380 0 0 {name=l67 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} -600 -410 1 0 {name=l68 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} -600 -380 2 0 {name=l69 sig_type=std_logic lab=VDD_1V8}
N -1160 -350 -1160 -300 {}
N -860 -350 -860 -300 {}
N -600 -350 -600 -300 {}
N -1160 -300 -600 -300 {}
C {devices/lab_pin.sym} -600 -300 2 0 {name=l70 sig_type=std_logic lab=VS}
C {REY_ATR_SKY130A/REYATR_PCH_2C1F2.sym} -1200 -230 0 0 {name=xip}
C {devices/lab_pin.sym} -1160 -230 2 0 {name=l71 sig_type=std_logic lab=VDD_1V8}
N -1160 -300 -1160 -260 {}
C {REY_ATR_SKY130A/REYATR_NCH_2C1F2.sym} -1200 -110 0 0 {name=xin}
C {devices/lab_pin.sym} -1160 -80 3 0 {name=l72 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -1160 -110 2 0 {name=l73 sig_type=std_logic lab=VSS}
N -1160 -200 -1160 -170 {}
N -1160 -170 -1160 -140 {}
N -1160 -170 -1060 -170 {}
C {devices/lab_pin.sym} -1060 -170 2 0 {name=l74 sig_type=std_logic lab=Y}
N -1200 -230 -1240 -230 {}
N -1240 -230 -1240 -170 {}
N -1240 -170 -1240 -110 {}
N -1240 -110 -1200 -110 {}
C {devices/lab_pin.sym} -1240 -170 0 0 {name=l75 sig_type=std_logic lab=A}
T {fixed mirror: sets f_min; tunable mirror through the VCTRL device: the rest} -1300 -30 0 0 0.3 0.3 {}
P 4 5 -1520 -860 -450 -860 -450 80 -1520 80 -1520 -860 {dash=4}
