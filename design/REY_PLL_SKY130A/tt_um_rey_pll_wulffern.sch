v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {tt_um_rey_pll_wulffern: REY_PLL in a Tiny Tapeout tile} -1450 -820 0 0 0.5 0.5 {}
C {devices/opin.sym} -1400 -740 0 0 {name=p0 lab=uio_oe[7:0]}
C {devices/ipin.sym} -1200 -740 0 0 {name=p1 lab=VDPWR}
C {devices/ipin.sym} -1040 -740 0 0 {name=p2 lab=VGND}
C {devices/ipin.sym} -880 -740 0 0 {name=p3 lab=ui_in[7:0]}
C {devices/ipin.sym} -720 -740 0 0 {name=p4 lab=uio_in[7:0]}
C {devices/ipin.sym} -560 -740 0 0 {name=p5 lab=ena}
C {devices/ipin.sym} -400 -740 0 0 {name=p6 lab=rst_n}
C {devices/ipin.sym} -240 -740 0 0 {name=p7 lab=clk}
C {devices/opin.sym} -80 -740 0 0 {name=p8 lab=uo_out[7:0]}
C {devices/opin.sym} 80 -740 0 0 {name=p9 lab=uio_out[7:0]}
C {REY_PLL_SKY130A/REY_PLL.sym} -1000 -400 0 0 {name=x1}
C {devices/lab_pin.sym} -1150 -570 0 0 {name=l1 sig_type=std_logic lab=VDPWR}
C {devices/lab_pin.sym} -1150 -550 0 0 {name=l2 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} -1150 -510 0 0 {name=l3 sig_type=std_logic lab=clk}
C {devices/lab_pin.sym} -1150 -530 0 0 {name=l4 sig_type=std_logic lab=ui_in[0]}
C {devices/lab_pin.sym} -1150 -490 0 0 {name=l5 sig_type=std_logic lab=ui_in[1]}
C {devices/lab_pin.sym} -1150 -470 0 0 {name=l6 sig_type=std_logic lab=ui_in[2]}
C {devices/lab_pin.sym} -1150 -450 0 0 {name=l7 sig_type=std_logic lab=ui_in[3]}
C {devices/lab_pin.sym} -1150 -430 0 0 {name=l8 sig_type=std_logic lab=ui_in[4]}
C {devices/lab_pin.sym} -1150 -410 0 0 {name=l9 sig_type=std_logic lab=ui_in[5]}
C {devices/lab_pin.sym} -850 -550 2 0 {name=l10 sig_type=std_logic lab=uo_out[0]}
C {devices/lab_pin.sym} -850 -530 2 0 {name=l11 sig_type=std_logic lab=uo_out[1]}
C {devices/lab_pin.sym} -850 -510 2 0 {name=l12 sig_type=std_logic lab=uo_out[2]}
C {devices/lab_pin.sym} -850 -490 2 0 {name=l13 sig_type=std_logic lab=uo_out[3]}
T {Antenna diodes on the inputs} -1400 20 0 0 0.4 0.4 {}
C {sky130_fd_pr/diode.sym} -1300 150 0 0 {name=D0 model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 spiceprefix=X}
C {devices/lab_pin.sym} -1300 180 3 0 {name=l14 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} -1300 120 1 0 {name=l15 sig_type=std_logic lab=clk}
C {sky130_fd_pr/diode.sym} -1080 150 0 0 {name=D1 model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 spiceprefix=X}
C {devices/lab_pin.sym} -1080 180 3 0 {name=l16 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} -1080 120 1 0 {name=l17 sig_type=std_logic lab=ui_in[0]}
C {sky130_fd_pr/diode.sym} -860 150 0 0 {name=D2 model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 spiceprefix=X}
C {devices/lab_pin.sym} -860 180 3 0 {name=l18 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} -860 120 1 0 {name=l19 sig_type=std_logic lab=ui_in[1]}
C {sky130_fd_pr/diode.sym} -640 150 0 0 {name=D3 model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 spiceprefix=X}
C {devices/lab_pin.sym} -640 180 3 0 {name=l20 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} -640 120 1 0 {name=l21 sig_type=std_logic lab=ui_in[2]}
C {sky130_fd_pr/diode.sym} -420 150 0 0 {name=D4 model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 spiceprefix=X}
C {devices/lab_pin.sym} -420 180 3 0 {name=l22 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} -420 120 1 0 {name=l23 sig_type=std_logic lab=ui_in[3]}
C {sky130_fd_pr/diode.sym} -200 150 0 0 {name=D5 model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 spiceprefix=X}
C {devices/lab_pin.sym} -200 180 3 0 {name=l24 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} -200 120 1 0 {name=l25 sig_type=std_logic lab=ui_in[4]}
C {sky130_fd_pr/diode.sym} 20 150 0 0 {name=D6 model=diode_pw2nd_05v5 area=2.025e11 perim=1.8e6 spiceprefix=X}
C {devices/lab_pin.sym} 20 180 3 0 {name=l26 sig_type=std_logic lab=VGND}
C {devices/lab_pin.sym} 20 120 1 0 {name=l27 sig_type=std_logic lab=ui_in[5]}
T {Outputs nothing drives, tied low through a metal resistor each} -1400 300 0 0 0.4 0.4 {}
C {sky130_fd_pr/res_generic_m4.sym} -1300 520 0 0 {name=R0[7:0] W=0.3 L=0.3 model=res_generic_m4 mult=1}
C {devices/lab_pin.sym} -1300 490 1 0 {name=l28 sig_type=std_logic lab=uio_oe[7:0]}
C {devices/lab_pin.sym} -1300 550 3 0 {name=l29 sig_type=std_logic lab=VGND}
C {sky130_fd_pr/res_generic_m4.sym} -1000 520 0 0 {name=R1[7:0] W=0.3 L=0.3 model=res_generic_m4 mult=1}
C {devices/lab_pin.sym} -1000 490 1 0 {name=l30 sig_type=std_logic lab=uio_out[7:0]}
C {devices/lab_pin.sym} -1000 550 3 0 {name=l31 sig_type=std_logic lab=VGND}
C {sky130_fd_pr/res_generic_m4.sym} -700 520 0 0 {name=R2[3:0] W=0.3 L=0.3 model=res_generic_m4 mult=1}
C {devices/lab_pin.sym} -700 490 1 0 {name=l32 sig_type=std_logic lab=uo_out[7:4]}
C {devices/lab_pin.sym} -700 550 3 0 {name=l33 sig_type=std_logic lab=VGND}
P 4 5 -1490 -860 240 -860 240 650 -1490 650 -1490 -860 {dash=4}
