cmd_log=cmdbluetooth.csv
# $usb: Connected to Arduino: e.g. /dev/ttyACM2
oldLine="none"
while read line; do
    if [ ${#line} == 7 ] && [ "$line" != "$oldLine" ]; then
        echo $line >> $usb
        oldLine=$line
    fi
    sleep 0.000000000000000000000000000000000000000000000000000000000000000001
done < $cmd_log

#while read line; do
#    echo $line >> $usb
#    sleep 0.00000000000000000000000000000000000000000000000000000000000001
#done < $cmd_log
