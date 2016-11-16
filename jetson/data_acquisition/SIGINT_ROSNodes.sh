tmux ls
tmux send -t core '^C' ENTER
tmux send -t relay '^C' ENTER
tmux send -t ino '^C' ENTER
sleep 2
echo
tmux ls
