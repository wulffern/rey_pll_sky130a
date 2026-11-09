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
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} 200 -490 0 0 {name=xmpca}
C {devices/lab_pin.sym} 200 -490 0 0 {name=l58 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 240 -520 3 0 {name=l59 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 240 -490 2 0 {name=l60 sig_type=std_logic lab=VDD_1V8}
N 240 -460 240 -435 {}
N 240 -435 240 -410 {}
C {devices/lab_pin.sym} 240 -435 0 0 {name=l61 sig_type=std_logic lab=NC}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_4C5F0.sym} 200 -380 0 0 {name=xmpv}
C {devices/lab_pin.sym} 200 -380 0 0 {name=l62 sig_type=std_logic lab=VCTRL}
C {devices/lab_pin.sym} 240 -380 2 0 {name=l63 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} 500 -380 0 0 {name=xmpfa}
C {devices/lab_pin.sym} 500 -380 0 0 {name=l64 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 540 -410 3 0 {name=l65 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 540 -380 2 0 {name=l66 sig_type=std_logic lab=VDD_1V8}
C {REY_ATR_SKY130A/REYATR_LVT_PCH_8C5F0.sym} 760 -380 0 0 {name=xmpfb}
C {devices/lab_pin.sym} 760 -380 0 0 {name=l67 sig_type=std_logic lab=VBP}
C {devices/lab_pin.sym} 800 -410 3 0 {name=l68 sig_type=std_logic lab=VDD_1V8}
C {devices/lab_pin.sym} 800 -380 2 0 {name=l69 sig_type=std_logic lab=VDD_1V8}
N 240 -350 240 -300 {}
N 540 -350 540 -300 {}
N 800 -350 800 -300 {}
N 240 -300 800 -300 {}
C {devices/lab_pin.sym} 800 -300 2 0 {name=l70 sig_type=std_logic lab=VS}
C {REY_ATR_SKY130A/REYATR_PCH_2C1F2.sym} 200 -230 0 0 {name=xip}
C {devices/lab_pin.sym} 240 -230 2 0 {name=l71 sig_type=std_logic lab=VDD_1V8}
N 240 -300 240 -260 {}
C {REY_ATR_SKY130A/REYATR_NCH_2C1F2.sym} 200 -110 0 0 {name=xin}
C {devices/lab_pin.sym} 240 -80 1 0 {name=l72 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 240 -110 2 0 {name=l73 sig_type=std_logic lab=VSS}
N 240 -200 240 -170 {}
N 240 -170 240 -140 {}
N 240 -170 340 -170 {}
C {devices/lab_pin.sym} 340 -170 2 0 {name=l74 sig_type=std_logic lab=Y}
N 200 -230 160 -230 {}
N 160 -230 160 -170 {}
N 160 -170 160 -110 {}
N 160 -110 200 -110 {}
C {devices/lab_pin.sym} 160 -170 0 0 {name=l75 sig_type=std_logic lab=A}
T {fixed mirror: sets f_min; tunable mirror through the VCTRL device: the rest} 100 -30 0 0 0.3 0.3 {}
