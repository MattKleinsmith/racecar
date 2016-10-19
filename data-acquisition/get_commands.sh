sudo rfcomm release /dev/rfcomm0
channel=$(sdptool browse --l2cap $phone | sed "1,/Jetson Remote Control/d" | \
	grep -o 'Channel: [0-9]*' | head -1 | grep -o '[0-9]*')
sudo rfcomm bind /dev/rfcomm0 $phone $channel
if [ $# -eq 1 ]; then
	prefix=$1
	dir=""
else
	prefix=$(cat /tmp/camera_datetime.txt)
	dir="/media/ubuntu/WD TB/"
fi
pathprefix=${dir}${prefix}
echo "aclk,throttle,steering" > ${pathprefix}_commands.csv
cat /dev/rfcomm0 >> ${pathprefix}_commands.csv
