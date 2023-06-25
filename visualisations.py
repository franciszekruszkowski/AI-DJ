import matplotlib.pyplot as plt


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


def plot_waveform_with_downbeats(audio, sr, downbeats):
    # Compute the time values for the waveform
    times = np.linspace(0, len(audio) / sr, len(audio))

    # Create a figure
    plt.figure(figsize=(14, 5))
    plt.plot(times, audio, alpha=0.6)

    # Plot the detected downbeats as vertical lines
    for downbeat in downbeats:
        plt.axvline(x=downbeat[0], color='r')

    plt.ylim(-1, 1)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform with Detected Downbeats')
    plt.show()


def plot_waveform_with_cue_points(audio, sr, cue_points):
    # Compute the time values for the waveform
    times = np.linspace(0, len(audio) / sr, len(audio))

    # Create a figure
    plt.figure(figsize=(14, 5))
    plt.plot(times, audio, alpha=0.6)

    # Plot the cue points as vertical lines
    for cue_point in cue_points:
        plt.axvline(x=cue_point, color='g')

    plt.ylim(-1, 1)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform with Detected Cue Points')
    plt.show()