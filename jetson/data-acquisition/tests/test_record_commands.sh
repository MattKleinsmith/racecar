bluetooth=/dev/rfcomm0 # Connected to Android
usb=/dev/ttyACM1 # Connected to Arduino
cmd_log=commands.csv

if [ "$#" -eq 1 ]; then 
	channel=$1
else
	channel=$(sdptool browse --l2cap $phone | sed "1,/Jetson Remote Control/d" | \
		grep -o 'Channel: [0-9]*' | head -1 | grep -o '[0-9]*')
fi
sudo rfcomm release $bluetooth
sudo rfcomm bind $bluetooth $phone $channel

cat /dev/null > $cmd_log
cat /dev/null > $cmd_log.log
cat /dev/null > $cmd_log.error
#echo "aclk,throttle,steering" > $cmd_log
while read line; do
  if [ ${#line} == 7 ]; then
    #echo $line >> $usb
    echo $line >> $cmd_log
    echo `date +%s%3N`,$line >> $cmd_log.log
  else
    echo `date +%s%3N`,$line >> $cmd_log.error
  fi
done < $bluetooth
