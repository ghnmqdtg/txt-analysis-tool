import os
import json
import pandas as pd
import streamlit as st
import utils.plots as plot
import plotly.express as px
import config

TARGET_COLUMNS = config.TARGET_COLUMNS
EXCLUDE_FLIES = config.EXCLUDE_FLIES
LONG_FORM = config.LONG_FORM
PARAMS_SPEC = config.PARAMS_SPEC


def section_upload():
    uploaded_files = st.file_uploader(
        'Choose a folder of your experiment to upload', accept_multiple_files=True)

    df_list = []
    setup = None
    last_idx = None

    for uploaded_file in uploaded_files:
        if (uploaded_file is not None):
            if (uploaded_file.name not in EXCLUDE_FLIES):
                if (uploaded_file.name.endswith('.txt')):

                    col_name = os.path.splitext(uploaded_file.name)[
                        0].replace('_', '')

                    tmp_df = pd.read_csv(uploaded_file,
                                         usecols=TARGET_COLUMNS['range'],
                                         names=['datetime', col_name],
                                         header=None,
                                         delim_whitespace=True)

                    if (len(df_list) == 0):
                        # Set the initial value of last valid index
                        last_idx = tmp_df.last_valid_index()
                        # Convert the timestamp to a datetime format
                        tmp_df['datetime'] = pd.to_datetime(
                            tmp_df['datetime'], unit='ms')

                    else:
                        # Only save the timestamp of the first file
                        tmp_df.drop('datetime', inplace=True, axis=1)

                    df_list.append(tmp_df)

                    if (tmp_df.last_valid_index() < last_idx):
                        last_idx = tmp_df.last_valid_index()

                elif (uploaded_file.name.endswith('.json')):
                    setup = json.load(uploaded_file)
                    # print(json.dumps(setup,
                    #                  sort_keys=True, indent=4))

    if (len(df_list)):
        df = pd.concat(df_list, axis=1, ignore_index=False).iloc[:last_idx+1]
    else:
        df = None

    return df, setup


def main():
    st.write('## Setup 1: Upload the experiment data')
    df, setup = section_upload()

    if (df is not None and setup is not None):
        st.write('## Setup 2: Select data')
        # print(df, setup)
        selected_params = st.multiselect(
            'Select parameter(s) to be plotted', [item for item in df.columns.values.tolist()
                                                  if item != 'datetime'])
        # Convert the dataframe into a long form, which is better for plotly to use
        # Tidy data: https://vita.had.co.nz/papers/tidy-data.pdf
        if (LONG_FORM):
            df = df[selected_params + ['datetime']].melt('datetime', var_name='param',
                                                         value_name='value')

        # Create distplot with custom bin_size
        fig = px.line(df, x='datetime',
                      y='value',
                      color='param', title=setup['experiment_title'] if 'experiment_title' in setup else setup['title'],
                      height=600)
        fig.update_traces(mode='lines', hovertemplate=None)
        fig.update_layout(hovermode='x unified')
        fig.update_layout(xaxis=dict(rangeslider=dict(visible=True),
                                     type="date"))

        for param in selected_params:
            # Some data can't set by the user, so it won't be in settings.json
            # We well skip them
            if (param in PARAMS_SPEC):
                upper, lower = plot.get_boundaries(setup, PARAMS_SPEC[param])
                if (upper != None) and (lower != None):
                    fig.add_hline(y=upper)
                    fig.add_hline(y=lower)

        st.plotly_chart(fig, use_container_width=True)


if __name__ == '__main__':
    st.write('# Data Analysis Tool')
    main()
