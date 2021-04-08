import sys
sys.path.append("../../source")

from replayer import Replayer
import angr
from claripy.ast.bv import BV
import claripy
import os
from util.info_print import  stack_backtrace, printable_backtrace, printable_memory

# os.system("../../set-aslr.sh off")

rr = Replayer("./wget", "./syscalls.record", "./maps", new_syscall=True)


# rr.do_track()


import time
time_start = time.time()
#
# rr.enable_analysis(["heap_analysis", "shellcode_analysis", "leak_analysis", "got_analysis", "call_analysis"])
# rr.enable_analysis(["call_analysis", "shellcode_analysis"])
# rr.enable_analysis(["heap_analysis"])

# rr.do_analysis()
#
rr.do_track()
time_end = time.time()
print("time cost: %s s" % (time_end-time_start))
#
# rr.generate_report()
# now: read
# now: read
# INFO    | 2021-01-05 17:02:38,513 | shellcode_analysis | Found shellcode written at 0x1dc0040 (heap).
# Found exploited state: execve('/bin///sh', None, ...)
# Replay finished.
# time cost: 134.38854503631592 s

# now: read
# now: read
# INFO    | 2021-01-05 17:07:08,717 | shellcode_analysis | Found shellcode written at 0x1dc0040 (heap).
# Found exploited state: execve('/bin///sh', None, ...)
# Replay finished.
# time cost: 201.5395269393921 s

# rr.generate_report()
# rr.packer.pack()
