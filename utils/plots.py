import plotly.express as px
import plotly.graph_objects as go
import config

PARAMS_SPEC = config.PARAMS_SPEC
COLORS = config.COLORS


def get_units(column):
    if (column == 'liquid level'):
        return 'mm'
    elif (column == 'mixing rate'):
        return 's'
    elif (column == 'temperature'):
        return '°C'
    elif (column == 'CO2' or column == 'humidity'):
        return '%'
    else:
        return None


def get_boundaries(setup: dict, spec: dict, yaxis_scale: bool = False):
    """
    Get the boundaries of the selected parameter.

    Parameters
    ----------
    setup: dict
        The dict object loaded from the configuration experiment settings.
    spec: dict
        The specification of the selected parameter.
    yaxis: bool
        To indicate whether to enlarge the boundaries of the parameters to be the y-axis scale.
    """
    try:
        # Some data can't set by the user, so it won't be in settings.json
        # That's why we use try/except here.
        setup_val = setup[spec['name']]['val']
        if (not yaxis_scale):
            return (setup_val + spec['accuracy'], setup_val - spec['accuracy'])
        else:
            return (setup_val + spec['accuracy'] * 1.1, setup_val - spec['accuracy'] * 1.1)
    except:
        # The param can't be set by the user
        return (None, None)


def single_y_chart(setup, selected_params, df):
    """
    Plot the single y axis chart, the df has to be long format
    """

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
            upper, lower = get_boundaries(
                setup, PARAMS_SPEC[param])
            if (upper != None) and (lower != None):
                fig.add_hline(y=upper)
                fig.add_hline(y=lower)

    return fig


def multi_y_chart(setup, selected_params, df):
    """
    Plot the multi y axis chart, the df has to be wide format
    """
    # Plot the multi y axis chart
    fig = go.Figure()
    # Update layout properties
    fig.update_layout(
        title_text=setup['experiment_title'] if 'experiment_title' in setup else setup['title'],
        xaxis=dict(domain=[0.15, 0.85],
                   rangeslider=dict(visible=True),
                   type="date"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified',
        height=600
    )

    fig.update_traces(mode='lines', hovertemplate=None)

    units = []

    for idx, param in enumerate(selected_params):

        if (param != 'datetime'):
            unit = get_units(param)

            if (unit != None):
                units.append(unit)

            print(idx+1, unit, units)

            fig.add_trace(go.Scatter(
                x=df['datetime'],
                y=df[param],
                name=f'{param}',
                yaxis=f'y{idx+1}',
            ))

            if (param in PARAMS_SPEC):
                upper, lower = get_boundaries(
                    setup, PARAMS_SPEC[param])

                if (upper != None) and (lower != None):
                    fig.add_hline(y=upper)
                    fig.add_hline(y=lower)

            # Create axis objects
            if (idx == 0):
                fig.update_layout(
                    yaxis=dict(
                        title=(units[idx] if len(units) > 0 else ''),
                        titlefont=dict(
                            color=COLORS[idx]
                        ),
                        tickfont=dict(
                            color=COLORS[idx]
                        )
                    )
                )
            elif (idx == 1):
                fig.update_layout(
                    yaxis2=dict(
                        title=(units[idx] if len(units) > 1 else ''),
                        titlefont=dict(
                            color=COLORS[idx]
                        ),
                        tickfont=dict(
                            color=COLORS[idx]
                        ),
                        anchor="x",
                        overlaying="y",
                        side="right"
                    ),
                )
            elif (idx == 2):
                fig.update_layout(
                    yaxis3=dict(
                        title=(units[idx] if len(units) > 2 else ''),
                        titlefont=dict(
                            color=COLORS[idx]
                        ),
                        tickfont=dict(
                            color=COLORS[idx]
                        ),
                        anchor="free",
                        overlaying="y",
                        side="left",
                        position=0.1
                    )
                )
            elif (idx == 3):
                fig.update_layout(
                    yaxis4=dict(
                        title=(units[idx] if len(units) > 3 else ''),
                        titlefont=dict(
                            color=COLORS[idx]
                        ),
                        tickfont=dict(
                            color=COLORS[idx]
                        ),
                        anchor="free",
                        overlaying="y",
                        side="right",
                        position=0.9
                    )
                )
            elif (idx == 4):
                fig.update_layout(
                    yaxis5=dict(
                        title=(units[idx] if len(units) > 4 else ''),
                        titlefont=dict(
                            color=COLORS[idx]
                        ),
                        tickfont=dict(
                            color=COLORS[idx]
                        ),
                        anchor="free",
                        overlaying="y",
                        side="left",
                        position=0.05
                    )
                )

    return fig
