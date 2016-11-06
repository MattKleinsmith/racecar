#!/bin/bash
h=$(head -1 commands.csv.log | cut -d , -f 1)
t=$(tail -1 commands.csv.log | cut -d , -f 1)
ms=$(bc <<< "scale = 10; $t - $h")
cmd=$(cat commands.csv.log | wc -l)
echo
echo "Average number of ms per command:"
echo $(bc <<< "scale = 10; ($ms / $cmd)")
echo
