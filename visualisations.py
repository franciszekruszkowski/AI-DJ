import matplotlib.pyplot as plt
import numpy as np


def plot_waveform(audio, sr):
    # Compute the time values for the waveform
    times = np.linspace(0, len(audio) / sr, len(audio))

    # Create a figure
    plt.figure(figsize=(14, 5))
    plt.plot(times, audio, alpha=0.6)
    plt.ylim(-1, 1)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform')
    plt.show()


def plot_waveform_with_hot_cues(audio, sr, hot_cues):
    # Create a time array for the waveform
    duration = len(audio) / sr
    times = np.linspace(0, duration, len(audio))

    # Create the plot
    plt.figure(figsize=(14, 5))
    plt.plot(times, audio, alpha=0.6)

    # Plot the hot cues as vertical lines
    for hot_cue in hot_cues:
        plt.axvline(x=hot_cue, color='r')

    plt.ylim(-1, 1)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform with Hot Cues')
    plt.show()
