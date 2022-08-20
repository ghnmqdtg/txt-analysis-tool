import os
import json
import streamlit as st
import pandas as pd
import config
from utils import txt_to_csv
from utils.utils import parse_folder
from utils.plots import line_chart


def main():
    add_selectbox = st.sidebar.selectbox(
        'Which folder do you want to select?',
        list(filepaths.keys())
    )

    if (add_selectbox):
        # Get data and setup for the selected folder
        data_src = filepaths[add_selectbox][0]
        setup_src = setuppaths[add_selectbox][0]
        setup = json.load(open(setup_src))

        df = pd.read_csv(data_src)
        col_names = [item for item in df.columns.values.tolist()
                     if item != 'datetime']

        selected_params = st.multiselect(
            'Select parameter(s) to be plotted', col_names)
        selected_range = st.slider(
            'Select a range of values',
            0, len(df), (0, len(df)))
        selected_data = df[selected_range[0]:selected_range[1]]

        # print(json.dumps(setup,
        #       sort_keys=True, indent=4))

        if (selected_params):
            chart = line_chart(setup, selected_params, selected_data)

            st.altair_chart(chart,
                            use_container_width=True)


if __name__ == '__main__':
    CSV_DST_FOLDER = config.CSV_DST_FOLDER
    EXCLUDE_FLIES = config.EXCLUDE_FLIES
    TARGET_COLUMNS = config.TARGET_COLUMNS

    filepaths = parse_folder(CSV_DST_FOLDER, '.csv', EXCLUDE_FLIES)
    setuppaths = parse_folder(CSV_DST_FOLDER, '.json', EXCLUDE_FLIES)

    if (filepaths):
        main()
    else:
        # If the target folder doesn't exist, convert the txt files
        txt_to_csv.txt_converter()
        filepaths = parse_folder(CSV_DST_FOLDER, '.csv', EXCLUDE_FLIES)
        setuppaths = parse_folder(CSV_DST_FOLDER, '.json', EXCLUDE_FLIES)
        main()
