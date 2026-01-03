def load_file(path):
    with open(path, "r") as fh:
        file_data = fh.read()
    return file_data
