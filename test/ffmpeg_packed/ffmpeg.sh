#/bin/sh
#LD_BIND_NOW=1 ./ptrace ./ffmpeg -i http://127.0.0.1:12345
LD_BIND_NOW=1 ./ptrace ./ffmpeg -i http://127.0.0.1:12345
#LD_BIND_NOW=1 rr record -o ./record ./ffmpeg_g -i http://127.0.0.1:12345
