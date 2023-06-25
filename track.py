import os
import librosa
from file_load_conversion import *
from preprocessing import detect_downbeats, estimate_tempo_from_downbeats, calculate_rms_transitions_indices, \
    filter_consecutive_indices, get_cue_points_from_filtered_indices, detect_beats


class Track:
    def __init__(self, wav_file):
        self.wav_file = wav_file
        self.audio, self.sr = librosa.load(wav_file)
        self.tempo = None
        self.downbeats = None
        self.cue_points = None
        self.beats = None
        self.filtered_indices = None
        self.downbeat_differences = None

    def detect_downbeats(self):
        self.downbeats = detect_downbeats(self.wav_file)

    def estimate_tempo_from_downbeats(self):
        self.tempo, _, self.downbeat_differences = estimate_tempo_from_downbeats(self.wav_file, self.downbeats)

    def calculate_rms_transition_cue_points(self):
        top_rms_indices, rms_transitions = calculate_rms_transitions_indices(self.audio, self.sr, self.downbeats)
        self.filtered_indices = filter_consecutive_indices(top_rms_indices, rms_transitions)
        self.cue_points = get_cue_points_from_filtered_indices(self.filtered_indices, self.downbeats)

    def detect_beats(self):
        self.beats = detect_beats(self.wav_file, self.sr)


# Instantiate the Track class for each WAV file
tracks = {}

for wav_file in wav_files:
    # Extract the base name of the file without extension
    track_name = os.path.splitext(os.path.basename(wav_file))[0]

    # Create an instance of Track
    track = Track(wav_file)

    # Store the Track instance in the dictionary
    tracks[track_name] = track

for name, track in tracks.items():
    print(f"Processing {name}...")
    track.detect_downbeats()
    track.estimate_tempo_from_downbeats()
    track.calculate_rms_transition_cue_points()
    track.detect_beats()

    print("Tempo:", track.tempo)
    print("Cue points:", track.cue_points)
    print("Filtered Indices:", track.filtered_indices)
    print("Downbeat Differences:", track.downbeat_differences)
    print("\n\n")
