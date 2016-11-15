channel=$(sdptool browse $phone | sed "1,/Jetson Remote Control/d" | \
		grep -o 'Channel: [0-9]*' | head -1 | grep -o '[0-9]*')
sudo rfcomm release $bluetooth
sudo rfcomm bind $bluetooth $phone $channel
