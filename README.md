# Txt Analysis Tool
![Screen Shot 2022-08-31 at 12 28 48](https://user-images.githubusercontent.com/6580698/187592942-ab4c7376-1b75-4d06-9ddd-fc524aaecfd8.png)

## Abstract
This tool is designed to convert txt files of datetime and value into line chart and read the file `setting.json` to assign the boundary lines of parameters, both txt and json files are needed. With the help of Streamlit and Plotly, you can read visualized data in the browser.

## Demo
Try this out on the streamlit cloud:

https://ghnmqdtg-txt-analysis-tool-main-ct2cig.streamlitapp.com/

## Introduction
This tool can parse a folder of txts and json inside, and convert them into pandas dataframes. Just drag the whole folder in the field in page.

## Input data Format
**Example files are in the src folder, you can check it yourself.**
1. Text files
    
    The target txt file is in the format of 2 columns: Unix timestamps and value, with no header. The filename indicates the data, such as CO2, temperature or pressure.

2. JSON files

    You have to specify the experiment title, parameter names and its setup values.

## Develop Environment
- MacOS 12.5 / Windows 11
- Python 3.9.7 64-bits

## Usage
```=python
# Install package
$ pip3 install -r requirements.txt

# Run the app
$ streamlit run main.py
```


## How to build the app?
The best way to share the Streamlit app would be to run it on a server and share the app URL, but sometimes we need to run it internally. It's possible but a little bit complex to build the app with Pyinstaller. I built it on Windows by following this [tutorial](https://discuss.streamlit.io/t/using-pyinstaller-or-similar-to-create-an-executable/902/18), and made some updates.


1. Create a wrap for the `main.py` at the root folder. For example: `./run_main.py`:
    #### **`./run_main.py`**
    ```python
    import streamlit.cli

    if __name__ == '__main__':
        streamlit.cli._main_run_clExplicit('main.py', 'streamlit run')
    ```

2. Add function `_main_run_clExplicit()` to `cli.py` in streamlit distribution:
    #### **`${YOUR_CONDA_ENV}/lib/site-packages/streamlit/cli.py`**
    ```python
    def _main_run_clExplicit(file, command_line, args=[]):
        streamlit._is_running_with_streamlit = True
        bootstrap.run(file, command_line, args, flag_options={})
    ```

3. Create `./hooks/hook-streamlit.py` to copy the metadata of streamlit:
    #### **`./hooks/hook-streamlit.py`**
    ```python
    from PyInstaller.utils.hooks import copy_metadata
    
    datas = copy_metadata('streamlit')
    ```

4. Create `./.streamlit/config.toml` to set the port:
    #### **`./.streamlit/config.toml`**
    ```toml
    [global]
    developmentMode = false

    [server]
    port = 8501
    ```

5. Create a `.sepc` file by running this command (my wrap is called `run_main.py`):
    
    ```shell
    pyinstaller --onefile --additional-hooks-dir=./hooks run_main.py --clean
    ```

    These two options will set into the `.spec` file:
    1. `--onefile`: To tell the pyinstaller to build a single `.exe` file.
    2. `--additional-hooks-dir`: Add the additional hooks directory.

6. Edit the generated `run_main.spec`:
    
    #### **`./run_main.spec`**
    ```python
    # -*- mode: python ; coding: utf-8 -*-

    block_cipher = None

    added_files = [
        (
            "${YOURPYTHONENV}/Lib/site-packages/altair/vegalite/v4/schema/vega-lite-schema.json",
            "./altair/vegalite/v4/schema/"
        ),
        (
            "${YOURPYTHONENV}/Lib/site-packages/streamlit/static",
            "./streamlit/static"
        )
    ]

    a = Analysis(['run_main.py'],
                pathex=['.'],
                binaries=[],
                datas=[],
                ...,
                noarchive=False)
    pyz = PYZ(...)
    exe = EXE(...)
    ```

7. Build the app by running the following command:
    ```shell
    pyinstaller run_main.spec --clean
    ```

8. Clone the following files and folders into `./dist` and run the `run_main.exe` command:

    1. `main.py`
    2. `config.py`
    3. `./.streamlit`
    4. `./utils`
    
    If the app runs successfully, congratulate!
