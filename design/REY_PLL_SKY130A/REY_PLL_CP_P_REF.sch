v {xschem version=3.0.0 file_version=1.2 }
G {}
K {}
V {}
S {}
E {}
C {devices/iopin.sym} 0 0 0 0 {name=p0 lab=VBN}
C {devices/iopin.sym} 0 20 0 0 {name=p1 lab=VBP}
C {devices/iopin.sym} 0 40 0 0 {name=p2 lab=VCTRL}
C {devices/iopin.sym} 0 60 0 0 {name=p3 lab=VDD_1V8}
C {devices/iopin.sym} 0 80 0 0 {name=p4 lab=VHI_N}
C {REY_ATR_SKY130A/REYATR_PCH_4C1F2.sym} 400 0 0 0 {name=Xxmph}
N 440.0 50.0 440.0 30.0 {lab=VCTRL}
C {devices/lab_pin.sym} 440.0 50.0 1 0 {name=l0 sig_type=std_logic lab=VCTRL }
N 380.0 0.0 400.0 0.0 {lab=VHI_N}
C {devices/lab_pin.sym} 380.0 0.0 0 0 {name=l1 sig_type=std_logic lab=VHI_N }
N 440.0 -50.0 440.0 -30.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 -50.0 3 0 {name=l2 sig_type=std_logic lab=VDD_1V8 }
N 460.0 0.0 440.0 0.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 460.0 0.0 2 0 {name=l3 sig_type=std_logic lab=VDD_1V8 }
C {REY_ATR_SKY130A/REYATR_LVT_PCH_4C5F0.sym} 400 170 0 0 {name=Xxmpn}
N 440.0 220.0 440.0 200.0 {lab=VBN}
C {devices/lab_pin.sym} 440.0 220.0 1 0 {name=l4 sig_type=std_logic lab=VBN }
N 380.0 170.0 400.0 170.0 {lab=VBP}
C {devices/lab_pin.sym} 380.0 170.0 0 0 {name=l5 sig_type=std_logic lab=VBP }
N 440.0 120.0 440.0 140.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 440.0 120.0 3 0 {name=l6 sig_type=std_logic lab=VDD_1V8 }
N 460.0 170.0 440.0 170.0 {lab=VDD_1V8}
C {devices/lab_pin.sym} 460.0 170.0 2 0 {name=l7 sig_type=std_logic lab=VDD_1V8 }
