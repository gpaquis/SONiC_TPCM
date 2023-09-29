# SONiC_TPCM

This Script permit to deploy a TPCM remotely on a Dell Enterprise SONiC device
By using REST API, you can install, list, remove or update a TPCM 

## Running Python Code
remote_tpcm_py is the master script

**usage:** 
  `python3 remote_tpcm.py --switch_ip 192.168.122.114 --sonic_username admin --sonic_password YourPaSsWoRd`
  

## Config File
The config file **remote_tpcm.conf** contain all parameters
The config file contain all entry require to deploy a dockerhub container.

