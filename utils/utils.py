import os


def create_folder(dir):
    """
    Create a folder if it doesn't already exist
    """
    if not os.path.exists(dir):
        os.makedirs(dir)


def parse_folder(folder: str, extension: tuple, exclude: list = []):
    """
    Parse a folder and its subfolders, and return the paths files in it

    Parameters
    ----------
    folder: str
        Path to the parent folder
    extension: tuple of strings
        To get the files with specific extensions
    exclude: list
        To exclude specific files
    """

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


def get_nest_name(indexes: list) -> list:
    """
    Get the name of the nest

    Parameters
    ----------
    indexes: list
        List of indexes

    Returns
    -------
    col_name: list
        Names of the nest
    """
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
