# SONiC_TPCM

>[!WARNING] This Script is for test purposed only.

The remote-tpmc is a proof script to remotely manipulate the TPCM REST-API on a Dell Enterprise SONiC device.
This script permit to list, deploy, remove a TPCM.

## Running Python script
remote_tpcm.py is the master script

**usage:** 
  `python3 remote_tpcm.py --switch_ip 192.168.122.114 --sonic_username admin --sonic_password YourPaSsWoRd`
  

## Config File
The config file **remote_tpcm.conf** contain all parameters to deploy the container require
the structure of the config file is define in the remote_tpcm.conf
