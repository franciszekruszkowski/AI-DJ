"""Preprocessing functions."""

import numpy as np
import librosa
import madmom
from scipy.stats import mode
from essentia.standard import BeatTrackerMultiFeature, MonoLoader
from itertools import groupby
from operator import itemgetter
import essentia

from file_load_conversion import main as load_conversion


def calculate_beats_multifeature(audio_file):
    """Calculate the beats of an audio file using Essentia's multi-feature beat tracker."""
    # Load the audio
    loader = MonoLoader(filename=audio_file, resampleQuality=0)
    audio = loader()

    # Initialize the BeatTrackerMultiFeature
    tracker = BeatTrackerMultiFeature()

    # Calculate the beats
    beats, _ = tracker(audio)

    return beats


def detect_downbeats(audio_file, sr=44100, fps=100):
    """Detect the downbeats of an audio file using madmom's DBNDownBeatTrackingProcessor."""
    # Load the audio signal without resampling
    signal = madmom.audio.signal.Signal(audio_file, sample_rate=sr, num_channels=1)

    # Get the beat and downbeat activations
    act = madmom.features.RNNDownBeatProcessor()(signal)

    # Create a downbeat processor
    proc = madmom.features.DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=fps)

    # Get the beats and downbeats
    beats_and_downbeats = proc(act)

    # Filter downbeats (those with beat position 1)
    downbeats = [beat for beat in beats_and_downbeats if beat[1] == 1]

    return np.array(downbeats)


def estimate_tempo_from_downbeats(audio_file, downbeats):
    """Estimate the tempo of an audio file based on its downbeats."""
    # Calculate the time difference between consecutive downbeats
    downbeat_differences = np.around(np.diff(downbeats[:, 0]), decimals=6)

    # Get the mode of the differences
    mod_diff = mode(downbeat_differences).mode

    # Calculate the tempo: 60 seconds divided by the average difference
    # Since downbeat_differences are in seconds, this gives beats per minute
    tempo = 4 * (60 / mod_diff)

    tempo = round(tempo)

    return tempo, mod_diff, downbeat_differences


def calculate_rms_transitions_indices(audio, sr, beats, window_size=1024, hop_length=512):
    """Calculate the RMS transitions between beats and return the indices of the most significant transitions."""
    # Calculate RMS
    rms = librosa.feature.rms(y=audio, frame_length=window_size, hop_length=hop_length).squeeze()

    # This will hold our feature transitions and corresponding downbeat indices
    rms_transitions = []
    transition_indices = []

    for i in range(len(beats)):  # Include all downbeats
        # Identify the frames for the previous, current and next beat
        prev_frame = int(librosa.time_to_samples(beats[i-1], sr=sr) / hop_length) if i > 0 else None
        current_frame = int(librosa.time_to_samples(beats[i], sr=sr) / hop_length)
        next_frame = int(librosa.time_to_samples(beats[i+1], sr=sr) / hop_length) if i < len(beats) - 1 else None

        # Calculate the transitions for RMS
        if prev_frame is not None and next_frame is not None:
            rms_transition = max(np.abs(rms[current_frame] - rms[prev_frame]), np.abs(rms[current_frame] - rms[next_frame]))
        elif prev_frame is not None:  # Handle the last downbeat
            rms_transition = np.abs(rms[current_frame] - rms[prev_frame])
        else:  # Handle the first downbeat
            rms_transition = np.abs(rms[current_frame] - rms[next_frame])

        rms_transitions.append(rms_transition)
        transition_indices.append(i)

    # Convert to numpy arrays for easier manipulation
    rms_transitions = np.array(rms_transitions)
    transition_indices = np.array(transition_indices)

    # Identify the indices of the beats with the highest RMS transitions
    # Here we're choosing the top 10%, but this can be adjusted
    top_rms_indices = transition_indices[rms_transitions >= np.percentile(rms_transitions, 97.5)]

    # Always include the first beat
    top_rms_indices = np.append(0, top_rms_indices)

    return top_rms_indices, rms_transitions


def filter_consecutive_indices(indices, rms_transitions, consecutive_index_distance=3):
    """Filter out consecutive indices that are too close to each other."""
    if len(indices) <= 4:
        return indices

    filtered_indices = []

    for _, group in groupby(enumerate(indices), lambda ix: ix[0] - ix[1]):
        sequence = list(map(itemgetter(1), group))
        sequence.sort()

        sequence = [index for index in sequence if index < len(rms_transitions)]

        if sequence:  # Check that the sequence is not empty
            amplitudes = [rms_transitions[index] for index in sequence]
            max_amplitude_index = sequence[np.argmax(amplitudes)]
            filtered_indices.append(max_amplitude_index)

    return filtered_indices


def get_cue_points_from_filtered_indices(filtered_indices, beats_or_downbeats):
    """Get the cue points corresponding to the given indices."""
    # Handle 2D array (downbeats) or 1D array (beats)
    if len(beats_or_downbeats.shape) > 1:
        beats_or_downbeats = beats_or_downbeats[:, 0]

    # Convert indices to time stamps using the downbeats/beats array
    cue_points = beats_or_downbeats[filtered_indices]

    return cue_points
