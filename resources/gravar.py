from flask_restful import Resource
from PIL import ImageGrab
import cv2
import numpy as np
import os, psutil
import multiprocessing as mp
from datetime import datetime
import socket

#PID = 0
class Gravar(Resource):
    def gravar(self, jobs, cdChamado):
        PID = os.getpid()
        PPID = os.getppid()
        data = datetime.now()

        p = ImageGrab.grab()
        a, b = p._size
        filenameLocal = (f'C://Users/{os.getlogin()}/Videos/{cdChamado}-{data.day}-{data.month}-{data.year}-{data.hour}{data.minute}{data.second}.avi')
        #filename = (f'/home/vector/Documentos/{cdChamado}-{data.day}-{data.month}-{data.year}-{data.hour}{data.minute}{data.second}.avi')
        filenameServidor = (f"/var/gravacoes/tela/{cdChamado}-{data.day}-{data.month}-{data.year}-{data.hour}{data.minute}{data.second}.avi")
        pathLocal = filenameLocal.replace("/", "_")
        pathServidor = filenameServidor.replace("/", "_")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        frame_rate = 10
        out = cv2.VideoWriter()
        capturing = True
        HOSTNAME = socket.gethostname()
        LOCALIP = socket.gethostbyname(HOSTNAME)
        process_sub = psutil.Process(PID)
        process_princ = psutil.Process(PPID)
        MEMORIA_SUB = (process_sub.memory_info().rss / (1024 ** 2)) # in MB
        MEMORIA_PRIN = (process_princ.memory_info().rss / (1024 ** 2))  # in MB

        
        jobs.put([PID, HOSTNAME, LOCALIP, pathLocal, pathServidor])

        print(f'PID: {PID} | PPID: {PPID} | HOSTNAME: {HOSTNAME} | IP: {LOCALIP} | Memória Proc Sec: {MEMORIA_SUB} | Memória Proc Princ: {MEMORIA_PRIN}' )

        if not out.isOpened():
            out.open(filenameLocal, fourcc, frame_rate, (a,b))
            print("Recording ...")
            while capturing:
                img = ImageGrab.grab()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)

        return PID, HOSTNAME, LOCALIP

    def get(self, cdChamado):

        jobs = mp.Queue()
        p = mp.Process(target=self.gravar, args=(jobs, cdChamado))
        p.start()
        lista = str(jobs.get()).strip("[]'").split(", ")

        return [lista[0], lista[1].strip("'"), lista[2].strip("'"), lista[3].strip("'"), lista[4].strip("'")]
