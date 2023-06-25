from file_load_conversion import main
import madmom
import numpy as np
import librosa
from scipy.stats import mode
import subprocess
from file_load_conversion import main as load_conversion
from itertools import groupby
from operator import itemgetter

loaded_tracks, wav_files = load_conversion()
# Now you can use loaded_tracks and wav_files


def detect_beats(audio_file,sr):
    # Load the audio file
    audio = madmom.audio.signal.Signal(audio_file, sample_rate=sr)

    # Create a beat tracking processor
    act = madmom.features.beats.RNNBeatProcessor()(audio_file)

    # Detect beats
    beats = madmom.features.beats.BeatTrackingProcessor(fps=100)(act)

    return np.array(beats)


def detect_downbeats(audio_file, fps=100):
    # Get the beat and downbeat activations
    act = madmom.features.RNNDownBeatProcessor()(audio_file)

    # Create a downbeat processor
    proc = madmom.features.DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=fps)

    # Get the beats and downbeats
    beats_and_downbeats = proc(act)

    # Filter downbeats (those with beat position 1)
    downbeats = [beat for beat in beats_and_downbeats if beat[1] == 1]

    return np.array(downbeats)


def estimate_tempo_from_downbeats(audio_file, downbeats):
    # Calculate the time difference between consecutive downbeats
    downbeat_differences = np.diff(downbeats[:, 0])

    # Calculate the time difference between consecutive downbeats
    downbeat_differences = np.around(np.diff(downbeats[:, 0]), decimals=6)

    # Get the mode of the differences
    mod_diff = mode(downbeat_differences).mode[0]

    # Calculate the tempo: 60 seconds divided by the average difference
    # Since downbeat_differences are in seconds, this gives beats per minute
    tempo = 4 * (60 / mod_diff)

    return tempo, mod_diff, downbeat_differences


def calculate_bpm_change(bpm_track1, bpm_track2):

    change = (bpm_track2 - bpm_track1) / bpm_track1 * 100
    print(f"BPM change: {change}%")

    return change


def calculate_rms_transitions_indices(audio, sr, downbeats, window_size=1024, hop_length=512):
    # Calculate RMS
    rms = librosa.feature.rms(y=audio, frame_length=window_size, hop_length=hop_length).squeeze()

    # This will hold our feature transitions and corresponding downbeat indices
    rms_transitions = []
    transition_indices = []

    for i in range(1, len(downbeats) - 1):  # We ignore the first and last downbeat for this analysis
        # Identify the frames for the previous, current and next downbeat
        prev_frame = int(librosa.time_to_samples(downbeats[i-1][0], sr=sr) / hop_length)
        current_frame = int(librosa.time_to_samples(downbeats[i][0], sr=sr) / hop_length)
        next_frame = int(librosa.time_to_samples(downbeats[i+1][0], sr=sr) / hop_length)

        # Calculate the transitions for RMS
        rms_transition = max(np.abs(rms[current_frame] - rms[prev_frame]), np.abs(rms[current_frame] - rms[next_frame]))

        rms_transitions.append(rms_transition)
        transition_indices.append(i)

    # Convert to numpy arrays for easier manipulation
    rms_transitions = np.array(rms_transitions)
    transition_indices = np.array(transition_indices)

    # Identify the indices of the downbeats with the highest RMS transitions
    # Here we're choosing the top 10%, but this can be adjusted
    top_rms_indices = transition_indices[rms_transitions >= np.percentile(rms_transitions, 90)]

    return top_rms_indices, rms_transitions


def filter_consecutive_indices(indices, rms_transitions, consecutive_index_distance=3):
    # If there are 4 or less indices, return them all
    if len(indices) <= 4:
        return indices

    filtered_indices = []

    # Group consecutive indices together
    for _, group in groupby(enumerate(indices), lambda ix : ix[0] - ix[1]):
        sequence = list(map(itemgetter(1), group))
        sequence.sort()  # ensure the sequence is ordered

        # Only consider sequences that have more than one element
        if len(sequence) > 1:
            # Remove any indices from the sequence that are out of bounds for the rms_transitions array
            sequence = [index for index in sequence if index < len(rms_transitions)]

            # Find the index with the highest amplitude in the sequence
            amplitudes = [rms_transitions[index] for index in sequence]
            max_amplitude_index = sequence[np.argmax(amplitudes)]
            filtered_indices.append(max_amplitude_index)

    return filtered_indices


def get_cue_points_from_filtered_indices(filtered_indices, downbeats):
    # Convert indices to time stamps using the downbeats array
    cue_points = downbeats[filtered_indices]

    # The result is a 2D array where the first column contains the timestamps
    # So let's return just this first column
    return cue_points[:, 0]


def adjust_tempo(track, output, tempo_change):
    # Use the SoundStretch tool to adjust the tempo of the audio file
    command = ["soundstretch", track, output, f"-tempo={tempo_change}"]
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command)
    return output


def preprocessing(wav_file):
    # Load the track
    audio, sr = librosa.load(wav_file)

    # Detect the downbeats
    downbeats = detect_downbeats(wav_file)

    # Calculate the RMS transitions
    transitions_indices, rms_transitions = calculate_rms_transitions_indices(audio, sr, downbeats)

    # Filter the indices
    filtered_indices = filter_consecutive_indices(transitions_indices, rms_transitions)

    # Get the cue points
    cue_points = get_cue_points_from_filtered_indices(filtered_indices, downbeats)

    return transitions_indices, filtered_indices, cue_points