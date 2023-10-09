# SONiC_TPCM

### This Script is for test purposed only.

The remote-tpmc is a proof script to remotely manipulate the TPCM REST-API on a Dell Enterprise SONiC device
This script permit to list, deploy, remove a TPCM.

## Running Python script
remote_tpcm.py is the master script

**usage:** 
  `python3 remote_tpcm.py --switch_ip 192.168.122.114 --sonic_username admin --sonic_password YourPaSsWoRd`
  

## Config File
The config file **remote_tpcm.conf** contain all parameters to deploy the container require
the structure of the the file is :
`[TPCM1]
docker-name = container name
image-source = source location (http/https/ssh/sftp) for docker hub use *pull*
image-name = remote/name:version
args = arguments`
