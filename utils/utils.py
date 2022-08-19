import os


def create_folder(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def parse_folder(folder, extension, exclude=[]):
    filepaths = {}

    for dirPath, dirNames, fileNames in os.walk(folder, topdown=True):
        # Skip the root directory that os.walk returns
        if (dirPath != folder):
            dirPath = dirPath.replace('\\', '/')
            filepaths[dirPath] = []
            for f in [f for f in fileNames if (f not in exclude and f.endswith(extension))]:
                filepaths[dirPath].append(
                    os.path.join(dirPath, f).replace('\\', '/'))

    return filepaths


def get_nest_name(indexes):
    col_name = []

    for idx in indexes:
        if idx % 4 == 0:
            col_name.append(f'A{idx % 6 + 1}')
        if idx % 4 == 1:
            col_name.append(f'B{idx % 6 + 1}')
        if idx % 4 == 2:
            col_name.append(f'C{idx % 6 + 1}')
        if idx % 4 == 3:
            col_name.append(f'D{idx % 6 + 1}')

    return col_name
