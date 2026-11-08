v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=VCTRL}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=VDD_1V8}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=VLPFZ}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=VSS}
C {REY_PLL_SKY130A/REY_PLL_LPF.sym} 400 0 0 0 {name=Xxlpf}
N 250.0 -90.0 250.0 -70.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 250.0 -90.0 3 0 {name=l0 sig_type=std_logic lab=VDD_1V8 }
N 250.0 -70.0 250.0 -50.0 {lab=VSS}
C {devices/lab_pin.sym} 250.0 -70.0 3 0 {name=l1 sig_type=std_logic lab=VSS }
N 250.0 -10.0 250.0 -30.0 {lab=VCTRL}
C {devices/lab_pin.sym} 250.0 -10.0 1 0 {name=l2 sig_type=std_logic lab=VCTRL }
N 250.0 10.0 250.0 -10.0 {lab=VLPFZ}
C {devices/lab_pin.sym} 250.0 10.0 1 0 {name=l3 sig_type=std_logic lab=VLPFZ }
