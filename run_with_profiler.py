# -*- coding: utf-8 -*-

from server.app import create_app
from werkzeug.contrib.profiler import ProfilerMiddleware

app = create_app()


app.config['PROFILE'] = True
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
