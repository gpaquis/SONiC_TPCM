### SONiC_TPCM

# This Script is for test purposed only.

It's permit to remotely manipulate the TPCM REST-API on a Dell Enterprise SONiC device.
This script permit to list, deploy, remove a TPCM.

## Running Python Code
remote_tpcm_py is the master script

**usage:** 
  `python3 remote_tpcm.py --switch_ip 192.168.122.114 --sonic_username admin --sonic_password YourPaSsWoRd`
  

## Config File
The config file **remote_tpcm.conf** contain all parameters
The config file contain all entry require to deploy a dockerhub container.

