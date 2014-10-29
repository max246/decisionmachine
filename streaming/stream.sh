echo "Start streaming"
avconv -f video4linux2 -video_size 640x480  -r 24 -i /dev/video0  -pix_fmt yuv420p -r 24 -f flv  rtmp://<link>
echo  "Exit"

