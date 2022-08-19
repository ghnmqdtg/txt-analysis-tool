import os
import json
import shutil
import pandas as pd
from tqdm import tqdm
from utils.utils import create_folder, parse_folder, get_nest_name
import config

# Import config
TXT_SRC_FOLDER = config.TXT_SRC_FOLDER
TARGET_COLUMNS = config.TARGET_COLUMNS
EXCLUDE_FLIES = config.EXCLUDE_FLIES
LONG_FORM = config.LONG_FORM
CSV_DST_FOLDER = config.CSV_DST_FOLDER


def convert_to_df(filepath, col_name):
    df = pd.read_csv(filepath,
                     usecols=TARGET_COLUMNS['range'],
                     names=['datetime', col_name],
                     header=None,
                     delim_whitespace=True)

    # Convert the timestamp to a datetime format
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

    # TODO: Split nest data
    if (col_name in ['DO', 'pH']):
        splited = df[col_name].str.split(
            ',', expand=True)
        splited.columns = get_nest_name(list(range(24)))
        # df = pd.concat([df['datetime'], splited])
        # print(df.head())

    return df


def txt_converter():
    create_folder(TXT_SRC_FOLDER)
    create_folder(CSV_DST_FOLDER)

    filepaths = parse_folder(TXT_SRC_FOLDER, ('.txt', '.json'), EXCLUDE_FLIES)
    # print(json.dumps(filepaths, sort_keys=True, indent=4))

    if (len(filepaths)):
        for folder in tqdm(filepaths, desc='Folders', bar_format='{l_bar}{bar:40}{r_bar}{bar:-10b}'):
            # Create empty dataframe for collecting all data from txt files
            df_list = []
            # Create dest folder
            foldername = folder.split('/')[-1]
            create_folder(f'{CSV_DST_FOLDER}/{foldername}')
            # Copy settings.json from src to dest
            setup_filepath = [path for path in filepaths[folder]
                              if path.endswith('.json')][0]
            shutil.copyfile(
                setup_filepath, f'{CSV_DST_FOLDER}/{foldername}/{os.path.basename(setup_filepath)}')
            # Remove settings.json from this list, only txt filepaths remains
            filepaths[folder].remove(setup_filepath)

            # Parse all the txt files and put them into dataframe as new columns
            for idx, data_filepath in enumerate(tqdm(filepaths[folder], desc='Files', bar_format='{l_bar}{bar:40}{r_bar}{bar:-10b}')):
                col_name = os.path.splitext(os.path.basename(data_filepath))[
                    0].replace('_', '')
                tmp_df = convert_to_df(data_filepath, col_name)
                if (idx == 0):
                    # Use the datetime of the first txt file as the datetime of csv
                    df_list.append(tmp_df)
                else:
                    if (len(tmp_df[col_name]) > len(df_list[0])):
                        df_list.append(tmp_df[col_name][: len(df_list[0])])
                    else:
                        df_list.append(tmp_df[col_name])

            df = pd.concat(df_list, axis=1, ignore_index=False)
            df.set_index('datetime')

            # Convert the dataframe into a long form, which is better for altair to use
            # But altair has an transform_fold() api to do this, so skip this.
            # Tidy data: https://vita.had.co.nz/papers/tidy-data.pdf
            # if (LONG_FORM):
            #     df = df.melt('datetime', var_name='param', value_name='value')

            df.to_csv(
                f'{CSV_DST_FOLDER}/{foldername}/{foldername}.csv', index=False)
    else:
        raise ValueError('Target folder has no folder')
