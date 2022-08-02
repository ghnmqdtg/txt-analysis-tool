# Files and paths settings
TXT_SRC_FOLDER = './src'
CSV_DST_FOLDER = './output'
TARGET_COLUMNS = {
    'range': [0, 1]
}
EXTENSIONS = ['.txt', '.csv']
EXCLUDE_FLIENAMES = [
    '_door_',
    '_tray_',
    '_lid_',
    '_plate_',
    'status',
    'uvStatus',
    'DO',
    'pH'
]
EXCLUDE_FLIES = [
    filename + extension for extension in EXTENSIONS for filename in EXCLUDE_FLIENAMES]
