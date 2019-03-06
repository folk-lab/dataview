# -*- coding: utf-8 -*-

from dataview import app

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8082, threaded=True)
