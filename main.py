import os
import streamlit as st
import altair as alt
import pandas as pd
import config
from utils import txt_to_csv
from utils.utils import parse_folder


if __name__ == '__main__':
    TXT_SRC_FOLDER = config.TXT_SRC_FOLDER
    CSV_DST_FOLDER = config.CSV_DST_FOLDER
    EXCLUDE_FLIES = config.EXCLUDE_FLIES
    TARGET_COLUMNS = config.TARGET_COLUMNS
    filepaths = parse_folder(CSV_DST_FOLDER, '.csv', EXCLUDE_FLIES)

    if (filepaths):
        add_selectbox = st.sidebar.selectbox(
            'How would you like to be contacted?',
            list(filepaths.keys())
        )

        if (add_selectbox):
            file = filepaths[add_selectbox][0]
            filename = os.path.splitext(os.path.basename(file))[0]
            st.write(f'Source: {file}')
            df = pd.read_csv(file)
            col_names = df.columns.values.tolist()

            selected_params = st.multiselect(
                'Select parameter(s) to be plotted', col_names)

            if (selected_params):
                chart = alt.Chart(df[:5]).mark_line().encode(
                    x=alt.X("datetime"),
                    y=alt.Y(alt.repeat('layer'),
                            scale=alt.Scale(reverse=True)),
                    color=alt.ColorDatum(alt.repeat('layer'))
                ).repeat(layer=selected_params)

                st.altair_chart(chart,
                                use_container_width=True)

    else:
        txt_to_csv.txt_converter()
