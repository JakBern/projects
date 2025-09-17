# Projects I Did During College

I don't usually use GitHub for any of my personal projects and since I've been handing out resumes recently I thought it would be prudent to make a repo to show them off.

## Table of Contents

## FPGA Synth in VHDL

This was a final project for a class. One of hte suggested projects was a "waveform generator", which made me want to create a full-fledged sequencer. I never finished the sequencing aspect or made a demo song to play off it, but the resulting project is a functional (albeit not very user-friendly) monophonic synthesizer on an FPGA. For all MIDI frequencies, it can output:
- Square waves (with pulse width modulation)
- Sawtooth waves (with incorrectly done pulse-width modulation)
- Triangle waves
- Sine waves
- Noise (which can change pitch, or can be more "metallic" and harsh sounding like the option on the NES noise channel)

Here's a video demonstrating it:
<video src="./VHDL_Synth/boardtest.mp4"/>
