---
layout: page
title: How It Was Made
---

REY_PLL was made by an AI agent (Claude Code) and one human, Carsten
Wulff, between the evening of 7 November and the morning of 12 November
2026. The human talked, mostly by voice and often while the agent was
still working. The agent drew the schematics, wrote the generators and
the layout scripts, ran the simulations and the checks, and wrote the
documentation, this page included.

This page is the record of that: what came out, what was said each day,
and where the human's words changed the course. Every prompt is here.

The same story as a deck of 16 slides: [slides.pdf](slides.pdf).

## What got built

| What                   | Result                                                                     |
|:-----------------------|:---------------------------------------------------------------------------|
| Circuit                | PLL: PFD, charge pump, loop filter, 7 stage current starved ring oscillator with a Vgs/R bias and 3 bit trim, divider, control |
| Core, `REY_PLL`        | 156.96 x 106.94 um                                                         |
| Tiny Tapeout wrapper   | `tt_um_rey_pll_wulffern`, one 161 x 111.52 um tile                          |
| Checks                 | DRC (magic and KLayout) and LVS clean on core and wrapper, antenna clean on the wrapper |
| Frequency              | Locks at 128 MHz from 8 MHz. The goal was 512 MHz                           |
| Corners                | The extracted layout locks in typical and in all 20 corners                 |
| Repository             | 33 commits, 7 to 12 November                                                |
| Tools                  | 12 commits in [cicpy](https://github.com/wulffern/cicpy), one in the shared sky130A flow |

The design itself is described in the
[README](https://github.com/wulffern/rey_pll_sky130a#readme) and on the
[documentation pages](https://analogicus.com/rey_pll_sky130a/).

## Day by day, with every prompt

The prompts are as they were typed or dictated. Dictation mishears the
names of things, so where a word came out wrong the meaning is in
*[brackets]*. "While working" marks a message sent while the agent was in
the middle of something.

### 7 November: an oscillator

The start was one sentence and a figure from a lecture. The agent asked
two things before it began, then built the oscillator and a Python model
of the loop.

> let's start a rey_pll variant of sun_pll I want to replace the oscillator with https://analogicus.com/aic2027/assets/media/osc_ring_adv_tikz.svg

The agent asked how to build it, and what to do about the new
oscillator's negative Kvco (a higher control voltage makes it slower).
The answers picked from its lists were "rey_pll_sky130a, ROSC first" and
"Swap UP/DN at the CP".

> and let's skip the ota buffer

(while working)

> go ahead, set the use the mirror to set the current, and maybe we should have a trimmed resistor or something. Could be trimmed by a

> added https://github.com/wulffern/rey_pll_sky130a

(while working)

> I want a prime number of stages, so 5 is fine, but also 7.

(while working)

> We could just make the ring oscillator transistors longer, particularly the NMOS. Use a different ray transistor *[rey transistor]*, the 5F0 for example. And for the bias trim, we could just use a configurable resistor. So the RPPO, and then connect that to the bias, and then figure out how to trim the current by switches or something.

### 8 November: bias, loop, generators and the first layouts

The longest day, 17 commits. In the morning the bias became a Vgs/R
bias so the frequency holds over temperature, the loop filter was
turned around to VDD, and the loop model sized the filter for a Tiny
Tapeout tile. The loop filter became a generated unit cell, a MiM
capacitor on top of a poly resistor. In the afternoon the rest of the
PLL was ported from sun_pll as a generator (`py/gen_pll.py`), the
schematic locked at 512 MHz, and by the evening five of the blocks had
layouts that were DRC and LVS clean. The top did not: the first
placement shorted the supplies.

> Let's try a GM cell.

> So if the V control is referenced to VDD, we also need to flip the loop filter so it's referenced to VDD. While you wait for the sims, you could also figure out how to do the layout using CSEPy *[cicpy]*.

> I also want to see if we can change it to fit inside a tiny table tile *[Tiny Tapeout tile]*, which means that we need to maybe make the loop filter smaller, which means that we maybe need to change the KVCO. So yeah, have a look at also the Python model to make sure that we compute the loop filter components before we actually start modifying them.

(while working)

> Yeah, I'm going to go for 512. Yeah, go make the changes. Yeah, maybe we should commit and push. And then... No, we should get it to work in the slow corner first. We should consider whether we do some sort of PVT tracking. So that means that it's probably okay to say that whatever... Yeah, no, it would be nice to not bother with PVT tracking over temperature. It would be nice if we can actually get it to work over temperature.

> Commit, push, and make it robust.

> While that's going on, maybe update the documentation and describe the schematics, and then commit and push. And then you can start working on the layout, figure out how it's going to work with the tiles and so on. You can have a look at lilo underscore temp *[lelo_temp]* for the tile

> / I want the UALs *[the uo_out pins]* to actually cover all the different, or as many different dividers as we can.

> Yeah, I think we need the loop filter capacitors needs to be a mem *[MiM]*. Currently, it's actually a mom *[MOS capacitor]*. So, we should use a mem instead.

(while working)

> You could always generate a CIC version of resistor and capacitor on top as a unit cell, right? So then we could more easily get this stacked thing and maybe reduce the size, but we can make a custom variant of the cap X1 that has a bit more unit capacitors. We can see how CIC generates them, and we can use CIC pi *[cicpy]* for that. So just make custom stuff, that's okay. But make sure it's compiled and using CIC pi.

> And also make the schematics pretty so it's easier to read by a human. But continue.

> Yeah. Make sure that you don't use any absolute routes. And also, for the automatic routes, if it's creating DRCers *[DRC errors]*, we should really fix CRCPy *[cicpy]*.

> keep working on the layout, but I think you also should port all the features from some TLL *[sun_pll]*, so we have that, and we can see that the total flow matches the tile.

> Maybe we should build that into CI/CPy *[cicpy]*, the schematic helper.

(while working. It is `cicpy.eda.schgen` now.)

> Let's have a look at the top layout. Yeah, go ahead and push.

> You have to modify the schematic for the div n. The names need to be correct.

(while working)

> So it looks like the ground connections is what shorts everything. So you probably need to route that by hand. We should also look into whether we can, I don't know, modify the RC layout or something, because there's quite a bit of white space in the system.

> And get all the sub-blocks clean before we proceed to the top level.

(while working)

> Go ahead. There's also a route ring that's possible to use to get out of hard situations.

### 9 November: small cells first

The oscillator had been laid out as one flat cell and after a day it
was still not clean. The first prompt of the day changed the method: one ring stage
as its own cell, then the bias as its own cell, then the oscillator
from the finished pieces. All three were clean by the evening.

> So in general, the actually maybe we have to lay out the inverter by itself first. Do that. Lay out the inverter first. General for layout, you have to combine it. Have a look at Lilo temp *[lelo_temp]* also. You have to combine it into groups, and then those groups has to be routed, and then further up can be routed.

> continue

> use a local tech file, leave the shared one alone

(while working. The agent had just added a rule to the technology file
that every IP shares. It took the rule out again and gave the PLL its
own copy.)

> contine

> the bias looks like the split should be vertical

(while working)

> Let's try and finish the top level first and see if we can get it clean. Then we can look into how to reduce the size.

> Show me how the top looks

(while working)

### 10 November: the top, clean but too big

The top came together DRC and LVS clean, at 209 x 155 um. The tile is
161 x 111.52, and the blocks alone were 15 511 um2, 86 % of it. The agent asked what to give
up, squeeze the blocks, drop divider taps, or take a second tile, and
the answer picked was "Squeeze, taps last".

> go

> save handoff

> Continue

> Continue.

### 11 November: one tile, and the wrong frequency

The top was floorplanned again and fit one tile. Squeezing was not
enough, so the divider went from ten flops and eight taps to six and
four, and half of the output pins are tied low. The Tiny Tapeout
wrapper was generated. Then the layout was extracted and simulated for
the first time, and it did not lock: with its wiring the oscillator is
2.4 times slower than its schematic and no trim code reaches 512 MHz.
The agent laid out three ways on: 128 MHz with the oscillator untouched,
256 MHz with a faster oscillator, or 512 MHz with a new one.

> Continue.

> continue

> continue

> Maybe we need to change the frequency.

(while working)

> Yeah, let's do option one first and get it DRC all guys clean and clean *[DRC and LVS clean]*.

> Show me a picture of the current layout

> commit push.

> Update the documentation while we wait and make sure to add all the schematics to the info page. Also, have a look at the schematics and see if we should make them more readable.

### 12 November: the flow

The corner runs finished: the extracted layout locks at 128 MHz in all
of them. The LVS workflow on GitHub still failed, on a crash in netgen
during `make lpe`. It was worked around in this repository first, and
then the shared flow got the hook that makes the workaround a setting.

> continue

> Yeah, have a look at the ZILBS folder.

(The agent had just offered to dig into the failing LVS workflow, and
took it as a yes.)

> This sounds like something we should fix in the central repository in Sky 138 *[tech_sky130A]*.

That is all of them: 46 prompts and three answers to questions,
897 words. Nine of the prompts are "continue" or "go". Left out
are the commands to the tool itself (permissions, compacting the
conversation).

## What the human decided

Most of the words above are permission to carry on. A few of them are
why the design looks as it does:

- **The architecture**: the lecture's current starved oscillator, no OTA
  buffer, a prime number of stages, longer transistors, a resistor that
  switches for trim.
- **No PVT tracking**: it should just work over temperature. That is
  where the Vgs/R bias comes from.
- **One Tiny Tapeout tile**, said on the second morning, before any
  layout. It set the loop filter, the Kvco and in the end the floorplan.
- **MiM over poly as a generated unit cell** for the loop filter.
- **The layout method**: no absolute coordinates, supplies by hand, small
  cells clean before the level above, groups routed before the groups of
  groups. The oscillator only came clean after this was said.
- **Fix the tool, not the design**: when an automatic route made a DRC
  error the fix went into cicpy, and the schematic generator went there
  too.
- **Leave the shared technology alone** for anything that is only this
  design's problem, and fix it there when it is everybody's.
- **128 MHz**: when the extracted layout turned out too slow, take the
  frequency that works and get it clean, rather than open the
  oscillator again.

## What was hard

- **The supplies.** The library cells and the guard rings stand a little
  outside their boxes, so blocks placed edge to edge shorted VDD to VSS.
  The first top placement was one short.
- **The oscillator as one cell.** Flat, it was not clean after a day.
  As a stage, a bias and a top that only routes between them, it was
  clean the next evening.
- **The tile.** The blocks filled 86 % of it before a single wire
  between them. The blocks of the top row lost their own supply rings,
  the phase detector was redone as two mirrored columns, and four of the
  eight divider taps went.
- **The parasitics, found late.** The oscillator was never simulated
  extracted until the top was finished. About 10 fF of wiring on every
  ring node, more than the devices' own load, cost a factor of four in
  the output frequency. This is the mistake of the project, and it is
  the agent's: the check was cheap and the order was wrong.
- **netgen.** The comparison at the end of `make lpe` crashed on a
  ladder of poly resistors, in the code that merges resistors in
  series. A local setup file turns the merging off for that device.

## Honest status

- It locks at 128 MHz, not 512. Getting back needs about 2.4 times the
  current in the ring stages, or fewer stages. Not started.
- The loop filter is the one sized for 512 MHz. At 128 MHz the phase
  margin is 20 to 38 degrees by hand calculation. The corner runs show
  lock, not margin.
- The trim codes are from the schematic sweep. The oscillator has not
  been swept extracted over all corners.
- Nothing is taped out and nothing is measured. There is no tapeout
  submodule yet, so the Tiny Tapeout precheck has not been run.
- The netgen crash is avoided, not reported.

The details are in
[plans/HANDOFF.md](https://github.com/wulffern/rey_pll_sky130a/blob/main/plans/HANDOFF.md).
