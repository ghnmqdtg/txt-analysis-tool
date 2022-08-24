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
