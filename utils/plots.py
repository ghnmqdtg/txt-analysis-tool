import pandas as pd
import altair as alt
import config


def get_boundaries(setup, spec, yaxis_scale=False):
    try:
        setup_val = setup[spec['name']]['val']
        if (not yaxis_scale):
            return (setup_val + spec['accuracy'], setup_val - spec['accuracy'])
        else:
            return (setup_val + spec['accuracy'] * 1.1, setup_val - spec['accuracy'] * 1.1)
    except:
        # The param can't be set by the user
        return (None, None)


def line_chart(setup, params, data):
    PARAMS_SPEC = config.PARAMS_SPEC

    if (len(params) == 1 and params[0] in PARAMS_SPEC):
        upper, lower = get_boundaries(
            setup, PARAMS_SPEC[params[0]], yaxis_scale=True)
        y_range_max = upper if (upper != None and upper >
                                data[params[0]].max()) else data[params[0]].max()
        y_range_min = lower if (lower != None and lower >
                                data[params[0]].min()) else data[params[0]].min()

    line = alt.Chart(data).transform_fold(
        params,
        as_=['params', 'value']
    ).mark_line().encode(
        x=alt.X('datetime:T', axis=alt.Axis(tickCount=5)),
        y=alt.Y('value:Q', scale=alt.Scale(domain=[y_range_min, y_range_max])) if (
            len(params) == 1 and params[0] in PARAMS_SPEC) else alt.Y('value:Q'),
        color='params:N',
        tooltip=params+['datetime']
    ).properties(
        height=450
    )

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single',
                            nearest=True,
                            on='mouseover',
                            fields=['datetime'],
                            empty='none')

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = alt.Chart(data).mark_point().encode(
        x='datetime:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
        size=alt.value(20)
    )
    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(data).mark_rule(color='gray').encode(
        x='datetime:T',
        tooltip=[alt.Tooltip(c) for c in params] +
        [alt.Tooltip('datetime:T', format='%Y-%m-%d %H:%M:%S')]
    ).transform_filter(
        nearest
    )

    # Add boundary lines to specific parameters
    for param in params:
        if (param in PARAMS_SPEC):
            upper, lower = get_boundaries(setup, PARAMS_SPEC[param])
            if (upper != None) and (lower != None):
                bound = pd.DataFrame({
                    'upper': [upper],
                    'lower': [lower],
                })

                uppper_bound = alt.Chart(bound).mark_rule(color='red').encode(
                    alt.Y('upper')
                )

                lower_bound = alt.Chart(bound).mark_rule(color='red').encode(
                    alt.Y('lower')
                )

                line = line + uppper_bound + lower_bound

    # Put the five layers into a chart and bind the data
    chart = alt.layer(
        line, selectors, points, rules, text
    ).configure_axis(
        titleFontSize=16
        # labelFontSize=14,
    )

    return chart
