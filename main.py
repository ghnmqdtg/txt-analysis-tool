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
            'Which folder do you want to select?',
            list(filepaths.keys())
        )

        if (add_selectbox):
            file = filepaths[add_selectbox][0]
            filename = os.path.splitext(os.path.basename(file))[0]
            df = pd.read_csv(file)
            col_names = df.columns.values.tolist()

            selected_params = st.multiselect(
                'Select parameter(s) to be plotted', col_names)
            selected_range = st.slider(
                'Select a range of values',
                0, len(df), (0, len(df)))
            selected_data = df[selected_range[0]:selected_range[1]]

            # print(df[selected_params]
            #       [selected_range[0]:selected_range[1]])

            if (selected_params):
                selected_params.append('datetime')

                line = alt.Chart(selected_data).transform_fold(
                    selected_params,
                    as_=['params', 'value']
                ).mark_line().encode(
                    x=alt.X('datetime', axis=alt.Axis(tickCount=5)),
                    y=alt.Y('value:Q'),
                    color='params:N',
                    tooltip=selected_params
                ).properties(
                    height=450
                )

                # Create a selection that chooses the nearest point & selects based on x-value
                nearest = alt.selection(type='single', nearest=True, on='mouseover',
                                        fields=['datetime'], empty='none')
                # Transparent selectors across the chart. This is what tells us
                # the x-value of the cursor
                selectors = alt.Chart(selected_data).mark_point().encode(
                    x='datetime',
                    opacity=alt.value(0),
                ).add_selection(
                    nearest
                )

                # Draw points on the line, and highlight based on selection
                points = line.mark_point().encode(
                    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
                )

                # Draw text labels near the points, and highlight based on selection
                text = line.mark_text(align='left', dx=5, dy=-5).encode(
                    text=alt.condition(nearest, 'value:Q', alt.value(' '))
                )

                # Draw a rule at the location of the selection
                rules = alt.Chart(selected_data).mark_rule(color='gray').encode(
                    x='datetime',
                    tooltip=[alt.Tooltip(c) for c in selected_params]
                ).transform_filter(
                    nearest
                )

                # Put the five layers into a chart and bind the data
                chart = alt.layer(
                    line, selectors, points, rules, text
                )

                st.altair_chart(chart,
                                use_container_width=True)

    else:
        txt_to_csv.txt_converter()
