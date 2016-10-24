port=/dev/rfcomm0
if [ "$#" -eq 1 ]; then 
	channel=$1
else
	channel=$(sdptool browse --l2cap $phone | sed "1,/Jetson Remote Control/d" | \
		grep -o 'Channel: [0-9]*' | head -1 | grep -o '[0-9]*')
fi
sudo rfcomm release $port
sudo rfcomm bind $port $phone $channel
date +%s%3N > jckl0.txt
#echo "aclk,throttle,steering" > commands.csv
cat $port >> commands.csv &
while true; do
	tail -1 commands.csv | cut -d, -f2- | tee -a sup.csv /dev/ttyACM0
done
