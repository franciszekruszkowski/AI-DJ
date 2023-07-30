"""Tempo-related functions."""

import librosa
import pyrubberband as pyrb
import soundfile as sf
from track import Track, preprocess


def adjust_tempo_pyrb(input_file, output_file, tempo_ratio):
    """Adjust the tempo of an audio file and save the result to a new file."""
    # Load the audio
    audio, sr = librosa.load(input_file, sr=44100)

    # Time stretch the audio
    audio_adjusted = pyrb.time_stretch(audio, sr, tempo_ratio)

    # Write the adjusted audio to a .wav file
    sf.write(output_file, audio_adjusted, sr)

    return audio_adjusted, output_file


def calculate_tempo_ratio(master, slave):
    """Calculate the tempo ratio between a master track and a slave track."""
    ratio = master.tempo / slave.tempo
    print(ratio)
    print(slave.tempo * ratio)
    print(master.tempo)
    print(slave.tempo)
    return ratio


def adjust_tempo_and_analyze(master_key, slave_key, tracks_dict):
    """Adjust the tempo of a slave track to match a master track and analyze the result."""
    master = tracks_dict[master_key]
    slave = tracks_dict[slave_key]

    # Calculate the tempo ratio
    tempo_ratio = calculate_tempo_ratio(master, slave)

    # Adjust the tempo of the slave track using pyrubberband
    adjusted_audio, output_file = adjust_tempo_pyrb(
        slave.wav_file, f"{slave_key}_AT_{master.tempo}bpm.wav", tempo_ratio)

    # Create a new Track instance for the adjusted audio
    adjusted_slave = Track(f"{slave_key}_AT_{master.tempo}bpm", output_file)

    # Add the adjusted track to the tracks dictionary
    tracks_dict[f"{slave_key}_AT_{master.tempo}bpm"] = adjusted_slave

    # Preprocess the adjusted track
    preprocess(adjusted_slave)

    return adjusted_slave
