# DashViewMeasurements
Using Python Dash, this project is a web-interface for viewing a directory sturcuture with hdf5 files to be viewed using plotly.

# Installation

The code is written in Python3. Get pip (`sudo apt-get install python3-setuptools` in Debian/Ubuntu) to install the required packages.
Install [Dash](https://plot.ly/products/dash/)
```
sudo pip3 install dash dash-core-components dash-html-components
```

If your files are accessed via Samba, you need [PySmb](https://pysmb.readthedocs.io/en/latest/):
```
sudo pip3 install pysmb
```

To run the app with the test server...
```
python index.py
```
