"""
Goal Survivor - NEON LAST STAND BGM
Neon synthwave survival track, 132 BPM, E minor, loopable.
Requires: pip install midiutil
Output: bgm.mid
"""
from midiutil import MIDIFile

BPM = 132
BARS = 24          # ~43.6s at 132bpm, seamless loop
BEATS_PER_BAR = 4

# Chord progression (repeats every 4 bars): Em - C - D - Bm
# Root notes (MIDI): E2=40, C2=36, D2=38, B1=35
PROG = [
    ("Em", 40, [64, 67, 71]),   # E4 G4 B4
    ("C",  36, [60, 64, 67]),   # C4 E4 G4
    ("D",  38, [62, 66, 69]),   # D4 F#4 A4
    ("Bm", 35, [59, 62, 66]),   # B3 D4 F#4
]

mf = MIDIFile(4)  # tracks: 0=bass, 1=arp, 2=pad, 3=drums
for t in range(4):
    mf.addTempo(t, 0, BPM)

# --- Track 0: Driving synth bass (GM 39 Synth Bass 2), channel 0 ---
mf.addProgramChange(0, 0, 0, 38)
for bar in range(BARS):
    _, root, _ = PROG[bar % 4]
    for eighth in range(8):  # pumping 8th notes
        time = bar * BEATS_PER_BAR + eighth * 0.5
        # octave jump on offbeats for neon drive
        note = root if eighth % 2 == 0 else root + 12
        vel = 110 if eighth % 2 == 0 else 90
        mf.addNote(0, 0, note, time, 0.45, vel)

# --- Track 1: 16th-note arpeggio (GM 81 Saw Lead), channel 1 ---
mf.addProgramChange(1, 1, 0, 81)
for bar in range(BARS):
    _, _, chord = PROG[bar % 4]
    # arp pattern: up-down across chord + octave
    seq = chord + [chord[0] + 12] + chord[::-1][:2]
    for i in range(16):
        time = bar * BEATS_PER_BAR + i * 0.25
        note = seq[i % len(seq)] + 12  # one octave up, cutting lead
        vel = 84 if i % 4 else 100     # accent each beat
        mf.addNote(1, 1, note, time, 0.22, vel)

# --- Track 2: Warm pad (GM 89 Pad 2 Warm), channel 2 ---
mf.addProgramChange(2, 2, 0, 89)
for bar in range(BARS):
    _, _, chord = PROG[bar % 4]
    time = bar * BEATS_PER_BAR
    for n in chord:
        mf.addNote(2, 2, n, time, BEATS_PER_BAR, 62)

# --- Track 3: Drums, channel 9 (GM percussion) ---
KICK, SNARE, CLAP, CH, OH, CRASH = 36, 38, 39, 42, 46, 49
for bar in range(BARS):
    base = bar * BEATS_PER_BAR
    # four-on-the-floor kick
    for beat in range(4):
        mf.addNote(3, 9, KICK, base + beat, 0.2, 118)
    # snare + clap on 2 & 4
    for beat in (1, 3):
        mf.addNote(3, 9, SNARE, base + beat, 0.2, 104)
        mf.addNote(3, 9, CLAP,  base + beat, 0.2, 92)
    # 8th hats, open hat on offbeats
    for eighth in range(8):
        t = base + eighth * 0.5
        if eighth % 2 == 1:
            mf.addNote(3, 9, OH, t, 0.2, 78)
        else:
            mf.addNote(3, 9, CH, t, 0.2, 66)
    # crash at each 4-bar section start
    if bar % 4 == 0:
        mf.addNote(3, 9, CRASH, base, 0.5, 100)

with open("bgm.mid", "wb") as f:
    mf.writeFile(f)

print(f"bgm.mid written: {BARS} bars @ {BPM} BPM "
      f"(~{BARS * BEATS_PER_BAR * 60 / BPM:.1f}s loop)")
