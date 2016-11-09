# $bluetooth:  Connected to Android: e.g. /dev/rfcomm0
channel=$(sdptool browse $phone | sed "1,/Jetson Remote Control/d" | \
		grep -o 'Channel: [0-9]*' | head -1 | grep -o '[0-9]*')
sudo rfcomm release $bluetooth
sudo rfcomm bind $bluetooth $phone $channel

cmd_log=cmdbluetooth.csv
cat /dev/null > $cmd_log
cat $bluetooth >> $cmd_log &

# $usb: Connected to Arduino: e.g. /dev/ttyACM2
while true; do
    line=$(tail -1 $cmd_log)
    if [ ${#line} == 7 ]; then
        echo $line >> $usb
    fi
    sleep 0.000000000000000000000000000000001
done

#while read line; do
#    echo $line >> $usb
#    sleep 0.00000000000000000000000000000000000000000000000000000000000001
#done < $cmd_log
