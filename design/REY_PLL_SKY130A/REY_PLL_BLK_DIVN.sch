v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=CK}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=CKO0}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=CKO1}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=CKO2}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=CKO3}
C {devices/iopin.sym} 0 100 0 0 {name=p5 lab=CK_FB}
C {devices/iopin.sym} 0 120 0 0 {name=p6 lab=VDD_1V8}
C {devices/iopin.sym} 0 140 0 0 {name=p7 lab=VSS}
C {REY_PLL_SKY130A/REY_PLL_DIVN.sym} 400 0 0 0 {name=Xxdivn}
N 230.0 -90.0 250.0 -90.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 230.0 -90.0 0 0 {name=l0 sig_type=std_logic lab=VDD_1V8 }
N 230.0 -70.0 250.0 -70.0 {lab=VSS}
C {devices/lab_pin.sym} 230.0 -70.0 0 0 {name=l1 sig_type=std_logic lab=VSS }
N 230.0 -50.0 250.0 -50.0 {lab=CK}
C {devices/lab_pin.sym} 230.0 -50.0 0 0 {name=l2 sig_type=std_logic lab=CK }
N 570.0 -90.0 550.0 -90.0 {lab=CK_FB}
C {devices/lab_pin.sym} 570.0 -90.0 2 0 {name=l3 sig_type=std_logic lab=CK_FB }
N 570.0 -70.0 550.0 -70.0 {lab=CKO0}
C {devices/lab_pin.sym} 570.0 -70.0 2 0 {name=l4 sig_type=std_logic lab=CKO0 }
N 570.0 -50.0 550.0 -50.0 {lab=CKO1}
C {devices/lab_pin.sym} 570.0 -50.0 2 0 {name=l5 sig_type=std_logic lab=CKO1 }
N 570.0 -30.0 550.0 -30.0 {lab=CKO2}
C {devices/lab_pin.sym} 570.0 -30.0 2 0 {name=l6 sig_type=std_logic lab=CKO2 }
N 570.0 -10.0 550.0 -10.0 {lab=CKO3}
C {devices/lab_pin.sym} 570.0 -10.0 2 0 {name=l7 sig_type=std_logic lab=CKO3 }
