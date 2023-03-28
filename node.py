import os
import sys
from mqtt_client import MqttClient
import time
import json
import pathlib

def node():
    client = MqttClient()
    user = sys.argv[1]
    job_path = sys.argv[2]

    #check path
    if not os.path.exists(job_path):
        print('No such file exists!!')
        print(f'Path provided: {job_path}')
        return


    abs_path = os.path.join(str(pathlib.Path(__file__).parent.resolve()))
    gpu = sys.argv[3]
    parallel = sys.argv[4]
    data = {"user": str(user), "path": job_path, "gpu": gpu, "parallel": parallel}
    payload = json.dumps(data)
    #time.sleep(1)
    client.publish("jobs/" + str(user), payload)
    client.stop()





if __name__ == '__main__':
        node()

