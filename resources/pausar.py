from flask_restful import Resource
import os, signal

class Pausar(Resource):
    def get(self, PID):
        print(PID)
        os.kill(int(PID), signal.SIGTERM)

        return {'message': f'Gravação {PID} encerrada com sucesso !'}
    
