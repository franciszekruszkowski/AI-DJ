"""
This module provides functions for adjusting the EQ of audio tracks.
"""

import math
import numpy as np
import yodel.filter


def lin2db(linval):
    """Converts a linear value to decibels."""
    if linval > 1e-5:
        return 20.0 * math.log10(linval)
    else:
        return -100.0


def db2lin(dbval):
    """Converts a decibel value to linear scale."""
    return math.pow(10, dbval / 20.0)


def adjust_highs(audio, sr, gain_db):
    """Adjusts the high frequencies of an audio signal."""
    # High shelf filter starting from 2kHz
    filter_obj = yodel.filter.Biquad()
    filter_obj.high_shelf(sr, 2000, 1, gain_db)  # 2000 Hz
    output = np.zeros_like(audio)
    filter_obj.process(audio, output)
    return output


def adjust_lows(audio, sr, gain_db):
    """Adjusts the low frequencies of an audio signal."""
    # Low shelf filter ending at 500Hz
    filter_obj = yodel.filter.Biquad()
    filter_obj.low_shelf(sr, 500, 1, gain_db)  # 500 Hz
    output = np.zeros_like(audio)
    filter_obj.process(audio, output)
    return output


def adjust_audio(audio, sr, gains):
    """
    Adjusts the EQ of an audio signal.

    Args:
        audio: The audio signal as a numpy array.
        sr: The sample rate of the audio signal.
        gains: A list of two values specifying the gains for low and high frequencies.

    Returns:
        The adjusted audio signal.
    """
    # Convert gains to dB
    gain_lows_db = 20 * np.log10(gains[0]) if gains[0] > 0 else -np.inf
    gain_highs_db = 20 * np.log10(gains[1]) if gains[1] > 0 else -np.inf

    # Adjust audio using the defined gains
    audio = adjust_lows(audio, sr, gain_lows_db)
    audio = adjust_highs(audio, sr, gain_highs_db)

    # Rescale audio to be within [-1, 1]
    max_val = np.max(np.abs(audio))
    if max_val != 0:
        audio = audio / max_val

    return audio


def rapid_eq(audio, sr, gains, cue_times, chunk_size=44100):
    """Applies rapid EQ changes to an audio signal."""
    # Calculate the cue samples
    cue_samples = [int(t * sr) for t in cue_times]

    # Create a new array to hold the processed audio
    processed_audio = np.zeros_like(audio)

    # Apply the EQ changes in chunks
    for i in range(len(cue_samples) - 1):
        # Calculate the slope of the EQ change for this period
        slope_lows = (gains[i + 1][0] - gains[i][0]) / (cue_samples[i + 1] - cue_samples[i])
        slope_highs = (gains[i + 1][1] - gains[i][1]) / (cue_samples[i + 1] - cue_samples[i])

        for j in range(cue_samples[i], cue_samples[i + 1], chunk_size):
            # Calculate the current time in seconds
            current_time = j / sr

            # Calculate the current gains
            current_gain_lows = gains[i][0] + slope_lows * (current_time - cue_times[i])
            current_gain_highs = gains[i][1] + slope_highs * (current_time - cue_times[i])

            # Ensure the gains never drop below a small positive value
            current_gain_lows = max(current_gain_lows, 0.01)
            current_gain_highs = max(current_gain_highs, 0.01)

            # Calculate the chunk end sample
            end_j = min(j + chunk_size, len(audio))

            # Apply the EQ changes
            processed_audio[j:end_j] = adjust_audio(audio[j:end_j], sr, [current_gain_lows, current_gain_highs])

    # After the last cue time, keep the EQ changes at the last gains
    if cue_samples[-1] < len(audio):
        processed_audio[cue_samples[-1]:] = adjust_audio(audio[cue_samples[-1]:], sr, gains[-1])

    return processed_audio


def sigmoid(x):
    """Sigmoid function."""
    return 1 / (1 + np.exp(-x))


def smooth_eq(audio, sr, gains, cue_times, chunk_size=44100):
    """Applies smooth EQ changes to an audio signal."""
    # Calculate the cue samples
    cue_samples = [int(t * sr) for t in cue_times]

    # Create a new array to hold the processed audio
    processed_audio = np.zeros_like(audio)

    # Apply the EQ changes in chunks
    for i in range(len(cue_samples) - 1):
        # Calculate the length of the transition in samples
        transition_length = cue_samples[i + 1] - cue_samples[i]

        for j in range(cue_samples[i], cue_samples[i + 1], chunk_size):
            # Calculate the proportion of the transition that has elapsed,
            # adjusted to go from -2 to 2 rather than from 0 to 1
            transition_progress = 4 * (j - cue_samples[i]) / transition_length - 2

            # Use the sigmoid function to calculate the current gains
            current_gain_lows = gains[i][0] + (gains[i + 1][0] - gains[i][0]) * sigmoid(transition_progress)
            current_gain_highs = gains[i][1] + (gains[i + 1][1] - gains[i][1]) * sigmoid(transition_progress)

            # Ensure the gains never drop below a small positive value
            current_gain_lows = max(current_gain_lows, 0.01)
            current_gain_highs = max(current_gain_highs, 0.01)

            # Calculate the chunk end sample
            end_j = min(j + chunk_size, len(audio))

            # Apply the EQ changes
            processed_audio[j:end_j] = adjust_audio(audio[j:end_j], sr, [current_gain_lows, current_gain_highs])

    # After the last cue time, keep the EQ changes at the last gains
    if cue_samples[-1] < len(audio):
        processed_audio[cue_samples[-1]:] = adjust_audio(audio[cue_samples[-1]:], sr, gains[-1])

    return processed_audio


def beats_to_seconds(bpm, beats):
    """Converts beats to seconds based on the given beats per minute."""
    beats_per_second = bpm / 60
    seconds = beats / beats_per_second
    return seconds


def normalize_audio_gain(audio, target=-10):
    """Normalizes the gain of an audio signal."""
    # Calculate the current gain of the audio
    rgain = 10 * np.log10(np.mean(audio**2))

    # Calculate the normalization factor
    factor = 10**((-(target - rgain)/10.0) / 2.0) # Divide by 2 because we want sqrt (amplitude^2 is energy)

    # Normalize the audio
    audio_normalized = audio * factor

    return audio_normalized


def create_eq_adjusted_tracks(track1, track2, t1_bass, t2_bass, sr):
    """Create EQ adjusted versions of two tracks."""
    # Define the gains and cue times for track1 (the master)
    gains1_bass = [[1, 1], [0.2, 1]]
    cue_times1_bass = [0, t1_bass]

    # Define the gains and cue times for track2 (the slave)
    gains2_bass = [[0.2, 1], [1, 1]]
    cue_times2_bass = [0, t2_bass]

    # Apply the EQ changes to the tracks
    track1_eq_bass = rapid_eq(track1, sr, gains1_bass, cue_times1_bass)
    track2_eq_bass = rapid_eq(track2, sr, gains2_bass, cue_times2_bass)

    return track1_eq_bass, track2_eq_bass


def create_eq_adjusted_tracks_treble(track1, track2, t1_treble, t2_treble, duration, sr):
    """Create EQ adjusted versions of two tracks with treble adjustments."""
    # Define the gains and cue times for track1 (the master)
    gains1_treble = [[1, 1], [1, 1], [1, 0.7], [1, 0.1]]
    cue_times1_treble = [0, t1_treble,
                         t1_treble+0.8*duration,
                         t1_treble+duration]

    # Define the gains and cue times for track2 (the slave)
    gains2_treble = [[1, 0.1], [1, 0.1], [1, 0.7], [1, 1]]
    cue_times2_treble = [0, t2_treble, t2_treble + 0.5*duration, t2_treble + duration]

    # Apply the EQ changes to the tracks
    track1_eq_treble = smooth_eq(track1, sr, gains1_treble, cue_times1_treble)
    track2_eq_treble = smooth_eq(track2, sr, gains2_treble, cue_times2_treble)

    return track1_eq_treble, track2_eq_treble
