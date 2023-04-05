# ISLa Lab mini-cluster 🚀

This is the repo containing the instructions and code to access and run your processes on the ISLa mini-cluster. Please read the instructions below carefully before proceeding. If you have any questions or errors contact alessandro.farinelli@univr.it.

## How use the mini-cluster

Our mini-cluster is based on a *publisher-subscriber* architecture. Specifically, we report the steps to obtain login credentials and the procedures to be performed to launch the scripts on our machines.

### 1) **Get the credentials**: 
contact alberto.castellini@univr.it to obtain credentials to one of the cluster nodes. In the email, specify whether you intend to use GPU or CPU only. The administrator given the availability of nodes will provide you with a username, password and the IP address of the node assigned. 



![](https://drive.google.com/uc?export=view&id=1UWtWTpfrK6k5sOWMG6bxEo22E2ZYl5tl)


### Resourses
|      |CPU - RAM     |GPU      |
|------|------------|---------|
|Node 1|20 cores - 64 Gb|Nvidia RTX 4070 ti 12 Gb|
|Node 2|8 cores - 48 Gb| Nvidia RTX 2070 Super 8Gb|
|Node 3|8 cores - 32 Gb| Nvidia GTX Titan X 12 Gb|
Node 4|12 cores - 8 Gb| - |

### 2) **Prepare your script and environment**: 
the second step involves preparing scripts to run on the cluster **on your machine(!)**, that is, the cluster should be used only to run jobs and not to program. Moreover, the result of the code execution should be written in a specific file (txt, csv, etc...). 

> <ins>*For the time being, our mini-cluster only supports the execution
> of python scripts.*<ins>
> 
> If you need to run any particular scripts other than python, send an email to alberto.castellini@univr.it.


Below are all the instructions for copying and eventually creating your own python virtual environment.

![](https://drive.google.com/uc?export=view&id=17tG2-YtLuNz4txxzLLRhvUm4JMuCRW7w)

#### Access to the assigned node and transfer files
To access the assigned node, *ssh* and a VPN should be used. In particular, once you have connected to the univr net using a VPN, open a terminal in your pc and type:
```bash
> ssh username@<IP_Node>
```
and click enter (the password will be required). 

Now you are inside the assigned node. As specified before, you should not code inside the node. Once you have create in your pc all the necessary python scripts to be execute inside the node, you can transfer these scripts using *sftp* or *scp*. For example suppose you have the file *example.py* in your desktop and you want to copy this file from your pc to the assigned node.  Just open another terminal and type:

```bash
> sftp username@<IP_Node>
```

(the password will be required). Once you are inside the node in this mode, just type in the terminal:

```bash
> put -r Desktop/example.py /home/student/Desktop/
```

This comand will copy your python script (located in your pc) in the Desktop folder of the assigned node. Similarly you can retrive files from the node to your computer using:

```bash
> get -r /home/student/example.py
```

assuming your file has been copied in the path */home/student/*.

#### Create a python virtual environment and install dependecies

 You can create various python virtual environments to have a 100% compatibility with your personal computer. These environments work similarly to *Conda*. 
 To create a virtual environment follow these commands:

```bash
> mkdir venv
> python -m venv venv/name_venv
> source venv/name_venv/bin/activate
```

now the *name_venv* virtual environment is activeted and you can install all the required dependences with *pip*.

#### Prepare the configuration.txt file

In order to run your scripts in the assigned node you need to create a txt configuration file. This must have the following name '*'username_config.txt*''. This file should contain the following commands:

```txt
python /home/student/example.py parameter1 parameter2
```

where *home/student/example.py* should be replaced with the absolute path to the python file (in the assigned node) to be run. parameter1, paramenters2 should be replaced with the ones necessary (if any). Multiple rows can be specified in the file, where each row can have different parameters (e.g., different seeds). 


### 3) **Run your jobs in the mini-cluster**: 

![](https://drive.google.com/uc?export=view&id=13z3Y-4-eggcfv0vyaytEJT-QQc5X06NX)

#### Install dependences

In order to use the mini-cluster, once you entered in ssh in the node, 
you should clone this repo https://github.com/Isla-lab/node_laucher.

> In order to use the GPU you should follow these steps:

```bash
> cd node_laucher
> ./add_paths
```

#### Run your jobs

To run your jobs on the assigned node of the mini-cluster just type:

```bash
> screen -S name_screen -dm bash -c 'python node.py username /home/username/path_to_your_config/your_config.txt GPU n_parallel'
```

Screen or GNU Screen is a terminal multiplexer. In other words, it means that you can start a screen session and then open any number of windows (virtual terminals) inside that session. Processes running in Screen will continue to run when their window is not visible even if you get disconnected. 

**Parameters**:

- *name_screen*: name of the screen to be used to re-enable a particular session.
- *username*: the username used to log in to SSH.
- */home/username/path_to_your_script/your_script.py*: absolute path to the end to run inside the node (you can retrieve the absolute path by typing the pwd command from terminal)
- *GPU*: boolean to indicate whether or not you want to use the GPU
- *n_parallel*: if GPU == False should be an integer $\geq$ 1 indicating how many rows you want to run in parallel of the *username_config.txt* file.

Regarding the parameter *n_parallel*, as specified it is possible to indicate how many lines of the configuration .txt file run in parallel. Please do some preliminary tests on your machine to understand the load on the CPU cores before launching on the node. We report in the next section on *best practices* for preparing python scripts to catch any runtime or other errors.

## Practical example:
Suppose we (username: *student*) want to run the example.py created in your pc. Suppose the file is something like this:

```python
import sys
from datetime import datetime
import time
import logging
logging.basicConfig(filename=f'output_{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}.log', level=logging.DEBUG)
logger=logging.getLogger(__name__)

try:
    arg1 = sys.argv[1]
    logger.info(arg1)
    print(arg1)
    time.sleep(10)

except Exception as e: 
    logger.error(e)

```

This script simply creates a log file where any errors will be saved. It then prints on the screen the parameters that are passed to the script. Please notice that it is good practice to put your code enclosed in *try-except* comands, in order to figure out why your script possibly does not work.
We then create the *.txt* configuration file in order to run our script on the assigned node. Specifically, suppose we want to use only the CPU and send 2 executions in parallel at a time. So we write the file as:

```txt
python /home/student/Desktop/example_file.py hello_1
python /home/student/Desktop/example_file.py hello_2
python /home/student/Desktop/example_file.py hello_3
python /home/student/Desktop/example_file.py hello_4
python /home/student/Desktop/example_file.py hello_5
python /home/student/Desktop/example_file.py hello_6
python /home/student/Desktop/example_file.py hello_7
```
Hence, we specify the command (python) and the absolute path where our script will be copied to the assigned node. Finally as the last arguments any parameters that our script requires (if needed).


### copying the file in the assigned node:

First of all, we connect via VPN to the UNIVR network. Now that we are connected to the UNIVR network, let's access via SSH to the assigned node (for this example, the node will be called *server*). Hence, let's open a terminal and digit:

```bash
ssh student@<IP_Node_server>
```

If everything is correct you should see in the terminal: 

```bash
student@pop-os:~$
```

Now open another terminal window and navigate in the folder where the files we want to copy are located. Here we again access the assigned node but this time with sftp:

```bash
sftp student@<IP_Node_server>
```

If everything is correct you should see in the terminal: 

```bash
Connected to <IP_Node_server>.
sftp>
```

We now copy the files in the assigned node usign the terminal with sftp with the commands:

```bash
sftp> put -r example.py /home/student/Desktop/
```

```bash
sftp> put -r student_config.txt /home/student/Desktop/
```

Now by typing the ls command into the desktop of the assigned node we should see our files.

### running our script in the assigned node:

First of all install paho-mqtt using this command:

```bash
pip install paho-mqtt
```
Let's now clone this repo in the assigned node. In the terminal with ssh type:

```bash
git clone https://github.com/Isla-lab/node_laucher.git
```

To launch the script on the assigned machine, we type the following command in the terminal with ssh:

```bash
screen -S name_screen -dm bash -c 'python node_laucher/node.py student /home/student/Desktop/student_config.txt False 2'
```
To check the terminal use: 
```bash
screen -r name_screen
```

To detach from the screen using ctrl+a and ctrl+d

```bash
Your job is starting...

hello_2
hello_1
hello_3
hello_4
hello_6
hello_5
hello_7

End all your jobs!
[screen is terminating]
```
