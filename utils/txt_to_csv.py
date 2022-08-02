import os
import json
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

    df['datetime'] = pd.to_datetime(
        df['datetime'], unit='ms')

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

    filepaths = parse_folder(TXT_SRC_FOLDER, '.txt', EXCLUDE_FLIES)
    # print(json.dumps(filepaths, sort_keys=True, indent=4))

    if (len(filepaths)):
        for folder in tqdm(filepaths, desc='Folders', bar_format='{l_bar}{bar:40}{r_bar}{bar:-10b}'):
            df_list = []
            foldername = folder.split('/')[-1]
            create_folder(f'{CSV_DST_FOLDER}/{foldername}')
            for idx, filepath in enumerate(tqdm(filepaths[folder], desc='Files', bar_format='{l_bar}{bar:40}{r_bar}{bar:-10b}')):
                col_name = os.path.splitext(os.path.basename(filepath))[
                    0].replace('_', '')
                tmp_df = convert_to_df(filepath, col_name)

                if (idx == 0):
                    df_list.append(tmp_df)
                else:
                    if (len(tmp_df[col_name]) > len(df_list[0])):
                        df_list.append(tmp_df[col_name][:len(df_list[0])])
                    else:
                        df_list.append(tmp_df[col_name])

            df = pd.concat(df_list, axis=1, ignore_index=False)
            df.set_index('datetime')

            if (LONG_FORM):
                df = df.melt('datetime', var_name='param', value_name='value')

            df.to_csv(
                f'{CSV_DST_FOLDER}/{foldername}/{foldername}.csv', index=False)
    else:
        raise ValueError('Target folder has no folder')
