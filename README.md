# Data View
Using Dash/plotly, this project is a web-interface for browsing a directory tree and viewing hdf5 data.

# Installation

Install with `python setup.py develop` or `pip install -e /path/to/dataview`

The code is written in Python3 and relies on the following pacakges: `h5py`,`numpy`,`dash`,`dash-core-components`, and `dash-html-components`. If your files are accessed via Samba, you also need `pysmb`

To run the app with the test server...

```
python run.py
```

I followed [this guide](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)
to set up the application on an NGINX web server.

```
$ cat /etc/nginx/sites-available/dataview
server {
        listen 8082;
        server_name server.physik.unibas.ch;
        ssl on;
        ssl_certificate /path/to/cert.crt;
        ssl_certificate_key /path/to/privatekey.key;
        location / {
                include proxy_params;
                proxy_pass http://unix:/srv/dataview/dataview.sock;
        }
}
```
You need a symbolic link to that file in sites-enabled
```
sudo ln -s /etc/nginx/sites-available/dataview /etc/nginx/sites-enabled
```
And this is the systemd service file:

```
$ cat /etc/systemd/system/dataview_gunicorn.service
[Unit]
Description = Gunicorn instance to serve Dataview.

[Service]
ExecStart = /usr/local/bin/gunicorn --workers 4 --worker-class gevent --bind unix:dataview.sock -m 007 --chdir=/srv/dataview run:app.server
User=www-data
Group=www-data

[Install]
WantedBy=multi-user.target
```
The source files for me are in /srv/dataview
You can get the source files by running
```
cd /srv/dataview
git clone https://github.com/folk-lab/dataview.git
```
