# AI-DJ
Master Thesis Project - AI-DJ

This project aims to create an AI DJ that uses machine learning algorithms to make music transitions, mimicking the style and techniques of a professional DJ.

We have made considerable progress so far in implementing the core functionalities of the AI DJ:

File Loading and Conversion: We have written a Python script to load audio files, convert them from MP3 to WAV format, and save the converted files. The files are stored in a specific directory on the user's system.

File Preprocessing: In this stage, we analyze the audio files to detect beats and downbeats, estimate the tempo, calculate the root mean square (RMS) transitions, filter out the indices that are close together and determine the cue points for transitions.

Mixing: We have started developing the functions for mixing two tracks. Currently, the transition between two tracks is achieved by a simple crossfading method, and we also adjust the BPM of the second track to match that of the first. While this approach is basic and the transitions may not always align perfectly, it provides a good starting point for our project.

The next steps of our project are to:

Improve the Sync Function: We will improve the function that adjusts the BPM of the second track to match that of the first track. This will involve syncing downbeats, beats, and the grid to achieve a more seamless blend between the two tracks.

Add EQ Features: We plan to add Equalizer (EQ) features to control the Low, Mid, and High frequencies of the tracks. This feature will allow us to cut out the bass (Lows) for 4, 8, or 16 bars, a common technique in DJing.

Create and Train a Machine Learning Model: We aim to build and train an Artificial Neural Network (ANN) that will learn how a transition is made. The ANN will be trained on examples of how the EQ knobs were moved in several mixes, seeking patterns of how EQs are changed and patterns of musical phrases of two tracks where the transition occurs.

Add Randomness: To ensure that every transition is unique, we plan to add an element of randomness. This could involve starting the transitions at different cue points, varying the length of the transitions, and changing the timestamps when the bass was swapped.

User Interface: Finally, we will create a simple interface where users can input a folder of files (in MP3 or WAV format), and the program will return a mix just like a DJ would record.

Through these steps, our project will simulate the intricate art of DJing, creating seamless transitions between tracks and providing an engaging experience for listeners. We aim to create a tool that can be useful for both experienced DJs and beginners alike, or anyone who wants to create a mix of their favourite songs.
