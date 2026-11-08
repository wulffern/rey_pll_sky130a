v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=DN_N}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=KICK}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=UP}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=VBP}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=VCTRL}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=VDD_1V8}
C {devices/iopin.sym} 0 120 0 0 {name=p6 lab=VHI_N}
C {devices/iopin.sym} 0 140 0 0 {name=p7 lab=VLO}
C {devices/iopin.sym} 0 160 0 0 {name=p8 lab=VLPFZ}
C {devices/iopin.sym} 0 180 0 0 {name=p9 lab=VSS}
C {REY_PLL_SKY130A/REY_PLL_CP.sym} 400 0 0 0 {name=Xxcp}
N 230.0 -150.0 250.0 -150.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 230.0 -150.0 0 0 {name=l0 sig_type=std_logic lab=VDD_1V8 }
N 230.0 -130.0 250.0 -130.0 {lab=VSS}
C {devices/lab_pin.sym} 230.0 -130.0 0 0 {name=l1 sig_type=std_logic lab=VSS }
N 230.0 -110.0 250.0 -110.0 {lab=VBP}
C {devices/lab_pin.sym} 230.0 -110.0 0 0 {name=l2 sig_type=std_logic lab=VBP }
N 230.0 -90.0 250.0 -90.0 {lab=UP}
C {devices/lab_pin.sym} 230.0 -90.0 0 0 {name=l3 sig_type=std_logic lab=UP }
N 230.0 -70.0 250.0 -70.0 {lab=DN_N}
C {devices/lab_pin.sym} 230.0 -70.0 0 0 {name=l4 sig_type=std_logic lab=DN_N }
N 230.0 -50.0 250.0 -50.0 {lab=VHI_N}
C {devices/lab_pin.sym} 230.0 -50.0 0 0 {name=l5 sig_type=std_logic lab=VHI_N }
N 230.0 -30.0 250.0 -30.0 {lab=VLO}
C {devices/lab_pin.sym} 230.0 -30.0 0 0 {name=l6 sig_type=std_logic lab=VLO }
N 230.0 -10.0 250.0 -10.0 {lab=KICK}
C {devices/lab_pin.sym} 230.0 -10.0 0 0 {name=l7 sig_type=std_logic lab=KICK }
N 570.0 -150.0 550.0 -150.0 {lab=VCTRL}
C {devices/lab_pin.sym} 570.0 -150.0 2 0 {name=l8 sig_type=std_logic lab=VCTRL }
N 570.0 -130.0 550.0 -130.0 {lab=VLPFZ}
C {devices/lab_pin.sym} 570.0 -130.0 2 0 {name=l9 sig_type=std_logic lab=VLPFZ }
