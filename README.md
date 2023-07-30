# Master Thesis Project - AI-DJ

The **AI-DJ** project is designed to create a virtual DJ that leverages machine learning algorithms to execute seamless musical transitions, just like a professional human DJ.

## Achievements So Far

Here are some of the core functionalities we have implemented in the AI-DJ project:

### File Loading and Conversion

Our Python script can load audio files, convert them from MP3 to WAV format, and save the converted files. All converted files are stored in a specified directory.

### File Preprocessing

At this stage, the audio files are analyzed to detect beats and downbeats, estimate the tempo, calculate the Root Mean Square (RMS) transitions, filter out closely located indices, and determine the cue points for transitions.

### Track Analysis and Visualisations

We have created a `track.py` class for handling track analysis tasks, such as BPM detection and beat grid placement. It also provides functions to generate visualisations of the audio data, which can be helpful for debugging and verification of the analysis results.

### Tempo Adjustment and Mixing

We have developed the functionality to adjust the tempo of tracks to match each other, allowing for smooth transitions. The transitions between tracks are accomplished through a basic crossfading technique.

### Equalization (EQ)

The EQ adjustment is implemented to control the Low, Mid, and High frequencies of the tracks during transition. This allows us to cut out the bass (Lows) for specific time frames (4, 8, or 16 bars), emulating a common DJing technique.

### Mixing

Successful mixing between two tracks, including beatmatching with correctly adjusted BPMs and EQ adjustments, has been implemented. A simple crossfade function is also in place for smooth transitions.

## What's Next? Project Roadmap

The following steps have been outlined to further develop and refine the AI-DJ project:

### Improve the Sync Function

This will include syncing downbeats, beats, and the grid to achieve a smoother blend between two tracks. We aim to improve the function so that it detects the optimal bars in beats more effectively and self-corrects if minor adjustments are necessary.

### Add Randomness

To ensure each transition is unique, we plan to incorporate an element of randomness. This may include starting transitions at different cue points, altering the length of transitions, and varying timestamps when the bass is swapped.

### User Interface

Finally, we aim to design a user-friendly interface where users can input a folder of files (MP3 or WAV format), and the program will return a mix, much like a traditional DJ set recording.

With these steps, the AI-DJ project aims to simulate the intricate art of DJing, creating seamless transitions between tracks and offering an engaging listener experience. Our ultimate goal is to create a tool that can be of value to both experienced DJs and beginners, or anyone wanting to create a mix of their favorite songs.
