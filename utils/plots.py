import pandas as pd
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


def single_y_chart(setup: dict, selected_params: list, df: pd.DataFrame):
    """
    Plot the single y axis chart, the df has to be long format

    Parameters
    ----------
    setup: dict
        The dict object loaded from the configuration experiment settings.
    selected_params: list
        The list of selected parameters
    df: pd.DataFrame
        A pandas.DataFrame containing the data
    """

    # Create distplot with custom bin_size
    fig = px.line(df, x='datetime',
                  y='value',
                  color='param', title=setup['experiment_title'] if 'experiment_title' in setup else setup['title'],
                  height=600)
    fig.update_traces(mode='lines', hovertemplate=None)
    fig.update_layout(hovermode='x unified')
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True),
                                 type="date"),
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=1.02,
                                  xanchor="right",
                                  x=1
                                  )
                      )

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


def multi_y_chart(setup: dict, selected_params: list, df: pd.DataFrame):
    """
    Plot the multi y axis chart, the df has to be wide format

    Parameters
    ----------
    setup: dict
        The dict object loaded from the configuration experiment settings.
    selected_params: list
        The list of selected parameters
    df: pd.DataFrame
        A pandas.DataFrame containing the data
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

    # Loopt through all selected parameters
    for idx, param in enumerate(selected_params):
        # Get the units of the parameter
        unit = get_units(param)

        if (unit != None):
            units.append(unit)

        # Plot the data
        fig.add_trace(go.Scatter(
            x=df['datetime'],
            y=df[param],
            name=f'{param}',
            yaxis=f'y{idx+1}',
        ))

        # Assign the boundaries
        if (param in PARAMS_SPEC):
            upper, lower = get_boundaries(
                setup, PARAMS_SPEC[param])

            if (upper != None) and (lower != None):
                fig.add_hline(y=upper)
                fig.add_hline(y=lower)

        # Create the y axis objects
        # plotly.express doesn't provide the multi yaxis feature
        # We have to use a lower level api plotly.graph_objects to make it
        # The name, color and position of yaxis, yaxis2, ..., yaxisN won't generate the automatically
        # It has to be defined manually separately
        if (idx == 0):
            fig.update_layout(
                yaxis=dict(
                    title=(units[idx]),
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
                    title=(units[idx]),
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
                    title=(units[idx]),
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
                    title=(units[idx]),
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
                    title=(units[idx]),
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
