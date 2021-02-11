from flask import Flask
from flask_restful import Api
from resources.gravar import Gravar
from resources.pausar import Pausar
from resources.upload import Upload
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)
api.add_resource(Gravar, '/record/<string:cdChamado>')
api.add_resource(Pausar, '/stop/<string:PID>')
api.add_resource(Upload, '/upload')

if __name__ == '__main__':
    app.run(debug=True)
