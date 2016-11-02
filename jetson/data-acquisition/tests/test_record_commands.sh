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
#cat $port >> commands.csv &

#tail -f /dev/ttyACM0 &
#while true; do
#	tail -f commands.csv | cut -d, -f1- | tee -a arduino.csv /dev/ttyACM0
#done

file=z.csv
cat /dev/null > $file
cat /dev/null > $file.errors
while read line; do
  if [ ${#line} == 7 ]; then
    echo $line >> $file
  else
    echo $line >> $file.errors
  fi
done < $port

