# Files and paths settings
TXT_SRC_FOLDER = './src'
CSV_DST_FOLDER = './output'
TARGET_COLUMNS = {
    'range': [0, 1]
}
EXTENSIONS = ['.txt', '.csv', '.json']
EXCLUDE_FLIENAMES = [
    '_door_',
    '_tray_',
    '_lid_',
    '_plate_',
    '_status_',
    '_cycle_',
    '_cycletimer_',
    'vemp1',
    'vemp2',
    'p_temp',
    'p_status',
    'CO2(raw)',
    'DO',
    'pH',
    'status',
    'uvStatus',
]
EXCLUDE_FLIES = [
    filename + extension for extension in EXTENSIONS for filename in EXCLUDE_FLIENAMES]
LONG_FORM = True

# Specifications of the machine
PARAMS_SPEC = {
    # "flowrate": {
    #     "name": "mixing_level",
    #     # TODO: Experimental value, it should be set to correct one
    #     "accuracy": 8
    # },
    "CO2": {
        "name": "co2_concentration",
        "accuracy": 0.2
    },
    "humidity": {
        "name": "humidity",
        "accuracy": 0.1
    },
    "temp": {
        "name": "temp",
        "accuracy": 0.1
    },
}
