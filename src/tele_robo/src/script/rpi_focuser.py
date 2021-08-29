from picam import CameraFunctions
from flask import Flask




app = Flask(__name__)


@app.route('/preview')
def preview(self):
    init.view()

if __name__ == '__main__':
    app.run(debug=True)
    init = CameraFunctions()