# CSV Analysis Tool
## Abstract
This tool is designed to convert txt files into a single CSV file, and visualize the data of it. With the help of Streamlit and Altair, you can read visualized data in the browser.

## Introduction
This tool can parse folders of txts inside source folder (default: `./src/<source folder name>`), generate CSV file into output folder (default: `./output/<source folder name>`). So you should put folder of txts into `./src`.

The target txt file is in the format of 2 columns: Unix timestamps and value, with no header. The filename indicates the data, such as CO2, temperature or pressure. The tool reads these files and converts them into a single CSV file in wide form.

```
# Content in txt file
1658989905219 3.947
1658989905469 6.163
1658989905719 56.895
```

## Develop Environment
- MacOS 12.5
- Python 3.9.7 64-bits

## Usage
```=python
# Install package
$ pip3 install -r requirements.txt

# Run the app
$ streamlit run main.py
```
![Screen Shot 2022-08-03 at 17 12 53](https://user-images.githubusercontent.com/6580698/182571482-8d62f137-dcd0-4fa8-acf7-5aec5a87af73.png)
