port=/dev/rfcomm0
channel=$(sdptool browse --l2cap $phone | sed "1,/Jetson Remote Control/d" | \
	grep -o 'Channel: [0-9]*' | head -1 | grep -o '[0-9]*')
sudo rfcomm release $port
sudo rfcomm bind $port $phone $channel
prefix=$(cat /tmp/camera_datetime.txt)
dir=$(cat /tmp/external_hard_drive.txt)
pathprefix=${dir}${prefix}
date +%s%3N > ${pathprefix}_jckl0.txt
echo "aclk,throttle,steering" > ${pathprefix}_commands.csv
cat $port >> ${pathprefix}_commands.csv
