from replayer import Replayer
# import angr.storage.memory_mixins.clouseau_mixin
import os
from util.info_print import *

# os.system("../../set-aslr.sh off")



rr = Replayer("./ffmpeg_g_normal", "./syscalls.record", "./maps", new_syscall=True)

# def _hook_tcache_init(state):
#     print("in socket")
#
#

# rr.hook_symbol("tcache_init", _hook_tcache_init())
# rr.hook_symbol("_int_malloc")

# rr.enable_analysis(["heap_analysis"])

# now: socket
# now: connect
# Found exploited state: execve('/bin/sh', [], ...)
# Replay finished.
# time cost: 860.9132940769196 s
# over

# now: socket
# now: connect
# Found exploited state: execve('/bin/sh', [], ...)
# Replay finished.
# time cost: 698.7854998111725 s
# over

import time
time_start = time.time()

rr.enable_analysis(["heap_analysis"])
rr.do_analysis()

time_end = time.time()
print("time cost: %s s" % (time_end-time_start))
# rr.do_track()
print("over")
# rr = Replayer("./ptrace/mutil/thread_tests/thread", "./ptrace/mutil/thread_tests/stdin.txt", "./ptrace/mutil/thread_tests/maps.76058", test=True)

rr.generate_report()
# from parse_helpers import *



# dumps = parse_dumps(rr, "./maps.19158.dump")

# def _hook_socket(state):
#     print("in socket")

# def _hook_ioctl(state):
#     print("in sigaction")
#     rsp = state.regs.rsp
#     assert (rsp.concrete)
#     # stack frame haven't been created, so return address is in rsp
#     ret_addr = state.memory.load(rsp, 8, endness='Iend_LE')
#     ret_addr = ret_addr.args[0]
#
#     def _ioctl_callback(state):
#         state.project.unhook(ret_addr)
#         print("out ioctl")
#
#     state.project.hook(ret_addr, _ioctl_callback)

def bp_overflow():
    def write_bp(state):
        target_addr = state.inspect.mem_write_address
        target_size = state.inspect.mem_write_length
        content = state.inspect.mem_write_expr
        if "1b28000" in hex(content.args[0]):
            print("expr: %s" % content)
            print("state: %x" % state.addr)
        # if type(target_addr) != int:
        #     target_addr = target_addr.args[0]
        # if target_size is None:
        #     return
        # if type(target_size) != int:
        #     target_size = target_size.args[0]
        #
        # if (target_addr >= start_addr + size) \
        #         or (start_addr >= target_addr + target_size):
        #     return
        #
        #
        # if (target_addr + target_size > start_addr + size):
        #     overflow_len = target_addr + target_size - (start_addr + size)
        #     overflow_content = state.inspect.mem_write_expr[overflow_len * 8 - 1:0]
        #     memory = printable_memory(state, min(start_addr, target_addr), max(size, target_size) \
        #                               , warn_pos=start_addr + size, warn_size=overflow_len, info_pos=target_addr \
        #                               , info_size=target_size)
        #     message = "Found chunk overflow at %s." % hex(start_addr)
        #     report_logger.warn(message, type='heap_overflow', start_addr=start_addr, size=size, target_addr=target_addr, \
        #                        target_size=target_size, overflow_len=overflow_len, overflow_content=overflow_content, \
        #                        memory=memory, state_timestamp=state_timestamp(state))
        return

    return write_bp

# rr.hook_symbol("socket", _hook_socket)
# rr.hook_symbol("tcgetattr", _hook_ioctl)
# rr.hook_symbol("sigaction", _hook_ioctl)
# simgr = rr.get_simgr()
# simgr.active[0].options.discard("UNICORN")
# simgr.active[0].options.add("SUPPORT_FLOATING_POINT")
# simgr.active[0].inspect.b("mem_write", action = bp_overflow())
# simgr.active[0].options.discard("UNICORN_TRACK_BBL_ADDRS")
# simgr.active[0].options.discard("UNICORN_SYM_REGS_SUPPORT")
# simgr.active[0].options.discard("UNICORN_HANDLE_TRANSMIT_SYSCALL")
# simgr.active[0].options.discard("DO_CCALLS")
# simgr.active[0].options.discard("REGION_MAPPING")
# simgr.active[0].options.discard("SYMBOLIC")
# simgr.active[0].options.discard("SYMBOLIC_INITIAL_VALUES")
# simgr.active[0].options.discard("'SYMBOLIC_MEMORY_NO_SINGLEVALUE_OPTIMIZATIONS'")


# simgr.run()
# simgr.explore(find=0x404980)
# simgr = rr.factory.simgr(simgr.found[0])
# simgr.explore(find=0x7ffff7b15fc0)
# simgr = rr.factory.simgr(simgr.found[0])
# simgr.explore(find=0xfb1a58)
# simgr = rr.factory.simgr(simgr.found[0])
# simgr.explore(find=0xfb1a60)
# simgr = rr.factory.simgr(simgr.found[0])
# simgr.explore(find=0xfb1a6d)
# simgr = rr.factory.simgr(simgr.found[0])
# simgr.explore(find=0xfb1a7d)
# simgr = rr.factory.simgr(simgr.found[0])
# simgr.explore(find=0xfb1a83)
# simgr = rr.factory.simgr(simgr.found[0])
# simgr.explore(find=0x478942)
# simgr.explore(find=0x7ffff7c05bef)
# simgr.explore(find=0x7ffff7ded360)
# simgr.explore(find=0x664b9f)
# simgr = rr.factory.simgr(simgr.found[0])

# simgr.explore(find=0x664ce7)

# simgr.explore(find=0x7ffff7b27a4c)
# simgr = rr.factory.simgr(simgr.found[0])

# b = rr.factory.block(simgr.found[0])
# print(simgr.found[0].memory.load(0x7ffff7ded360, 0x10, endness='Iend_LE'))
# state = simgr.found[0]
# output = state.solver.eval(state.memory.load(0x7ffff7ded360, 0x30), cast_to=bytes)
# print(output)
# import pyvex, archinfo

# b = pyvex.block.IRSB(output, 0x1000, archinfo.ArchAMD64())
# pyvex.lift(output, 0x1000, archinfo.ArchAMD64()).pp()

# pyvex.lift(b'\x8b\x0c$\x83\xf9\x00t9\x8bD$\x08\x89\xc3\xb9\x00\x00\x00\x00\xbe', 0x1000, archinfo.ArchX86()).pp()
# print(b.pp())
# r13 = state.regs.r13+0xf00
# addr = state.memory.load(r13,8, endness = 'Iend_LE')
# simgr.run()
# print("over")
# rr.enable_analysis(["heap_analysis"])
# rr.do_analysis()
# rr.generate_report()
# print(printable_callstack(simgr.found[0]))
# list = simgr.errored[0].state.history.bbl_addrs.hardcopy
# with open("log0.log", 'w') as f:
#     str = ""
#     for addr in list:
#         str += hex(addr) + "\n"
#     f.write(str)
#     f.close()
#
# list = simgr.deadended[0].history.bbl_addrs.hardcopy
# with open("log.log", 'w') as f:
#     str = ""
#     for addr in list:
#         str += hex(addr) + "\n"
#     f.write(str)
#     f.close()
# print("over")