
from GSP_WEB import app
import flask_excel as excel

if __name__ == '__main__':
    app.config.update(DEBUG=True)
    excel.init_excel(app)
    app.run(host='0.0.0.0', threaded=True,port=80)


