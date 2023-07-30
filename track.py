import librosa
from preprocessing import (
    calculate_beats_multifeature,
    detect_downbeats,
    estimate_tempo_from_downbeats,
    calculate_rms_transitions_indices,
    filter_consecutive_indices,
    get_cue_points_from_filtered_indices
)


class Track:
    def __init__(self, name, wav_file):
        self.name = name
        self.wav_file = wav_file
        self.audio, self.sr = librosa.load(wav_file, sr=44100)
        self.tempo = None
        self.downbeats = None
        self.cue_points_rms = None
        self.beats = None
        self.filtered_indices_rms = None
        self.downbeat_differences = None
        self.cue_point_counts = None

    def detect_downbeats(self):
        self.downbeats = detect_downbeats(self.wav_file)

    def estimate_tempo_from_downbeats(self):
        self.tempo, _, self.downbeat_differences = estimate_tempo_from_downbeats(self.wav_file, self.downbeats)

    def calculate_beats_multifeature(self):
        self.beats = calculate_beats_multifeature(self.wav_file)

    def calculate_rms_transition_cue_points(self):
        top_rms_indices, rms_transitions = calculate_rms_transitions_indices(self.audio, self.sr, self.beats)
        self.filtered_indices_rms = filter_consecutive_indices(top_rms_indices, rms_transitions)
        self.cue_points_rms = get_cue_points_from_filtered_indices(self.filtered_indices_rms, self.beats)

    def count_cue_points_in_all_beat_series(self):
        counts = [0, 0, 0, 0]
        # Increment the count for the appropriate series for each index
        for index in self.filtered_indices_rms:
            series_number = index % 4
            counts[series_number] += 1
        self.cue_point_counts = counts


def preprocess(track):
    track.detect_downbeats()
    track.estimate_tempo_from_downbeats()
    print(f"Tempo : {track.tempo}")

    track.calculate_beats_multifeature()
    track.calculate_rms_transition_cue_points()
    track.count_cue_points_in_all_beat_series()

    print("Tempo:", track.tempo)
    print("Filtered Indices (RMS):", track.filtered_indices_rms)
    print("Cue Points (RMS):", track.cue_points_rms)
    print("Beat series : ", track.cue_point_counts)
    print()
