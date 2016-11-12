tmux ls
tmux send -t core '^C' ENTER
tmux send -t ino '^C' ENTER
tmux send -t joy '^C' ENTER
sleep 2
echo
tmux ls
