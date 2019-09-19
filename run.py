from dataview import app
from config import config

if __name__ == '__main__':
    app.run_server(host=config['ServerHostName'], port=config['ServerPort'], threaded=True)
