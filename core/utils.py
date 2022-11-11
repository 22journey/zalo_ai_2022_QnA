import os

def get_all_file_in_folder(folder):
    for _, _, files in os.walk(folder):
        filenames = list(files)
        file_paths = [os.path.join(folder, f) for f in filenames]
        return filenames, file_paths
    return [], []