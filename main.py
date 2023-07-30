import os
from track import *
from visualisations import plot_waveform_with_hot_cues
from tempo import adjust_tempo_and_analyze
from eq import create_eq_adjusted_tracks, create_eq_adjusted_tracks_treble, beats_to_seconds, normalize_audio_gain
from IPython.display import Audio
from mixing import combine_tracks
import soundfile as sf



def main():
    # specify your path
    path = "raw-wavs"

    raw_wav_files = []

    for file_name in os.listdir(path):
        if file_name.endswith('.wav'):
            raw_wav_files.append(os.path.join(path, file_name))

    raw_tracks = {}

    for wav_file in raw_wav_files:
        track_name = os.path.splitext(os.path.basename(wav_file))[0]
        track = Track(track_name, wav_file)
        raw_tracks[track_name] = track

    new_tracks = {}
    counter = {}

    for old_key, track in raw_tracks.items():
        new_key = old_key.split()[0]
        if new_key in counter:
            counter[new_key] += 1
            new_key = f"{new_key}{counter[new_key]}"
        else:
            counter[new_key] = 1
        new_tracks[new_key] = track

    tracks = new_tracks

    """
    for name, track in tracks.items():
        print(f"Preprocessing : {name}:")
        preprocess(track)
    """
    for name, track in tracks.items():
        if name == "Bours-" or name == "JKS":
            print(f"Preprocessing : {name}:")
            preprocess(track)


    a = tracks['Bours-']
    c = tracks['JKS']

    adjusted_ca = adjust_tempo_and_analyze("Bours-", "JKS", tracks)

    b = tracks['JKS_AT_149bpm']

    plot_waveform_with_hot_cues(a.audio, a.sr, a.cue_points_rms)
    plot_waveform_with_hot_cues(b.audio, b.sr, b.cue_points_rms)

    seconds = beats_to_seconds(a.tempo, 8)
    acue = a.cue_points_rms[4]
    bcue = b.cue_points_rms[2]
    bbass = b.cue_points_rms[4]
    abass = acue + (bbass - bcue - seconds)

    track1_eq, track2_eq = create_eq_adjusted_tracks(a.audio, b.audio, abass, bbass, a.sr)
    a_both_eq, b_both_eq = create_eq_adjusted_tracks_treble(track1_eq, track2_eq, bcue, bcue, 120, a.sr)

    combined = combine_tracks(a_both_eq, b_both_eq, acue, bcue, a.sr)
    combined_normalized = normalize_audio_gain(combined)

    sf.write('Boursy_mixed_with_JKS_at_149bpm.wav', combined_normalized, a.sr)
    Audio(combined_normalized, rate=a.sr)


if __name__ == "__main__":
    main()
