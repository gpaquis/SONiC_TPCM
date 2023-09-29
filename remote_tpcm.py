import json
import argparse
import ast
import requests
import configparser
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import base64

def tpcm_list(switch_ip: str, user_name: str, password: str) -> str:
    """
	List all TPCM installed
	no value, list all TPCM in each VRF
    """
    
    
    request_data = {
	"openconfig-tpcm:input": {
	}
    }

    print(json.dumps(request_data))
    try:
       response = requests.post(url=f"https://{switch_ip}/restconf/operations/openconfig-tpcm:tpcm-list",
				data=json.dumps(request_data),
				headers={'Content-Type': 'application/yang-data+json'},
				auth=HTTPBasicAuth(f"{user_name}", f"{password}"),
				verify=False
				)
       response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print(f'{response}')
    
    return response.content
   
def tpcm_install(switch_ip: str, user_name: str, password: str) -> str:
    """
	Install TPCM
        Read from a config file, here the container install from DockerHUB
	[TPCM1]
	docker-name = "str",
	image-source = "str",
	image-name = "str/str:str",
	args = "str"	
    """	

    config = configparser.ConfigParser()
    config.read('remote_tpcm.conf')

    docker_name = config['TPCM1']['docker-name']
    image_source = config['TPCM1']['image-source']
    image_name = config['TPCM1']['image-name']
    tpcm_args = config['TPCM1']['args']
    
    request_data = {
  	"openconfig-tpcm:input": {
    	   "docker-name": docker_name,
    	   "image-source": image_source,
    	   "image-name": image_name,
    	   "args": tpcm_args
  	}
    }

    print(json.dumps(request_data))
    try:
       response = requests.post(url=f"https://{switch_ip}/restconf/operations/openconfig-tpcm:tpcm-instal
l",
				data=json.dumps(request_data),
				headers={'Content-Type': 'application/yang-data+json'},
				auth=HTTPBasicAuth(f"{user_name}", f"{password}"),
				verify=False
				)
       response.raise_for_status()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print(f'{response}')
    
    return response.content
   
 
def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument("--switch_ip", help="IP address of the switch to automate", type=str)
    parser.add_argument("--sonic_username", help="SONiC Login", type=str)
    parser.add_argument("--sonic_password", help="SONiC Password", type=str)
    args = parser.parse_args()

    switch_ip = args.switch_ip

    sonic_username = args.sonic_username
    sonic_password = args.sonic_password
    """
    result = tpcm_list(switch_ip=switch_ip, user_name=sonic_username, password=sonic_password) 
    print(f'{result}')
    """
    result = tpcm_install(switch_ip=switch_ip, user_name=sonic_username, password=sonic_password) 
    print(f'{result}')


if __name__ == '__main__':
    main()
  
