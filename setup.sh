#!/bin/sh

# compile record program
gcc ./source/ptrace/ptrace.c -o  record_ptrace

# apt installs
apt install -y graphviz

# install pypy3 before next steps
pypy3 -m pip install -r ./requirements.txt

# disable system's aslr
sh ./set-aslr.sh

# apt-get install -y tk-dev
# apt-get install -y python3-tk
