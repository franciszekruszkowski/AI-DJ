"""Mixing-related functions."""

import numpy as np


def crossfade_tracks(track1, track2, cue_points1, cue_points2, crossfade_duration, sr):
    """Crossfade between two tracks at specified cue points."""
    crossfade_cue_point1 = cue_points1
    crossfade_cue_point2 = cue_points2

    # Cut the tracks at the cue points
    track1_cut = track1[:int(crossfade_cue_point1 * sr)]
    track2_cut = track2[int(crossfade_cue_point2 * sr):]

    # Crossfade
    crossfade = np.linspace(0, 1, int(crossfade_duration * sr))
    track1_fadeout = track1_cut[-len(crossfade):] * (1 - crossfade)
    track2_fadein = track2_cut[:len(crossfade)] * crossfade

    # Combine the tracks
    combined = np.concatenate([track1_cut[:-len(crossfade)], track1_fadeout + track2_fadein, track2_cut[len(crossfade):]])

    return combined


def combine_tracks(track1, track2, cue_point1, cue_point2, sr):
    """Combine two tracks at specified cue points."""
    # Convert cue points from seconds to samples
    cue_point1_samples = int(cue_point1 * sr)
    cue_point2_samples = int(cue_point2 * sr)

    # Cut the tracks at the cue points
    track1_part1 = track1[:cue_point1_samples]
    track1_part2 = track1[cue_point1_samples:]
    track2_part = track2[cue_point2_samples:]

    # Make the overlapping parts the same length
    min_length = min(len(track1_part2), len(track2_part))
    track1_part2 = track1_part2[:min_length]
    track2_part = track2_part[:min_length]

    # Mix the overlapping parts of the tracks
    combined_part = (track1_part2 + track2_part) / 2

    # Combine all the parts
    combined = np.concatenate([track1_part1, combined_part, track2_part[min_length:]])

    return combined
