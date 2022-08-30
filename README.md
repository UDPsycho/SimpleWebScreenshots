# Simple Web Screenshots

**Simple Web Screenshots** is a script to take screenshots of a list of websites using Firefox.

The purpose of this tool is to get results as simple as possible (only images) without worrying about all the additional information provided by tools like *EyeWitness* and *gowitness*.

## Requirements

* A linux-based distribution
* Python 3.x
* pip3
* Firefox
* Selenium WebDriver

## Installation (Debian)

```bash
sudo apt install python3 python3-pip firefox-esr
pip3 install selenium
git clone https://www.github.com/UDPsycho/SimpleWebScreenshots.git
```

## Usage

```python
python3 sws.py -i <in_file> [-o <out_dir>] [-m {visible,whole} | -s <size>] [-w <time>]
```

## TODO

* Chrome/Opera support
* Basic proxy support
* Threaded version

## License

Copyright (c) 2022 Psycho. None right reserved.  
[Simple Web Screenshots](https://github.com/UDPsycho/SimpleWebScreenshots) is licensed under the MIT License.
