#!bin/sh

sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 29 -m $1 &
sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 26 -m $1 &
#sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 22 -m $1 &
#sudo python3 SGVHAK_Rover/lewansoul_wrapper.py --id 21 -m $1 &
wait
