*Master Thesis Project - AI-DJ*

The **AI-DJ** project is designed to create a virtual DJ that leverages machine learning algorithms to execute seamless musical transitions, just like a professional human DJ.

**Achievements So Far:**
Here are some of the core functionalities we have implemented in the AI-DJ project:

**File Loading and Conversion:**
Our Python script can load audio files, convert these from MP3 to WAV format, and save the converted files. All converted files are stored in a specified directory.

**File Preprocessing:**
At this stage, the audio files are analyzed to detect beats and downbeats, estimate the tempo, calculate the Root Mean Square (RMS) transitions, filter out closely located indices, and determine the cue points for transitions.

**Mixing:**
We have begun the process of developing functions for mixing two tracks. Currently, transitions between tracks are accomplished through a basic crossfading technique, and the Beats Per Minute (BPM) of the second track is adjusted to match the first track. This approach provides a good starting point, although the transitions may not be perfectly aligned at all times.

**What Next? Project Roadmap:**
The following steps have been outlined to further develop and refine the AI-DJ project:

**Improve the Sync Function:**
We plan to enhance the function that adjusts the BPM of the second track to match the first. This will include syncing downbeats, beats, and the grid to achieve a smoother blend between two tracks.

**Add EQ Features:**
We aim to add Equalizer (EQ) features that allow for control of the Low, Mid, and High frequencies of the tracks. This will enable us to cut out the bass (Lows) for specific time frames (4, 8, or 16 bars), emulating a common DJing technique.

**Create and Train a Machine Learning Model:**
Our goal is to build and train an Artificial Neural Network (ANN) that will understand how a transition is made. The ANN will be trained using examples of how EQ knobs were manipulated in several mixes, seeking patterns in EQ changes and patterns of musical phrases in two tracks where transitions occur.

**Add Randomness:**
To ensure each transition is unique, we plan to incorporate an element of randomness. This may include starting transitions at different cue points, altering the length of transitions, and varying timestamps when the bass is swapped.

**User Interface:**
Finally, we aim to design a user-friendly interface where users can input a folder of files (MP3 or WAV format), and the program will return a mix, much like a traditional DJ set recording.

With these steps, the AI-DJ project aims to simulate the intricate art of DJing, creating seamless transitions between tracks and offering an engaging listener experience. Our ultimate goal is to create a tool that can be of value to both experienced DJs and beginners, or anyone wanting to create a mix of their favorite songs.
