from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from app.main.controllers import api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
if __name__ == '__main__':
    app.config['CORS_HEADERS'] = 'Content-Type'

    CORS(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    api.init_app(app)
    app.run(debug=True,host="0.0.0.0") 