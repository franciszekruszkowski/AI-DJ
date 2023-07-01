import numpy as np
import soundfile as sf
import librosa
from scipy.signal import butter, lfilter
from preprocessing import preprocessing


def crossfade_tracks(track1, track2, cue_points1, cue_points2, crossfade_duration, sr):
    """Crossfade two tracks using the given cue points and crossfade duration."""

    # Get the cue point for the crossfade
    crossfade_cue_point1 = cue_points1[-2]
    crossfade_cue_point2 = cue_points2[2]  # Start at the beginning of track2

    # Cut the tracks at the cue points
    track1_cut = track1[:int(crossfade_cue_point1 * sr)]
    track2_cut = track2[int(crossfade_cue_point2 * sr):]

    print(f"track2_cut shape: {track2_cut.shape}")

    # Crossfade
    crossfade = np.linspace(0, 1, int(crossfade_duration * sr))
    track1_fadeout = track1_cut[-len(crossfade):] * (1 - crossfade)
    track2_fadein = track2_cut[:len(crossfade)] * crossfade

    # Combine the tracks
    combined = np.concatenate(
        [track1_cut[:-len(crossfade)], track1_fadeout + track2_fadein, track2_cut[len(crossfade):]]
    )

    return combined


def crossfade_multiple_tracks(track_list, cue_point_list, crossfade_duration, sr):
    combined_track = track_list[0]
    offset = 0

    for i in range(1, len(track_list)):
        cue_points_previous_track = [point - offset for point in cue_point_list[i-1]]
        cue_points_next_track = [point + len(track_list[i-1]) / sr for point in cue_point_list[i]]
        combined_track = crossfade_tracks(combined_track, track_list[i], cue_points_previous_track, cue_points_next_track, crossfade_duration, sr)
        offset += cue_points_next_track[1]

    return combined_track


def butter_bandstop_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    y = lfilter(b, a, data)
    return y


def cut_low_frequencies(audio, fs):
    return butter_bandstop_filter(audio, 300, 1500, fs)


def cut_mid_frequencies(audio, fs):
    return butter_bandstop_filter(audio, 1500, 2000, fs)


def cut_high_frequencies(audio, fs):
    return butter_bandstop_filter(audio, 2000, fs)


def main():
    """Main function to load, preprocess and crossfade two tracks."""

    # Replace with the path to your .wav files
    track1_path = "path_to_your_track1.wav"
    track2_path = "path_to_your_track2.wav"

    # Load the tracks
    track1, sr = librosa.load(track1_path)
    track2, _ = librosa.load(track2_path)  # Assuming the same sample rate for both tracks

    # Preprocess the tracks
    _, _, cue_points1 = preprocessing(track1, track1_path)
    _, _, cue_points2 = preprocessing(track2, track2_path)

    # Crossfade the tracks
    crossfade_duration = 30  # You can adjust this value as needed
    combined = crossfade_tracks(track1, track2, cue_points1, cue_points2, crossfade_duration, sr)

    # Write the mixed track to a .wav file
    sf.write('combined.wav', combined, sr)


if __name__ == "__main__":
    main()
