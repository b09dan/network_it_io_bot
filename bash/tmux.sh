#!/bin/bash
set -e

tmux new-session -d -s main './mon.sh top';
tmux split-window -v './mon.sh ps auxww';
tmux split-window -v './mon.sh vmstat 5';

tmux attach-session -d -t main
