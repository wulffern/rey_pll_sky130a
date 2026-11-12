
Tri-state phase frequency detector: two flops with D high, one clocked by
CK_REF (UP) and one by CK_FB (DN), cleared together when both are high.
The flop of the library clocks on NAND(CK, RN), so each reset is held by a
latch until that flop's own clock is low again. Drawn as the two columns
of the layout.
