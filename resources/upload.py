import os

from flask import request
from flask_restful import Resource
import paramiko


class Upload(Resource):
    def post(self):
        json_data = request.get_json()
        caminhoLocal = json_data['caminho'].replace("_","/")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='ipServer', username='username', password='passServer')
        sftp_client = ssh.open_sftp()
        sftp_client.put(caminhoLocal, f"/var/gravacoes/tela/{caminhoLocal.split('/')[-1]}")
        sftp_client.close()
        ssh.close()

        os.remove(caminhoLocal)

        return {'message': f'Upload realizado com sucesso !'}


