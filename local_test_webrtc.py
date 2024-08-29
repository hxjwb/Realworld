
YUV_SEND = "/home/xiangjie/720p_coded.yuv"


# kill the local process
def kill_process(process):

    import signal
    try:
        process.terminate() 
        process.wait()
        os.killpg(process.pid,signal.SIGTERM)
    except:
        print("Process already killed")


import subprocess

# kill 8888 port
cmd_kill = "fuser -k 8888/tcp"
import os
os.system(cmd_kill)
bin_path = "/home/xiangjie/sparkrtc/out/t"
cmd = f"{bin_path}/peerconnection_server"

stdoutfile = "local_server.txt"
f = open('stdout/'+stdoutfile, "w")
server_process = subprocess.Popen(cmd, stdin = subprocess.PIPE, shell=True,
                            # output the result of the connection
                                stdout = f,  
                                # output the error of the connection
                                stderr = f,
                                preexec_fn=os.setsid)

import time
time.sleep(1) # wait for server to start


ffmpeg_cmd = f"ffmpeg -f x11grab -video_size 1280x720 -i :1 -r 60 -c:v libx264 -preset ultrafast -qp 10 screen.mp4 -y"

# Directly YUV
ffmpeg_cmd = f"ffmpeg -f x11grab -video_size 1280x720 -i :1 -r 60 -c:v rawvideo -pix_fmt yuv420p screen.yuv -y"

ffmpeg_cmd = ffmpeg_cmd.split(" ")
stdoutfile = "ffmpeg.txt"
ff = open('stdout/'+stdoutfile, "w")
ffmpeg_process = subprocess.Popen(ffmpeg_cmd, 
                            # output the result of the connection
                                stdout = ff,  
                                # output the error of the connection
                                stderr = ff)

cmd_recv = f'{bin_path}/peerconnection_localvideo --gui --recon "rec.yuv" 2>/home/xiangjie/realworld/recv.log'
stdoutfile = "local_receiver.txt"
fr = open('stdout/'+stdoutfile, "w")
recv_process = subprocess.Popen(cmd_recv,  shell=True,
                            # output the result of the connection
                                stdout = fr,  
                                # output the error of the connection
                                stderr = fr,
                                # kill all the subprocesses when the parent process is killed
                                preexec_fn=os.setsid)



cmd_send= f'{bin_path}/peerconnection_localvideo --file {YUV_SEND} --height 720 --width 1280 --fps 24 2>/home/xiangjie/realworld/send.log'
stdoutfile = "local_sender.txt"
fs = open('stdout/'+stdoutfile, "w")
send_process = subprocess.Popen(cmd_send, shell=True,
                            # output the result of the connection
                                stdout = fs,  
                                # output the error of the connection
                                stderr = fs,
                                preexec_fn=os.setsid)

# wait for the sender to finish, longest time is 1 minute
try:
    send_process.wait(60)
except:
    print("Timeout, killing the process")
    kill_process(send_process)


kill_process(recv_process)
kill_process(server_process)
time.sleep(1)
ffmpeg_process.terminate()


# No need to convert to mp4 now since we capture the screen

# cmd = "ffmpeg -s 1280x720 -i rec.yuv -c:v libx264 -preset ultrafast -qp 20 -pix_fmt yuv420p output.mp4 -y"

# os.system(cmd)

# print("Done")
