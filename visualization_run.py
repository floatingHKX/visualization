import sys
import os

sys.path.append("./source")


from source.replayer import Replayer


def output_usage():
    print("usage:\n" + \
          "python visualization_run.py [pack_path] [binary] [lib_version]")


if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("args error!")
        output_usage()
        exit(-1)
    pack_path = sys.argv[1]
    binary = sys.argv[2]
    lib_version = None
    if len(sys.argv) == 4:
        lib_version = sys.argv[3]
    binary_path = os.path.join(pack_path, binary)
    log_path = os.path.join(pack_path, "syscalls.record")
    map_path = os.path.join(pack_path, "maps")
    replay = Replayer(binary_path=binary_path, log_path=log_path, \
                      map_path=map_path, lib_version=lib_version)
    replay.enable_analysis("heap_analysis")
    replay.do_analysis()
    replay.generate_report()