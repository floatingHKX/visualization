# README

##  Binary-Exploit-Visualization
This project is based on the open-source tool [angr](https://github.com/angr/angr). We implement a system named BveView, which is based on the record-and-replay method. We record the information of the exploit process by ptrace mechanism and replay the exploit process through the angr tool. During repeated replays, we analyze and capture abnormal behaviors which are closely related to the key points of the exploit to show the exploit process. We will get a visual report finally.

This tool is suitable for x86_64 program in the application layer under Linux. It is not suitable for programs related to hardware devices.

## System Overview
+ **Record Module:**  this module tracks and records the system call information during the execution of the target program and the memory snapshot under the entry point state of the target program when the vulnerability is being exploited. ([record_syscalls.md](./doc/record_syscalls.md))
+ **Replay Analysis Module:** this module loads binary files such as library files and target program executable files into the
simulation execution tool, initializing the program entry point memory. Then, the entry point is used as the starting point for replay, and we replay the recorded system call information to simulate the process of running the target programâ€™s vulnerability exploitation. When the monitoring program is running, it analyzes the function call situation, the modification of key program fields, the change of key data structure, memory read and write, to find and record abnormal program behavior.
+ **Abnormal Information Visualization Module:** this module analyzes the log in the replay analysis module and generate the visual report.

## Analysis Functions
+ **call analysis:** Trace the ROP attack and capture the overflow of stack return address.
+ **heap analysis:** Capture overflows in the heap and abnormal operations on the heap.
+ **GOT analysis:** Check whether the function pointer in the got table is abnormal, and trace the source of the abnormality
+ **leakage analysis:** Check whether there is memory address information in program output and get the symbol analysis result
+ **shellcode analysis:** Capture the behavior of shellcode writing to memory, and capture the shellcode jump in the control flow

## Setup
+ Install the pypy3.7 first. For example:
```bash
wget https://downloads.python.org/pypy/pypy3.7-v7.3.3-linux64.tar.bz2
tar jxvf pypy3.7-v7.3.3-linux64.tar.bz2
sudo mv pypy3.7-v7.3.3-linux64 /usr/lib/
export PATH=/usr/lib/pypy3.7-v7.3.3-linux64/bin:$PATH
```
+ Run the script file [setup.sh](./setup.sh) to install the python environment.

```bash
sh ./setup.sh
```

you will get  executable file *record_ptrace* in the root directory, which is used to record the target program.

## Usage

#### 1.Before Record

Disable the aslr mechanism. Run the script in the root directory.
```bash
./set-aslr.sh off
```

#### 2.Record the Exploit Process

+ set ``LD_BIND_NOW=1`` to disable the delay loading of link library

+ Run the target program by ***record_ptrace*** (in the project root directory after setup)

```bash
cp ./record_ptrace <workplace>
```

If you run target by cmd, the cmd's command is transformed into the following example. 

```bash
# path: ./exploit_samples/cve_2016_10190
# ffmpeg -i http://127.0.0.1:12345
LD_BIND_NOW=1 ./record_ptrace ./ffmpeg -i http://127.0.0.1:12345
```

If you exploit the through a exploit script (such as python), modify the script with the record module and the script modified is below.

```python
# path: ./exploit_samples/fastbin
from pwn import *
# p = process('./fast', env={"LD_BIND_NOW":"1"}) # origin code
p = process('./record_ptrace ./fast', shell=True, env={"LD_BIND_NOW":"1"}) # modified code
# exploit code
...
```
then you will get files such as ``maps``, ``maps.dump``, and ``syscalls.record``, which are generated by ***record_ptrace***.

```bash
cp ./pack.py <workplace>
```

Run ***pack.py*** (in the project root directory) to pack these files and library files to one directory named ``xxx_packed`` at last.

```bash
# python pack.py 
# Usage:
# python pack.py [maps_log_path] [syscalls_path] [target_dir_path]/default
# if target_dir_path is 'default', [target_dir_path]=/tmp/work/record_packed
python pack.py maps.12212 syscalls.record ./fastbin_packed
```

#### 3.Replay the Exploit Process

+ Move the packed directory ``fastbin_packed`` to the "./test/" direcotry. 
+ Create a new analysis script in this path ``./test/fastbin_packed/init.py``.

```python
# path=./test/fastbin_packed/init.py
import sys
sys.path.append("../../source") # to set the path which replayer exist in
from replayer import Replayer

r = Replayer('./fast', './syscalls.record', './maps', '2.23', new_syscall=True)
r.enable_analysis(["call_analysis", "heap_analysis", "shellcode_analysis", "got_analysis", "leak_analysis"]) # The analysis module can be combined arbitrarily according to the characteristics of the target program
rr.do_analysis() # start analysis
rr.generate_report() # generate the visualization report
```

+ Run the script to start analysis ``pypy3 init.py``.
+ Finally, you will get a visual report at the same path named ``html``. （The description of report is in [report_description](./doc/report_description.md)）

## Development Interface

The new analysis submodule only needs to implement a new class and implement the do_analysis method for it. 

For example:

```python
class X_analysis(analysis):
 def __init__(self, ):
 # do init
 def do_analysis(self):
 # do the work
 
register_analysis(X_analysis)
```