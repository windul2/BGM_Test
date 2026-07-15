"""
Goal Survivor - NEON LAST STAND BGM (8D Edition)
Neon synthwave survival track, 132 BPM, E minor, loopable.
8D effect: sine-wave pan (CC10) rotation per track + reverb (CC91).
Requires: pip install midiutil
Output: bgm.mid
"""
import math
from midiutil import MIDIFile

BPM = 132
BARS = 24          # ~43.6s at 132bpm, seamless loop
BEATS_PER_BAR = 4

# Chord progression (repeats every 4 bars): Em - C - D - Bm
PROG = [
    ("Em", 40, [64, 67, 71]),
    ("C",  36, [60, 64, 67]),
    ("D",  38, [62, 66, 69]),
    ("Bm", 35, [59, 62, 66]),
]

mf = MIDIFile(4)  # tracks: 0=bass, 1=arp, 2=pad, 3=drums
for t in range(4):
    mf.addTempo(t, 0, BPM)


def add_pan_lfo(track, channel, period_bars, depth, phase=0.0, step=0.25):
    """8D rotation: sweep CC10 pan in a sine wave around the listener."""
    total = BARS * BEATS_PER_BAR
    period = period_bars * BEATS_PER_BAR
    t = 0.0
    while t < total:
        pan = int(64 + depth * math.sin(2 * math.pi * t / period + phase))
        mf.addControllerEvent(track, channel, t, 10, max(0, min(127, pan)))
        t += step


# --- Track 0: Driving synth bass (GM 39), channel 0 ---
mf.addProgramChange(0, 0, 0, 38)
mf.addControllerEvent(0, 0, 0, 91, 30)          # light reverb, keep punch
add_pan_lfo(0, 0, period_bars=8, depth=18)      # subtle slow sway
for bar in range(BARS):
    _, root, _ = PROG[bar % 4]
    for eighth in range(8):
        time = bar * BEATS_PER_BAR + eighth * 0.5
        note = root if eighth % 2 == 0 else root + 12
        vel = 110 if eighth % 2 == 0 else 90
        mf.addNote(0, 0, note, time, 0.45, vel)

# --- Track 1: 16th-note arpeggio (GM 81 Saw Lead), channel 1 ---
mf.addProgramChange(1, 1, 0, 81)
mf.addControllerEvent(1, 1, 0, 91, 80)          # heavy reverb = spatial depth
add_pan_lfo(1, 1, period_bars=2, depth=60, step=0.125)  # main 8D rotation
for bar in range(BARS):
    _, _, chord = PROG[bar % 4]
    seq = chord + [chord[0] + 12] + chord[::-1][:2]
    for i in range(16):
        time = bar * BEATS_PER_BAR + i * 0.25
        note = seq[i % len(seq)] + 12
        vel = 84 if i % 4 else 100
        mf.addNote(1, 1, note, time, 0.22, vel)

# --- Track 2: Warm pad (GM 89), channel 2 ---
mf.addProgramChange(2, 2, 0, 89)
mf.addControllerEvent(2, 2, 0, 91, 100)         # max reverb, ambient wash
add_pan_lfo(2, 2, period_bars=4, depth=45, phase=math.pi)  # counter-rotation
for bar in range(BARS):
    _, _, chord = PROG[bar % 4]
    time = bar * BEATS_PER_BAR
    for n in chord:
        mf.addNote(2, 2, n, time, BEATS_PER_BAR, 62)

# --- Track 3: Drums, channel 9 (center, anchors the mix) ---
KICK, SNARE, CLAP, CH, OH, CRASH = 36, 38, 39, 42, 46, 49
mf.addControllerEvent(3, 9, 0, 91, 40)
for bar in range(BARS):
    base = bar * BEATS_PER_BAR
    for beat in range(4):
        mf.addNote(3, 9, KICK, base + beat, 0.2, 118)
    for beat in (1, 3):
        mf.addNote(3, 9, SNARE, base + beat, 0.2, 104)
        mf.addNote(3, 9, CLAP,  base + beat, 0.2, 92)
    for eighth in range(8):
        t = base + eighth * 0.5
        if eighth % 2 == 1:
            mf.addNote(3, 9, OH, t, 0.2, 78)
        else:
            mf.addNote(3, 9, CH, t, 0.2, 66)
    if bar % 4 == 0:
        mf.addNote(3, 9, CRASH, base, 0.5, 100)

with open("bgm.mid", "wb") as f:
    mf.writeFile(f)

print(f"bgm.mid written: {BARS} bars @ {BPM} BPM "
      f"(~{BARS * BEATS_PER_BAR * 60 / BPM:.1f}s loop, 8D pan enabled)")

