
import json
import sys
from mqtt_client import MqttClient
import yaml
import pathlib
import os
import shlex, subprocess
import datetime

class Node():

    def callback_msg(self, topic: str, payload: str):
        pay = json.loads(payload)
        if topic == "master_status/" + str(self.user) and pay["start"]:
            print('Your job is starting...\n')
            self.waiting_status_msg = True
           
    def __init__(self):
        path = str(pathlib.Path(__file__).parent.resolve())
        with open(os.path.join(path, 'config', 'config.yaml')) as file:
            self.file_config = yaml.load(file, Loader=yaml.FullLoader)
        self.timeout = self.file_config['timeout']
        self.client = MqttClient(callback=self.callback_msg)
        self.client.subscribe("master_status/#")
        self.waiting_status_msg = False
        self.user = sys.argv[1]
        self.job_path = sys.argv[2]
        self.gpu = sys.argv[3]
        self.parallel = int(sys.argv[4])
        data = {"user": str(self.user), "path": self.job_path, "gpu": self.gpu, "parallel": self.parallel}
        payload = json.dumps(data)
        self.client.publish("jobs/" + str(self.user), payload)

        #check path
        if not os.path.exists(self.job_path):
            print('No such file')
            print(f'Path provided: {self.job_path}')
            return
        self.loop()

    def loop(self):
        finished = False
        while True:
            while self.waiting_status_msg:

                path = str(pathlib.Path(__file__).parent.resolve())
                res = [-1]*self.parallel
                p = []
                index_lines = 0
                last_iter = False

                try:
                   
                    with open(os.path.join(self.job_path)) as file:
                        lines = file.readlines()
            
                    try:

                        for i in range(len(lines)):

                            block_lines = []
                           
                            if index_lines+self.parallel <= len(lines):
                                block_lines = lines[index_lines:index_lines+self.parallel]
                            else: 
                                block_lines = lines[index_lines:len(lines)]
                                last_iter = True

                            res = [-1]*len(block_lines)
                            p.clear()
                            

                            for line in block_lines:

                                args = shlex.split(str(line))
                                p.append(subprocess.Popen(args))
                                    
                            start_time = datetime.datetime.now().second       
                            end_time = start_time + self.timeout

                            while start_time < end_time and sum(res) != 0: 
                                for i in range(len(res)):
                                    res[i] = p[i].wait(self.timeout - start_time)

                                start_time = datetime.datetime.now().second

                            for j in range(len(block_lines)):
                                if res[j] != 0:
                                    p[j].kill()

                            if index_lines + self.parallel <= len(lines):
                                index_lines += self.parallel

                            if last_iter:
                                break

                    except Exception as e: 
                        print(e)
                        pass

                except Exception as e: 
                    print(e)
                    pass

              
                data = {"start": False, "end": True}
                payload = json.dumps(data)
                self.client.publish("node_status/" + str(self.user), payload)
                self.client.stop()
                finished = True
                print('\nEnd all your jobs!')
                break
            
            if finished:
                break


if __name__ == '__main__':
    Node()
