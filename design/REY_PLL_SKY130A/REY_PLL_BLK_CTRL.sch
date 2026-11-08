v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=KICK}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=OLH}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=OLL}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=PWRUP_1V8}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=VDD_1V8}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=VHI_N}
C {devices/iopin.sym} 0 120 0 0 {name=p6 lab=VLO}
C {devices/iopin.sym} 0 140 0 0 {name=p7 lab=VSS}
C {REY_PLL_SKY130A/REY_PLL_CTRL.sym} 400 0 0 0 {name=Xxctrl}
N 230.0 -90.0 250.0 -90.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 230.0 -90.0 0 0 {name=l0 sig_type=std_logic lab=VDD_1V8 }
N 230.0 -70.0 250.0 -70.0 {lab=VSS}
C {devices/lab_pin.sym} 230.0 -70.0 0 0 {name=l1 sig_type=std_logic lab=VSS }
N 230.0 -50.0 250.0 -50.0 {lab=PWRUP_1V8}
C {devices/lab_pin.sym} 230.0 -50.0 0 0 {name=l2 sig_type=std_logic lab=PWRUP_1V8 }
N 230.0 -30.0 250.0 -30.0 {lab=OLH}
C {devices/lab_pin.sym} 230.0 -30.0 0 0 {name=l3 sig_type=std_logic lab=OLH }
N 230.0 -10.0 250.0 -10.0 {lab=OLL}
C {devices/lab_pin.sym} 230.0 -10.0 0 0 {name=l4 sig_type=std_logic lab=OLL }
N 570.0 -90.0 550.0 -90.0 {lab=KICK}
C {devices/lab_pin.sym} 570.0 -90.0 2 0 {name=l5 sig_type=std_logic lab=KICK }
N 570.0 -70.0 550.0 -70.0 {lab=VHI_N}
C {devices/lab_pin.sym} 570.0 -70.0 2 0 {name=l6 sig_type=std_logic lab=VHI_N }
N 570.0 -50.0 550.0 -50.0 {lab=VLO}
C {devices/lab_pin.sym} 570.0 -50.0 2 0 {name=l7 sig_type=std_logic lab=VLO }
