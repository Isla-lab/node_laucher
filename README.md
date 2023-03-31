# ISLa Lab mini-cluster 🚀

This is the repo containing the instructions and code to access and run your processes on the ISLa mini-cluster. Please read the instructions below carefully before proceeding. If you have any questions or errors contact alessandro.farinelli@univr.it.

## How use the mini-cluster

Our mini-cluster is based on a *publisher-subscriber* architecture. Specifically, we report the steps to obtain login credentials and the procedures to be performed to launch the scripts on our machines.

### 1) **Get the credentials**: 
contact alberto.castellini@univr.it to obtain credentials to one of the cluster nodes. In the email, specify whether you intend to use GPU or CPU only. The administrator given the availability of nodes will provide you with a username and password. 



![](https://drive.google.com/uc?export=view&id=1UWtWTpfrK6k5sOWMG6bxEo22E2ZYl5tl)


### Resourses
|      |CPU/RAM     |GPU      |
|------|------------|---------|
|Node 1|20 cores - 64 Gb|Nvidia RTX 4070 ti 12 Gb|
|Node 2|8 cores - 48 Gb| Nvidia RTX 2070 Super 8gb|
|Node 3|8 cores - 32 Gb| Nvidia GTX Titan X |
Node 4|12 cores - 16 Gb| Nvidia GTX 960|

### 2) **Prepare your script and environment**: 
the second step involves preparing scripts to run on the cluster **on your machine(!)**, that is, the cluster should be used only to run jobs and not to program. Moreover, the result of the code execution should be written in a specific file (txt, csv, etc...). *For the time being, our mini-cluster only supports the execution of python scripts.* Below are all the instructions for copying and eventually creating your own python virtual environment.

![](https://drive.google.com/uc?export=view&id=17tG2-YtLuNz4txxzLLRhvUm4JMuCRW7w)

#### Access to the assigned node and transfer files
To access the assigned node, *ssh* should be used. In particular, open a terminal in your pc and type:
```bash
> ssh username@IP_Node
```
and click enter (the password will be required). 

Now you are inside the assigned node. As specified before, you should not code inside the node. Once you have create in your pc all the necessary python scripts to be execute inside the node, you can transfer these scripts using *sftp* or *scp*. For example suppose you have the file *example.py* in your desktop and you want to copy this file from your pc to the assigned node.  Just open another terminal and type:

```bash
> sftp username@IP_Node
```

(the password will be required). Once you are inside the node in this mode, just type in the terminal:

```bash
> put -r Desktop/example.py
```

This comand will copy your python script in the assigned node. Similarly you can retrive files from the node to your computer using:

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

where *home/student/example.py* should be replaced with the absolute path to the python file, in the assigned node, to be run. parameter1, paramenters2 should be replaced with the ones necessary (if any). Multiple rows can be specified in the file, where each row can have different parameters (e.g., different seeds). 


### 3) **Run your jobs in the mini-cluster**: 

![](https://drive.google.com/uc?export=view&id=13z3Y-4-eggcfv0vyaytEJT-QQc5X06NX)

#### Install dependences

In order to use the mini-cluster, once you entered in ssh in the node, 
you should clone this repo https://github.com/Isla-lab/node_laucher.
In order to use the GPU you should follow these steps: 
 
```bash
> cd node_laucher
> ./add_paths
```

#### Run your jobs

To run your jobs on the assigned node of the mini-cluster just type:

```bash
> screen -S name_screen -dm bash -c 'python node.py username /home/username/path_to_your_script/your_script.py GPU n_parallel'
```

Screen or GNU Screen is a terminal multiplexer. In other words, it means that you can start a screen session and then open any number of windows (virtual terminals) inside that session. Processes running in Screen will continue to run when their window is not visible even if you get disconnected. 

**Parameters**:

- *name_screen*: name of the screen to be used to re-enable a particular session.
- *username*: the username used to log in to SSH.
- */home/username/path_to_your_script/your_script.py*: absolute path to the end to run inside the node (you can retrieve the absolute path by typing the pwd command from terminal)
- *GPU*: boolean to indicate whether or not you want to use the GPU
- *n_parallel*: if GPU to False is an integer >= 1 indicating how many rows you want to run in parallel of the *username_config.txt* file.


**Practical example:**
suppose you want to run the test.py file located in the home of the assigned node.  
