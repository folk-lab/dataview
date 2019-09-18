# Data View
Using Dash/plotly, this project is a web-interface for browsing a directory tree and viewing hdf5 data.

# Installation

Install with `python setup.py develop` or `pip install -e /path/to/dataview`

The code is written in Python3 and relies on the following pacakges: `h5py`,`numpy`,`dash`,`dash-core-components`, and `dash-html-components`. If your files are accessed via Samba, you also need `pysmb`

To run the app with the test server...

```
python run.py
```

I used nginx webserver to run the Dash application. Installation guides for nginx that runs a Dash application can be found [here](https://kifarunix.com/installing-linux-dash-with-nginx-on-ubuntu-18-04-lts/).

The following is the content of /etc/nginx/sites-available/testdash
```
server {
        server_name     phys-dots-15.physik.unibas.ch;
        listen          8082 ssl;
        ssl_certificate /etc/ssl/certs/phys-dots-15.crt;
        ssl_certificate_key /etc/ssl/private/phys-dots-15.key;

        access_log      /var/log/nginx/testdash.log;
        error_log       /var/log/nginx/testdash.log;

        location / {
                proxy_pass              http://127.0.0.1:8882;
                proxy_set_header        Host $host;
                proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```