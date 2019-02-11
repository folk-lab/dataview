# DashViewMeasurements
Using Python Dash, this project is a web-interface for viewing a directory sturcuture with hdf5 files to be viewed using plotly.

# Installation

The code is written in Python3. Get pip (`sudo apt-get install python3-setuptools` in Debian/Ubuntu) to install the required packages.
Install [https://plot.ly/products/dash/](Dash)
```
sudo pip3 install dash dash-core-components dash-html-components
```

If your files are accessed via Samba, you need [https://pysmb.readthedocs.io/en/latest/](PySmb):
```
sudo pip3 install pysmb
```
