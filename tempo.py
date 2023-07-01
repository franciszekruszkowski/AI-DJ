import pyrubberband as pyrb
import soundfile as sf
import subprocess
from track import Track
from preprocessing import adjust_cue_points, align_cue_points_to_beats


# First adjust tempo function
def adjust_tempo_pyrubberband(audio, sr, tempo_change, output_file):
    # Time stretch the audio
    audio_adjusted = pyrb.time_stretch(audio, sr, tempo_change)

    # Write the adjusted audio to a .wav file
    sf.write(output_file, audio_adjusted, sr)

    return output_file


# Second adjust tempo function
def adjust_tempo(track, output, tempo_change):
    # Use the SoundStretch tool to adjust the tempo of the audio file
    command = ["soundstretch", track, output, f"-tempo={tempo_change}"]
    print(f"Running command: {' '.join(command)}")
    subprocess.run(command)
    return output


def adjust_cue_points(original_cue_points, old_bpm, new_bpm):
    """
    Adjust the cue points based on the speed change ratio.

    Parameters
    ----------
    original_cue_points : list or numpy array
        The original cue points in seconds.

    old_bpm : float
        The original tempo of the track in beats per minute.

    new_bpm : float
        The new tempo of the track in beats per minute.

    Returns
    -------
    adjusted_cue_points : list
        The adjusted cue points in seconds.
    """
    speed_change_ratio = new_bpm / old_bpm
    adjusted_cue_points = [original_cue_point / speed_change_ratio for original_cue_point in original_cue_points]
    return adjusted_cue_points


def align_cue_points_to_beats(adjusted_cue_points, beats):
    """
    Aligns the adjusted cue points to the nearest beat.

    Parameters
    ----------
    adjusted_cue_points : list or numpy array
        The adjusted cue points in seconds.

    beats : list or numpy array
        The beats of the track in seconds.

    Returns
    -------
    aligned_cue_points : list
        The aligned cue points in seconds.
    """
    aligned_cue_points = [beats[np.argmin(np.abs(np.array(beats) - cue_point))] for cue_point in adjusted_cue_points]
    return aligned_cue_points


def prepare_track(track_dict, original_track_name, new_bpm, sr):
    original_track = track_dict[original_track_name]
    original_bpm = original_track.tempo
    original_cue_points = original_track.cue_points
    original_audio = original_track.audio

    # Adjust the speed of the track
    new_track_name = f"{original_track_name}_{new_bpm}bpm"
    new_track_file = adjust_tempo_pyrubberband(original_audio, sr, new_bpm / original_bpm, f"{new_track_name}.wav")

    # Create a new instance of Track
    new_track = Track(new_track_file)
    new_track.detect_beats()
    new_track.detect_downbeats()  # Detect downbeats
    new_track.estimate_tempo_from_downbeats()  # Estimate tempo from downbeats
    new_track.detect_beats_librosa()  # if necessary

    # Adjust the cue points
    adjusted_cue_points = adjust_cue_points(original_cue_points, original_bpm, new_bpm)
    new_track.cue_points = align_cue_points_to_beats(adjusted_cue_points, new_track.beats)

    # Add the new Track instance to the tracks dictionary
    track_dict[new_track_name] = new_track