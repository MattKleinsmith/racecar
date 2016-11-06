while true; do
  #tail -1 commands.csv >> /dev/ttyACM1
  echo "061,025" >> /dev/ttyACM1
  sleep 0.03
done
