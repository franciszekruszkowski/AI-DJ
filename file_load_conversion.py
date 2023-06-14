import os
import pickle
from pydub import AudioSegment
import librosa


def convert_to_wav(mp3_file, wav_file):
    """
    Convert a given MP3 file to WAV format.
    :param mp3_file: Path to the input MP3 file.
    :param wav_file: Path to the output WAV file.
    """
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format='wav')


def load_track(wav_file):
    audio, sr = librosa.load(wav_file)
    return audio, sr


def main():
    # Define the paths to the pickle files
    tracks_pickle_file = "loaded_tracks.pkl"
    wav_files_pickle_file = "wav_files.pkl"

    # If the pickle files already exist, load them and return
    if os.path.exists(tracks_pickle_file) and os.path.exists(wav_files_pickle_file):
        with open(tracks_pickle_file, "rb") as f:
            loaded_tracks = pickle.load(f)
        with open(wav_files_pickle_file, "rb") as f:
            wav_files = pickle.load(f)
        return loaded_tracks, wav_files

    mp3_dir = "path_to_your_mp3_files"  # replace with the path to your MP3 files
    wav_dir = "path_to_store_converted_files"  # replace with the path where you want to store WAV files

    os.makedirs(wav_dir, exist_ok=True)

    file_names = os.listdir(mp3_dir)  # Get all the files in the directory
    file_names = [file_name for file_name in file_names if file_name.endswith(".mp3")]  # Filter for .mp3 files

    wav_files = []

    for file_name in file_names:
        mp3_file = os.path.join(mp3_dir, file_name)
        wav_file = os.path.join(wav_dir, f"{file_name[:-4]}.wav")  # replace .mp3 with .wav
        convert_to_wav(mp3_file, wav_file)
        wav_files.append(wav_file)

    loaded_tracks = [load_track(wav_file) for wav_file in wav_files]

    # Before returning, save the results to pickle files for next time
    with open(tracks_pickle_file, "wb") as f:
        pickle.dump(loaded_tracks, f)
    with open(wav_files_pickle_file, "wb") as f:
        pickle.dump(wav_files, f)

    return loaded_tracks, wav_files


if __name__ == "__main__":
    loaded_tracks, wav_files = main()
    for i, (track, wav_file) in enumerate(zip(loaded_tracks, wav_files)):
        print(f"Track {i}:")
        print(track)
        print(wav_file)
