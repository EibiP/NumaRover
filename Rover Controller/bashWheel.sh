#!bin/sh

sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 27 -s -$1 &
sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 25 -s $1 &
sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 23 -s -$1 &
sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 20 -s $1 &
sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 24 -s -$1 &
sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 28 -s $1 &
wait
